"""Parse Codex rollouts into normalized observations."""

import hashlib
import json
import re
from collections import Counter
from collections.abc import Mapping
from pathlib import Path
from typing import cast

from tracing.shared.events import METRICS, add, count, diagnostic, event, stamp
from tracing.shared.events import content as normalized_content
from tracing.shared.types import Content, Diagnostic, Event, EventDetails, Settings, Source, Usage

from .types import Native


def tokens(raw: Native | None) -> Usage:
    if not isinstance(raw, dict):
        raw = {}
    result = {k: count(raw.get(k)) for k in METRICS}
    i, c, o, r = (
        result[k]
        for k in (
            "input_tokens",
            "cached_input_tokens",
            "output_tokens",
            "reasoning_output_tokens",
        )
    )
    if i is not None and c is not None:
        if c > i:
            raise ValueError("cached tokens exceed input")
        result["uncached_input_tokens"] = i - c
    if r is not None and o is not None and r > o:
        raise ValueError("reasoning tokens exceed output")
    result["total_tokens"] = add(i, o)
    return result


def content(payload: Mapping[str, object], *fields: str) -> Content:
    # Native command wrappers report truncation in their returned text.
    truncated = any(
        isinstance(payload.get(key), str)
        and re.search(
            r"(?m)^Warning: truncated output \(original token count: \d+\)", cast(str, payload[key])
        )
        for key in fields
    )
    return normalized_content(payload, *fields, truncated=truncated)


def codex_result_outcome(payload: Native) -> str | None:
    if payload.get("type") == "mcp_tool_call_end":
        result = payload.get("result") or {}
        return (
            "failed"
            if "Err" in result or (result.get("Ok") or {}).get("isError")
            else "completed"
            if "Ok" in result
            else None
        )
    if payload.get("type") == "exec_command_end":
        status = payload.get("status")
        if status is None and isinstance(payload.get("exit_code"), int):
            status = "failed" if payload["exit_code"] != 0 else "completed"
        return status
    return "returned"


