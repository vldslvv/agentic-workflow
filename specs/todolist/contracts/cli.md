# CLI contract

- **Participants:** The [CLI](../tasks/02_cli.md) serves terminal users and the [local eval](../../../evals/README.md).
- **Sources:** [Project requirements](../project.md).
- **Interface:** Run each command as a separate process using `uv run todo` from `apps/todolist`.
- **Semantics:** Each successful command exits with code `0` and prints the specified stdout exactly, including one trailing newline.
- **Effects:** Adding tasks creates `tasks.json` in the app directory.
- **Guarantees:** Each subsequent process observes the persisted state from preceding commands.

Stderr is not part of this contract.
Invalid-input behavior is outside this contract's v1 scope.

## Examples

### Ordered scenario

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

### Help

`uv run todo help` exits with code `0` and prints exactly this text, including the trailing newline:

```text
Usage: todo <command>
Commands:
  add <text>
  list
  complete <id>
  delete <id>
  help
```
