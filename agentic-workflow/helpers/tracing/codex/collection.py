"""Codex identity, saved-turn selection, dispatch matching and assignments."""

import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import cast

from tracing.shared.assignments import annotate_assignments, assignment_tag
from tracing.shared.events import read_source, stamp
from tracing.shared.files import identifier, local_path, safe_destination, write_atomic
from tracing.shared.types import (
    Assignment,
    CollectedEvidence,
    Diagnostic,
    Event,
    EvidenceKey,
    Settings,
    Source,
)

from .diagnostics import classify, gap
from .parser import parse
from .types import Dispatch, Document, Native


def object_value(value: object) -> Native:
    if isinstance(value, dict):
        return cast(Native, value)
    if not isinstance(value, (str, bytes, bytearray)):
        return {}
    try:
        result = json.loads(value)
        return cast(Native, result) if isinstance(result, dict) else {}
    except (ValueError, TypeError):
        return {}


def lineage(meta: Native) -> tuple[str | None, str | None]:
    origin = object_value(meta.get("source"))
    spawn = (origin.get("subagent") or {}).get("thread_spawn") or {}
    return (
        meta.get("parent_thread_id") or spawn.get("parent_thread_id"),
        meta.get("agent_path") or spawn.get("agent_path"),
    )


def native_index() -> dict[str, Native]:
    """Read only identity/path/parent metadata, never search by cwd or recency."""
    home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    databases = sorted(
        home.glob("state_*.sqlite"), key=lambda p: int(p.stem.split("_")[-1]), reverse=True
    )
    if not databases:
        raise OSError("native index unavailable")
    with closing(
        sqlite3.connect(databases[0].resolve().as_uri() + "?mode=ro", uri=True)
    ) as connection:
        connection.execute("PRAGMA query_only=ON")
        columns = {r[1] for r in connection.execute("PRAGMA table_info(threads)")}
        fields = ["id", "rollout_path", "source"] + [f for f in ("agent_path",) if f in columns]
        entries: dict[str, Native] = {}
        for row in connection.execute("SELECT " + ",".join(fields) + " FROM threads"):
            values: dict[str, object] = dict(zip(fields, row))
            sid, path = values["id"], values["rollout_path"]
            source, agent_path = values["source"], values.get("agent_path")
            if not isinstance(sid, str) or not isinstance(path, str):
                raise ValueError("native index needs string identities and rollout paths")
            if source is not None and not isinstance(source, (str, bytes)):
                raise ValueError("native index source must be serialized metadata")
            if agent_path is not None and not isinstance(agent_path, str):
                raise ValueError("native index agent path must be a string")
            entry: Native = {"id": sid, "rollout_path": path, "source": source}
            if "agent_path" in values:
                entry["agent_path"] = agent_path
            entries[sid] = entry
    return entries


def codex_document(path: Path | str) -> Document:
    """Keep raw lines separately from parsed selection metadata, including tails."""
    path = Path(path)
    raw_rows = path.read_bytes().splitlines(keepends=True)
    meta: Native | None = None
    records: list[tuple[str | None, Native | None, bytes]] = []
    active: str | None = None
    for raw in raw_rows:
        try:
            row = json.loads(raw)
            if not isinstance(row, dict) or not isinstance(row.get("payload"), dict):
                raise ValueError("invalid native record")
        except (ValueError, UnicodeError):
            records.append((active, None, raw))
            continue
        row = cast(Native, row)
        p = row["payload"]
        if row["type"] == "session_meta":
            if meta and meta.get("id") != p.get("id"):
                raise ValueError("ambiguous native session metadata")
            meta = p
            records.append((None, row, raw))
            continue
        if row["type"] == "turn_context" or (
            row["type"] == "event_msg" and p.get("type") == "task_started"
        ):
            active = p.get("turn_id", active)
        turn = (
            p.get("turn_id")
            or (p.get("internal_chat_message_metadata_passthrough") or {}).get("turn_id")
            or active
        )
        records.append((turn, row, raw))
    if not meta or not meta.get("id"):
        raise ValueError("native file needs session metadata")
    sid = identifier(meta["id"])
    foreign = {
        turn
        for turn, row, _ in records
        if row
        and row["type"] == "token_usage_record"
        and row["payload"].get("thread_id", sid) != sid
    }
    creation = stamp(meta.get("timestamp"))
    turns: list[str] = []
    for turn, row, _ in records:
        if not turn or turn in foreign:
            continue
        if meta.get("forked_from_id"):
            # Forks can copy parent history. Native creation bounds that history;
            # it never establishes a relationship to another session.
            t = stamp(row.get("timestamp")) if row else None
            if creation is None or t is None or t < creation:
                continue
        if turn not in turns:
            turns.append(identifier(turn))
    return dict(path=path, meta=meta, session_id=sid, records=records, turns=turns)


