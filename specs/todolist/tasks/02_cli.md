Implement a user-facing CLI for TODO app.

User commands should allow to:
 - add tasks
 - delete tasks
 - complete tasks
 - list tasks
 - help

## CLI contract

Run each command as a separate process using `uv run todo` from `apps/todolist`.
Each successful command exits with code `0`. Stdout must match the text below
exactly, including one trailing newline. Stderr is not part of this contract.

Start with no `tasks.json` in the app directory, then run these commands in order:

| Arguments | Expected stdout (line breaks shown as `<br>`) |
|---|---|
| `list` | `No tasks.` |
| `add "Buy milk"` | `Added task 1: Buy milk` |
| `add "Write tests"` | `Added task 2: Write tests` |
| `list` | `1 [ ] Buy milk`<br>`2 [ ] Write tests` |
| `complete 1` | `Completed task 1` |
| `list` | `1 [x] Buy milk`<br>`2 [ ] Write tests` |
| `delete 1` | `Deleted task 1` |
| `list` | `2 [ ] Write tests` |
| `delete 2` | `Deleted task 2` |
| `list` | `No tasks.` |

Adding tasks creates `tasks.json` in the app directory. Each subsequent process
must observe the persisted state from preceding commands.

`uv run todo help` must exit with code `0` and print exactly this text, including
the trailing newline:

```text
Usage: todo <command>
Commands:
  add <text>
  list
  complete <id>
  delete <id>
  help
```

Invalid-input behavior is outside this contract's v1 scope.

