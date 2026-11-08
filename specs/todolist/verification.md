# Verification

## Scenario — commands and persistence

- **Task/source clauses:** [Task operations](contracts/task_operations.md) and the [CLI contract](contracts/cli.md).
- **Setup and inputs:** Preserve any existing `tasks.json` as evidence, then start without that file in `apps/todolist`.
- **Actions:** Run the [ordered scenario](contracts/cli.md#ordered-scenario) and [help check](contracts/cli.md#help), using a separate `uv run todo` process for every command.
- **Pass rule:** Match every specified exit status and stdout exactly, including trailing newlines, and verify that adding tasks creates `tasks.json`.
- **Cleanup:** Preserve scenario evidence and restore any pre-existing `tasks.json` after removing the scenario's file.
- **Evidence:** Record commands, exit statuses, stdout and persisted-file observations.

## Scenario — hierarchy and subtree deletion

- **Task/source clauses:** [Task hierarchy](contracts/task_operations.md#task-hierarchy) and [hierarchical listing](contracts/cli.md#hierarchical-listing).
- **Setup and inputs:** Preserve any existing `tasks.json`, then start without that file in `apps/todolist`.
- **Actions:** Run the [hierarchy scenario](contracts/cli.md#hierarchy-scenario) using a separate process for every command.
- **Pass rule:** Match every exit status and stdout, preserve parent relationships across processes, and verify deleted descendants are absent from persisted state.
- **Cleanup:** Preserve scenario evidence and restore any pre-existing `tasks.json` after removing the scenario's file.
- **Evidence:** Record commands, exit statuses, stdout and persisted-file observations.

## Scenario — invalid parent assignments

- **Task/source clauses:** [Parent input checks](contracts/cli.md#parent-input-checks).
- **Setup and inputs:** Preserve any existing `tasks.json`, then create the fresh store specified by the parent input checks.
- **Actions:** Run each parent input check and list tasks after each rejected command.
- **Pass rule:** Verify nonzero exits, empty stdout, unchanged persisted tasks and unchanged listings.
- **Cleanup:** Preserve scenario evidence and restore any pre-existing `tasks.json` after removing the scenario's file.
- **Evidence:** Record commands, exit statuses, stdout and persisted state before and after rejected commands.

The local [todolist eval](../../evals/README.md) runs generation and separately checks
CLI behavior and trace-file presence; acceptance requires all scenarios above.

