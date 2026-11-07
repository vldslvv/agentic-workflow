# Plan — 02_cli

## Request and scope

Implement the user-facing Rust TODO CLI authorized by the direct implementation request, under `apps/todolist_rust`. Mode: **full**, following the implementer's assessment: a new public process interface combines argument validation, persistence, error/output handling and end-to-end verification. Ordinary command spelling and presentation choices below are authorized derived decisions. No routine reapproval is required.

Add `add`, `delete`, `complete`, `list`, and `help`. Preserve the accepted business layer and its JSON persistence. Task 03's Docker/PostgreSQL replacement and database-alive check on every invocation are later work; do not introduce that dependency in task 02.

## Acceptance

Separate authoritative derived acceptance: [acceptance.md](acceptance.md), CLI-01–CLI-08. Sources remain authoritative.

## Sources and dependencies

- [Project](../../../../specs/todolist_rust/project.md): simple design, Rust, target path.
- [Task](../../../../specs/todolist_rust/tasks/02_cli.md): user-facing commands.
- [Order](../../../../specs/todolist_rust/task_order.md): accepted 01_business_logic precedes 02_cli; 03_database follows.
- [Verification](../../../../specs/todolist_rust/verification.md): run end-to-end scenarios including add/remove/delete; `remove` is covered by the required `delete` operation, not an additional command alias.
- Engineering source: `/home/vv/ccode/generate-prototype/guidelines.md`: functional core, explicit side effects, cohesive small interfaces, public-interface checks with real disposable persistence, simple implementation.
- Accepted prerequisite: `.suite/004_todolist_rust/runs/01_business_logic/implementer/result.md` and `reviewer/result.md` both PASS. Public contract: [README](../../../../apps/todolist_rust/README.md), `src/lib.rs`. `TodoStore::project()` uses compile-time Cargo-project-root `tasks.json`; API reloads each operation, persists before mutation success, preserves descriptions, IDs/order and idempotent completion, returns not-found/storage errors.
- No project memory consulted or handed off. No prior app implementation inspected.

## Approach and public interface

Add a Cargo binary entry point using the existing library. Parse arguments into one command, run at most one requested operation, render success only after the library succeeds, and exit. Keep argument parsing/presentation separate from storage effects without building a framework. Standard-library parsing is sufficient; a dependency is optional only with a concrete simplicity benefit.

Invocation: `cargo run -- <command>` or the built binary. Commands:

- `add <description>` accepts exactly one UTF-8 argument, including a quoted empty description or quoted spaces, preserving its supplied value.
- `delete <id>` and `complete <id>` accept exactly one nonempty ASCII decimal digit string representable as `u64`. Zero is syntactically valid and follows the library's not-found behavior; negatives, signs, non-digits and overflow are usage errors.
- `list` and `help` accept no operands. No arguments, `-h`, and `--help` also display help successfully. Unknown commands/options and missing/extra operands fail as usage errors. A quoted description beginning with `-` remains a description.

Help documents syntax for every command, quoting descriptions, storage location, and completion markers. Help returns 0 without mutating storage. Every successful data command returns 0, prints useful stdout and leaves stderr empty. Add/delete/complete confirmations identify the affected ID; list displays each ID, description and distinguishable completed/incomplete state in creation order, or an explicit empty-state message. Exact prose/spacing is implementation-owned, documented, and checked semantically.

Usage failures return 2, print useful stderr including a help hint or usage, leave stdout empty and never mutate storage. Business/storage failures return 1, print explanatory stderr (including the affected ID for not-found), leave stdout empty, and preserve prior data. Unsupported non-UTF-8 command input may be rejected as a usage failure without panic; no lossy mutation is acceptable. Do not add path options or environment hooks solely for tests.

## Checks and handoff

Run from `apps/todolist_rust`: `cargo fmt --check`, `cargo check --offline`, `cargo test --offline`, `cargo clippy --offline --all-targets -- -D warnings` (network-enabled Cargo equivalent only if offline cache is unavailable). Retain existing public business tests. Add proportionate public process checks for argument/output/error contracts and a real persistent process lifecycle; test code may be developed during implementation. Follow the test-audit skill if authoring tests.

For the manifest-root path, create a disposable project copy excluding `target` and `tasks.json`, build there with an isolated temporary Cargo target, invoke the copied binary from outside its project directory, and inspect its real JSON. This avoids touching any app data and needs no production testing seams. A single process lifecycle can own empty → add A/B → list → complete A twice → list → delete B → list → delete A → empty → add C, observing persisted identity/order/state across launches. Include empty and spaced descriptions. Use deterministic real filesystem failures (for example a directory at the expected file path) and corrupt JSON; capture stdout/stderr/status and unchanged data for failures. Help and usage checks can share the fixture, but tests must restore/clean their owned data.

Save command evidence and a requirement-linked result under `.suite/004_todolist_rust/runs/02_cli/implementer/` (or its assigned run directory). Required fresh independent review follows a stable candidate; review receives source, acceptance and applicable engineering path, excluding this plan and memory. Supervisor later performs whole-app validation after task 03; this task's process scenario is an applicable partial assembled-app check, not final app acceptance.

Planner result: `.suite/004_todolist_rust/runs/02_cli/planner/result.md`. Retained planner handle: `/root/cli_plan`. Retained implementer: `/root/cli`. No unresolved requirements or required unavailable capabilities identified.
