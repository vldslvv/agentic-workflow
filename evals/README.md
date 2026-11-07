# Todolist end-to-end eval

Run from this checkout with Python 3.10+, Git, uv, and an authenticated local Codex
CLI on a POSIX host:

```sh
python3 evals/todolist.py run
python3 evals/todolist.py clean
```

Before running, commit the evaluator and intended source changes and manually
resolve other staged, unstaged, or non-ignored untracked changes. `apps/todolist`,
`.suite`, and `.evals/todolist` must be absent, even if ignored. The runner rejects
an unsuitable checkout before creating files. It never stashes or resets changes.

`run` launches one `codex exec` with the exact prompt `Implement specs/todolist`.
It resolves the Supervisor default profile from
[MODELS.md](../spec-source-suite/MODELS.md), enables subagents, requests the
workspace-write sandbox and outbound network access for dependencies, and sets
approval policy to `never`. Native session persistence stays enabled. The CLI
uses local authentication/configuration; unsupported settings or host restrictions
are failures to investigate, not triggers for a retry. Launch settings follow the
[Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

The default limits are 1,800 seconds for Codex and 60 seconds per grading command.
Override them with `--agent-timeout SECONDS` and `--command-timeout SECONDS`.
Timeouts and SIGINT/SIGTERM terminate the launched process group, including its
descendants, and retain available evidence. SIGKILL or a host crash cannot be
handled. Do not run cleanup while a trial is active.

After Codex exits, the evaluator checks the [CLI contract](../specs/todolist/tasks/02_cli.md#cli-contract)
with separate `uv run todo` processes in the app directory. It saves any generated
`tasks.json` as `generation-tasks.json` before removing it, and checks that adding
tasks creates the file again. Expected output is owned by the evaluator. Raw
stdout is compared byte-for-byte, including trailing newlines; stderr is retained
but does not affect the CLI grade.

The artifact grade requires a single implementation directory under `.suite` with
regular files `reports/usage.json`, `reports/usage.md`, `reports/timeline.json`,
and at least one `native/*/*.jsonl`. Empty files pass. Contents, sizes, worker
counts, task documents, and workflow compliance are not graded. The evaluator
never produces or repairs these artifacts.

`.evals/todolist/` contains `run.json` (launch settings and source commit),
`events.jsonl`, `agent.stderr`, Codex's `final-response.txt` when available,
per-command raw stdout/stderr, and `result.json`. The result reports agent
execution, CLI behavior, and artifact presence separately, with observed output,
missing paths, and elapsed time. Partial CLI evidence is also saved in `cli.json`.
Overall PASS requires all three checks to pass. Exit codes are `0` for PASS, `1`
for failed assertions or unsuccessful agent exit, `2` for runner errors, `124`
for timeout, and `128 + signal` for interruption. An interruption skips any
remaining CLI commands.

Generated files remain available for inspection. `clean` requires this checkout's
eval run marker and checks all three removal paths against the Git index and HEAD
before deleting anything. It refuses symlinked removal paths. It removes only
`apps/todolist`, `.suite`, and `.evals/todolist`; any remaining repository changes
are reported for manual handling. Local Codex session history remains intact.

Run the fast checks without a model call:

```sh
python3 -m unittest discover -s evals/tests -v
```

These checks use disposable Git repositories and PATH-selected subprocess
fixtures for Codex and uv. The fixture app has real on-disk task persistence;
these checks validate the evaluator, not Codex generation or dependency setup.
Follow them with one real `run` in the clean current checkout. No worktree,
snapshot, automatic retry, repeated-trial statistics, baseline comparison, CI
integration, or trace-content audit is part of this eval.
