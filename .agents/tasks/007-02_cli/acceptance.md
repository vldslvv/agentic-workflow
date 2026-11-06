# Acceptance record — 02_cli

Status: Authorized derived handoff under the user’s implementation request and instruction to proceed without approval prompts.
Baseline: `07fd1484a33826b53c9e669b7490175bce1bd11a`.
Source: `specs/todolist/tasks/02_cli.md`, shared project constraints, task order, and verification intent.
Prerequisites: 01_business_logic, accepted at its exact reviewed revision; derived from task_order.md.
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

Command contract: `uv run todo add "TITLE"`, `delete ID`, `complete ID`, `list`, `help`, and `--help`, run from `apps/todolist`. List displays IDs, titles, and `[ ]` / `[x]` markers; empty list prints `No tasks.`. Exact alignment and success wording are delegated. Success/help exit zero; missing/unknown commands, invalid IDs, blank titles, unknown task IDs, and storage errors exit nonzero with concise stderr and no traceback. Help does not access task data.

| ID | Source clause | Required observable check |
|---|---|---|
| CLI-01 / C1 | add tasks | Real CLI adds two titles; fresh list process shows distinct IDs, titles, and incomplete state. |
| CLI-02 / C2 | delete tasks | Delete one ID; fresh process shows only the other. Unknown ID fails without changing storage. |
| CLI-03 / C3 | complete tasks | Complete a task; fresh process displays completed state. Repeating succeeds. |
| CLI-04 / C4 | list tasks | Missing storage prints No tasks. without creating a file; populated list preserves file bytes. |
| CLI-05 / C5 | help | help and --help document all commands, exit zero, and preserve even malformed storage. |
| CLI-06 / C6 | delegated error contract | Missing/unknown command, invalid ID, blank title, malformed storage, and storage path occupied by a directory fail as specified without overwriting data. |
| CLI-07 / A1 | verification.md | Separate processes add two tasks, complete one, delete the other, and list. Final JSON agrees with output. Invoke from another working directory and confirm the same app-root data is used. |

Run CLI checks against temporary copies of the actual app, through its uv console entry point. A1 also runs separately against the assembled candidate after both subsystem gates pass.

## Verification and approval

Each check starts with isolated temporary fixtures, executes the real public API or CLI, asserts all listed outcomes, records inputs/results/exit codes, and cleans up fixtures. All mandatory assertions must pass. Freeze executable checks, source documents, these records, adapters, and fixtures before implementation. Checks live under `.suite/runs/006-01_business_logic/checks/`; exact commands and public API are recorded in the frozen inventory. Shared scenario authority is `specs/todolist/verification.md`. No user-only manual criterion applies.

Mandatory gates: applicable checks, fresh independent reviewer execution and coverage assessment, actual dependency integration, protected-input and candidate integrity, and assembled A1 after both tasks pass. Isolation is procedural. No initial assets/data/services are retained; CLI retains the accepted business candidate.

`approval.json` binds exact plan/acceptance/source digests to the implementation request and the user’s instruction: “Don't ask me for approval -- specs are enough. Adjust your instructions to not do that.” These documents are agent-authored derived handoffs, not separately reviewed user text.
