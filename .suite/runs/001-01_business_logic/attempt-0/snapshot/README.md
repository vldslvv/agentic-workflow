# TODO list

A small Python business layer with JSON persistence. Requires Python 3.11 or later
and uv.

From the repository root, install the project:

```sh
uv sync --project apps/todolist
```

Use the public business API from the project's environment:

```python
from todolist import TaskStore

store = TaskStore()
task = store.create_task("Buy milk")
store.complete_task(task["id"])
print(store.list_tasks())
store.delete_task(task["id"])
```

By default, tasks live in `apps/todolist/tasks.json`, regardless of the working
directory. `TaskStore(path)` accepts a custom JSON file path whose parent exists.
The file contains an array of objects with `id`, `title`, and `completed` fields.
IDs are positive integers unique among current tasks; deleted IDs may be reused.

Empty titles, unknown IDs, and invalid stored data raise `ValueError`. Failed
validation leaves existing storage unchanged. File access errors propagate to
the caller. Each operation reloads storage; writes replace the file atomically.
Concurrent writers are outside this app's scope.
