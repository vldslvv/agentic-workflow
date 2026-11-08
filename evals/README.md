# Local evaluations

Run from the source repository on POSIX with Python 3.10+ and an authenticated
local Codex CLI. Todolist evals also require Git and uv.

## Review and repair workflow documents

Pause concurrent edits, then run:

```sh
make eval-workflow
```

This runs one fresh, read-only snapshot review under
[Workflow review](../agentic-workflow/guides/WORKFLOW_REVIEW.md), including current
uncommitted package files, root entry points, model override and installed
wrappers. Failures without uncertainty trigger one automatic repair in working
Markdown files. Inspect `.agentic-workflow/evals/workflow/review-*/report.md`, `result.json`,
`repair/` evidence and the diff; partial edits remain after failure or interruption.
Resolve remaining findings before requesting another review.

| Outcome | Meaning |
|---|---|
| `PASS` | Review passed without edits. |
| Any review row is `UNCLEAR` | No repair runs, even alongside failures. |
| `FIXED` | Editor reports resolution, package checks pass and the source contract is unchanged. |
| `UNCLEAR` after repair | Findings remain unresolved; edits are retained. |
| Error or interruption | Inspect retained evidence and partial edits. |

`FIXED` includes no independent re-review and does not prove agent behavior.
Review and repair share these settings, independently of model policy files:

| Setting | Default |
|---|---|
| `WORKFLOW_MODEL` | `gpt-6-astra` |
| `WORKFLOW_REASONING` | `medium` |
| `WORKFLOW_TIMEOUT` | 1,800 seconds per invocation or check |

```sh
make eval-workflow WORKFLOW_MODEL=gpt-6.1-sol WORKFLOW_REASONING=high WORKFLOW_TIMEOUT=900
```

## Todolist end-to-end eval

```sh
make eval EVAL_AGENT_TIMEOUT=1800 EVAL_COMMAND_TIMEOUT=60
```

Runs one trial from committed `HEAD` in a clean temporary worktree, using the
invoking checkout's eval tooling. Uncommitted app inputs are excluded.
Logs, generated app and execution records are archived under
`.agentic-workflow/evals/todolist-worktrees/<unique-run>/` before worktree removal. Inspect
`result.json` for agent, CLI and artifact grades and `worktree.json` for worktree
status. If archiving or removal fails, recover from the reported worktree path.
The invoking checkout changes only to save eval evidence.

## Evaluate current todolist inputs

Use this mode to retain generated files in the current checkout. Require a clean
checkout, or select uncommitted inputs explicitly with `--allow-dirty`.
`apps/todolist` and `.agentic-workflow/evals/todolist` must be absent. Supervisor settings follow
[model routing](../agentic-workflow/policies/MODELS.md#routing-source).

Pause concurrent workflow work so new execution records belong to this trial:

```sh
python3 evals/todolist.py run
```

Inspect `.agentic-workflow/evals/todolist/result.json`; the app, logs and new execution records
remain in the checkout. Overall `PASS` requires passing agent,
[CLI contract](../specs/todolist/tasks/02_cli.md#cli-contract) and artifact-presence
grades. Artifact presence does not establish trace quality or workflow compliance.
`--agent-timeout` and `--command-timeout` override the 1,800-second and 60-second
limits. Inspect results before requesting cleanup.

## Clean a completed current-checkout eval

Only after cleanup is requested and the trial stops, preserve needed evidence and
run:

```sh
python3 evals/todolist.py clean
```

Uses the checkout's eval marker and completed records inventory to remove the app,
that trial's records and `.agentic-workflow/evals/todolist`. Existing records and unrelated changes
remain; handle refused paths or other reported changes manually.

## Check eval runners

After eval tooling changes, run fixture checks with Python 3.10+ and Git on POSIX:

```sh
python3 -m unittest discover -s evals/tests -v
```

These make no model calls; use a real eval to validate generation or judge quality.
