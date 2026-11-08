# Task operations

- **Participants:** The [business layer](../tasks/01_business_logic.md) provides operations consumed by the [CLI](../tasks/02_cli.md).
- **Sources:** [Project requirements](../project.md) and the [CLI contract](cli.md).
- **Interface:** Create, list, complete and delete tasks.
- **Semantics:** Expose task identifiers, descriptions, completion state and parent relationships needed by the CLI.
- **Effects:** Preserve tasks in `tasks.json` at the app root, `apps/todolist`.
- **Guarantees:** Each process observes the persisted state from preceding commands.

## Operations

| Operation | Required behavior |
|---|---|
| Create | Add a task from its description and optional parent identifier, exposing its identifier and initial incomplete state. |
| List | Return tasks, their completion state and parent relationships for display, including the empty result. |
| Complete | Mark only the identified task complete. |
| Delete | Remove the identified task and all descendants from persisted state and subsequent listings. |

## Task hierarchy

Apply when creating, listing or deleting tasks.

- Allow each task to have zero or one parent.
- Allow a parent to have multiple children.
- Allow children to have children at further levels.
- Assign an optional existing parent when creating a task.
- Reject references to nonexistent parents and multiple parent assignments without changing persisted tasks.
- Keep parent relationships acyclic.
- Persist parent relationships across process invocations.
- Preserve ancestors, siblings and unrelated tasks when deleting a subtree.
- Expose enough hierarchy information for the [CLI listing rules](cli.md#hierarchical-listing).

## Examples

Use the [ordered CLI scenario](cli.md#ordered-scenario) for required task state transitions and identifiers.
Use the [hierarchy scenario](cli.md#hierarchy-scenario) for parent relationships and subtree deletion.
