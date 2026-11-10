"""Native input shapes and portable telemetry/report contracts.

Native schemas are partial: missing fields retain their existing parser defaults.
Opaque provider payloads remain objects and are serialized without interpretation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal, TypedDict


class Native(TypedDict, total=False):
    id: str
    type: str
    payload: Native
    timestamp: str | float
    source: Native | str | bytes | None
    subagent: Native
    thread_spawn: Native
    parent_thread_id: str
    agent_path: str | None
    agent_nickname: str
    forked_from_id: str
    cli_version: str
    turn_id: str
    internal_chat_message_metadata_passthrough: Native
    thread_id: str
    role: str
    recipient: str
    content: list[Native]
    text: str
    message: str
    summary: object
    item: Native
    agent_thread_id: str
    call_id: str
    parent_call_id: str
    output: object
    stdout: str
    stderr: str
    aggregated_output: str
    arguments: object
    input: object
    name: str
    model: str
    effort: str
    started_at: str | float
    response_id: str
    usage: Native
    metadata: Native
    truncated: bool
    result: Native
    Ok: Native
    Err: object
    isError: bool
    status: str
    exit_code: int
    input_tokens: int
    cached_input_tokens: int
    output_tokens: int
    reasoning_output_tokens: int
    input_tokens_details: Native
    cached_tokens: int
    cache: Native
    read: int
    write: int
    reasoning: int
    implementation: str
    task: str
    purpose: str
    target: str
    task_name: str
    agent_id: str
    message_id: str
    reasoning_effort: str
    error: object
    rollout_path: str


class OpenCode(TypedDict, total=False):
    info: OpenCode
    messages: list[OpenCode]
    id: str
    version: str
    parentID: str
    sessionID: str
    type: str
    role: str
    time: dict[str, float]
    text: str
    parts: list[OpenCode]
    content: list[OpenCode]
    model: OpenCode
    modelID: str
    providerID: str
    variant: str
    outcome: Literal["succeeded", "failed", "interrupted"]
    error: object
    tokens: Native
    finish: str
    reason: str
    state: OpenCode
    callID: str
    name: str
    tool: str
    status: str
    metadata: OpenCode
    system: object
    input: object
    output: object


class Source(TypedDict, total=False):
    id: str
    path: str
    adapter: str
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
    source_id: str


class Provenance(TypedDict):
    source_id: str
    path: str
    location: int | str
    adapter: str
    source_version: str


class Content(TypedDict):
    availability: str
    values: dict[str, object]
    encrypted: dict[str, object]
    upstream_truncated: bool


Usage = dict[str, int | None]


class EventDetails(Settings, total=False):
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
    call_event_id: str | None
    tool_name: str | None
    turn_event_id: str | None


class Event(Context, EventDetails, total=False):
    kind: str
    native_event_id: str
    provenance: list[Provenance]


class Document(TypedDict):
    path: Path
    meta: Native
    session_id: str
    records: list[tuple[str | None, Native | None, bytes]]
    turns: list[str]


class Dispatch(TypedDict, total=False):
    kind: str
    arguments: Native
    call_id: str | None
    timestamp: float | None
    turn: str | None
    result: Native


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


class TimingMetadata(TypedDict):
    timing_omissions: list[dict[str, str]]


class Timeline(TypedDict):
    metadata: TimingMetadata
    traceEvents: list[dict[str, object]]
    displayTimeUnit: str


class EventReport(TypedDict):
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
