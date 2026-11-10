"""Provider-independent accounting, timeline generation and report presentation."""

import json
import time
from collections import Counter, defaultdict
from datetime import timedelta
from typing import cast

from .events import METRICS
from .types import (
    AssignmentAccumulator,
    AssignmentRow,
    Diagnostic,
    Event,
    Group,
    Metric,
    NodeAccumulator,
    Omission,
    Report,
    Settings,
    Source,
    SpawnTree,
    Summary,
    Timeline,
    TimelineEvent,
)


def summarize(events: list[Event], diagnostics: list[Diagnostic]) -> Summary:
    events = [e for e in events if e["kind"] in ("agent", "model", "tool")]
    models = [e for e in events if e["kind"] == "model"]
    calls = [e for e in events if e["kind"] == "tool"]
    unknown = sum(d.get("coverage_effect") == "missing_measurement" for d in diagnostics)
    incomplete = any(
        d.get("coverage_effect") in ("incomplete", "missing_measurement") for d in diagnostics
    )
    metrics: dict[str, Metric] = {}
    for metric in METRICS:
        values = [(e.get("usage") or {}).get(metric) for e in models]
        measured = [v for v in values if v is not None]
        missing = len(values) - len(measured) + unknown
        metrics[metric] = dict(
            total=sum(measured) if measured and not missing and not incomplete else None,
            known_subtotal=sum(measured) if measured else None,
            measured_records=len(measured),
            missing_records=missing,
        )
    durations = [
        end - start
        for e in events
        if (start := e.get("start")) is not None
        and (end := e.get("end")) is not None
        and end >= start
    ]
    return dict(
        tokens=metrics,
        observed_model_measurements=len(models),
        observed_tool_calls=len(calls),
        wrapper_calls=sum(e.get("is_wrapper", False) for e in calls),
        observed_nested_operations=sum(bool(e.get("parent_call_id")) for e in calls),
        missing_parent_call_relationships=sum(not e.get("parent_call_id") for e in calls),
        outcomes=dict(sorted(Counter(e["outcome"] or "unknown" for e in calls).items())),
        observed_operation_seconds=sum(durations) if durations else None,
        timed_operations=len(durations),
        untimed_operations=len(events) - len(durations),
        coverage=dict(sorted(Counter(d["code"] for d in diagnostics).items())),
    )


def spawn_tree(events: list[Event]) -> SpawnTree:
    nodes: dict[str, NodeAccumulator] = {}
    relations = set()
    for e in events:
        node = nodes.setdefault(
            e["agent_id"],
            dict(
                agent_id=e["agent_id"], session_id=e["session_id"], agent_run_ids=set(), turns=set()
            ),
        )
        if e.get("agent_run_id"):
            node["agent_run_ids"].add(e["agent_run_id"])
        node["turns"].add(e["turn_id"])
        for field, kind in [
            ("parent_session_id", "spawn"),
            ("forked_from_id", "fork"),
            ("continued_from_id", "continuation"),
        ]:
            if e.get(field):
                relations.add((f"{e['adapter']}:{e.get(field)}", e["agent_id"], kind))
    return dict(
        nodes=[
            dict(
                agent_id=n["agent_id"],
                session_id=n["session_id"],
                agent_run_ids=sorted(n["agent_run_ids"]),
                turns=sorted(t for t in n["turns"] if t is not None),
            )
            for _, n in sorted(nodes.items())
        ],
        edges=[
            dict(parent=p, child=c, relationship=k, parent_in_selection=p in nodes)
            for p, c, k in sorted(relations)
        ],
    )


