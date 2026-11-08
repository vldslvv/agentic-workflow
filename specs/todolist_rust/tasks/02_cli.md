# CLI — user commands

## Context

- **Responsibility:** Expose TODO operations and help through a command-line interface.
- **Boundary:** Own command behavior against initial JSON storage; Postgres wiring and invocation-time availability checks belong to [integration](04_integration.md).
- **Sources:** [Project requirements](../project.md).

## Contracts

- **Provides:** User-facing `add`, `delete`, `complete`, `list` and `help` commands.
- **Consumes:** The business layer's [task operations](../contracts/task_operations.md).

## Behavior

- **Inputs:** Commands, task descriptions and identifiers.
- **Effects:** Invoke the business layer through its accepted interfaces.
- **Outputs:** Observable command results and help describing the required commands.

## Acceptance

| Scenario | Observable pass condition |
|---|---|
| Add, list, complete and delete with JSON storage | Commands expose the business layer's accepted operation behavior. |
| Help | Output describes all required commands. |
