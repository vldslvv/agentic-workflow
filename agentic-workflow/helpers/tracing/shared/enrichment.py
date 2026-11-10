"""Enrich and deduplicate normalized evidence using explicit assignment joins."""

import hashlib
import json
from pathlib import Path
from typing import cast

from .types import CollectedEvidence, Diagnostic, Event


def identity(*parts: object) -> str:
    return hashlib.sha256(json.dumps(parts, separators=(",", ":")).encode()).hexdigest()[:24]


def enrich(root: Path, evidence: CollectedEvidence) -> tuple[list[Event], list[Diagnostic]]:
    """Join normalized measurements and assignment context without host I/O."""
    root = Path(root)
    sources, assignments, requested = evidence.sources, evidence.assignments, evidence.requested
    diagnostics = [d for d in evidence.diagnostics if "source_id" not in d]
    events: dict[str, Event] = {}
    for source in sources:
        native = [e for e in evidence.events if e["provenance"][0]["source_id"] == source["id"]]
        gaps = [d for d in evidence.diagnostics if d.get("source_id") == source["id"]]
        for item in [*native, *gaps]:
            assignment = assignments.get(
                (source["adapter"], source["session_id"], item.get("turn_id")), {}
            )
            item.update(
                {
                    "implementation_id": root.name,
                    "adapter": source["adapter"],
                    "tracing_provider": source["adapter"],
                    "agent_id": f"{source['adapter']}:{source['session_id']}",
                    "task_id": assignment.get("task"),
                    "role": assignment.get("role"),
                    "agent_run_id": f"{source['adapter']}:{source['session_id']}",
                    "assignment_id": identity(source["session_id"], assignment),
                }
            )
        for e in native:
            assignment = assignments.get(
                (source["adapter"], source["session_id"], e["turn_id"]), {}
            )
            e["requested"] = requested.get(
                (source["adapter"], source["session_id"], e["turn_id"]), {}
            )
            e["native_agent_path"] = e.get("native_agent_path") or source.get("native_agent_path")
            e["agent_name"] = e.get("native_agent_name") or (
                "root" if e["native_agent_path"] == "/root" else e["agent_id"]
            )
            e["purpose"] = assignment.get("purpose")
            e["assignment_source"] = assignment.get("source", "native") if assignment else None
            e["assignment_evidence"] = assignment.get("evidence", [])
            e["event_id"] = identity(
                e["implementation_id"], e["agent_id"], e["kind"], e["native_event_id"]
            )
            old = events.get(e["event_id"])
            if old:
                ignored = {"provenance"}
                if {k: v for k, v in old.items() if k not in ignored} != {
                    k: v for k, v in e.items() if k not in ignored
                }:
                    raise ValueError("conflicting duplicate native event")
                old["provenance"] += e["provenance"]
            else:
                events[e["event_id"]] = e
        for turn in source["turn_ids"]:
            if not assignments.get((source["adapter"], source["session_id"], turn)):
                gaps.append(
                    dict(
                        code="missing_assignment",
                        coverage_effect="informational",
                        tracing_provider=source["adapter"],
                        session_id=source["session_id"],
                        turn_id=turn,
                        source_id=source["id"],
                    )
                )
        diagnostics.extend(gaps)
    # Repeated copies can contain identical source-wide diagnostics.
    unique = {json.dumps(d, sort_keys=True): d for d in diagnostics}
    observed = list(events.values())
    calls = {
        (e["agent_id"], e["turn_id"], e["call_id"]): e for e in observed if e["kind"] == "tool"
    }
    turns = {(e["agent_id"], e["turn_id"]): e for e in observed if e["kind"] == "agent"}
    for e in observed:
        e["provenance"] = list({json.dumps(p, sort_keys=True): p for p in e["provenance"]}.values())
        if e["kind"] == "tool":
            parent = calls.get((e["agent_id"], e["turn_id"], e.get("parent_call_id")))
            e["parent_event_id"] = parent["event_id"] if parent else None
            e["outputs"] = []
        if e["kind"] == "agent":
            e["instructions"] = []
    for e in observed:
        if e["kind"] == "tool_result":
            call = calls.get((e["agent_id"], e["turn_id"], e["call_id"]))
            e["call_event_id"] = call["event_id"] if call else None
            if call:
                e["tool_name"] = call.get("name")
                call["outputs"].append(e)
        if e["kind"] == "instruction":
            agent = turns.get((e["agent_id"], e["turn_id"]))
            e["turn_event_id"] = agent["event_id"] if agent else None
            if agent:
                agent["instructions"].append(e)
    for e in observed:
        for field in ("outputs", "instructions"):
            if field in e:
                e[field].sort(key=event_order)
    return sorted(observed, key=event_order), [unique[k] for k in sorted(unique)]


def event_order(e: Event) -> tuple[bool, float, str, tuple[int, ...], str]:
    observed = next((e.get(k) for k in ("timestamp", "start", "end") if e.get(k) is not None), None)
    location = e["provenance"][0]["location"]
    # Keep native ordering for records sharing a timestamp, including parts.
    order = tuple(int(part) for part in str(location).split("/") if part.isdigit())
    return (observed is None, cast(float, observed or 0), e["agent_id"], order, e["event_id"])