def observation_id(
    row: Native, turn: str | None, occurrences: Counter[tuple[str | None, str]]
) -> str:
    """Native IDs win; ID-less records retain repeated occurrences within a turn.

    Fingerprints ignore file offsets so selected copies deduplicate on import.
    An identical ID-less row repeated in one file cannot safely be called a copy.
    """
    payload = row.get("payload") or {}
    if payload.get("id") or payload.get("message_id"):
        return f"{turn}:{row['type']}:{payload.get('type')}:{payload.get('id') or payload['message_id']}"
    digest = hashlib.sha256(
        json.dumps(row, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()
    key = (turn, digest)
    occurrences[key] += 1
    return f"{turn}:{digest}:{occurrences[key]}"


def parse(source: Source, path: Path) -> tuple[list[Event], list[Diagnostic]]:
    events: list[Event] = []
    diagnostics: list[Diagnostic] = []
    calls: dict[str, Event] = {}
    agents: dict[str | None, Event] = {}
    models: dict[str, Event] = {}
    selected = set(source["turn_ids"])
    active: str | None = None
    settings: Settings = {}
    meta: EventDetails = {}
    contexts: dict[str | None, Settings] = {}
    observations: list[Event] = []
    occurrences: Counter[tuple[str | None, str]] = Counter()
    session_context: dict[str, object] = {}
    declared, native_version = False, None
    with path.open("rb") as stream:
        for line, raw in enumerate(stream, 1):
            try:
                row = cast(Native, json.loads(raw))
            except ValueError:
                diagnostics.append(diagnostic(source, "invalid_json_line", location=line))
                continue
            p = row.get("payload") or {}
            kind = row.get("type")
            if kind == "session_meta":
                if p.get("id") != source["session_id"]:
                    raise ValueError("session identity mismatch")
                declared = True
                native_version = p.get("cli_version")
                origin = p.get("source")
                spawn = (
                    ((origin.get("subagent") or {}).get("thread_spawn") or {})
                    if isinstance(origin, dict)
                    else {}
                )
                meta = dict(
                    parent_session_id=p.get("parent_thread_id") or spawn.get("parent_thread_id"),
                    native_agent_name=p.get("agent_nickname") or spawn.get("agent_nickname"),
                    native_agent_path=p.get("agent_path") or spawn.get("agent_path"),
                    forked_from_id=p.get("forked_from_id"),
                    continued_from_id=None,
                    spawn_timestamp=stamp(p.get("timestamp")),
                )
                session_context = {key: value for key, value in p.items() if "instruction" in key}
                session_location = line
                continue
            if kind == "turn_context":
                active = p.get("turn_id")
                settings = dict(model=p.get("model"), reasoning_effort=p.get("effort"))
                contexts[active] = settings
            if kind == "event_msg" and p.get("type") == "task_started":
                active = p.get("turn_id", active)
            turn = (
                p.get("turn_id")
                or (p.get("internal_chat_message_metadata_passthrough") or {}).get("turn_id")
                or active
            )
            if (
                turn not in selected
                or p.get("thread_id", source["session_id"]) != source["session_id"]
            ):
                continue
            settings = contexts.get(turn, {})
            t = stamp(row.get("timestamp"))
            if turn not in agents:
                agents[turn] = event(source, "agent", turn, turn, line, **meta)
                if session_context:
                    observations.append(
                        event(
                            source,
                            "instruction",
                            f"{turn}:session-context",
                            turn,
                            session_location,
                            content=content(session_context, *session_context),
                            name="session instructions",
                            context_scope="session",
                        )
                    )
            agent = agents[turn]
            subtype = p.get("type")
            observation_kind = None
            fields: tuple[str, ...] = ()
            if kind == "turn_context":
                observation_kind, fields = "instruction", tuple(p)
            elif kind == "response_item" and subtype in ("message", "reasoning"):
                observation_kind = (
                    "instruction" if p.get("role") in ("developer", "system") else "message"
                )
                fields = ("content", "summary")
            elif kind in ("event_msg", "response_item") and subtype in (
                "user_message",
                "agent_message",
                "agent_reasoning",
                "agent_reasoning_raw_content",
            ):
                observation_kind, fields = "message", ("message", "text", "content")
            elif (
                kind == "response_item"
                and subtype in ("function_call_output", "custom_tool_call_output")
                or kind == "event_msg"
                and subtype in ("exec_command_end", "mcp_tool_call_end")
            ):
                observation_kind, fields = (
                    "tool_result",
                    ("output", "stdout", "stderr", "aggregated_output", "result"),
                )
            if observation_kind:
                observations.append(
                    event(
                        source,
                        observation_kind,
                        observation_id(row, turn, occurrences),
                        turn,
                        line,
                        timestamp=t,
                        call_id=p.get("call_id"),
                        name=subtype or kind,
                        message_role=p.get("role")
                        or ("user" if subtype == "user_message" else None),
                        outcome=codex_result_outcome(p)
                        if observation_kind == "tool_result"
                        else None,
                        content=content(p, *fields),
                        native_record=p,
                        **settings,
                    )
                )
            if kind == "turn_context":
                agent.update(cast(Event, settings))
            if kind == "event_msg":
                subtype = p.get("type")
                if subtype == "task_started":
                    start = stamp(p.get("started_at"))
                    agent["start"] = start if start is not None else t
                elif subtype in ("task_complete", "task_completed", "turn_aborted"):
                    agent.update(
                        {
                            "end": t,
                            "outcome": "aborted" if subtype == "turn_aborted" else "completed",
                        }
                    )
                elif subtype == "token_count":
                    diagnostics.append(diagnostic(source, "aggregate_snapshot_excluded", turn))
                elif subtype in ("exec_command_end", "mcp_tool_call_end"):
                    call = calls.get(p.get("call_id", ""))
                    if call:
                        call.update({"end": t, "outcome": codex_result_outcome(p)})
                continue
            if kind == "token_usage_record":
                rid = p.get("response_id")
                if not rid:
                    diagnostics.append(
                        diagnostic(source, "unidentified_usage", turn, location=line)
                    )
                    continue
                model = event(
                    source,
                    "model",
                    rid,
                    turn,
                    line,
                    timestamp=t,
                    end=t,
                    outcome="completed",
                    usage=tokens(p.get("usage")),
                    **settings,
                )
                old = models.get(rid)
                if old:
                    if any(
                        old.get(k) != model.get(k)
                        for k in ("turn_id", "usage", "model", "reasoning_effort")
                    ):
                        raise ValueError("conflicting duplicate usage")
                    old["provenance"] += model["provenance"]
                else:
                    models[rid] = model
            if kind == "response_item":
                subtype, cid = p.get("type"), p.get("call_id")
                if subtype in ("function_call", "custom_tool_call"):
                    if not cid:
                        diagnostics.append(
                            diagnostic(source, "unidentified_tool", turn, location=line)
                        )
                        continue
                    call = event(
                        source,
                        "tool",
                        cid,
                        turn,
                        line,
                        start=t,
                        timestamp=t,
                        call_id=cid,
                        name=p.get("name"),
                        is_wrapper=p.get("name") in ("functions.exec", "exec"),
                        parent_call_id=p.get("parent_call_id"),
                        content=content(p, "arguments", "input"),
                        native_record=p,
                        **settings,
                    )
                    if cid in calls:
                        old = calls[cid]
                        if any(
                            old.get(k) != call.get(k)
                            for k in (
                                "turn_id",
                                "name",
                                "parent_call_id",
                                "content",
                                "native_record",
                            )
                        ):
                            raise ValueError("conflicting duplicate tool call")
                        old["provenance"] += call["provenance"]
                    else:
                        calls[cid] = call
                elif subtype in ("function_call_output", "custom_tool_call_output"):
                    if cid in calls:
                        # Completion is observed; success is unknown without structured status.
                        calls[cid]["end"] = t
                        calls[cid]["outcome"] = calls[cid]["outcome"] or "returned"
                    else:
                        diagnostics.append(
                            diagnostic(source, "orphan_tool_result", turn, location=line)
                        )
    if not declared:
        diagnostics.append(diagnostic(source, "missing_native_identity"))
    if native_version != "0.167.0":
        diagnostics.append(
            diagnostic(source, "unverified_native_version", native_version=native_version)
        )
    events.extend(agents.values())
    events.extend(models.values())
    events.extend(calls.values())
    events.extend(observations)
    for item in events:
        for field in (
            "native_agent_name",
            "native_agent_path",
            "parent_session_id",
            "forked_from_id",
            "continued_from_id",
            "spawn_timestamp",
        ):
            item.update(cast(Event, {field: meta.get(field)}))
    return events, diagnostics
