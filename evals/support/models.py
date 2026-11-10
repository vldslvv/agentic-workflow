"""Settings and evidence contracts shared by evaluation commands."""

from dataclasses import dataclass
from typing import Literal, NotRequired, TypedDict

Status = Literal[
    "PASS",
    "FAIL",
    "UNCLEAR",
    "FIXED",
    "NOT_RUN",
    "RUNNER_ERROR",
    "JUDGE_ERROR",
    "REPAIR_ERROR",
    "TIMEOUT",
    "INTERRUPTED",
]


@dataclass(frozen=True)
class ReviewSettings:
    timeout: float = 1800
    model: str = "gpt-6-astra"
    reasoning: str = "medium"
    bundle: str | None = None
    repair: bool = False


@dataclass(frozen=True)
class RoleSettings:
    profile: str
    model: str
    reasoning: str


class State(TypedDict):
    exists: bool
    value: object


class Execution(TypedDict):
    status: Status
    command: NotRequired[list[str]]
    returncode: NotRequired[int | None]
    signal: NotRequired[int]
    error: NotRequired[str]
    elapsed_seconds: NotRequired[float]
    expected_stdout: NotRequired[str]
    expected_exit: NotRequired[int | Literal["nonzero"]]
    stdout: NotRequired[str]
    stderr: NotRequired[str]
    state_before: NotRequired[State]
    state_after: NotRequired[State]
    checks: NotRequired[dict[str, bool]]


class Check(TypedDict):
    contract: str
    status: Literal["PASS", "FAIL", "UNCLEAR"]
    evidence: str


class Judgment(TypedDict):
    scope: str
    excluded_inputs: list[str]
    checks: list[Check]


class Review(TypedDict):
    status: Status
    scope: NotRequired[str]
    excluded_inputs: NotRequired[list[str]]
    checks: NotRequired[list[Check]]


class Inputs(TypedDict, total=False):
    bundles: list[str]
    excluded_inputs: list[str]
    checks: list[Check]


class RepairResponse(TypedDict):
    status: Literal["FIXED", "UNCLEAR"]
    summary: str


class Repair(TypedDict):
    status: Status
    attempted: bool
    execution: NotRequired[Execution]
    signal: NotRequired[int]
    response: NotRequired[RepairResponse]
    checks: NotRequired[Execution]
    source_contract_unchanged: NotRequired[bool]
    reason: NotRequired[str]
    note: NotRequired[str]
    error: NotRequired[str]


class DocumentResult(TypedDict):
    status: Status
    review: Review
    execution: Execution
    repair: NotRequired[Repair]
    signal: NotRequired[int]
    error: NotRequired[str]
    note: NotRequired[str]
    partial_edits_may_remain: NotRequired[bool]
    bundles: NotRequired[list[str]]


class ArtifactGrade(TypedDict):
    status: Status
    implementations: NotRequired[list[str]]
    missing: NotRequired[list[str]]
    native_files: NotRequired[list[str]]
    error: NotRequired[str]


class ScenarioGrade(TypedDict):
    status: Status
    commands: list[Execution]
    signal: NotRequired[int]
    error: NotRequired[str]
    name: NotRequired[str]
    contract: NotRequired[str]


class CLIGrade(TypedDict):
    status: Status
    scenarios: NotRequired[list[ScenarioGrade]]
    signal: NotRequired[int]
    error: NotRequired[str]


class TrialResult(TypedDict):
    status: Status
    generation: Execution
    cli: CLIGrade
    artifacts: ArtifactGrade
    records_created: NotRequired[list[str]]
    signal: NotRequired[int]
    error: NotRequired[str]
    elapsed_seconds: NotRequired[float]
    git_status: NotRequired[str]
    unexpected_changes: NotRequired[str]


class WorktreeResult(TypedDict):
    status: Status
    exit_code: int
    source_commit: str
    source_root: str
    worktree: str
    worktree_removed: bool
    error: NotRequired[str]
    cleanup_error: NotRequired[str]
