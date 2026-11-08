# CLI contract

- **Participants:** The [CLI](../tasks/02_cli.md) serves terminal users and the [local eval](../../../evals/README.md).
- **Sources:** [Project requirements](../project.md).
- **Interface:** Run each command as a separate process using `uv run todo` from `apps/todolist`.
- **Semantics:** Each successful command exits with code `0` and prints the specified stdout exactly, including one trailing newline.
- **Effects:** Adding tasks creates `tasks.json` in the app directory.
- **Guarantees:** Each subsequent process observes the persisted state from preceding commands.

Stderr is not part of this contract.
Invalid-input behavior is outside this contract's scope except for the [parent input checks](#parent-input-checks).

## Parent selection

Apply when creating a task.

- Accept `add <text> [--parent <id>]`.
- Create a top-level task when `--parent` is omitted.
- Use the supplied identifier as the parent under the [task hierarchy contract](task_operations.md#task-hierarchy).
- Keep the successful response as `Added task <id>: <text>`.

## Hierarchical listing

Apply to `list` output.

- Display each task once beneath its parent using depth-first traversal.
- Order top-level tasks and siblings by ascending task identifier.
- Indent each level by two spaces before the existing `<id> [<state>] <text>` format.
- Leave top-level tasks unindented.
- Print `No tasks.` when no tasks remain.

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
  add <text> [--parent <id>]
  list
  complete <id>
  delete <id>
  help
```

### Hierarchy scenario

Start with no `tasks.json` and run each command in a separate process.

| Arguments | Expected stdout |
|---|---|
| `add "Project"` | `Added task 1: Project` |
| `add "Unrelated"` | `Added task 2: Unrelated` |
| `add "Build" --parent 1` | `Added task 3: Build` |
| `add "Document" --parent 1` | `Added task 4: Document` |
| `add "Test" --parent 3` | `Added task 5: Test` |
| `complete 1` | `Completed task 1` |

Run `list` and expect exactly:

```text
1 [x] Project
  3 [ ] Build
    5 [ ] Test
  4 [ ] Document
2 [ ] Unrelated
```

Run `delete 3`, expect `Deleted task 3`, then run `list` and expect exactly:

```text
1 [x] Project
  4 [ ] Document
2 [ ] Unrelated
```

Run `delete 1`, expect `Deleted task 1`, then run `list` and expect exactly:

```text
2 [ ] Unrelated
```

Run `delete 2`, expect `Deleted task 2`, then run `list` and expect `No tasks.`.

### Parent input checks

Create two top-level tasks with identifiers `1` and `2` in a fresh store.
Run each command below in a separate process.
Each command must exit nonzero, print no stdout and leave persisted tasks unchanged.

| Arguments | Invalid condition |
|---|---|
| `add "Orphan" --parent 999` | Parent does not exist. |
| `add "Ambiguous" --parent 1 --parent 2` | More than one parent is supplied. |
| `add "Repeated" --parent 1 --parent 1` | The parent option is repeated. |
