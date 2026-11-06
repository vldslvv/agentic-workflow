# Todo list

A small Python command-line app with JSON persistence. Requires Python 3.11 or
newer and uv. From the repository root:

```sh
cd apps/todolist
uv sync --locked
uv run todo add "Buy café beans"
uv run todo add "Write notes"
uv run todo list
uv run todo complete 1
uv run todo delete 2
uv run todo help
```

`uv run todo --help` also lists the commands. `list` displays each task's ID,
title, and `[ ]` (incomplete) or `[x]` (complete) state. An empty list prints
`No tasks.`. Commands report invalid input or storage errors on stderr and exit
with a nonzero status.

Tasks are saved in `apps/todolist/tasks.json`, next to this README, when a task
is first added. The file is ignored by Git. Listing and help do not create it.
The uv-managed editable installation keeps this location independent of your
working directory. From elsewhere, use the app's absolute path:

```sh
uv run --project /absolute/path/to/repository/apps/todolist todo list
```

Titles are trimmed and must not be blank. IDs identify current tasks and may be
reused after deletion. Completing an already completed task succeeds. Invalid
task data is reported without overwriting the file. Concurrent writes are not
supported.

The reusable business API is `todolist.core.TaskStore(path)`, with `create`,
`list`, `delete`, and `complete` methods. Domain and storage failures raise
`todolist.core.TodoError`.
