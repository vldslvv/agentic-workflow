# Acceptance record — 01_business_logic

Status: Authorized derived handoff under the user’s implementation request and instruction to proceed without approval prompts.
Baseline: `07fd1484a33826b53c9e669b7490175bce1bd11a`.
Source: `specs/todolist/tasks/01_business_logic.md`, shared project constraints, task order, and verification intent.
Prerequisites: None; first in task_order.md.
Scope: all behavior in the selected source task; historical task records supply no behavior.

## Source identities

- `specs/todolist/project.md`: `583d6507f3e0d4eb48ba9010ec0ea25c5f4450038a559d901c1ad1a407b9d487`
- `specs/todolist/task_order.md`: `f89c23d15e659a2657fe7c7edb4b283e592f53adb26e1477c3c6f48340d19912`
- `specs/todolist/tasks/01_business_logic.md`: `1262a1da26f58cb390a87ac067f8775dc33c366e1da83ad3d2928ef96ad2556f`
- `specs/todolist/tasks/02_cli.md`: `63c8988e27105cc3155a06a48fe087ec3ce42f49d7ce137137656253a02e85fd`
- `specs/todolist/verification.md`: `01b5eeb3ceace6c7e6fb7565e72082f40dbc5296fcbdfbd6a57730b65ca014f6`

## Recorded implementation defaults

Implementation defaults under the user’s delegation:
- Project root means `apps/todolist`; the CLI always uses `apps/todolist/tasks.json`, independent of caller working directory.
- JSON is an array of tasks with positive integer `id`, nonempty trimmed `title`, and Boolean `completed` (initially false). IDs are unique among current tasks; deletion need not reserve IDs. Listing preserves creation order.
- Missing storage means no tasks. Create storage on the first successful mutation. Listing/help and failed operations preserve existing file contents.
- Unknown IDs, blank titles, malformed task data, and inaccessible storage produce clear errors without overwriting data. Repeated completion succeeds and leaves the task complete.
- No web interface, deployment, accounts, due dates, migrations, or concurrent-writer guarantees. Use Python standard library; internal implementation choices are delegated.

## Requirement mapping

| ID | Source clause | Required observable check |
|---|---|---|
| BL-01 / B1 | create tasks | Create two tasks including Unicode; distinct IDs, trimmed titles, initially incomplete. Blank title fails without changing storage. |
| BL-02 / B2 | list tasks | Missing storage lists empty; populated list preserves order and exposes each task's ID/title/state; reads preserve bytes. |
| BL-03 / B3 | delete tasks | Delete one task; only it disappears, including after reopening. Unknown ID fails without changing storage. |
| BL-04 / B4 | complete tasks | Complete one task and reopen; only its state changed. Repeated completion succeeds. Unknown ID fails without changing storage. |
| BL-05 / B5 | persisted tasks.json | JSON has the approved shape and survives reopening. Malformed JSON/records and inaccessible paths fail without overwriting data. |
| BL-06 / B6 | project.md | uv prepares the project using pyproject.toml; reviewer confirms simple Python app within apps/todolist. |

B1–B5 exercise the public business API with disposable storage; choose and document its production API before freezing checks. A storage-path parameter supports reusable business logic. B6 combines uv execution and independent reviewer inspection.

## Verification and approval

Each check starts with isolated temporary fixtures, executes the real public API or CLI, asserts all listed outcomes, records inputs/results/exit codes, and cleans up fixtures. All mandatory assertions must pass. Freeze executable checks, source documents, these records, adapters, and fixtures before implementation. Checks live under `.suite/runs/006-01_business_logic/checks/`; exact commands and public API are recorded in the frozen inventory. Shared scenario authority is `specs/todolist/verification.md`. No user-only manual criterion applies.

Mandatory gates: applicable checks, fresh independent reviewer execution and coverage assessment, actual dependency integration, protected-input and candidate integrity, and assembled A1 after both tasks pass. Isolation is procedural. No initial assets/data/services are retained; CLI retains the accepted business candidate.

`approval.json` binds exact plan/acceptance/source digests to the implementation request and the user’s instruction: “Don't ask me for approval -- specs are enough. Adjust your instructions to not do that.” These documents are agent-authored derived handoffs, not separately reviewed user text.
