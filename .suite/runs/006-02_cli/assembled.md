# Assembled app verification

Actual app, separate CLI processes, real app-root storage, unrelated temporary cwd.

Command: `uv run --project apps/todolist python -m todolist help`
Exit: 0
```text
usage: todolist [-h] {add,list,complete,delete,help} ...

Manage your TODO list.

positional arguments:
  {add,list,complete,delete,help}
    add                 Add a task
    list                List tasks and their completion status
    complete            Complete a task
    delete              Delete a task
    help                Show this help message

options:
  -h, --help            show this help message and exit

```

Command: `uv run --project apps/todolist python -m todolist --help`
Exit: 0
```text
usage: todolist [-h] {add,list,complete,delete,help} ...

Manage your TODO list.

positional arguments:
  {add,list,complete,delete,help}
    add                 Add a task
    list                List tasks and their completion status
    complete            Complete a task
    delete              Delete a task
    help                Show this help message

options:
  -h, --help            show this help message and exit

```

Command: `uv run --project apps/todolist python -m todolist list`
Exit: 0
```text
No tasks yet.

```

Command: `uv run --project apps/todolist python -m todolist add Buy café beans`
Exit: 0
```text
Added task 1: Buy café beans

```

Command: `uv run --project apps/todolist python -m todolist add Write report`
Exit: 0
```text
Added task 2: Write report

```

Command: `uv run --project apps/todolist python -m todolist list`
Exit: 0
```text
1 [pending] Buy café beans
2 [pending] Write report

```

Command: `uv run --project apps/todolist python -m todolist complete 1`
Exit: 0
```text
Completed task 1: Buy café beans

```

Command: `uv run --project apps/todolist python -m todolist delete 2`
Exit: 0
```text
Deleted task 2.

```

Command: `uv run --project apps/todolist python -m todolist list`
Exit: 0
```text
1 [completed] Buy café beans

```

Command: `uv run --project apps/todolist python -m todolist complete 999999`
Exit: 1
```text
Error: Task 999999 not found

```

Command: `uv run --project apps/todolist python -m todolist add`
Exit: 2
```text
usage: todolist add [-h] title
todolist add: error: the following arguments are required: title

```

Command: `uv run --project apps/todolist python -m todolist delete 1`
Exit: 0
```text
Deleted task 1.

```

Command: `uv run --project apps/todolist python -m todolist list`
Exit: 0
```text
No tasks yet.

```

PASS: help, cross-process lifecycle, errors without mutation, Unicode titles, app-root persistence, final empty state.
Cleanup: preexisting storage restored, or generated storage removed.
