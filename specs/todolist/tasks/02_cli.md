# CLI — user commands

## Context

- **Responsibility:** Expose TODO operations and help through a command-line interface.
- **Boundary:** Own command parsing and presentation; task state and persistence belong to the business layer.
- **Sources:** [Project requirements](../project.md).

## Contracts

- **Provides:** The user-facing [CLI contract](../contracts/cli.md).
- **Consumes:** The business layer's [task operations](../contracts/task_operations.md).

## Behavior

- **Inputs:** `add`, `delete`, `complete`, `list` and `help` command arguments.
- **Effects:** Invoke the business layer for task operations.
- **Outputs:** Exit statuses and exact stdout under the [CLI contract](../contracts/cli.md).

## Acceptance

| Scenario | Observable pass condition |
|---|---|
| Ordered task lifecycle | Separate command processes satisfy the [ordered scenario](../contracts/cli.md#ordered-scenario). |
| Help | Exit status and stdout satisfy the [help contract](../contracts/cli.md#help). |

## Workflow requirements

Workflow: direct

