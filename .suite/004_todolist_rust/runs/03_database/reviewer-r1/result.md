# Fresh independent review — task 03_database repair r1

**FAIL: original R1 is resolved; one further actionable creation/default finding remains.**

## Scope and authority

Candidate `/home/vv/ccode/generate-prototype/apps/todolist_rust`, no Git revision supplied (untracked candidate). Reviewed full source, tests, example, Cargo configuration, compose and README without modifying candidate or requirements. Inputs: `specs/todolist_rust/{project.md,task_order.md,verification.md,tasks/01_business_logic.md,tasks/02_cli.md,tasks/03_database.md}`; `.suite/004_todolist_rust/tasks/03_database/acceptance.md`; preceding two task acceptances only as amended by task03. Applied `/home/vv/ccode/generate-prototype/guidelines.md`, shared suite rules and Reviewer routine. No plans, memory, other apps or conversations consulted.

Requested demanding Reviewer route: escalation, `gpt-6-astra`, medium, for backend/data-preservation correctness. Observed host settings unavailable. Test-audit skill read and applied; auxiliary boundary guide unavailable as disclosed in handoff. No test edits or production test hooks. SQL effects are localized to the store; CLI delegates to the public API. No material guideline exception found.

## R2 — creation trusts unchecked database defaults

Priority: medium. `apps/todolist_rust/src/lib.rs:157` inserts only description. The compatibility predicate at line 120 verifies column types, nullability, identity primary key and enum members, but creation also depends on defaults for status and timestamps.

Independent reproduction `python3 .suite/004_todolist_rust/runs/03_database/reviewer-r1/default_probe.py` creates the required native enum and five correctly typed, non-null columns, integer identity primary key, ordinary timestamp defaults, but `status task_status NOT NULL DEFAULT 'Deleted'`. It seeds one row. The candidate accepts `help` (exit 0) and `add 'unexpected write'` (exit 0, `Added task 2`). Direct SQL shows the newly inserted row has status Deleted. Such a successful creation is hidden by normal list. See `default-probe.log`; uniquely owned fixture cleanup succeeded.

This violates DB-04/DB-05 creation as New and DB-09 incompatible-schema handling. Expected: new tasks must be New with current equal creation timestamps, or incompatible storage must be rejected before a successful mutation. Required resolution: ensure the creation invariants cannot depend on unchecked defaults. Explicitly writing New and creation timestamps is a narrow option; rejecting incompatible defaults is another. No generic schema migration or exhaustive arbitrary-DDL validator is requested. Extend the existing public-boundary regression to cover this credible same-type incompatibility and assert the chosen compliant outcome. Review the analogous timestamp defaults dependency while making that repair.

## Executed checks and coverage

From app root independently executed `cargo fmt --check`, `cargo check --offline`, `cargo clippy --offline --all-targets -- -D warnings`: all exit 0 (check and clippy reported finished dev profile). Commands ran together in sequence; no required static check skipped.

Independently executed `python3 tests/cli_e2e.py`: exit 0; full output in `e2e.log`. The runner executed real fixture-backed Cargo tests and API example on separate databases, CLI processes outside project root, direct catalog/row/sequence queries, lifecycle, timestamps, Unicode/descriptions, argument and not-found errors, all-command outage handling, restart preservation and incompatible-schema cases. Fixture `todo-test-e93d09091562` cleaned successfully. Independent default probe fixture `todo-review-703dc1a60420` cleaned successfully. Cleanup failures: none.

Original R1 same-column text-status case now returns incompatible-schema error for help/add without altering rows/sequence/type in the required runner. Source inspection confirms validation occurs inside initialization transaction and failure rolls back. Prior FAIL history remains intact.

Inspected implementer `repair-r1.md`, `cargo-repair-r1.log`, `e2e-repair-r1.log`, `manual-repair-r1.log` and prior reviewer finding/reproduction. README manual evidence shows final candidate startup/readiness/help/CRUD, compose down/up preserving data and next identity, and scoped volume removal. That manual evidence was inspected, not claimed as independently repeated; independent runner exercises real startup, SQL, stop/start and volume cleanup.

DB-01–03, DB-06–08 and DB-10–11 have adequate finite observed coverage. Fresh generated schema and ordinary creation satisfy DB-04–05, but R2 demonstrates their existing-schema creation coverage gap and DB-09 failure. Tests use independently expected SQL state and real boundaries; API return types/reconnection add distinct coverage beyond CLI rendering. No mocks, passing skips, or production test seams found.

## Remaining gates and limits

Task cannot pass until R2 is repaired and freshly reviewed. No infrastructure blocker or required check omitted. No migration, concurrent-writer, crash recovery or gapless aborted-transaction guarantee assessed, consistent with scope. Final assembled-app validation remains separate and pending. Usage aggregate pending Supervisor; measured counters unavailable in this review context.