def build_report(events: list[Event], diagnostics: list[Diagnostic]) -> Report:
    """Pure accounting. No harness-specific parsing or grouping in adapters."""
    events = [e for e in events if e["kind"] in ("agent", "model", "tool")]
    groups: dict[str, list[Group]] = {}
    omissions: dict[str, Omission] = {}
    for name, fields in [
        ("task", ("task_id",)),
        ("agent_run", ("agent_run_id",)),
        ("role", ("role",)),
        ("model", ("model",)),
        ("effort", ("reasoning_effort",)),
        ("model_effort", ("model", "reasoning_effort")),
        ("task_model_effort", ("task_id", "model", "reasoning_effort")),
        ("tool", ("name",)),
        ("task_tool", ("task_id", "name")),
    ]:
        grouped, gaps = defaultdict(list), defaultdict(list)
        omitted = []
        for e in events:
            if (
                name in ("model", "effort", "model_effort", "task_model_effort")
                and e["kind"] != "model"
            ):
                continue
            if name in ("tool", "task_tool") and e["kind"] != "tool":
                continue
            key = tuple(e.get(k) for k in fields)
            if name != "task" and any(v is None for v in key):
                omitted.append(e["event_id"])
            else:
                grouped[key].append(e)
        unassigned_gaps = 0
        for d in diagnostics:
            key = tuple(d.get(k) for k in fields)
            if all(v is not None for v in key):
                gaps[key].append(d)
                continue
            unassigned_gaps += 1
            # Preserve diagnostic scope across grouping. A source-wide gap can
            # affect several assignments; a turn gap can affect multiple models.
            affected = {
                tuple(e.get(k) for k in fields)
                for e in events
                if any(p.get("source_id") == d.get("source_id") for p in e["provenance"])
                and (d.get("turn_id") is None or e["turn_id"] == d["turn_id"])
            }
            affected = {
                key for key in affected if name == "task" or all(v is not None for v in key)
            }
            if not affected and d.get("coverage_effect") in ("incomplete", "missing_measurement"):
                affected = set(grouped)  # Unknown attribution cannot prove completeness.
            for key in affected:
                gaps[key].append(d)
        groups[name] = [
            dict(
                key=dict(zip(fields, cast(tuple[str | None, ...], key))),
                summary=summarize(grouped[key], gaps[key]),
            )
            for key in sorted(
                grouped.keys() | gaps.keys(), key=lambda key: tuple(v or "" for v in key)
            )
        ]
        omissions[name] = dict(event_ids=omitted, diagnostics_without_attribution=unassigned_gaps)
    return dict(
        version=2,
        summary=summarize(events, diagnostics),
        groups=groups,
        attribution_omissions=omissions,
        spawn_tree=spawn_tree(events),
        diagnostics=diagnostics,
        assignments=assignments(events),
        native_sources=native_sources(events),
        limitations=[
            "Only saved native turns, proven dispatch descendants and background continuations are included.",
            "Known subtotals exclude missing measurements; totals are scoped to observed evidence.",
            "Operation durations can overlap and are not wall-clock, CPU or billed time.",
            "Absent parent-call relationships do not establish absence of nested operations.",
            "Observed settings come from native context, not necessarily provider confirmation.",
        ],
    )


def native_sources(events: list[Event]) -> list[Source]:
    sources: dict[tuple[str, str | None, str, str], set[str]] = {}
    for e in events:
        for p in e["provenance"]:
            key = (p["adapter"], e["session_id"], p["path"], p["source_version"])
            sources.setdefault(key, set()).add(cast(str, e["turn_id"]))
    return [
        dict(
            adapter=adapter,
            tracing_provider=adapter,
            session_id=cast(str, session),
            path=path,
            source_version=version,
            turn_ids=sorted(turns),
        )
        for (adapter, session, path, version), turns in sorted(sources.items())
    ]


def assignments(events: list[Event]) -> list[AssignmentRow]:
    """Unique observed assignments, preserving session reuse and explicit context."""
    fields = (
        "agent_id",
        "agent_run_id",
        "agent_name",
        "native_agent_name",
        "native_agent_path",
        "task_id",
        "role",
        "purpose",
        "assignment_id",
        "assignment_source",
        "assignment_evidence",
    )
    rows: dict[tuple[str, str | None], AssignmentAccumulator] = {}
    for e in events:
        key = (e["agent_id"], e.get("assignment_id"))
        row = rows.setdefault(
            key,
            dict(
                base=cast(AssignmentRow, {k: e.get(k) for k in fields}),
                turns=set(),
                outcomes=set(),
                observed_settings=set(),
                requested_settings=set(),
            ),
        )
        row["turns"].add(e.get("turn_id"))
        settings = (e.get("model"), e.get("reasoning_effort"), e.get("variant"))
        if any(value is not None for value in settings):
            row["observed_settings"].add(settings)
        request = e.get("requested") or {}
        pair = (request.get("model"), request.get("reasoning_effort"))
        if any(v is not None for v in pair):
            row["requested_settings"].add(pair)
        if e["kind"] == "agent":
            row["outcomes"].add(e.get("outcome") or "unfinished")
    return [
        dict(
            **row["base"],
            turns=sorted(t for t in row["turns"] if t),
            outcomes=sorted(row["outcomes"]),
            requested_settings=[
                dict(model=model, reasoning_effort=effort)
                for model, effort in sorted(
                    row["requested_settings"], key=lambda pair: tuple(v or "" for v in pair)
                )
            ],
            observed_settings=[
                dict(
                    model=model,
                    reasoning_effort=effort,
                    **({"variant": variant} if variant is not None else {}),
                )
                for model, effort, variant in sorted(
                    row["observed_settings"], key=lambda pair: tuple(v or "" for v in pair)
                )
            ],
        )
        for _, row in sorted(rows.items(), key=lambda item: str(item[0]))
    ]