def saved_documents(root: Path) -> list[Document]:
    return [
        codex_document(local_path(root, path))
        for path in sorted((root / "native").rglob("*.jsonl"))
        if path.is_file()
    ]


def save_turn(root: Path, document: Document, turn: str) -> bool:
    if turn not in document["turns"]:
        return False
    sid = document["session_id"]
    path = safe_destination(
        root, Path(root) / "native" / identifier(sid) / (identifier(turn) + ".jsonl")
    )
    content = b"".join(
        raw
        for tid, row, raw in document["records"]
        if (row and row["type"] == "session_meta") or tid == turn
    )
    if path.exists():
        old = path.read_bytes()
        # An active writer may expose an incomplete final record, or an index
        # can briefly point at a shorter rollout. Keep already captured evidence.
        if old.startswith(content) and len(old) > len(content):
            return False
        if old == content:
            return False
    write_atomic(path, content)
    return True


def capture_current(root: Path, sid: str) -> list[Diagnostic]:
    try:
        entry = native_index().get(sid)
        if not entry:
            return [gap("native_identity_unresolved", sid)]
        doc = codex_document(entry["rollout_path"])
        if doc["session_id"] != sid:
            return [gap("native_identity_mismatch", sid)]
        if not doc["turns"]:
            return [gap("active_turn_unavailable", sid)]
        save_turn(root, doc, doc["turns"][-1])
        return []
    except (OSError, sqlite3.Error):
        return [gap("native_storage_unavailable", sid)]
    except ValueError:
        return [gap("invalid_native_source", sid)]


def message_text(payload: Native) -> str:
    content = payload.get("content") or []
    return (
        "\n".join(part.get("text", "") for part in content if isinstance(part, dict))
        if isinstance(content, list)
        else ""
    )


def assignment_message(payload: Native, agent_path: str | None) -> bool:
    return payload.get("role") in ("user", "assistant") or (
        payload.get("type") == "agent_message"
        and agent_path is not None
        and payload.get("recipient") == agent_path
    )


def observed_agent_paths(
    documents: list[Document], diagnostics: list[Diagnostic]
) -> dict[str, str]:
    """Resolve paths by explicit native identity, including activity about the root."""
    paths: dict[str, set[str]] = {}
    for doc in documents:
        sid, path = doc["session_id"], lineage(doc["meta"])[1]
        if path:
            paths.setdefault(sid, set()).add(path)
        for turn, row, _ in doc["records"]:
            if turn not in doc["turns"] or not row or row["type"] != "event_msg":
                continue
            item = row["payload"].get("item") or {}
            if (
                item.get("type") == "SubAgentActivity"
                and item.get("agent_thread_id")
                and (observed_path := item.get("agent_path"))
            ):
                paths.setdefault(item["agent_thread_id"], set()).add(observed_path)
    resolved = {}
    for sid, values in paths.items():
        if len(values) == 1:
            resolved[sid] = next(iter(values))
        else:
            diagnostics.append(gap("ambiguous_native_agent_path", sid))
    return resolved


