# TODO CLI

Requires Rust and Docker with Compose. From this application directory:

```sh
docker compose up -d --wait
cargo build --locked
cargo run -- add "Buy milk"
cargo run -- list
cargo run -- complete 1
cargo run -- delete 1
cargo run -- help
```

The built binary is `target/debug/todolist`. It also accepts `--help` or no
arguments for usage. Quote descriptions containing spaces; IDs are positive
integers. Invalid commands or failed operations print an error to stderr and
return a nonzero exit status.

Every invocation, including help and invalid commands, connects to PostgreSQL
before handling arguments. The default URL is
`postgres://todolist:todolist@127.0.0.1:5432/todolist`. Set `DATABASE_URL` to use
another database. Each TCP connection attempt times out after three seconds;
the entire connection and schema initialization has a five-second deadline,
including DNS and PostgreSQL authentication. Failure prints an error and exits
nonzero, including when an endpoint accepts TCP but never responds.
The supplied local setup uses an unencrypted connection.

For a different host port, set both variables before starting Compose and the CLI:

```sh
export POSTGRES_PORT=5433
export DATABASE_URL=postgres://todolist:todolist@127.0.0.1:5433/todolist
docker compose up -d --wait
cargo run -- list
```

The CLI creates the schema automatically. PostgreSQL stores all tasks in
`public.tasks`: generated integer `id`, text `description`, timestamp `added`,
timestamp `"update"`, and the native `task_status` enum (`New`, `Completed`,
`Deleted`). IDs increase without reuse; gaps are possible. Descriptions are
trimmed and must not be blank. Completion is idempotent. Delete preserves the row
with status `Deleted`, hides it from normal listings, and prevents later changes.
Mutations preserve `added` and advance `"update"` when the status changes.
The application no longer reads or writes `tasks.json`.

`list` emits a tab-separated `id`, `status`, `description` header and active rows
ordered by ID. Status is `New` or `Completed`. Backslashes, tabs, carriage returns,
and newlines in descriptions display as `\\`, `\t`, `\r`, and `\n` so each task
occupies one row. Mutations print a confirmation containing the task ID.

`docker compose stop` stops the database; `docker compose start --wait` starts it
again. Tasks survive container restarts and `docker compose down` through the
named volume. `docker compose down -v` also removes the volume and all its tasks.
