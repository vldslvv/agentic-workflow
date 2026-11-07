# Plan — 03_database

## Request, scope and acceptance

Implement [03_database](../../../../specs/todolist_rust/tasks/03_database.md) for implementation `004_todolist_rust`, replacing the accepted JSON backend with Docker PostgreSQL. This is the ready third task in [task_order.md](../../../../specs/todolist_rust/task_order.md). The Supervisor reports tasks `01_business_logic` and `02_cli` accepted PASS. Task02 [implementer](../../runs/02_cli/implementer/result.md) and [independent reviewer](../../runs/02_cli/reviewer/result.md) results supply the accepted dependency contracts.

Mode is **full**, as assessed in [assessment.md](../../runs/03_database/implementer/assessment.md): new infrastructure, persistence/domain/API changes, preflight on all process entry paths, and real dependency/failure/restart checks interact. Separate [acceptance.md](acceptance.md), DB-01–DB-11, is the normative task check record. Fresh independent review follows implementation; final independent assembled-app validation remains a Supervisor gate.

Sources are the selected bundle's [project](../../../../specs/todolist_rust/project.md), [verification](../../../../specs/todolist_rust/verification.md), [business task](../../../../specs/todolist_rust/tasks/01_business_logic.md), [CLI task](../../../../specs/todolist_rust/tasks/02_cli.md), and [database task](../../../../specs/todolist_rust/tasks/03_database.md). Resolved engineering source is `/home/vv/ccode/generate-prototype/guidelines.md`: explicit state and side-effect boundaries, cohesive small interfaces, public-interface tests with disposable real dependencies, and no unsolicited compatibility. Suite instructions are `/home/vv/ccode/generate-prototype/spec-source-suite/{AGENTS,PLANNER,MODELS}.md`.

Scope ends at `apps/todolist_rust` plus this implementation's records. Do not alter reusable suite guidance, other apps, unrelated user files, containers or volumes. No project memory, other apps or earlier implementations are inputs. No JSON migration, compatibility adapter, auto-starting Docker from each CLI command, concurrent-writer guarantees, distributed service, or crash/power-loss proof is requested.

## Source-directed contract replacements

Keep accepted task01/task02 records intact as historical evidence. Task03 explicitly says “instead of text file” and requires a live database “When executing the CLI.” Consequently the following earlier storage-specific expectations are superseded for this assembled app only:

- `tasks.json`, missing-file empty state, JSON serialization/atomic replacement and filesystem-specific errors become configured PostgreSQL storage, idempotent schema initialization and database errors. No JSON import or fallback.
- `u64` task IDs become positive PostgreSQL `integer` IDs; values above `2147483647` are usage errors. Zero still parses and returns not-found. Leading zeros remain accepted.
- `completed: bool` becomes the required status enum plus datetime fields. Delete records `Deleted` and hides the row from normal task operations instead of removing the row.
- Help and usage errors now require successful database preflight. Parsing-only no-persistence expectations no longer apply. With a live database they still preserve task rows, statuses, timestamps and the ID sequence.

Other accepted behavior remains: descriptions preserve empty/whitespace/leading-hyphen text; one command per invocation; command spellings/arity, help aliases, list row markers/order/empty text, confirmation IDs, and output/error channels. Complete on an already completed visible task succeeds without changing its row. Missing or deleted IDs return not-found.

## Implementation approach

### Runtime and developer setup

Add `apps/todolist_rust/compose.yaml` with one PostgreSQL service `db`, a readiness health check and a named data volume. Use a maintained stable PostgreSQL image version, record it in the README, and avoid unnecessary services. Local development credentials/database are `todo`/`todo`/`todo`; bind the service to localhost, with `${TODO_DB_PORT:-5432}` as the configurable host port. Application configuration is `DATABASE_URL`, with local default `postgres://todo:todo@127.0.0.1:5432/todo`. A custom compose port needs a matching URL. Database choice is independent of invocation cwd.

Document and actually exercise exact commands from the app directory:

```sh
docker compose up -d --wait db
export DATABASE_URL=postgres://todo:todo@127.0.0.1:5432/todo
cargo run -- help
cargo run -- add "Buy milk"
cargo run -- list
cargo run -- complete 1
cargo run -- delete 1
docker compose down
```

Explain that `down` retains the volume and `down -v` intentionally deletes this compose project's data. Explain how to run an isolated compose project/port and how to wait/check readiness. Do not run destructive cleanup against a user's default project. Tests/manual evidence use unique project/container/volume names and only clean their owned resources.

### Database and domain boundary

Replace filesystem persistence with a small synchronous PostgreSQL boundary behind the existing create/list/complete/delete responsibilities. Choose normal Rust PostgreSQL/time dependencies and remove obsolete JSON-only dependencies. Keep domain state explicit and SQL/I/O confined to the store; do not add a generic repository framework or migration subsystem. An appropriate revised API is a fallible configured connection constructor and `Task { id, description, added, update, status }`, with a Rust enum corresponding to SQL status. No compatibility with the old path-based constructor or boolean task representation is needed. Update the example and README to compile and describe the actual API.

