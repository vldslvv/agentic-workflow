"""Private Codex rollout and index shapes."""

from __future__ import annotations

from pathlib import Path
from typing import TypedDict


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
