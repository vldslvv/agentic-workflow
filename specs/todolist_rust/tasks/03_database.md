# Database — Postgres storage

## Context

- **Responsibility:** Persist TODO tasks in Postgres through the accepted storage interface.
- **Boundary:** Own Postgres storage and its Docker setup; CLI wiring belongs to [integration](04_integration.md).
- **Sources:** [Project requirements](../project.md).

## Contracts

- **Provides:** The Postgres implementation of [task operations and storage](../contracts/task_operations.md).

## Behavior

- **Inputs:** Storage operations and task data from the business layer.
- **Effects:** Persist task state in the real Docker-hosted Postgres database.
- **Outputs:** The same operation results and errors as initial JSON storage.
- **State and lifecycle:** Store the specified [fields and statuses](../contracts/task_operations.md#task-data).

## Constraints

Apply when implementing Postgres storage.

- Supply a Docker setup that starts Postgres.
- Verify storage against the real database without requiring CLI changes.

## Acceptance

| Scenario | Observable pass condition |
|---|---|
| Start the supplied Docker setup | Postgres is available for storage checks. |
| Create, list, complete and delete | Database observations satisfy the [shared operations and schema contract](../contracts/task_operations.md). |
| Storage failure | Observable failure behavior matches the agreed contract. |

