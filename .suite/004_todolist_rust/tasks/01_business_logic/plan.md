# Task 01_business_logic plan

## Request and scope

Implement the TODO business layer requested by [task 01](../../../../specs/todolist_rust/tasks/01_business_logic.md), using Rust at `apps/todolist_rust`, under [project rules](../../../../specs/todolist_rust/project.md). The direct implementation request authorizes this derived plan and acceptance without routine approval.

Mode: **full**. The implementer's assessment identifies a new Rust domain API, JSON persistence, filesystem errors, data-loss risks and reload verification. Fresh independent task review is required after implementation. This task provides create, list, complete and delete with project-root `tasks.json`; subsequent CLI and database tasks remain outside its scope. No earlier application, historical implementation or project memory was consulted.

## Acceptance

The separate [acceptance](acceptance.md) maps BL-01 through BL-08 to observable checks. Required expectations are fixed there; implementation may develop suitable check code and command names.

## Sources and dependencies

- [Project](../../../../specs/todolist_rust/project.md): simplicity, Rust, target path.
- [Task](../../../../specs/todolist_rust/tasks/01_business_logic.md): business operations and JSON preservation.
- [Shared verification](../../../../specs/todolist_rust/verification.md): end-to-end task lifecycle scenarios.
- [Engineering guidelines](../../../../guidelines.md), resolved `/home/vv/ccode/generate-prototype/guidelines.md`: explicit state, functional core, explicit side-effect boundaries, cohesive interfaces, observable public-interface tests and disposable real dependencies. These are design defaults; explain material departures.
- Task 01 is the first ordered task; no accepted prerequisite task contract is required. No project memory exists, as established by supervisor handoff.

## Approach

Create a minimal Cargo project rooted at `/home/vv/ccode/generate-prototype/apps/todolist_rust`. Expose a small library business API suitable for the later CLI: create a task with a description, list tasks, mark an identified task complete, and delete an identified task. A task needs only an unambiguous identifier, description and completion state. New tasks start incomplete; completion preserves the description and identifier; deletion removes only the addressed task. Choose a straightforward identifier representation and deterministic list ordering, document those public contracts, and avoid adding product policy such as title validation, timestamps or priorities.

Keep domain transitions explicit and isolate filesystem/JSON work behind a narrow persistence boundary. A path-aware persistence boundary is appropriate for isolated real-file tests; normal application storage resolves to `tasks.json` at the project root. Keep the interface small enough that the later ordered persistence replacement can preserve domain operations without prematurely implementing a generic storage framework.

Treat an absent storage file as an empty initial collection. Save successful mutations before reporting success; reload from disk through a fresh business-layer instance to demonstrate actual persistence. Preserve distinct identities across deletion and reload. Handle an unknown identifier explicitly without changing existing data. Choose and document completion of an already complete task as an ordinary public contract; either an unchanged success or a clear non-mutating result is acceptable. Surface malformed stored JSON and filesystem failures as clear errors, preserving existing readable data rather than silently reinitializing it. Use a simple safe write approach suitable for ordinary local-file failures; crash/power-loss and multi-process concurrency guarantees are not requested.

No CLI, interactive prompt, database, Docker service, backwards-compatibility layer or speculative abstraction is required in this task. Minimal usage documentation may explain how to exercise the library and run checks.

## Checks and handoff

From `apps/todolist_rust`, run `cargo fmt --check`, `cargo check`, and `cargo test`; use normal Rust linting if configured or practical. Inspect the final diff against source scope and engineering defaults. Tests must drive public business/persistence interfaces and real isolated temporary storage, without test-only production seams or assertions tied to internal representation. Cover the acceptance table using focused lifecycle and failure checks; do not duplicate assertions merely to increase test counts.

The shared lifecycle scenario is: start in empty storage; add two distinct tasks; list both incomplete; complete one; freshly reload and observe only that task complete; delete the other; freshly reload and observe only the completed survivor. Delete the survivor and reload an empty collection. Separately create after deletion/reload and verify no surviving identity collision. Failure checks cover missing IDs, repeat completion contract, malformed JSON and a deterministic filesystem failure. Verify the default storage location is the app project root using a disposable fixture or isolated staged copy, preserving any developer data.

Save execution evidence and the implementer result under `/home/vv/ccode/generate-prototype/.suite/004_todolist_rust/runs/01_business_logic/<agent-run-id>/`. Record actual commands, outcomes, public API invocation, evidence paths and any unavailable checks. Fresh reviewer receives authoritative sources, acceptance, applicable guidelines, candidate and evidence, excluding this plan and memory. Overall final validation occurs after all ordered tasks, where the later storage requirement supersedes this intermediate JSON implementation.

Planner handle: `/root/business_plan`. Return planning defects to this retained worker. Planning result: [planner/result.md](../../runs/01_business_logic/planner/result.md).
