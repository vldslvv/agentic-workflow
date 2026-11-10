"""Construct and validate normalized observations without native interpretation."""

import math
from collections.abc import Callable, Mapping
from datetime import datetime
from pathlib import Path
from typing import Unpack, cast

from .types import Content, Diagnostic, DiagnosticDetails, Event, EventDetails, Source

METRICS = (
    "input_tokens",
    "cached_input_tokens",
    "cache_write_input_tokens",
    "uncached_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
)


def stamp(value: object, milliseconds: bool = False) -> float | None:
    if isinstance(value, (float, int)) and not isinstance(value, bool):
        return value / (1000 if milliseconds else 1) if math.isfinite(value) else None
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return parsed.timestamp() if parsed.tzinfo else None
        except ValueError:
            pass
    return None


def count(value: object) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None


def add(*values: int | None) -> int | None:
    return (
        sum(value for value in values if value is not None)
        if all(v is not None for v in values)
        else None
    )


def event(
    source: Source,
    kind: str,
    native_id: str,
    turn: str | None,
    location: str | int,
    **values: Unpack[EventDetails],
) -> Event:
    result: Event = dict(
        kind=kind,
        tracing_provider=source["adapter"],
        native_event_id=native_id,
        session_id=source["session_id"],
        turn_id=turn,
        start=None,
        end=None,
        timestamp=None,
        outcome=None,
        model=None,
        reasoning_effort=None,
        variant=None,
        provider=None,
        parent_session_id=None,
        forked_from_id=None,
        continued_from_id=None,
        parent_call_id=None,
        call_id=None,
        usage=None,
        provenance=[
            dict(
                source_id=source["id"],
                path=source["path"],
                location=location,
                adapter=source["adapter"],
                tracing_provider=source["adapter"],
                source_version=source["source_version"],
            )
        ],
    )
    return {**result, **values}


def diagnostic(
    source: Source, code: str, turn: str | None = None, **values: Unpack[DiagnosticDetails]
) -> Diagnostic:
    result: Diagnostic = {
        "source_id": source["id"],
        "session_id": source["session_id"],
        "turn_id": turn,
        "code": code,
    }
    result.update(cast(Diagnostic, values))
    return result


def content(payload: Mapping[str, object], *fields: str, truncated: bool = False) -> Content:
    """Keep the recorded value, including empty values and opaque evidence."""
    values = {key: payload[key] for key in fields if key in payload}
    encrypted = {
        key: value for key, value in payload.items() if "encrypted" in key and value is not None
    }
    metadata = payload.get("metadata")
    truncated = bool(
        truncated
        or payload.get("truncated")
        or isinstance(metadata, dict)
        and metadata.get("truncated")
    )
    state = "recorded" if values else "missing"
    if values and all(value in ("", [], {}, None) for value in values.values()):
        state = "empty" if all(value is not None for value in values.values()) else "missing"
    if encrypted:
        state = "partially_encrypted" if state == "recorded" else "encrypted"
    if truncated:
        state = "upstream_truncated"
    return dict(
        availability=state, values=values, encrypted=encrypted, upstream_truncated=truncated
    )


def read_source(
    source: Source,
    path: Path,
    parse: Callable[[Source, Path], tuple[list[Event], list[Diagnostic]]],
) -> tuple[list[Event], list[Diagnostic]]:
    if not path.is_file():
        events: list[Event] = []
        diagnostics = [diagnostic(source, "source_unavailable")]
    else:
        events, diagnostics = parse(source, path)
    for turn in source["turn_ids"]:
        selected = [e for e in events if e["turn_id"] == turn]
        if not selected:
            diagnostics.append(diagnostic(source, "selected_turn_absent", turn))
        if not any(e["kind"] == "model" for e in selected) and not any(
            d["code"] == "unidentified_usage" and d.get("turn_id") == turn for d in diagnostics
        ):
            diagnostics.append(diagnostic(source, "missing_usage", turn))
        if not any(e["kind"] == "agent" and e["outcome"] for e in selected):
            diagnostics.append(diagnostic(source, "unfinished_turn", turn))
    return events, diagnostics
