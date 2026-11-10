"""Private OpenCode export shapes."""

from __future__ import annotations

from typing import Literal, TypedDict


class Tokens(TypedDict, total=False):
    input: int
    output: int
    reasoning: int
    cache: dict[str, int]


class OpenCode(TypedDict, total=False):
    source: str
    childID: str
    shellID: str
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
    tokens: Tokens
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
