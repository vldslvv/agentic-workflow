"""Capture selected OpenCode turns through its export CLI, never by recency."""

import json
import shutil
import subprocess
from pathlib import Path
from typing import cast

from tracing.shared.files import identifier, safe_destination, write_atomic
from tracing.shared.types import Diagnostic, Source
from tracing.shared.values import object_value

from .diagnostics import gap
from .types import OpenCode


def export_session(session: str) -> OpenCode:
    identifier(session)
    executable = shutil.which("opencode") or str(Path.home() / ".opencode/bin/opencode")
    result = subprocess.run(
        [executable, "session", "export", session],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        timeout=20,
        check=True,
    )
    data = cast(OpenCode, json.loads(result.stdout))
    if data["info"]["id"] != session or not isinstance(data["messages"], list):
        raise ValueError("OpenCode export identity mismatch")
    return data


def turns(data: OpenCode) -> dict[str, list[OpenCode]]:
    """V2 idle markers delimit turns; steered prompts stay in the active turn."""
    result: dict[str, list[OpenCode]] = {}
    active: str | None = None
    for message in data["messages"]:
        if active is None and message["type"] in ("user", "synthetic"):
            active = message["id"]
            result[active] = []
        if active is not None:
            result[active].append(message)
        if message["type"] == "idle":
            active = None
    return result


def initiators(data: OpenCode) -> list[OpenCode]:
    return [messages[0] for messages in turns(data).values()]


def selected_turn(data: OpenCode, turn: str) -> OpenCode:
    selected = turns(data).get(turn)
    if selected is None:
        raise ValueError("selected OpenCode turn unavailable")
    return dict(info=data["info"], messages=selected)


def save(root: Path, data: OpenCode, turn: str) -> OpenCode:
    selected = selected_turn(data, turn)
    path = safe_destination(
        root, Path(root) / "native" / identifier(data["info"]["id"]) / (identifier(turn) + ".json")
    )
    if path.exists():
        previous = cast(OpenCode, json.loads(path.read_text()))
        # A partial export or removed host history must not erase saved evidence.
        old = {
            m["id"]: {p["id"] for p in m.get("content", []) if p["type"] == "tool"}
            for m in previous["messages"]
        }
        new = {
            m["id"]: {p["id"] for p in m.get("content", []) if p["type"] == "tool"}
            for m in selected["messages"]
        }
        if any(mid not in new or not parts <= new[mid] for mid, parts in old.items()):
            raise ValueError("OpenCode export lost saved observations")
    content = json.dumps(selected, ensure_ascii=False, indent=2) + "\n"
    if not path.exists() or path.read_text() != content:
        write_atomic(path, content)
    return selected


EXPORT_ERRORS = (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError)


def capture_current(root: Path, session: str) -> list[Diagnostic]:
    try:
        data = export_session(session)
        prompts = initiators(data)
        if not prompts:
            return [gap("active_turn_unavailable", session)]
        # OpenCode exports messages in native chronological order.
        save(root, data, prompts[-1]["id"])
        return []
    except EXPORT_ERRORS:
        return [gap("opencode_export_unavailable", session)]


def dispatch_turns(data: OpenCode, part: OpenCode) -> list[str]:
    """Match delivered prompts, including steering, without a completion deadline."""
    prompt = object_value(part.get("state", {}).get("input")).get("prompt")
    clock = part.get("time") or {}
    start = clock.get("ran", clock.get("created"))
    if not isinstance(prompt, str) or not isinstance(start, (int, float)):
        return []
    return [
        turn
        for turn, messages in turns(data).items()
        for message in messages
        if message["type"] == "user"
        and message.get("time", {}).get("created", -1) >= start
        and message.get("text")
        in (
            prompt,
            "You are a subagent spawned by another session.\n" + prompt,
        )
    ]


def notification(message: OpenCode) -> tuple[str, str] | None:
    metadata = message.get("metadata") or {}
    source = metadata.get("source")
    key = {"subagent": "childID", "shell": "shellID"}.get(source or "")
    target = metadata.get(key) if key else None
    return (source, target) if isinstance(source, str) and isinstance(target, str) else None


def refresh(root: Path, sources: list[Source]) -> list[Diagnostic]:
    """Follow dispatches and wake-ups to a fixed point, bounded by new user turns."""
    diagnostics: list[Diagnostic] = []
    cache: dict[str, OpenCode | None] = {}
    seen: set[tuple[str, str]] = set()
    unresolved: set[tuple[str, str]] = set()

    def load(session: str) -> OpenCode | None:
        if session not in cache:
            cache[session] = None
            try:
                cache[session] = export_session(session)
            except EXPORT_ERRORS:
                diagnostics.append(gap("opencode_export_unavailable", session))
        return cache[session]

    pending = [
        (s["session_id"], t)
        for s in sources
        for t in s["turn_ids"]
        if s["path"] == f"native/{s['session_id']}/{t}.json"
    ]
    while pending:
        session, turn = pending.pop()
        if (session, turn) in seen:
            continue
        seen.add((session, turn))
        data = load(session)
        if data is None:
            continue
        try:
            selected = save(root, data, turn)
        except EXPORT_ERRORS:
            diagnostics.append(gap("opencode_turn_unavailable", session, turn))
            continue
        dispatched: set[tuple[str, str]] = set()
        for message in selected["messages"]:
            for part in message.get("content", []):
                if part.get("type") != "tool":
                    continue
                state = part.get("state") or {}
                metadata = state.get("metadata") or {}
                if part.get("name") == "shell":
                    shell = metadata.get("shellID")
                    if shell:
                        dispatched.add(("shell", shell))
                    elif metadata.get("status") == "running" or object_value(
                        state.get("input")
                    ).get("background"):
                        diagnostics.append(gap("opencode_dispatch_unresolved", session, turn))
                    continue
                if part.get("name") != "subagent":
                    continue
                child = metadata.get("sessionID")
                if not child:
                    diagnostics.append(gap("opencode_dispatch_unresolved", session, turn))
                    continue
                target = load(child)
                if target is None:
                    continue
                if target["info"].get("parentID") != session:
                    diagnostics.append(gap("opencode_parent_mismatch", child))
                    continue
                dispatched.add(("subagent", child))
                candidates = dispatch_turns(target, part)
                if len(candidates) != 1:
                    diagnostics.append(
                        gap(
                            "ambiguous_dispatch_turn"
                            if candidates
                            else "opencode_dispatch_unresolved",
                            child,
                        )
                    )
                else:
                    pending.append((child, candidates[0]))
        after = False
        for following, messages in turns(data).items():
            if following == turn:
                after = True
                continue
            if not after:
                continue
            if messages[0]["type"] == "user":
                break
            if any(notification(m) in dispatched for m in messages if m["type"] == "synthetic"):
                pending.append((session, following))
            else:
                unresolved.add((session, following))
    diagnostics.extend(
        gap("opencode_continuation_unresolved", session, turn)
        for session, turn in sorted(unresolved - seen)
    )
    return diagnostics
