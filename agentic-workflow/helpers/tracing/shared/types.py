"""Normalized evidence and report contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict


class Source(TypedDict, total=False):
    id: str
    path: str
    adapter: str
    tracing_provider: str
    session_id: str
    turn_ids: list[str]
    source_version: str
    native_agent_path: str | None


class Assignment(TypedDict, total=False):
    implementation: str
    task: str
    role: str
    purpose: str
    source: str
    evidence: list[str]


class Settings(TypedDict, total=False):
    model: str | None
    reasoning_effort: str | None
    variant: str | None
    provider: str | None


class Context(TypedDict, total=False):
    implementation_id: str
    adapter: str
    tracing_provider: str
    agent_id: str
    task_id: str | None
    role: str | None
    agent_run_id: str
    assignment_id: str
    session_id: str | None
    turn_id: str | None


class DiagnosticDetails(TypedDict, total=False):
    location: int | str
    native_version: str | None
    native_event_id: str


class Diagnostic(Context, DiagnosticDetails, total=False):
    code: str
    coverage_effect: Literal["informational", "incomplete", "missing_measurement"]
    source_id: str


class Provenance(TypedDict):
    source_id: str
    path: str
    location: int | str
    adapter: str
    tracing_provider: str
    source_version: str


class Content(TypedDict):
    availability: str
    values: dict[str, object]
    encrypted: dict[str, object]
    upstream_truncated: bool


Usage = dict[str, int | None]


class EventDetails(Settings, total=False):
    is_wrapper: bool
    event_id: str
    start: float | None
    end: float | None
    timestamp: float | None
    outcome: str | None
    parent_session_id: str | None
    forked_from_id: str | None
    continued_from_id: str | None
    parent_call_id: str | None
    call_id: str | None
    usage: Usage | None
    native_agent_name: str | None
    native_agent_path: str | None
    spawn_timestamp: float | None
    content: Content
    context_scope: str
    name: str | None
    message_role: str | None
    message_id: str
    parent_message_id: str | None
    native_record: object
    finish_reason: str | None
    requested: Settings
    agent_name: str
    purpose: str | None
    assignment_source: str | None
    assignment_evidence: list[str]
    parent_event_id: str | None
    outputs: list[Event]
    instructions: list[Event]
    turn_ids: list[str]
    selected_turns: list[Event]
    call_event_id: str | None
    tool_name: str | None
    turn_event_id: str | None


class Event(Context, EventDetails, total=False):
    kind: str
    native_event_id: str
    provenance: list[Provenance]


class Metric(TypedDict):
    total: int | None
    known_subtotal: int | None
    measured_records: int
    missing_records: int


class Summary(TypedDict):
    tokens: dict[str, Metric]
    observed_model_measurements: int
    observed_tool_calls: int
    wrapper_calls: int
    observed_nested_operations: int
    missing_parent_call_relationships: int
    outcomes: dict[str, int]
    observed_operation_seconds: float | None
    timed_operations: int
    untimed_operations: int
    coverage: dict[str, int]


class Group(TypedDict):
    key: dict[str, str | None]
    summary: Summary


class Omission(TypedDict):
    event_ids: list[str]
    diagnostics_without_attribution: int


class AgentNode(TypedDict):
    agent_id: str
    session_id: str | None
    agent_run_ids: list[str]
    turns: list[str]


class Edge(TypedDict):
    parent: str
    child: str
    relationship: str
    parent_in_selection: bool


class SpawnTree(TypedDict):
    nodes: list[AgentNode]
    edges: list[Edge]


class AssignmentRow(TypedDict, total=False):
    agent_id: str
    agent_run_id: str
    agent_name: str
    native_agent_name: str | None
    native_agent_path: str | None
    task_id: str | None
    role: str | None
    purpose: str | None
    assignment_id: str
    assignment_source: str | None
    assignment_evidence: list[str]
    turns: list[str]
    outcomes: list[str]
    observed_settings: list[Settings]
    requested_settings: list[Settings]


class Report(TypedDict, total=False):
    tracing_provider: str
    version: int
    summary: Summary
    groups: dict[str, list[Group]]
    attribution_omissions: dict[str, Omission]
    spawn_tree: SpawnTree
    diagnostics: list[Diagnostic]
    assignments: list[AssignmentRow]
    native_sources: list[Source]
    limitations: list[str]
    implementation_id: str


class TimingMetadata(TypedDict, total=False):
    tracing_provider: str
    timing_omissions: list[dict[str, str]]


class Timeline(TypedDict):
    metadata: TimingMetadata
    traceEvents: list[dict[str, object]]
    displayTimeUnit: str


class EventReport(TypedDict):
    tracing_provider: str
    timing_omissions: list[dict[str, str]]
    version: int
    implementation_id: str
    events: list[Event]


class NodeAccumulator(TypedDict):
    agent_id: str
    session_id: str | None
    agent_run_ids: set[str]
    turns: set[str | None]


class AssignmentAccumulator(TypedDict):
    base: AssignmentRow
    turns: set[str | None]
    outcomes: set[str]
    observed_settings: set[tuple[str | None, str | None, str | None]]
    requested_settings: set[tuple[str | None, str | None]]


class TimelineEvent(TypedDict, total=False):
    name: str
    cat: str
    pid: int
    tid: int
    args: dict[str, object]


EvidenceKey = tuple[str, str | None, str | None]


@dataclass
class CollectedEvidence:
    events: list[Event]
    sources: list[Source]
    assignments: dict[EvidenceKey, Assignment]
    requested: dict[EvidenceKey, Settings]
    diagnostics: list[Diagnostic]
