# Business layer — task operations and initial JSON storage

## Context

- **Responsibility:** Manage TODO tasks through an interchangeable storage interface.
- **Boundary:** Own business operations, the storage interface and initial JSON storage; CLI and Postgres implementation belong to other components.
- **Sources:** [Project requirements](../project.md).

## Contracts

- **Provides:** [Task operations and storage](../contracts/task_operations.md) for the CLI and Postgres implementation.

## Behavior

- **Inputs:** Task descriptions and identifiers.
- **Effects:** Preserve tasks in `tasks.json` at the app root, `apps/todolist_rust`.
- **Outputs:** Operation results, task data and errors under the [shared contract](../contracts/task_operations.md).
- **State and lifecycle:** Preserve task fields and statuses across process invocations using initial JSON storage.

## Constraints

- Establish the shared interfaces and error behavior under the [contract definition requirements](../contracts/task_operations.md#behavior).

## Acceptance

| Scenario | Observable pass condition |
|---|---|
| Create, list, complete and delete | Operation results and task data satisfy the [shared contract](../contracts/task_operations.md). |
| Reload JSON state | A later process observes the persisted fields and statuses. |
| Storage failure | Observable failure behavior matches the agreed storage contract. |

