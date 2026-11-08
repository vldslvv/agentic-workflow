# Business layer — task operations and JSON persistence

## Context

- **Responsibility:** Manage TODO tasks and persist their state.
- **Boundary:** Own business operations and JSON persistence; CLI parsing and presentation belong to the CLI component.
- **Sources:** [Project requirements](../project.md).

## Contracts

- **Provides:** [Task operations](../contracts/task_operations.md) for the CLI.

## Behavior

- **Inputs:** Task descriptions, identifiers and optional parent identifiers supplied through the task operations interface.
- **Effects:** Persist task changes under the [task operations contract](../contracts/task_operations.md).
- **Outputs:** Task identities, descriptions, completion state and parent relationships for the CLI.
- **State and lifecycle:** Load persisted tasks across separate process invocations.

## Acceptance

| Scenario | Observable pass condition |
|---|---|
| Create and list tasks | Task identities, descriptions and initial completion state satisfy the [operations contract](../contracts/task_operations.md). |
| Complete or delete a task | A later process observes the changed state required by the [lifecycle example](../contracts/cli.md#ordered-scenario). |
| Persist parent-child relationships | Separate processes preserve the [task hierarchy](../contracts/task_operations.md#task-hierarchy). |
| Delete a subtree | Deletion removes all descendants and preserves unrelated tasks under the [hierarchy scenario](../contracts/cli.md#hierarchy-scenario). |
| Reject invalid parents | Invalid parent assignments leave persisted tasks unchanged under the [parent input checks](../contracts/cli.md#parent-input-checks). |

## Workflow requirements

Workflow: plan-review

