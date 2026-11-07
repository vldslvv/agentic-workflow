# Local evaluations

## Workflow document validation

- Context: use [Workflow review](../agentic-workflow/guides/WORKFLOW_REVIEW.md) to judge document agreement with [WORKFLOW.md](../agentic-workflow/WORKFLOW.md), the fixed source of truth.
- Inputs: current package files, root `AGENTS.md`, installed `.agents/skills/agentic-workflow-*` wrappers, Python 3.10+, and an authenticated local Codex CLI on POSIX. Uncommitted changes are included.
- Effects: run `make eval-workflow`. The launcher snapshots these inputs and starts one fresh, read-only LLM judge pass. When that review fails without uncertainty, a separate editor automatically attempts one repair directly in the working Markdown files, preserving existing work and the fixed source contract. The launcher then runs the package checker with integration checks and compares `WORKFLOW.md` with the original snapshot. Both LLM invocations disable subagents, automatic project instructions and memory injection. There is no retry or second LLM review. Repairs remain uncommitted and are not rolled back, including on failure or interruption. Avoid concurrent edits throughout the command.
- Outputs: the console verdict and a unique `.evals/workflow/review-*/` directory containing `inputs/`, the review prompt and schema, `run.json`, `events.jsonl`, `agent.stderr`, `judgment.json`, `result.json` and the rendered initial `report.md` when judging succeeds. A repair adds `repair/` with its own prompt, schema, `run.json`, `events.jsonl`, `agent.stderr`, editor `output.json`, and `checks.stdout`/`checks.stderr` when checks run. The initial review remains intact; `result.json` records the final outcome and available repair evidence. Partial evidence and partial edits remain available on errors or interruption. These are advisory findings about document agreement, not proof of agent behavior.

The judge follows the guide across the whole package and its entry points. Its
table covers each workflow step and linked contract, with source locations,
reading paths, omissions and corrective guidance. The launcher derives the
initial review verdict from those rows: any `FAIL`, otherwise any `UNCLEAR`,
otherwise `PASS`. A valid `FAIL` or `UNCLEAR` report is a completed review.
The final command outcome also accounts for uncertainty and repairs:

| Review or repair outcome | Command behavior |
|---|---|
| Review `PASS` | Exit successfully without launching an editor or changing project files. |
| Any review `UNCLEAR` row, including alongside `FAIL` | Return `UNCLEAR` without repairs. |
| Review `FAIL` with no uncertainty | Launch one editor with the findings and original snapshot. |
| Editor reports all findings resolved; checks pass; source contract unchanged | Return `FIXED`. No independent re-review occurred. |
| Editor reports unresolved findings | Return `UNCLEAR`; retain any edits. |
| Editor/check failure, malformed output, changed contract, or interruption | Return nonzero; partial edits may remain. |

Both review and repair default to `gpt-6-astra` with `medium` reasoning. Set
`WORKFLOW_MODEL` and optionally `WORKFLOW_REASONING` to select settings for both:

```sh
make eval-workflow WORKFLOW_MODEL=gpt-6.1-sol WORKFLOW_REASONING=high
```

The Python runner accepts the same settings through `--model` and `--reasoning`,
with the same defaults. This command takes its launch settings from these
options; model policy files remain review inputs and do not select the model.
Requested settings are recorded separately from unavailable observed settings.
The reviewer runs read-only in the snapshot; the editor runs with workspace-write
permissions in the project root. It is instructed to make
only necessary corrections to reviewed Markdown files and return `UNCLEAR` if
any finding remains unresolved.
The CLI uses local authentication and configuration. Its
[structured-output options](https://learn.chatgpt.com/docs/non-interactive-mode)
provide the machine-readable judgment; semantic coverage is assessed by the LLM.
Input selection and the prompt exclude history and app artifacts; this is not a
filesystem read-isolation guarantee.

Override the 1,800-second limit with
`make eval-workflow WORKFLOW_TIMEOUT=900`, or run
`python3 evals/workflow.py --timeout 900` from the repository root.
The limit applies separately to each LLM invocation and to the mechanical check
command. The Python runner exits `0` for `PASS`/`FIXED`, `1` for failed checks or
`UNCLEAR`, `2` for launcher, judge or editor errors, `124` for timeout, and
`128 + signal` for interruption. Make returns a nonzero status for any unsuccessful
outcome. Timeout and interruption terminate the active process group and retain
evidence. Each invocation makes at most one judge attempt and one repair attempt;
a setup failure skips the affected LLM launch. `FIXED` records the editor's
resolution claim and passing mechanical checks, without an independent judgment
of the edited documents.

Run `python3 -m unittest discover -s evals/tests -v` for the subprocess fixture
checks. Those verify the launcher contract without spending model calls; they do
not measure the quality of the judge's conclusions or the editor's corrections.

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
