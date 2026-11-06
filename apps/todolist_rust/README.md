# TODO CLI

A small Rust TODO application backed by PostgreSQL 17. Install Rust/Cargo and
Docker with Compose, then run these commands from this directory:

```sh
cargo build
docker compose up -d --wait
cargo run -- help
cargo run -- add "Buy coffee"
cargo run -- list
cargo run -- complete 1
cargo run -- delete 1
```

The built executable is named `todolist_rust`. Use `help` or `--help` for usage.
`add` takes one nonblank description argument; quote text containing spaces.
`complete` and `delete` take a positive 32-bit task ID. Missing, extra, or invalid
arguments return a nonzero exit status and an error on stderr.

`add` and `complete` print the affected task as JSON. `list` prints a JSON array
of active tasks ordered by ID. Each task has `id`, `description`, `added`, `update`,
and `status` fields, with UTC timestamps and status `New`, `Completed`, or
`Deleted`. Completing a completed task is harmless. Deletion hides the task from
the list; accessing a missing or deleted task fails. Successful deletion produces
no output.

The database listens only on `127.0.0.1:5432`, using local development credentials
`todo:todo` and database `todo`. Operational commands require a live connection;
an unavailable database returns a nonzero exit status and stderr error. Help works
offline. The CLI initializes the schema on first use and does not start Docker
itself. Connection establishment uses a five-second timeout per address.

To use a different host port, configure both Compose and the CLI:

```sh
export TODO_DB_PORT=5433
export DATABASE_URL=postgres://todo:todo@127.0.0.1:5433/todo
docker compose up -d --wait
cargo run -- list
```

`DATABASE_URL` may point to another PostgreSQL database; the account needs schema
creation and task read/write privileges. This local client uses an unencrypted
connection. Tasks live in `public.tasks`: integer identity primary key `id`, text
`description`, UTC `added`/`update` timestamps, and native enum `status`. IDs
increase and may have gaps. Deleted rows remain stored. Repeated completion
preserves the task's timestamp. Existing `tasks.json` data is not migrated or used.

Stop the database with `docker compose down`. Its named volume retains tasks
across container restarts and recreation. To intentionally delete all stored
tasks, run `docker compose down --volumes`.