def format_settings(settings: list[Settings]) -> str:
    """Keep observed model/effort pairs together, without filling gaps from requests."""
    return (
        "; ".join(
            f"{s.get('model') or 'unavailable'} / {s.get('reasoning_effort') or 'unavailable'}"
            + (f" · variant: {s['variant']}" if s.get("variant") is not None else "")
            for s in settings
        )
        or "unavailable"
    )


def timeline_lanes(
    events: list[Event], lanes: dict[str, int]
) -> tuple[dict[str, int], list[tuple[str, int, int]]]:
    """Pack intervals into tracks where slices can nest without crossing."""
    stacks: dict[str, list[tuple[int, list[float]]]] = {
        agent: [(tid, [])] for agent, tid in lanes.items()
    }
    assigned, extra = {}, []
    next_lane = len(lanes) + 1
    spans = [
        e
        for e in events
        if e.get("start") is not None
        and (
            (e.get("end") is not None and cast(float, e["end"]) >= cast(float, e["start"]))
            or (e["kind"] == "agent" and e.get("end") is None)
        )
    ]
    for e in sorted(
        spans,
        key=lambda e: (
            round(cast(float, e["start"]) * 1_000_000),
            -round(cast(float, e["end"]) * 1_000_000)
            if e.get("end") is not None
            else -float("inf"),
            e["event_id"],
        ),
    ):
        start = round(cast(float, e["start"]) * 1_000_000)
        end = round(cast(float, e["end"]) * 1_000_000) if e.get("end") is not None else float("inf")
        tracks = stacks[e["agent_id"]]
        for tid, ends in tracks:
            while ends and ends[-1] <= start:
                ends.pop()
            if not ends or end <= ends[-1]:
                break
        else:
            tid, ends = next_lane, []
            next_lane += 1
            tracks.append((tid, ends))
            extra.append((e["agent_id"], tid, len(tracks)))
        ends.append(end)
        assigned[e["event_id"]] = tid
    return assigned, extra


def agent_spans(events: list[Event]) -> list[Event]:
    """Project selected turns onto elapsed session spans without changing accounting."""
    grouped: dict[str, list[Event]] = {}
    result = []
    for e in events:
        if e["kind"] == "agent":
            grouped.setdefault(e["agent_id"], []).append(e)
        else:
            result.append(e)
    for turns in grouped.values():
        turns.sort(key=lambda e: (e.get("start") is None, e.get("start") or 0, e["event_id"]))
        starts = [start for e in turns if (start := e.get("start")) is not None]
        ends = [end for e in turns if (end := e.get("end")) is not None]
        span = cast(Event, dict(turns[0]))
        span.update(
            {
                "start": min(starts) if starts else None,
                "end": max(ends) if len(ends) == len(turns) else None,
                "turn_ids": [tid for e in turns if (tid := e.get("turn_id")) is not None],
                "selected_turns": turns,
                "instructions": [i for e in turns for i in e.get("instructions", [])],
            }
        )
        if len(turns) > 1:
            # Assignments and outcomes belong to individual turns, not the span.
            span["name"] = "; ".join(
                (
                    a.get("purpose")
                    or " / ".join(v for v in (a.get("role"), a.get("task_id")) if v)
                    or a["agent_id"]
                )
                + " · "
                + format_settings(a["observed_settings"])
                for a in assignments([e for e in events if e["agent_id"] == span["agent_id"]])
            )
            span = cast(
                Event,
                {
                    k: v
                    for k, v in span.items()
                    if k
                    not in (
                        "turn_id",
                        "task_id",
                        "role",
                        "purpose",
                        "outcome",
                        "assignment_id",
                        "assignment_source",
                        "assignment_evidence",
                        "model",
                        "reasoning_effort",
                        "variant",
                    )
                },
            )
        result.append(span)
    return result


