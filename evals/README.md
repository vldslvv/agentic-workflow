# Local evaluations

## Workflow document validation

- Context: use [Workflow review](../agentic-workflow/guides/WORKFLOW_REVIEW.md) to judge document agreement with [WORKFLOW.md](../agentic-workflow/WORKFLOW.md), the fixed source of truth.
- Inputs: current package files, root `AGENTS.md`, installed `.agents/skills/agentic-workflow-*` wrappers, Python 3.10+, and an authenticated local Codex CLI on POSIX. Uncommitted changes are included.
- Effects: run `make validate-workflow`. The launcher snapshots these inputs and starts one fresh, read-only LLM judge pass. It disables subagents, automatic project instructions and memory injection so candidate instructions can be read as evidence. It does not run the app workflow, retry, or correct findings. Keep files stable while the initial snapshot is copied.
- Outputs: the console verdict and a unique `.evals/workflow/review-*/` directory containing `inputs/`, the prompt and output schema, `run.json`, `events.jsonl`, `agent.stderr`, `judgment.json`, `result.json` and the rendered `report.md` when judging succeeds. Partial evidence remains available on errors or interruption. These are advisory findings about document agreement, not proof of agent behavior.

The judge follows the guide across the whole package and its entry points. Its
table covers each workflow step and linked contract, with source locations,
reading paths, omissions and corrective guidance. The launcher derives the
overall verdict from those rows: any `FAIL`, otherwise any `UNCLEAR`, otherwise
`PASS`. Only `PASS` exits successfully; missing or malformed judge output also
fails. A valid `FAIL` or `UNCLEAR` report is a completed review.

The Reviewer default route comes from `.agentic-workflow/MODELS.md` when present,
otherwise [the packaged model policy](../agentic-workflow/policies/MODELS.md).
The existing eval routing reader applies that route without merging defaults.
Requested settings are recorded separately from unavailable observed settings.
The CLI uses local authentication and configuration. Its
[structured-output options](https://learn.chatgpt.com/docs/non-interactive-mode)
provide the machine-readable judgment; semantic coverage is assessed by the LLM.
Input selection and the prompt exclude history and app artifacts; this is not a
filesystem read-isolation guarantee.

Override the 1,800-second limit with
`make validate-workflow WORKFLOW_TIMEOUT=900`, or run
`python3 evals/workflow.py --timeout 900` from the repository root.
The Python runner exits `0` for `PASS`, `1` for `FAIL`/`UNCLEAR`, `2` for launcher
or judge errors, `124` for timeout, and `128 + signal` for interruption. Make
returns a nonzero status for any unsuccessful outcome. Timeout and interruption
terminate the judge process group and retain evidence. Each invocation makes
at most one judge attempt; setup failures make none.

Run `python3 -m unittest discover -s evals/tests -v` for the subprocess fixture
checks. Those verify the launcher contract without spending model calls; they do
not measure the quality of the judge's conclusions.

## Todolist end-to-end eval

Run with Python 3.10+, Git, uv, and an authenticated local Codex CLI on a POSIX host:

```sh
make eval
```

This creates a detached temporary worktree at committed `HEAD`, verifies that its
Git state is clean, and runs one full todolist eval with the default strict checks.
Your current branch, index, and files stay unchanged; uncommitted app inputs are
not included. The launcher and grader come from the invoking checkout, so changes
to the eval tooling itself can be exercised without committing them. A fresh
worktree starts clean, so no reset or deletion in your current checkout is needed.

The command prints the agent, CLI, artifact, and overall outcomes, returning a
nonzero Make exit status on failure. It saves logs, `result.json`, `worktree.json`,
the generated app (excluding its virtual environment and bytecode), and the new
execution evidence (under `records/`) under `.evals/todolist-worktrees/<unique-run>/` before removing
the worktree, including after a failed eval. If preserving evidence or removing
the worktree fails, it reports the retained location for recovery. Runs do not
overwrite previous reports.

Override timeouts with `make eval EVAL_AGENT_TIMEOUT=1800 EVAL_COMMAND_TIMEOUT=60`.
This target runs the end-to-end eval; the fixture tests below verify the runner.

To run directly in the current checkout and retain generated files there:

```sh
python3 evals/todolist.py run
python3 evals/todolist.py clean
```

By default, commit intended source changes and resolve other staged, unstaged,
or non-ignored untracked changes before running. Pass `run --allow-dirty` to
evaluate uncommitted inputs instead; `run.json` records the initial Git status,
and `source_commit` identifies the base commit rather than all evaluated inputs.
This option does not commit, stash, or reset anything. `apps/todolist`
and `.evals/todolist` must be absent, even if ignored. Existing `.agentic-workflow` records
are allowed under the selected checkout policy. The runner rejects
an unsuitable checkout before creating files. It never stashes or resets changes.

`run` launches one `codex exec` with the exact prompt `Implement specs/todolist`.
It resolves the Supervisor default profile from
`<project-root>/.agentic-workflow/MODELS.md` when present, otherwise
[the packaged defaults](../agentic-workflow/policies/MODELS.md#routing-source). An override
is a complete replacement; malformed configuration fails without falling back.
The launcher enables subagents, requests the
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

The runner records existing `.agentic-workflow` entry names before launch and identifies new
implementation directories after Codex exits. Run without concurrent workflow work
so those new directories can be attributed to this eval.
The artifact grade requires a single new implementation directory with
regular files `reports/usage.json`, `reports/usage.md`, `reports/timeline.json`,
and at least one `native/*/*.jsonl`. Empty files pass. Contents, sizes, worker
counts, task documents, and workflow compliance are not graded. The evaluator
never produces or repairs these artifacts.

`.evals/todolist/` contains `run.json` (launch settings, source commit, and existing
records entry names),
`events.jsonl`, `agent.stderr`, Codex's `final-response.txt` when available,
per-command raw stdout/stderr, and `result.json`. The result reports agent
execution, CLI behavior, and artifact presence separately, with observed output,
missing paths, and elapsed time. Partial CLI evidence is also saved in `cli.json`.
Overall PASS requires all three checks to pass. Exit codes are `0` for PASS, `1`
for failed assertions or unsuccessful agent exit, `2` for runner errors, `124`
for timeout, and `128 + signal` for interruption. An interruption skips any
remaining CLI commands.

Generated files remain available for inspection. `clean` requires this checkout's
eval run marker and the completed run's records inventory in `result.json`. It checks
removal paths against the Git index and HEAD before deleting anything and refuses
symlinked removal paths. It removes only `apps/todolist`, the implementation
directories recorded as created by this eval, and `.evals/todolist`. Existing
records entries, directories added after the eval, and the shared `.agentic-workflow` directory
remain. Other repository changes are reported for manual handling. A missing
inventory requires manual cleanup. Local Codex session history remains intact.

Run the fast checks without a model call:

```sh
python3 -m unittest discover -s evals/tests -v
```

These checks use disposable Git repositories and PATH-selected subprocess
fixtures for Codex and uv. The fixture app has real on-disk task persistence;
these checks validate the evaluator, not Codex generation or dependency setup.
Follow them with one real `run`. The runner uses the current checkout; it does not
create worktrees or snapshots. Automatic retries, repeated-trial statistics,
baseline comparisons, CI integration, and trace-content audits are outside this eval.
