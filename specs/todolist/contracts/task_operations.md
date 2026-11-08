# Task operations

- **Participants:** The [business layer](../tasks/01_business_logic.md) provides operations consumed by the [CLI](../tasks/02_cli.md).
- **Sources:** [Project requirements](../project.md) and the [CLI contract](cli.md).
- **Interface:** Create, list, complete and delete tasks.
- **Semantics:** Expose task identifiers, descriptions and completion state needed by the CLI.
- **Effects:** Preserve tasks in `tasks.json` at the app root, `apps/todolist`.
- **Guarantees:** Each process observes the persisted state from preceding commands.

## Operations

| Operation | Required behavior |
|---|---|
| Create | Add a task from its description and expose its identifier and initial incomplete state. |
| List | Return tasks and their completion state for display, including the empty result. |
| Complete | Mark the identified task complete. |
| Delete | Remove the identified task from subsequent listings. |

## Examples

Use the [ordered CLI scenario](cli.md#ordered-scenario) for required task state transitions and identifiers.
