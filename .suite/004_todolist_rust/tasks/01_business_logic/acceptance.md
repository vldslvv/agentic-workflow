# Task 01_business_logic acceptance

## Request, sources and scope

The direct implementation request authorizes a Rust TODO business layer. Normative inputs are [project.md](../../../../specs/todolist_rust/project.md), [01_business_logic.md](../../../../specs/todolist_rust/tasks/01_business_logic.md), and [verification.md](../../../../specs/todolist_rust/verification.md). The selected task covers JSON-backed business behavior; later CLI and database tasks are outside this acceptance.

Applicable engineering guidance is [guidelines.md](../../../../guidelines.md), resolved `/home/vv/ccode/generate-prototype/guidelines.md`: prefer explicit state and functional transformations; localize effects behind explicit boundaries; use cohesive modules with small interfaces; test observable public behavior with real isolated dependencies; explain material departures from these defaults; avoid unnecessary validation, locks, checksums, manifests and backwards-compatible functionality.

## Prerequisites

This is the first ordered task, with no preceding task or separately declared prerequisite contract. Full workflow applies, including fresh independent review before task acceptance.

## Target and paths

Rust source and project files: `/home/vv/ccode/generate-prototype/apps/todolist_rust`. Normal JSON persistence: `/home/vv/ccode/generate-prototype/apps/todolist_rust/tasks.json`. Execution evidence: `/home/vv/ccode/generate-prototype/.suite/004_todolist_rust/runs/01_business_logic/<agent-run-id>/`. Use disposable storage for checks; do not overwrite existing developer data.

| Requirement ID | Source clause and observable outcome | Check method and pass rule |
|---|---|---|
| BL-01 | `project.md` lines 2–4: keep things simple, use Rust, implement at `apps/todolist_rust`; task line 1: a business layer. | Inspect Cargo/source layout and public API at target path; `cargo check` succeeds. Operations are callable as business behavior without requiring a CLI, database or external service. Inspect engineering conformance and explain material departures. |
| BL-02 | Task line 4, create tasks. Ordinary clarification: tasks have distinct usable IDs, descriptions and completion state; newly created tasks are incomplete. | Through public interfaces, create at least two descriptions and observe both values, distinct identifiers and incomplete state. After deleting a task and reloading, another creation cannot collide with a surviving task's ID. |
| BL-03 | Task line 5, list tasks. | List empty initial storage and receive an empty collection. After creating two tasks, list returns each exactly once with the correct description, ID and completion state; no unrelated entries appear. Ordering need only match the documented public contract. |
| BL-04 | Task line 7, complete tasks. | Complete one of two tasks by ID; list shows it complete with original ID/description and the other remains unchanged. Repeat completion follows the documented public contract without corrupting data. An unknown ID produces an explicit non-success/non-mutating result and leaves existing tasks unchanged. |
| BL-05 | Task line 6, delete tasks. | Delete one of two tasks by ID; list contains only its unchanged survivor. Delete the survivor and list is empty. An unknown ID produces an explicit non-success/non-mutating result and leaves existing tasks unchanged. |
| BL-06 | Task line 9: tasks preserved in `tasks.json` at project root. | Drive creates, completion and deletion against real isolated filesystem storage, constructing fresh instances between mutations and observations. Reload yields the full previously saved state, including IDs and completion; deleting all tasks reloads empty. Verify documented normal/default operation selects app-root `tasks.json` in a disposable fixture or staged project. A missing file permits a new empty collection. |
| BL-07 | Task line 9 preservation; engineering effects and observable testing defaults. Ordinary error clarification: unreadable/corrupt storage and unsuccessful saves cannot be reported as successful persistence or silently discard prior data. | Load malformed JSON: receive a clear error and original bytes remain unchanged. Exercise a deterministic real filesystem read/write failure (e.g. a path whose parent is a regular file, avoiding permission assumptions); operation returns an error without panic or success. Reopen any prior valid stored collection after the failed operation and verify its data is retained when that file was not itself externally changed. No crash/power-loss guarantee is required. |
| BL-08 | Shared `verification.md` line 1: run end-to-end adding/removing/deleting scenarios. | Run the full public-interface lifecycle: empty → add A/B → list both incomplete → complete A → fresh reload A complete/B incomplete → delete B → fresh reload only A → delete A → fresh reload empty. Capture commands/results. End-to-end for this task means the business API plus real JSON persistence; CLI/database checks belong to later tasks. |

## Shared, regression and final checks

Run `cargo fmt --check`, `cargo check`, and `cargo test` in the target project; all must succeed. Meaningful public-interface checks cover the table and use real disposable JSON/filesystem storage, with no required network or database. Fresh independent task review must find no unresolved actionable findings. The shared scenario is required for this task and later assembled-app validation with the then-applicable storage contract; final whole-app validation follows all ordered tasks.

## Limits and decisions

No unavailable required capability is currently known. Storage failures are checked deterministically; process crashes, power loss, concurrent writers and migration compatibility are outside stated scope. API names, ID representation, JSON layout and repeat-completion response are ordinary implementation choices, documented with their observable contract. These choices may not weaken task operations or persistence. Coverage is finite and does not establish universal filesystem reliability.
