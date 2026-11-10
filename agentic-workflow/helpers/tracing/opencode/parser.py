"""Parse the supported OpenCode export versions."""

import json
from pathlib import Path
from typing import cast

from tracing.shared.events import add, content, count, diagnostic, event, stamp
from tracing.shared.types import Diagnostic, Event, Settings, Source, Usage

from .types import OpenCode, Tokens


def tokens(raw: Tokens | None) -> Usage:
    if not isinstance(raw, dict):
        raw = {}
    cache = raw.get("cache") or {}
    base, c, w, o, r = (
        count(v)
        for v in (
            raw.get("input"),
            cache.get("read"),
            cache.get("write"),
            raw.get("output"),
            raw.get("reasoning"),
        )
    )
    i = add(base, c, w)
    result = dict(
        input_tokens=i,
        cached_input_tokens=c,
        cache_write_input_tokens=w,
        uncached_input_tokens=add(base, w),
        output_tokens=o,
        reasoning_output_tokens=r,
    )
    if r is not None and o is not None and r > o:
        raise ValueError("reasoning tokens exceed output")
    result["total_tokens"] = add(i, o)
    return result


def parse(source: Source, path: Path) -> tuple[list[Event], list[Diagnostic]]:
    data = cast(OpenCode, json.loads(path.read_text()))
    info = data["info"]
    if "version" not in info:
        from .v2 import parse as parse_v2

        return parse_v2(source, data)
    if info.get("id") != source["session_id"]:
        raise ValueError("session identity mismatch")
    diagnostics, events = [], []
    if info.get("version") != "1.2.27":
        diagnostics.append(
            diagnostic(source, "unverified_native_version", native_version=info.get("version"))
        )
    selected = set(source["turn_ids"])  # Native user-message IDs are OpenCode turns.
    parents = {m["info"]["id"]: m["info"].get("parentID") for m in data["messages"]}

    def turn_for(mid: str | None) -> str | None:
        seen = set()
        while mid not in selected and mid in parents and mid not in seen:
            seen.add(mid)
            mid = parents[mid]
        return mid if mid in selected else None

    agents: dict[str, Event] = {}
    for index, message in enumerate(data["messages"]):
        m = message["info"]
        if m.get("sessionID") != source["session_id"]:
            continue
        turn = turn_for(m["id"])
        if not turn:
            continue
        location = f"messages/{index}"
        if turn not in agents:
            agents[turn] = event(
                source,
                "agent",
                turn,
                turn,
                location,
                parent_session_id=info.get("parentID"),
                spawn_timestamp=stamp((info.get("time") or {}).get("created"), True),
            )
        agent = agents[turn]
        time = m.get("time") or {}
        if not message["parts"]:
            events.append(
                event(
                    source,
                    "message",
                    f"{m['id']}:empty-message",
                    turn,
                    location,
                    timestamp=stamp(time.get("created"), True),
                    message_role=m["role"],
                    name="message",
                    message_id=m["id"],
                    parent_message_id=m.get("parentID"),
                    content=content({}, "text"),
                )
            )
        for part_index, part in enumerate(message["parts"]):
            if part["type"] in ("text", "reasoning", "subtask", "compaction", "file", "agent"):
                pt = part.get("time") or {}
                events.append(
                    event(
                        source,
                        "message",
                        f"{m['id']}:{part.get('id', part_index)}",
                        turn,
                        f"{location}/parts/{part_index}",
                        timestamp=stamp(pt.get("start", time.get("created")), True),
                        message_role=m["role"],
                        name=part["type"],
                        message_id=m["id"],
                        parent_message_id=m.get("parentID"),
                        content=content(part, "text", "prompt"),
                        native_record=part,
                    )
                )
        if "system" in m:
            events.append(
                event(
                    source,
                    "instruction",
                    f"{m['id']}:system",
                    turn,
                    location,
                    timestamp=stamp(time.get("created"), True),
                    name="system instructions",
                    content=content(m, "system"),
                )
            )
        if m.get("error"):
            events.append(
                event(
                    source,
                    "message",
                    f"{m['id']}:error",
                    turn,
                    location,
                    timestamp=stamp(time.get("completed"), True),
                    name="message error",
                    message_role=m["role"],
                    outcome="failed",
                    content=content(m, "error"),
                )
            )
        if m["role"] == "user":
            agent["start"] = stamp(time.get("created"), True)
            continue
        if m["role"] != "assistant":
            continue
        settings: Settings = dict(
            model=m.get("modelID"), provider=m.get("providerID"), variant=m.get("variant")
        )
        end = stamp(time.get("completed"), True)
        outcome = "failed" if m.get("error") else ("completed" if end is not None else None)
        steps = [p for p in message["parts"] if p["type"] == "step-finish"]
        if steps:
            # Parts are model steps; message.tokens repeats only the latest step.
            for p in steps:
                events.append(
                    event(
                        source,
                        "model",
                        p["id"],
                        turn,
                        f"{location}/parts/{p['id']}",
                        usage=tokens(p.get("tokens")),
                        outcome="completed",
                        finish_reason=p.get("reason"),
                        **settings,
                    )
                )
            diagnostics.append(
                diagnostic(source, "message_snapshot_excluded", turn, native_event_id=m["id"])
            )
        else:
            # Completion also occurs after errors; initialized zeros are not usage.
            measured = end is not None and m.get("finish") and not m.get("error")
            usage = tokens(m.get("tokens") if measured else None)
            diagnostics.append(
                diagnostic(
                    source,
                    "message_only_usage" if measured else "unmeasured_message",
                    turn,
                    native_event_id=m["id"],
                )
            )
            events.append(
                event(
                    source,
                    "model",
                    m["id"],
                    turn,
                    location,
                    start=stamp(time.get("created"), True),
                    end=end,
                    outcome=outcome,
                    usage=usage,
                    **settings,
                )
            )
        if m.get("finish") and m["finish"] not in ("tool-calls", "unknown") or m.get("error"):
            agent.update({"end": end, "outcome": outcome})
        for p in message["parts"]:
            if p["type"] != "tool":
                continue
            state = p.get("state") or {}
            time = state.get("time") or {}
            cid = p.get("callID")
            if not cid:
                diagnostics.append(diagnostic(source, "unidentified_tool", turn, location=location))
                continue
            events.append(
                event(
                    source,
                    "tool",
                    cid,
                    turn,
                    f"{location}/parts/{p['id']}",
                    call_id=cid,
                    name=p.get("tool"),
                    is_wrapper=False,
                    start=stamp(time.get("start"), True),
                    end=stamp(time.get("end"), True),
                    outcome="failed" if state.get("status") == "error" else state.get("status"),
                    content=content(state, "input"),
                    native_record=p,
                    **settings,
                )
            )
            if "output" in state or "error" in state:
                events.append(
                    event(
                        source,
                        "tool_result",
                        f"{cid}:{p['id']}:result",
                        turn,
                        f"{location}/parts/{p['id']}",
                        call_id=cid,
                        name=p.get("tool"),
                        is_wrapper=False,
                        timestamp=stamp(time.get("end"), True),
                        outcome="failed" if state.get("status") == "error" else state.get("status"),
                        content=content(state, "output", "error"),
                        native_record=state,
                        **settings,
                    )
                )
    return list(agents.values()) + events, diagnostics
