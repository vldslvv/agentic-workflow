# Independent assembled-app validation

**PASS.** Required checks and final real-dependency scenarios passed. No actionable findings, repair specification, outstanding required check or infrastructure blocker.

## Scope and independence

Implementation `004_todolist_rust`; fixed candidate `/home/vv/ccode/generate-prototype/apps/todolist_rust` is untracked in enclosing Git, with no revision. No candidate source, tests, specifications or acceptance records changed during validation. Build artifacts were produced by required checks. This fresh Validator inspected the full app source, tests, example, Cargo configuration, compose and README, original `specs/todolist_rust/{project.md,task_order.md,verification.md,tasks/01_business_logic.md,tasks/02_cli.md,tasks/03_database.md}`, and all three `.suite/004_todolist_rust/tasks/<task-id>/acceptance.md` records. Task03's explicit PostgreSQL/schema/preflight replacements govern former JSON/u64/bool/physical-delete/help-bypass behavior; unaffected CLI and business contracts remain applicable.

Read shared suite rules, Validator routine, routing configuration and `/home/vv/ccode/generate-prototype/guidelines.md`. No plans, memory, conversations, other apps or prior implementation records consulted. Current task03 implementer and fresh reviewer-r2 result summaries were allowed supporting inputs; none substituted for independent execution.

Model route: demanding Validator, escalation profile, requested `gpt-6-astra` / medium for assembled backend and data preservation correctness. Observed host model/reasoning unavailable; no known fallback. All scheduled tasks were handed off accepted FULL with fresh reviews; this validation independently establishes final assembled behavior.

## Executed checks

All command exits below were 0. Commands ran from `/home/vv/ccode/generate-prototype/apps/todolist_rust` unless stated otherwise.

| Requirements | Method and observed outcome | Evidence |
|---|---|---|
| DB-01; retained project/CLI build requirements | `cargo fmt --check`, `cargo check --offline`, `cargo clippy --offline --all-targets -- -D warnings` all passed. | [static.log](static.log) |
| DB-01–10; retained business/CLI contracts; shared verification | Independently ran `python3 tests/cli_e2e.py`. Actual unique Docker PostgreSQL fixture, fixture-backed `cargo test --offline` (one public API integration test, no failures/ignored tests), lifecycle example and separate CLI processes outside project root all passed. | [e2e.log](e2e.log) |
| DB-02/03/06/10/11; usable consumer startup | Independently executed README isolated configuration and exact `docker compose up -d --wait db`, `docker compose ps`, `cargo run -- help/add/list/complete/delete`, `docker compose down`, then up again. Direct SQL matched the Deleted row byte-for-byte after down/up; next create returned ID 2. | [manual.log](manual.log), reproducible [manual.py](manual.py) |

The process suite's independently queried PostgreSQL catalog confirms five required columns, integer identity primary key, non-null text and timezone-aware datetime columns, and native enum with exactly Completed/New/Deleted. Lifecycle checks independently observe IDs 1/2 then 3 after deletions, exact descriptions including empty/whitespace/quotes/UTF-8/leading hyphen, New creation and equal timestamps within the measured window, completion and deletion with later update and preserved immutable fields, idempotent repeated completion, hidden Deleted rows, and ascending list order. Missing/deleted IDs fail without mutating snapshots.

Healthy help aliases, argument arity, nondecimal/signed/Unicode/overflow IDs and POSIX non-UTF-8 arguments return expected exit/output channels. Leading-zero IDs work; zero/max int32 are supported absent IDs. Help, usage and not-found leave rows/timestamps/sequence unchanged. With the fixture stopped, every command/help alias/invalid-argument family—including non-UTF-8—fails database preflight with exit 1 and empty stdout. Configured unreachable endpoint also fails. Retained-volume restart preserves the complete snapshot and sequence; next ID is 7. A malformed unrelated JSON sentinel remains untouched; no invocation-directory JSON appears.

Both prior review findings remain resolved: same-column text-status schema is rejected before writes with unchanged data/type/sequence; differing stored defaults cannot make new tasks Deleted or give them fabricated timestamps. Missing-column incompatible schema also remains preserved. These checks independently passed in this Validator run.

## Engineering and coverage judgment

SQL effects are localized in the connection-owning business store; CLI delegates through its small typed public interface. Resource ownership justifies stateful `TodoStore`. No material guideline exception, unnecessary framework, compatibility fallback or test-only production seam found. Applied main test-audit gates: API coverage protects typed return/error and connection-lifetime behavior, while process/SQL checks protect transport, persistent lifecycle and real schema semantics. Assertions use external expected behavior, real infrastructure and independent SQL rather than mock-generated outputs.

All required evidence outcomes passed with adequate coverage and zero actionable failures. README startup was executed using its documented separate compose project/port configuration, avoiding existing user resources; the default URL/port path was inspected in source/configuration, not separately bound to port 5432. Cargo emits its own build diagnostics on stderr during `cargo run`; direct binary checks verify the application itself has empty stderr on successful commands.

Owned test project `todo-test-6c6a48922f8d` (port 39749) and manual project `todo-validation-7a118eda6c83` were cleaned with only their own volumes/networks. Cleanup succeeded; no product or cleanup failure occurred. Docker actions used approved sandbox escalation.

Finite execution does not claim arbitrary schema migration, concurrent-writer guarantees, gapless IDs after aborted transactions, JSON migration or crash/power-loss durability; these remain outside the accepted scope. Auxiliary test-audit guide `/home/vv/docs/help/testing/writing-tests.md` was unavailable as disclosed in the handoff; the main skill gates were applied and no required product check was unavailable.

## Usage

Supervisor aggregate usage report pending. Native measured counters and observed model settings unavailable to this worker; this is a reporting limit only. No repair task/order change required.
