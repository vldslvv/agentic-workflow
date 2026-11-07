# TODO app

Requires Rust, Docker Engine and Docker Compose. PostgreSQL runs in the official
`postgres:18` image with a named data volume and readiness health check.
From this Cargo project directory:

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

`down` retains data. `docker compose down -v` deliberately deletes this compose
project's data volume. These commands use local development credentials
`todo`/`todo` and database `todo`, bound to localhost. For a separate project or
occupied port, set both the compose project/port and matching URL:

```sh
export COMPOSE_PROJECT_NAME=todo-sandbox
export TODO_DB_PORT=55432
export DATABASE_URL=postgres://todo:todo@127.0.0.1:55432/todo
docker compose up -d --wait db
docker compose ps
cargo run -- help
# Run the same add/list/complete/delete commands above.
docker compose down
```

The CLI uses `DATABASE_URL`, defaulting to
`postgres://todo:todo@127.0.0.1:5432/todo`, independently of invocation cwd.
A fresh database initializes automatically without consuming task IDs. Every
invocation connects and checks the database before handling arguments, including
help, no arguments and invalid usage. Connection timeout is five seconds per
connection attempt; database failures exit 1 with explanatory stderr and empty
stdout. An existing incompatible schema is reported without resetting it.
The app uses plain local PostgreSQL connections; configure secure transport
separately before using it beyond local development. No JSON is read, written,
imported or used as fallback.

Each invocation performs one command. `add` takes exactly one UTF-8 description
argument: quote spaces, use `""` for empty text, and quote a leading hyphen normally
(`add "-urgent"`). Descriptions are preserved exactly. `complete` and `delete`
take one ASCII decimal ID from 0 to 2147483647; actual stored IDs start at 1.
Leading zeros are accepted. `list` and `help` take no operands. No arguments,
`-h`, and `--help` also show help. List rows are `ID [ ] description` for New and
`ID [x] description` for Completed, ordered by ID. Deleted tasks are hidden;
an empty list prints `No tasks.`. Add/complete/delete confirmations identify ID.
Success exits 0 with stdout and empty stderr; usage errors exit 2 with stderr
and empty stdout after successful database preflight. Missing/deleted task IDs
are operation failures (exit 1).

## Business API and schema

```rust,no_run
use todolist_rust::{Status, TodoStore};
let mut store = TodoStore::project()?; // configured live database
// Or TodoStore::connect("postgres://todo:todo@127.0.0.1:5432/todo")?
let task = store.create("Buy milk")?;
assert_eq!(task.status, Status::New);
store.complete(task.id)?;
let tasks = store.list()?;
store.delete(task.id)?;
# Ok::<(), todolist_rust::Error>(())
```

`TodoStore` owns a live connection and confines SQL effects to create/list/
complete/delete. Tasks expose `id: i32`, `description: String`, `added` and
`update: chrono::DateTime<Utc>`, and `status: Status::{Completed, New, Deleted}`.
The `tasks` table has those exact five columns: integer identity primary key,
non-null text, two non-null `timestamptz` values, and a non-null native PostgreSQL
`task_status` enum with exactly `Completed`, `New`, `Deleted`.

Creation assigns New and equal added/update instants. State-changing completion
or deletion advances update while preserving added. Repeated completion succeeds
without changing the row. Delete records Deleted; complete/delete of an absent
or Deleted ID returns `Error::NotFound(id)`. Successful mutations commit before
returning. Sequential IDs increase across deletions and container restarts;
concurrent writers, gapless numbering after failed SQL, JSON migration and
crash/power-loss guarantees are outside scope.

Run `python3 tests/cli_e2e.py` for the full real-dependency check. It creates a
unique disposable compose project/volume and port, builds a temporary project
copy offline, invokes processes outside the project root, runs `cargo test`
against a separate database, and runs the lifecycle example against another.
It checks schema/data directly using PostgreSQL, stops/restarts its own container
and removes only its own resources. Missing Docker or database fails the check.
Dependencies must already be fetched (`cargo fetch` if necessary).
`cargo test` alone needs `DATABASE_URL` pointing at a fresh disposable database.
`cargo run --example lifecycle` also requires a fresh disposable database;
its assertions create and soft-delete their own fixture tasks.
