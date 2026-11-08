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

## Review specification bundles

Review current bundle files, including uncommitted changes, against the current
[bundle templates and policies](../agentic-workflow/policies/BUNDLE.md):

```sh
make eval-specs
make eval-specs SPEC_BUNDLE=specs/todolist
```

The default scope is every bundle directory directly under `specs/`. Each run
uses one fresh, read-only model invocation and reports findings and suggested
corrections without repairs. The snapshot preserves relative paths for selected
bundles, templates, applicable policies and linked repository source documents,
including interface definitions. Application outputs, project memory and execution
history are excluded; unavailable and excluded references are recorded explicitly.
Unavailable required references prevent a clean pass. Invalid or empty selections
return a runner error without invoking the model.

Inspect `.agentic-workflow/evals/specs/review-*/` for the input snapshot, prompt,
schema, settings, model output, Markdown report and final `result.json`.
Each finding must cite the template or policy clause, affected spec location and
suggested correction. `FAIL` takes precedence over `UNCLEAR`, then `PASS`.
Exit codes are `0` for `PASS`, `1` for findings or uncertainty, `2` for runner
errors, `124` for timeout and `128 + signal` for interruption.

| Setting | Default |
|---|---|
| `SPECS_MODEL` | `gpt-6-astra` |
| `SPECS_REASONING` | `medium` |
| `SPECS_TIMEOUT` | 1,800 seconds |

Equivalent CLI options are available directly:

```sh
python3 -B evals/specs.py --bundle specs/todolist --model gpt-6-astra --reasoning medium --timeout 1800
```

Fixture checks establish runner behavior; use a separate live eval to judge
specification quality. Workflow review retains its automatic repair behavior.

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
[CLI contract](../specs/todolist/contracts/cli.md) and artifact-presence
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
