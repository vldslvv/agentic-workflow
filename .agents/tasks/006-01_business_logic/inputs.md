# Execution input inventory — todolist

Status: authorized; executable checks and normative inputs frozen before implementation.
Baseline: `07fd1484a33826b53c9e669b7490175bce1bd11a`. Mode: initial.

- Bundle: `specs/todolist`; exact source hashes are in acceptance and approval records.
- DAG: `01_business_logic` → `02_cli`. Two unique listed files exist; no cycles or additional declared prerequisites.
- Task records: `.agents/tasks/006-01_business_logic/` and `.agents/tasks/007-02_cli/`, each containing plan.md, acceptance.md, approval.json.
- Supplied constraints: simple app, uv + pyproject.toml, output `apps/todolist`.
- Storage: `apps/todolist/tasks.json`, chosen under user delegation.
- Environment: Python 3.14.10, uv 0.13.6. Internal standard-library choices delegated by the implementation request.
- Owned candidate root: `apps/todolist/`. Protected: `specs/todolist/`, `spec-source-suite/`, task records, frozen checks, historical evidence.
- Evidence root: `.suite/runs/006-01_business_logic/`; per-task implementer logs and reviewer-owned review directories beneath it.
- Verification mapping: B1–B6 business, C1–C6 CLI, A1 assembled. No user-only manual gate.
- Frozen inventory: `.suite/runs/006-01_business_logic/frozen-inventory.json`, created before implementer dispatch.
- Approval references: both approval.json files bind the request and delegation; no separate approval prompt.
- Retained inputs: none initially; CLI requires accepted business candidate/evidence.

## Frozen production API and commands

The public business API is `from todolist.core import TaskStore, TodoError`, with `TaskStore(path)` exposing `create(title) -> Task`, `list() -> list[Task]`, `delete(id)`, and `complete(id)`. Task values expose `id`, `title`, `completed`. Domain/storage failures raise `TodoError` with useful text. API naming is an implementation choice fixed before the check freeze; the business storage-path parameter serves normal reusable application use.

Run from repository root:
- `python3 .suite/runs/006-01_business_logic/checks/business.py --app apps/todolist --evidence <owned-output>`
- `python3 .suite/runs/006-01_business_logic/checks/cli.py --app apps/todolist --evidence <owned-output>`
- Assembled only: append `--only A1` to the CLI check command.
- Before/after each phase: `python3 .suite/runs/006-01_business_logic/checks/integrity.py --app apps/todolist --output <owned-output.json>`.

Business fixtures exercise supplied paths; CLI fixtures install disposable copies via `uv sync --locked --offline` then execute fresh processes via `uv run --offline --no-sync --project <copy> todo`. Build dependencies must first be cached by the implementer's real project installation. No held-out checks. Required reviewer B6 inspection assesses project simplicity. No user-only manual gates.