def timeline(events: list[Event]) -> Timeline:
    refreshed = time.time()
    first_seen: dict[str, float] = {}
    for e in events:
        observed = next(
            (e[key] for key in ("start", "timestamp", "end") if e.get(key) is not None),
            float("inf"),
        )
        first_seen[e["agent_id"]] = min(
            first_seen.get(e["agent_id"], float("inf")), cast(float, observed)
        )
    lanes = {
        agent: i + 1
        for i, agent in enumerate(sorted(first_seen, key=lambda agent: (first_seen[agent], agent)))
    }
    labels = defaultdict(set)
    for assignment in assignments(events):
        context = " / ".join(v for v in (assignment.get("role"), assignment.get("task_id")) if v)
        label = assignment.get("agent_name") or assignment["agent_id"]
        label = f"{label} · {context}" if context else label
        labels[assignment["agent_id"]].add(
            f"{label} · {format_settings(assignment['observed_settings'])}"
        )
    events = agent_spans(events)
    event_lanes, extra = timeline_lanes(events, lanes)
    tracks = sorted(
        [(agent, tid, 1) for agent, tid in lanes.items()] + extra,
        key=lambda track: (lanes[track[0]], track[2]),
    )
    output = []
    for rank, (agent, tid, number) in enumerate(tracks):
        label = "; ".join(sorted(labels[agent])) + (f" · parallel {number}" if number > 1 else "")
        output.append(dict(ph="M", name="thread_name", pid=1, tid=tid, args={"name": label}))
        # Perfetto otherwise applies its own thread ordering. Keep parallel
        # tracks adjacent to their session, in session start order.
        output.append(
            dict(ph="M", name="thread_sort_index", pid=1, tid=tid, args={"sort_index": rank})
        )
    omitted, flows = [], set()
    ordered = sorted(
        events,
        key=lambda e: (
            round(
                (
                    cast(float, e.get("start"))
                    if e.get("start") is not None
                    else e.get("timestamp") or e.get("end") or 0
                )
                * 1_000_000
            ),
            -round(cast(float, e["end"]) * 1_000_000)
            if e.get("end") is not None
            else -float("inf"),
            e["event_id"],
        ),
    )
    for e in ordered:
        start, end = e.get("start"), e.get("end")
        point = e.get("timestamp")
        label = (
            e.get("name") or (e.get("agent_name") if e["kind"] == "agent" else None) or e["kind"]
        )
        if e["kind"] == "agent" and not e.get("name"):
            label += " · " + (
                e.get("purpose")
                or " / ".join(v for v in (e.get("role"), e.get("task_id")) if v)
                or "assignment unavailable"
            )
            label += " · " + format_settings([e])
        base: TimelineEvent = dict(
            name=label,
            cat=e["kind"],
            pid=1,
            tid=event_lanes.get(e["event_id"], lanes[e["agent_id"]]),
            args={
                k: e.get(k)
                for k in (
                    "event_id",
                    "task_id",
                    "role",
                    "agent_run_id",
                    "agent_id",
                    "agent_name",
                    "native_agent_name",
                    "native_agent_path",
                    "purpose",
                    "assignment_source",
                    "assignment_evidence",
                    "outcome",
                    "model",
                    "reasoning_effort",
                    "variant",
                    "call_id",
                    "parent_call_id",
                )
            },
        )
        if e["kind"] == "agent":
            base["args"]["turn_ids"] = e["turn_ids"]
            base["args"]["span_meaning"] = (
                "Elapsed observed span, including waits between selected turns"
            )
        base["args"].update(
            {f"tokens.{k}": v for k, v in (e.get("usage") or {}).items() if v is not None}
        )
        for key in (
            "native_event_id",
            "session_id",
            "turn_id",
            "message_role",
            "call_event_id",
            "parent_event_id",
            "turn_event_id",
            "message_id",
            "parent_message_id",
        ):
            if e.get(key) is not None:
                base["args"][key] = e.get(key)
        # JSON strings keep complete arrays/structured values inspectable in
        # Perfetto, whose argument importer otherwise flattens nested objects.
        for key in (
            "content",
            "outputs",
            "instructions",
            "native_record",
            "provenance",
            "selected_turns",
        ):
            if key in e:
                base["args"][key] = json.dumps(e.get(key), ensure_ascii=False, indent=2)
        if start is not None and end is not None and end >= start:
            output.append(
                dict(
                    base,
                    ph="X",
                    ts=round(start * 1_000_000),
                    dur=round(end * 1_000_000) - round(start * 1_000_000),
                )
            )
        elif e["kind"] == "agent" and start is not None and end is None:
            # Keep the slice open so Perfetto fades its unfinished edge.
            # Elapsed time is a snapshot, not an observed completion.
            elapsed_through = max(start, refreshed)
            elapsed = elapsed_through - start
            base["args"]["elapsed_through"] = elapsed_through
            base["args"]["elapsed_seconds"] = elapsed
            output.append(
                dict(
                    base,
                    name=label + f" · unfinished · {timedelta(seconds=int(elapsed))} elapsed",
                    ph="B",
                    ts=round(start * 1_000_000),
                )
            )
            # Extend the trace bounds through the snapshot even when there
            # have been no recent native events.
            output.append(
                dict(
                    name="Elapsed time snapshot",
                    cat="snapshot",
                    ph="i",
                    s="t",
                    pid=1,
                    tid=base["tid"],
                    ts=round(elapsed_through * 1_000_000),
                )
            )
            omitted.append(dict(event_id=e["event_id"], reason="duration_unavailable"))
        elif start is not None or end is not None or point is not None:
            observed = start if start is not None else end if end is not None else point
            output.append(dict(base, ph="i", s="t", ts=round(cast(float, observed) * 1_000_000)))
            if e["kind"] in ("agent", "model", "tool"):
                omitted.append(dict(event_id=e["event_id"], reason="duration_unavailable"))
        else:
            omitted.append(dict(event_id=e["event_id"], reason="timing_unavailable"))
        parent = f"{e['adapter']}:{e.get('parent_session_id')}"
        spawn = e.get("spawn_timestamp")
        if parent in lanes and spawn is not None and e["agent_id"] not in flows:
            flows.add(e["agent_id"])
            fid = lanes[
                e["agent_id"]
            ]  # Chrome/Perfetto IDs are numeric (not arbitrary hash strings).
            for phase, agent in [("s", parent), ("f", e["agent_id"])]:
                # Bind each endpoint to an explicit observed creation instant.
                # Without anchors Perfetto can attach to unrelated enclosing
                # slices and reverse a flow when one lane has only instants.
                output.append(
                    dict(
                        name="native spawn",
                        cat="agent",
                        ph="i",
                        s="t",
                        pid=1,
                        tid=lanes[agent],
                        ts=round(spawn * 1_000_000),
                    )
                )
                output.append(
                    dict(
                        name="spawn",
                        cat="agent",
                        ph=phase,
                        id=fid,
                        pid=1,
                        tid=lanes[agent],
                        ts=round(spawn * 1_000_000),
                        **({"bp": "e"} if phase == "f" else {}),
                    )
                )
    return dict(traceEvents=output, displayTimeUnit="ms", metadata=dict(timing_omissions=omitted))