On connecting, verify the database with a real request before accepting a CLI invocation. Use a finite connection timeout. Connection/preflight failure exits 1 with explanatory stderr and no stdout, even for help, no arguments, invalid commands, malformed IDs and non-UTF-8 arguments. Preflight must precede any branch that could return usage/help. Subsequent database-operation/schema failures also fail explicitly; never report success without a committed mutation. No fallback data store or reset.

Initialize a fresh database automatically and idempotently, without creating task rows or consuming IDs. Use a `tasks` table with required columns exactly named `id`, `description`, `added`, `update`, `status`; quote `update` in SQL as necessary. Schema:

- `id integer PRIMARY KEY`, database-generated sequence/identity starting at 1, positive and unique. Successful ordinary serial creates increase by 1; delete/restart never resets or reuses IDs. Gapless numbering after aborted SQL or concurrent operations is outside scope.
- `description text NOT NULL`, preserving supported supplied strings exactly.
- `added` and `update` as non-null timezone-aware datetimes. Creation gives both the same UTC instant. Preserve `added` forever; state-changing completion/deletion sets `update` to current time. Repeating complete preserves the whole row.
- `status` uses an actual PostgreSQL enum with exactly `Completed`, `New`, `Deleted`; non-null and initially `New`.

Normal list returns only `New`/`Completed`, ordered by ascending ID. Complete changes only `New` to `Completed`; repeated complete is successful and unchanged. Delete changes a visible `New` or `Completed` task to `Deleted`, retaining its ID/description/added timestamp. Complete/delete of a missing or deleted ID returns not-found with no state change. Use atomic SQL updates/transactions as needed; commit before returning success. An incompatible existing database must return an error when encountered and must not be reset or destructively rewritten.

### CLI and evidence refresh

Keep the existing minimal parser and external presentation except required integer domain, storage/help text, and startup preflight. Decimal ASCII IDs remain unsigned in syntax; parse the supported integer range, preserving leading-zero acceptance. Invalid arity/commands/negative/signed/nondecimal/overflow/non-UTF-8 inputs return usage exit 2 only after successful preflight. Operation errors return 1; success returns 0. Errors have empty stdout, success empty stderr. Delete confirmations retain their affected ID while deleted rows disappear from list.

Replace stale JSON fixtures/assertions in `tests/business.rs`, `tests/cli_e2e.py` and `examples/lifecycle.rs`. Reuse these public boundaries instead of preserving obsolete tests or adding duplicate suites. The process runner should own a unique disposable real PostgreSQL fixture, supply its URL to Rust tests and real binaries, and inspect SQL state independently. It may compile once and run commands from a separate cwd. Every required database check must actually run: absence of Docker/database is BLOCKED, not a passing skip. Prevent parallel tests from sharing mutable task fixtures; use isolated databases/schemas or a serial lifecycle. Do not add test-only production seams.

## Checks and handoff

From `/home/vv/ccode/generate-prototype/apps/todolist_rust` run `cargo fmt --check`, `cargo check`, `cargo clippy --all-targets -- -D warnings`, and the evolved `python3 tests/cli_e2e.py`. The real-dependency runner must execute `cargo test` with its owned fixture's `DATABASE_URL`, then the process/schema/outage/restart scenarios in acceptance. Offline execution is useful if dependencies are cached, but old offline-only commands are not source requirements for the new dependencies. Record exact commands and dependency-fetch limitations.

Check schema types/defaults/nullability and native enum membership directly in PostgreSQL; validate initial and changed timestamps/statuses independently of CLI output. Exercise all four commands across fresh processes, sequence continuation after deletion, container stop/start with the same owned volume, all help aliases and usage classes while database is alive, and outage precedence for all CLI forms. Snapshot database rows and sequence around read-only/failure checks; after restart prove failures made no task mutation and persisted content is retained. Deliberately wait until a later observable instant before state-changing timestamp checks.

Also manually exercise the documented compose startup/help/CRUD/stop commands on an isolated project/port and retain terminal output plus direct SQL inspection. These checks satisfy [verification.md](../../../../specs/todolist_rust/verification.md)'s add/remove/delete lifecycle with the required real Docker database. Failure and cleanup errors remain separate; do not erase useful failure logs.

Evidence goes to `/home/vv/ccode/generate-prototype/.suite/004_todolist_rust/runs/03_database/implementer/`; this Planner's result is under `runs/03_database/planner/`. Fresh reviewer receives sources, acceptance, guidelines, candidate and implementation evidence, excluding this plan and memory. The Supervisor decides task acceptance separately. Parent's retained implementer `/root/database` must receive these paths and explicit resume; this planner remains `/root/database_plan` for corrections.

Routing: **careful**, selected for interacting backend/domain/CLI changes and data-loss correctness. Requested `gpt-6.1-sol`, high reasoning; observed native settings unavailable, no known fallback. No unavailable product capability is established by planning; real Docker/compose execution remains required. Parent reports Docker access through the authorized `require_escalated` docker prefix. No runtime execution or production implementation is performed by this Planner.
