# Independent review — 03_database

**Status: FAIL — one actionable schema-validation finding.** Required supplied checks pass; coverage judgment fails the incompatible-schema contract.

## Scope and routing

Reviewed fixed candidate `/home/vv/ccode/generate-prototype/apps/todolist_rust`, untracked in enclosing Git with no revision. Candidate and requirements were not edited. Fresh reviewer context used selected `specs/todolist_rust/{project.md,task_order.md,verification.md,tasks/01_business_logic.md,tasks/02_cli.md,tasks/03_database.md}`, separate task03 acceptance, earlier acceptances only with task03 replacement mapping, implementation and declared evidence. No plans, memory, other applications or implementation histories consulted.

Applied `/home/vv/ccode/generate-prototype/guidelines.md` and test-audit skill `/home/vv/.agents/skills/test-audit/SKILL.md`. Auxiliary testing boundary guide unavailable as handed off; main instructions applied. Requested demanding Reviewer route: escalation `gpt-6-astra`, medium; observed runtime settings unavailable. Full workflow, independent task review; final assembled-app validation remains pending.

## Finding R1 — incompatible same-column schema is silently accepted and mutated

**Priority: medium.** Authority: DB-04 requires a native PostgreSQL enum; DB-09 requires an encountered incompatible schema to return an error and preserve it. README also promises incompatible schemas are reported without reset.

At `apps/todolist_rust/src/lib.rs:109`, startup uses `CREATE TABLE IF NOT EXISTS` followed at line 118 by a zero-row SELECT that only establishes column availability. A pre-existing table with all expected columns but `status text` is accepted. Its status cannot enforce the required enum contract, yet `help` succeeds and `add` writes new rows.

Reproduction: `python3 .suite/004_todolist_rust/runs/03_database/reviewer/schema_probe.py` creates a unique disposable PostgreSQL compose fixture with identity integer id, non-null text description, both timestamp columns and **text status**, seeds one row, then invokes the candidate. Observed `help` exit 0 and `add 'unexpected write'` exit 0 (`Added task 2`); direct SQL confirms status remains text and row 2 was written. Expected database error exit 1, empty stdout and unchanged existing rows for this incompatible schema. See `schema-probe.log`; cleanup succeeded.

Required resolution: reject incompatible existing schema before allowing command execution, using a proportionate check of the required schema contract; preserve existing schema/data rather than migrating or resetting. Extend the current real-database incompatible-schema test to cover a same-column incompatible type so the guard is exercised beyond missing-column failures. No compatibility or migration feature requested.

## Independent checks and coverage

From app root, independently ran `cargo fmt --check`, `cargo check`, `cargo clippy --all-targets -- -D warnings` successfully. Cargo check reported successful dev profile completion; clippy output in `clippy.log`.

Independently ran `python3 tests/cli_e2e.py` with authorized Docker access: exit 0, `e2e.log`. This actually ran the Rust API test and lifecycle example on separate real databases, compiled the binary, and exercised CLI processes outside the project directory. SQL assertions cover schema creation, ids, exact descriptions, statuses, timestamps, idempotence, soft deletion, not-found behavior, argument errors, all-command outage preflight and unchanged rows/sequence across container restart. No passing skips or mocked database outcomes. Owned fixture `todo-test-645add7716d0` cleaned successfully. Additional reviewer fixture `todo-review-07438da32c01` also cleaned successfully.

Inspected README and implementer's separately executed `manual-compose.log`: documented compose startup/readiness/help/CRUD/down/up commands retain volume data and sequence, then scoped volume cleanup succeeds. This is supplied manual evidence, not claimed as independently repeated manual execution; independent automated fixture exercises critical startup/restart/SQL behavior.

DB-01–08 and DB-10–11 have adequate observed coverage for selected finite scenarios. DB-09 fails R1 despite its existing two-column incompatible-table test passing. Healthy newly initialized schema itself satisfies DB-04. No other actionable source-fidelity or engineering findings. SQL and connection lifetime are localized in TodoStore; CLI delegates through typed API, no test-only production hooks, no unwanted JSON compatibility. Tests use independent SQL expectations and real process/resource lifecycles. API-level coverage has a distinct typed return/error and reconnection purpose; no test edits performed.

## Limits and handoff

No prior actionable findings supplied. No required command blocked or skipped. Finite fixture checks do not establish concurrency, crash recovery, arbitrary migrations or gapless aborted transactions, all outside scope. Missing auxiliary guide is disclosed, not substituted for real-dependency checks. Candidate changes resolving R1 require a fresh review. Usage aggregate pending supervisor; native counters unavailable.