def markdown(report: Report) -> str:
    lines = [
        "# Selected implementation usage",
        "",
        f"Tracing provider: {report.get('tracing_provider', 'unavailable')}",
        "",
        "Null means unavailable. Known subtotals exclude missing measurements. Scope and omissions are in usage.json.",
        "",
        "| Metric | Total | Known subtotal | Measured records | Missing records |",
        "|---|---:|---:|---:|---:|",
    ]

    def cell(value: object) -> str:
        return (
            str(value).replace("|", "\\|").replace("\n", " ")
            if value is not None
            else "unavailable"
        )

    for metric, measurement in report["summary"]["tokens"].items():
        lines.append("| " + " | ".join(map(cell, [metric, *measurement.values()])) + " |")
    for name, rows in report["groups"].items():
        tools = name in ("tool", "task_tool")
        models = name in ("model", "effort", "model_effort", "task_model_effort")
        headers = (
            ["Group", "Observed calls", "Outcomes", "Observed seconds", "Untimed"]
            if tools
            else ["Group", "Total tokens", "Known subtotal", "Missing records"]
            + ([] if models else ["Tools"])
        )
        lines += [
            "",
            f"## By {name}",
            "",
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
        ]
        for row in rows:
            s = row["summary"]
            tokens = s["tokens"]["total_tokens"]
            values = (
                [
                    s["observed_tool_calls"],
                    s["outcomes"],
                    s["observed_operation_seconds"],
                    s["untimed_operations"],
                ]
                if tools
                else [tokens["total"], tokens["known_subtotal"], tokens["missing_records"]]
                + ([] if models else [s["observed_tool_calls"]])
            )
            label = ", ".join(v if v is not None else "unavailable" for v in row["key"].values())
            lines.append("| " + " | ".join(map(cell, [label, *values])) + " |")
        omission = report["attribution_omissions"][name]
        lines += [
            "",
            f"Attribution omissions: {len(omission['event_ids'])} events; {omission['diagnostics_without_attribution']} diagnostics.",
        ]
    lines += ["", "## Native lineage", ""]
    for edge in report["spawn_tree"]["edges"]:
        lines.append(f"- {edge['parent']} → {edge['child']} ({edge['relationship']})")
    lines += ["", "## Coverage diagnostics", ""]
    for code, n in report["summary"]["coverage"].items():
        lines.append(f"- {code}: {n}")
    return "\n".join(lines) + "\n"