def dispatches(document: Document, selected: set[str]) -> list[Dispatch]:
    results: dict[str | None, Native] = {}
    calls: list[Dispatch] = []
    for turn, row, _ in document["records"]:
        if turn not in selected or not row or row["type"] != "response_item":
            continue
        p = row["payload"]
        if p.get("type") in ("function_call_output", "custom_tool_call_output"):
            results[p.get("call_id")] = object_value(p.get("output"))
        name = p.get("name", "").rsplit(".", 1)[-1]
        if p.get("type") in ("function_call", "custom_tool_call") and name in (
            "spawn_agent",
            "followup_task",
            "send_message",
        ):
            calls.append(
                dict(
                    kind=name,
                    arguments=object_value(p.get("arguments") or p.get("input")),
                    call_id=p.get("call_id"),
                    timestamp=stamp(row.get("timestamp")),
                    turn=turn,
                )
            )
    for call in calls:
        call["result"] = results.get(call["call_id"], {})
    return calls


def dispatch_turn(document: Document, call: Dispatch, before: float | None = None) -> str | None:
    """Use returned native turn IDs or matching delivered messages before timing.

    A single new native turn following a dispatch is resolvable once identity is
    proven. Multiple possible turns remain ambiguous; never select all of them.
    """
    explicit = call["result"].get("turn_id")
    if explicit:
        return explicit if explicit in document["turns"] else None
    message = call["arguments"].get("message")
    mid = call["result"].get("message_id")
    matches = [
        tid
        for tid, row, _ in document["records"]
        if tid in document["turns"]
        and row
        and row["type"] == "response_item"
        and row["payload"].get("role") == "user"
        and (
            (mid and row["payload"].get("id") == mid)
            or (message and message_text(row["payload"]) == message)
        )
        and (
            before is None
            or (
                stamp(row.get("timestamp")) is not None
                and cast(float, stamp(row["timestamp"])) < before
            )
        )
        and (
            call["timestamp"] is None
            or stamp(row.get("timestamp")) is None
            or cast(float, stamp(row["timestamp"])) >= call["timestamp"]
        )
    ]
    matches = list(dict.fromkeys(matches))
    if len(matches) == 1:
        return matches[0]
    if call["kind"] == "spawn_agent":
        return document["turns"][0] if document["turns"] else None
    candidates = []
    for turn in document["turns"]:
        starts = [
            stamp(row.get("timestamp"))
            for tid, row, _ in document["records"]
            if tid == turn
            and row
            and row["type"] == "event_msg"
            and row["payload"].get("type") == "task_started"
        ]
        if (
            starts
            and starts[0] is not None
            and call["timestamp"] is not None
            and starts[0] >= call["timestamp"]
            and (before is None or starts[0] < before)
        ):
            candidates.append(turn)
    if len(candidates) == 1 and call["kind"] == "followup_task":
        return candidates[0]
    if call["kind"] in ("send_message", "followup_task") and call["timestamp"] is not None:
        active_turns: list[str] = []
        for turn in document["turns"]:
            start_times: list[float] = []
            ends: list[float] = []
            for tid, row, _ in document["records"]:
                if tid != turn or not row or row["type"] != "event_msg":
                    continue
                p, t = row["payload"], stamp(row.get("timestamp"))
                if t is None:
                    continue
                if p.get("type") == "task_started":
                    start_times.append(t)
                elif p.get("type") in ("task_complete", "task_completed", "turn_aborted"):
                    ends.append(t)
            if (
                start_times
                and min(start_times) <= call["timestamp"]
                and (not ends or call["timestamp"] <= max(ends))
            ):
                active_turns.append(turn)
        if len(active_turns) == 1:
            return active_turns[0]
    return None


