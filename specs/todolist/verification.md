Run the ordered end-to-end scenario and help check in the
[CLI contract](tasks/02_cli.md#cli-contract), from the generated app directory.
Use a separate `uv run todo` process for every command to exercise persistence.
Preserve any existing `tasks.json` as evidence before removing it for the scenario.
Verify that adding tasks creates `tasks.json` in the app directory and that every
exit code and stdout matches the contract exactly, including trailing newlines.

The local [todolist eval](../../evals/README.md) runs generation before these checks
and separately checks trace-file presence.

