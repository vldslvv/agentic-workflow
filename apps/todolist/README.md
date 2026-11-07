# TODO list

A small, single-user TODO app with JSON persistence and no runtime dependencies.
Install Python 3.11 or newer and uv, then run from this directory:

```sh
uv sync
uv run python -m todolist help
uv run python -m todolist add "Buy milk"
uv run python -m todolist add "Walk the dog"
uv run python -m todolist list
uv run python -m todolist complete 1
uv run python -m todolist delete 2
```

`list` shows each task's ID, title, and `pending` or `completed` status. Use the
IDs shown by `list` for `complete` and `delete`. Quote multiword titles. `help`,
`--help`, or no command displays usage; each command also accepts `--help`.
Successful changes print a confirmation. Invalid arguments, unknown IDs, blank
titles, unreadable files, and corrupt storage report errors on stderr and exit
with a nonzero status.

Tasks are saved in `tasks.json` in this application directory, regardless of the
working directory. The file is created on the first successful change. To run
from another directory, use `uv run --directory /absolute/path/to/apps/todolist
python -m todolist list` (as one shell command).

New IDs are one greater than the largest existing ID, starting at 1 for an empty
list. Deleted IDs can therefore be reused. Titles are trimmed, and completing an
already completed task is harmless. This app is intended for one user running
one command at a time; concurrent writes are not supported.

Run the regression tests from this directory:

```sh
uv run python -m unittest discover -s tests -v
```