def collect(implementation_dir: Path) -> CollectedEvidence:
    """Refresh saved selections and their proven dispatch descendants.

    Caller holds the implementation lock across collection and report writes.
    Returns normalized events, source descriptors, assignment context, requested
    settings and coverage diagnostics. Source descriptors are never persisted.
    """
    root = Path(implementation_dir).resolve()
    saved = saved_documents(root)
    diagnostics, index = [], {}
    try:
        index = native_index()
    except (OSError, sqlite3.Error):
        diagnostics.append(gap("native_storage_unavailable"))
    documents: dict[str, Document] = {}
    selected: dict[str, set[str]] = {}
    for doc in saved:
        sid = doc["session_id"]
        selected.setdefault(sid, set()).update(doc["turns"])
        if sid in documents:
            documents[sid]["records"].extend(doc["records"])
            documents[sid]["turns"] = list(dict.fromkeys(documents[sid]["turns"] + doc["turns"]))
        else:
            documents[sid] = doc
    loaded, refreshed = set(), set()

    def load(sid: str) -> Document | None:
        if sid in loaded:
            return documents.get(sid)
        loaded.add(sid)
        if sid not in index:
            if index:
                diagnostics.append(gap("native_identity_unresolved", sid))
            return documents.get(sid)
        try:
            doc = codex_document(index[sid]["rollout_path"])
            if doc["session_id"] != sid:
                diagnostics.append(gap("native_identity_mismatch", sid))
            else:
                documents[sid] = doc
                refreshed.add(sid)
        except (OSError, ValueError):
            diagnostics.append(gap("native_source_unavailable", sid))
        return documents.get(sid)

    for doc in documents.values():
        order: dict[str | None, float] = {}
        for turn, row, _ in doc["records"]:
            if row and turn in doc["turns"]:
                order.setdefault(turn, stamp(row.get("timestamp")) or 0)
        doc["turns"].sort(key=lambda turn: (order.get(turn, 0), turn))
    # Metadata from saved files also resolves descendants during offline analysis.
    candidates = dict(index)
    for sid, doc in documents.items():
        candidates.setdefault(sid, cast(Native, dict(doc["meta"], id=sid)))

    def tree_root(sid: str) -> str:
        seen = set()
        while sid in candidates and sid not in seen:
            seen.add(sid)
            parent = lineage(candidates[sid])[0]
            if not parent:
                return sid
            sid = parent
        return sid

    assignments: dict[EvidenceKey, Assignment] = {}
    requested: dict[EvidenceKey, Settings] = {}
    seen: set[tuple[str, str | None]] = set()
    changed = True
    while changed:
        changed = False
        for sid, turns in list(selected.items()):
            loaded_doc = load(sid)
            if not loaded_doc:
                continue
            doc = loaded_doc
            calls = dispatches(doc, turns)
            for call in calls:
                key = (sid, call["call_id"])
                if key in seen:
                    continue
                seen.add(key)
                args, result = call["arguments"], call["result"]
                if result.get("error") or result.get("status") in ("failed", "error"):
                    continue
                target = result.get("agent_id") or result.get("thread_id")
                path = result.get("task_name") or result.get("agent_path") or args.get("target")
                if not target and path in candidates:
                    target = path
                if not target:
                    if not path and call["kind"] == "spawn_agent" and args.get("task_name"):
                        path = (lineage(doc["meta"])[1] or "/root") + "/" + args["task_name"]
                    if path and not path.startswith("/"):
                        path = (lineage(doc["meta"])[1] or "/root") + "/" + path
                    scope = tree_root(sid)
                    matches = [
                        cid
                        for cid, entry in candidates.items()
                        if (lineage(entry)[1] or ("/root" if cid == scope else None)) == path
                        and (
                            lineage(entry)[0] == sid
                            if call["kind"] == "spawn_agent"
                            else tree_root(cid) == scope
                        )
                    ]
                    if len(matches) == 1:
                        target = matches[0]
                    else:
                        diagnostics.append(
                            gap(
                                "ambiguous_native_identity"
                                if matches
                                else "native_identity_unresolved",
                                sid,
                                call["turn"],
                            )
                        )
                        continue
                child = load(target)
                if not child:
                    diagnostics.append(gap("native_source_unavailable", target))
                    continue
                aliases = {target, lineage(child["meta"])[1]}
                next_dispatch = [
                    c["timestamp"]
                    for c in calls
                    if c["timestamp"] is not None
                    and call["timestamp"] is not None
                    and c["timestamp"] > call["timestamp"]
                    and (
                        c["arguments"].get("target") in aliases
                        or c["arguments"].get("target")
                        == (lineage(child["meta"])[1] or "").rsplit("/", 1)[-1]
                    )
                ]
                turn = dispatch_turn(child, call, min(next_dispatch) if next_dispatch else None)
                if not turn:
                    diagnostics.append(gap("ambiguous_dispatch_turn", target))
                    continue
                if turn not in selected.setdefault(target, set()):
                    selected[target].add(turn)
                    changed = True
                tag, ambiguous = assignment_tag(args.get("message") or "", root.name)
                if ambiguous:
                    diagnostics.append(gap("ambiguous_assignment", target, turn))
                if tag:
                    previous = assignments.get(("codex", target, turn))
                    if previous and previous != tag:
                        diagnostics.append(gap("ambiguous_assignment", target, turn))
                        assignments[("codex", target, turn)] = {}
                    else:
                        assignments[("codex", target, turn)] = tag
                request = requested.setdefault(("codex", target, turn), {})
                request.update(
                    cast(
                        Settings,
                        {
                            k: args.get(k)
                            for k in ("model", "reasoning_effort")
                            if args.get(k) is not None
                        },
                    )
                )
    # Capture only selected turns, including active partial logs. Host files are
    # read-only. Never overwrite explicitly supplied saved exports at other paths.
    for sid, turns in selected.items():
        if sid in refreshed:
            for turn in sorted(turns):
                if turn not in documents[sid]["turns"]:
                    diagnostics.append(gap("native_turn_unavailable", sid, turn))
                else:
                    save_turn(root, documents[sid], turn)
    # Re-read the copies: parsing and reports must describe the saved evidence.
    saved = saved_documents(root)
    sources: list[Source] = []
    if not saved:
        diagnostics.append(gap("no_native_evidence"))
    paths = observed_agent_paths(saved, diagnostics)
    for doc in saved:
        path = str(doc["path"].relative_to(root))
        sources.append(
            dict(
                id=path,
                path=path,
                adapter="codex",
                session_id=doc["session_id"],
                source_version="codex-rollout-" + str(doc["meta"].get("cli_version")),
                turn_ids=doc["turns"],
                native_agent_path=paths.get(doc["session_id"]),
            )
        )
    # Assignment inheritance is native-session scoped, in native turn order.
    for sid in sorted({s["session_id"] for s in sources if s["adapter"] == "codex"}):
        session_docs = [d for d in saved if d["session_id"] == sid]
        order = {}
        for d in session_docs:
            for turn, row, _ in d["records"]:
                if turn in d["turns"] and row:
                    order.setdefault(turn, stamp(row.get("timestamp")) or 0)
        previous = None
        prior_request: Settings = {}
        for turn in sorted(order, key=lambda t: (order[t], t or "")):
            text = "\n".join(
                message_text(row["payload"])
                for d in session_docs
                for tid, row, _ in d["records"]
                if tid == turn
                and row
                and row["type"] == "response_item"
                and assignment_message(row["payload"], paths.get(sid))
            )
            tag, ambiguous = assignment_tag(text, root.name)
            if ambiguous:
                diagnostics.append(gap("ambiguous_assignment", sid, turn))
                previous = None
            elif tag:
                previous = tag
            elif ("codex", sid, turn) in assignments:
                previous = assignments[("codex", sid, turn)] or None
            assignments[("codex", sid, turn)] = previous or {}
            request = requested.get(("codex", sid, turn), {})
            prior_request = {
                "model": request.get("model") or prior_request.get("model"),
                "reasoning_effort": request.get("reasoning_effort")
                or prior_request.get("reasoning_effort"),
            }
            requested[("codex", sid, turn)] = prior_request.copy()
    annotate_assignments(root, sources, assignments, "codex")
    events: list[Event] = []
    for source in sources:
        source["tracing_provider"] = "codex"
        native, gaps = read_source(source, root / source["path"], parse)
        events.extend(native)
        diagnostics.extend(gaps)
    return CollectedEvidence(events, sources, assignments, requested, classify(diagnostics))
