# Verification

## Scenario — commands and persistence

- **Task/source clauses:** [Task operations](contracts/task_operations.md) and the [CLI contract](contracts/cli.md).
- **Setup and inputs:** Preserve any existing `tasks.json` as evidence, then start without that file in `apps/todolist`.
- **Actions:** Run the [ordered scenario](contracts/cli.md#ordered-scenario) and [help check](contracts/cli.md#help), using a separate `uv run todo` process for every command.
- **Pass rule:** Match every specified exit status and stdout exactly, including trailing newlines, and verify that adding tasks creates `tasks.json`.
- **Cleanup:** Preserve scenario evidence and restore any pre-existing `tasks.json` after removing the scenario's file.
- **Evidence:** Record commands, exit statuses, stdout and persisted-file observations.

The local [todolist eval](../../evals/README.md) runs generation before these checks
and separately checks trace-file presence.

