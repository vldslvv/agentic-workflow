# TODO list

Requires Python 3.11 or newer and uv. From the repository root:

```sh
cd apps/todolist
uv sync
uv run todolist help
uv run todolist add "Buy café beans"
uv run todolist add "Read a book"
uv run todolist list
uv run todolist complete 1
uv run todolist delete 2
uv run todolist --help
```

Quote titles containing spaces. `add` prints the new task's ID; use the IDs
shown by `list` for `complete` and `delete`. Listing shows each task as
`ID [pending] TITLE` or `ID [complete] TITLE`. Completing a task again is safe.
Use `uv run todolist COMMAND --help` for a command's arguments.

Tasks persist in `apps/todolist/tasks.json` (the application root), even when
the installed `.venv/bin/todolist` executable is run from another directory.
Help and listing an empty application do not create this file. Invalid input
or unreadable storage produces an error and a nonzero exit status.

Run the tests from `apps/todolist` with `uv run pytest -q`.
