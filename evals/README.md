# Local evaluations

## Review and repair workflow documents

- Context: use [Workflow review](../agentic-workflow/guides/WORKFLOW_REVIEW.md) to check agreement with the fixed workflow contract.
- Inputs:
  - Current package, root entry points, model override and installed workflow wrappers, including uncommitted changes.
  - Python 3.10+ and an authenticated local Codex CLI on POSIX.
- Effects:
  1. Pause concurrent edits.
  2. Run `make eval-workflow`.
  3. Inspect `report.md`, `result.json` and any repair diff.
- Outputs:
  - Review evidence under `.evals/workflow/review-*/`, with repair evidence under `repair/`.
  - One fresh, read-only review of a snapshot.
  - One automatic repair in working Markdown files for failures without uncertainty.
  - Uncommitted repairs remain after failure or interruption.
- Next: resolve remaining findings before another requested review.

| Outcome | Meaning |
|---|---|
| `PASS` | Review passed without edits. |
| `UNCLEAR` in any review row | No repair runs, even alongside failures. |
| `FIXED` | Editor reports resolution, package checks pass and the source contract is unchanged. |
| `UNCLEAR` after repair | Findings remain unresolved; edits are retained. |
| Error or interruption | Inspect retained evidence and any partial edits. |

`FIXED` has no independent re-review and does not prove agent behavior.

| Setting | Default |
|---|---|
| `WORKFLOW_MODEL` | `gpt-6-astra` |
| `WORKFLOW_REASONING` | `medium` |
| `WORKFLOW_TIMEOUT` | 1,800 seconds per invocation or check |

```sh
make eval-workflow WORKFLOW_MODEL=gpt-6.1-sol WORKFLOW_REASONING=high WORKFLOW_TIMEOUT=900
```

These settings control both review and repair, independently of model policy files.

## Todolist end-to-end eval

- Context: use for one end-to-end generation trial from committed `HEAD`.
- Inputs: Python 3.10+, Git, uv and an authenticated local Codex CLI on POSIX.
- Effects:
  1. Run `make eval`.
  2. Inspect the saved `result.json` and `worktree.json`.
- Outputs:
  - One trial in a clean temporary worktree using committed inputs and the invoking checkout's eval tooling.
  - Agent, CLI and artifact grades under `.evals/todolist-worktrees/<unique-run>/`.
  - Archived logs, generated app and execution records before worktree removal.
- Next: recover from the reported worktree path if archiving or removal fails.

The invoking checkout stays unchanged, apart from saved eval evidence.
Uncommitted app inputs are excluded.

```sh
make eval EVAL_AGENT_TIMEOUT=1800 EVAL_COMMAND_TIMEOUT=60
```

## Evaluate current todolist inputs

- Context: use when generated files should remain in the current checkout.
- Inputs:
  - The same tools as the committed eval.
  - A clean checkout, or explicit selection of uncommitted inputs with `--allow-dirty`.
  - Absent `apps/todolist` and `.evals/todolist` paths.
  - Supervisor settings from [model routing](../agentic-workflow/policies/MODELS.md#routing-source).
- Effects:
  1. Pause concurrent workflow work so new execution records can be attributed to this trial.
  2. Run `python3 evals/todolist.py run`, adding `--allow-dirty` for uncommitted inputs.
  3. Inspect agent, CLI and artifact results in `.evals/todolist/result.json`.
- Outputs:
  - Generated app, logs and new execution records retained in the checkout.
  - Separate agent, [CLI contract](../specs/todolist/tasks/02_cli.md#cli-contract) and artifact-presence grades.
  - Overall `PASS` only when all three grades pass.
- Next: inspect results before requesting cleanup.

Artifact presence does not establish trace quality or workflow compliance.
Use `--agent-timeout` and `--command-timeout` to override the 1,800-second and 60-second limits.

## Clean a completed current-checkout eval

- Context: use only when cleanup is requested after the trial stops.
- Inputs: this checkout's eval marker and completed records inventory.
- Effects:
  1. Preserve any evidence needed later.
  2. Run `python3 evals/todolist.py clean`.
- Outputs: removal of the generated app, that trial's records and `.evals/todolist`.
- Next: handle refused paths or other reported changes manually.

Existing records and unrelated changes remain.

## Check eval runners

- Context: use after changing eval tooling.
- Inputs: Python 3.10+ and Git on POSIX.
- Effects: run `python3 -m unittest discover -s evals/tests -v`.
- Outputs: fixture-based launcher checks without model calls.
- Next: run a real eval when validating generation or judge quality.
