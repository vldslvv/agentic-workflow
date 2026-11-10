# Local evaluations

Run from the source repository on POSIX with Python 3.11+ and an authenticated
local Codex CLI. Todolist trials also require Git and uv.

## Layout

The root Python modules expose typed `run()` functions containing each evaluation's
orchestration. Their `main()` functions parse arguments and map results to exit
codes; supporting operations live in `support/`.

```text
evals/
├── specs.py, workflow.py    # Capture, invoke, grade and save reviews
├── todolist.py, worktree.py # Generate/grade and create/archive/clean trials
├── support/                # Typed evidence, grading, snapshots and process helpers
├── prompts/                # Model instructions
├── schemas/                # Model response contracts
└── tests/                  # Behavior tests and external-process fixtures
```

| Function | Visible flow |
|---|---|
| `specs.run()` | Capture inputs → load prompt → invoke reviewer → grade → save |
| `workflow.run()` | Capture inputs → review → optional repair and checks → save |
| `todolist.run()` | Prepare trial → prompt agent → grade CLI and artifacts → save |
| `worktree.run()` | Create checkout → call `todolist.run()` → archive → clean up |

## Choose an evaluation

| Command | Evaluated inputs | Flow |
|---|---|---|
| `make eval-specs` | Current bundles under `specs/`, including uncommitted files | Select → snapshot → review → report |
| `make eval-workflow` | Current workflow package and installed entry points | Snapshot → review → report |
| `make eval-workflow WORKFLOW_REPAIR=1` | Same workflow snapshot | Review → eligible repair → mechanical checks → report |
| `make eval` | Committed `HEAD` | Create worktree → generate todolist → grade → archive → remove worktree |
| `python3 evals/todolist.py run` | Current clean checkout, or explicit `--allow-dirty` inputs | Generate → grade → retain outputs |

Document reviews assess agreement with their reference documents. Todolist trials
assess generated CLI behavior and evidence presence. Neither establishes general
agent reliability or workflow compliance.

## Prompts and model responses

Read these files to see exactly what each model invocation is asked to do:

| Invocation | Prompt | Response contract |
|---|---|---|
| Specification review | [specs-review.md](prompts/specs-review.md) | [review.json](schemas/review.json) |
| Workflow review | [workflow-review.md](prompts/workflow-review.md) | [review.json](schemas/review.json) |
| Optional workflow repair | [workflow-repair.md](prompts/workflow-repair.md) | [repair.json](schemas/repair.json) |
| Todolist generation | [todolist-generation.md](prompts/todolist-generation.md) | Free-text final response; external graders determine success |

The runner substitutes selected bundles or repair evidence paths into the prompt,
saves the rendered text as `prompt.txt`, and passes that exact string as the final
`codex exec` argument. Document calls pass the saved schema with `--output-schema`.
Reviewers run in the captured input directory with automatic project instructions
and memories disabled. Generation runs in the trial checkout using its workflow
instructions and Supervisor model route.

## Results and evidence

Each run saves evidence under `.agentic-workflow/evals/`:

| File | Meaning |
|---|---|
| `run.json` | Launch inputs, command, requested settings and timeout |
| `prompt.txt`, `schema.json` | Exact rendered prompt and response schema, when applicable |
| `inputs/` | Document review snapshot |
| `judgment.json` | Raw document reviewer response |
| `events.jsonl`, `agent.stderr` | Model process output and diagnostics |
| `result.json` | Final evaluator result with top-level `status` |
| `report.md` | Human-readable document verdict and optional repair outcome |
| `repair/` | Separate request, raw editor response and mechanical-check evidence |
| `cli.json` | Todolist scenario results and command observations |
| `worktree.json` | Worktree archival/removal status and recovery location |

Document results separate `review` from optional `repair`; execution facts are
recorded separately from the model's assessment. Todolist results separate
`generation`, `cli`, and `artifacts`. A successful generation process only means
it exited successfully. Artifact grading checks file presence, not contents.

| Status | Meaning | Exit code |
|---|---|---|
| `PASS` | All required grades passed | 0 |
| `FIXED` | Requested repair reported resolution, mechanical checks passed, source contract unchanged | 0 |
| `FAIL`, `UNCLEAR` | Failed criteria or unresolved assessment | 1 |
| Runner/model error | Evaluation could not complete normally | 2 |
| `TIMEOUT` | Invocation exceeded its timeout | 124 |
| `INTERRUPTED` | Invocation was interrupted | 128 + signal |

`FIXED` preserves the original failed review and includes no independent re-review.
A new review is needed to assess the edited documents. Missing or invalid model
responses cannot produce a passing result. Historical reports retain their original
format; new reports use the contracts above.

## Review specification bundles

- Context: assess document validity against [bundle templates and policies](../agentic-workflow/policies/BUNDLE.md).
- Inputs: all bundles directly under `specs/`, or `SPEC_BUNDLE=specs/todolist`.
- Effects: capture current bundles, templates, applicable policies and linked local sources, then invoke one read-only reviewer.
- Outputs: findings with reference clauses, affected locations and suggested corrections under `.agentic-workflow/evals/specs/review-*/`.
- Next: inspect findings and correct the source documents separately.

Application outputs, project memory and execution history are excluded. Missing
required references prevent a clean pass; invalid or empty selections fail before
model invocation. Review precedence is `FAIL`, then `UNCLEAR`, then `PASS`.

```sh
make eval-specs SPEC_BUNDLE=specs/todolist
python3 -B evals/specs.py --bundle specs/todolist --model gpt-6-astra --reasoning medium --timeout 1800
```

## Review and repair workflow documents

- Context: assess current instructions under [Workflow review](../agentic-workflow/guides/WORKFLOW_REVIEW.md).
- Inputs: package files, root entry points, model override and installed wrappers, including uncommitted changes.
- Effects: capture inputs and run one fresh review; repair only when explicitly requested and failures contain no uncertain checks.
- Outputs: review and optional repair outcomes under `.agentic-workflow/evals/workflow/review-*/`.
- Next: inspect the report and diff, including retained partial edits after failed or interrupted repairs.

Pause concurrent edits before running. An explicit repair makes at most one editor
invocation, preserves the source contract, and runs package checks. Uncertainty
prevents repair even when other checks fail.

```sh
make eval-workflow
make eval-workflow WORKFLOW_REPAIR=1
python3 -B evals/workflow.py --repair
```

Review and repair settings are independent of model policy files:

| Setting | Default |
|---|---|
| `SPECS_MODEL`, `WORKFLOW_MODEL` | `gpt-6-astra` |
| `SPECS_REASONING`, `WORKFLOW_REASONING` | `medium` |
| `SPECS_TIMEOUT`, `WORKFLOW_TIMEOUT` | 1,800 seconds per invocation/check |

## Todolist end-to-end eval

- Context: generate and grade the [todolist specification](../specs/todolist/project.md).
- Inputs: committed `HEAD` for `make eval`, using the invoking checkout's eval tooling.
- Effects: create a clean worktree, generate the app, grade it, archive evidence, and remove the worktree.
- Outputs: app, logs and new execution records under `.agentic-workflow/evals/todolist-worktrees/<unique-run>/`.
- Next: inspect `result.json` and `worktree.json`; recover from the reported worktree path if archival or removal failed.

The invoking checkout changes only to save eval evidence. The CLI grader runs three
fresh-store scenarios: commands/persistence/help, hierarchy/subtree deletion, and
invalid parent assignments. Each command runs as a separate process under the
[CLI contract](../specs/todolist/contracts/cli.md). Original generation-time data is
preserved as evidence and restored after grading.

```sh
make eval EVAL_AGENT_TIMEOUT=1800 EVAL_COMMAND_TIMEOUT=60
```

### Evaluate current todolist inputs

Pause concurrent workflow work so new execution records belong to this trial.
Require a clean checkout, or select uncommitted inputs with `--allow-dirty`.
Both `apps/todolist` and `.agentic-workflow/evals/todolist` must be absent.
Supervisor settings follow [model routing](../agentic-workflow/policies/MODELS.md#routing-source).

```sh
python3 evals/todolist.py run
```

The app, logs and new execution records remain in the checkout. Inspect
`.agentic-workflow/evals/todolist/result.json`. Override generation and command
limits with `--agent-timeout` and `--command-timeout` (defaults: 1,800 and 60 seconds).

### Clean a completed current-checkout eval

After cleanup is requested and the trial stops, preserve needed evidence and run:

```sh
python3 evals/todolist.py clean
```

The checkout's marker and completed inventory identify the app, trial records and
results eligible for removal. Existing records and unrelated changes remain;
handle refused paths manually.

## Check eval runners

After tooling changes, run:

```sh
python3 -B -m unittest discover -s evals/tests -v
make check
make check-portability
```

Tests exercise command-line behavior with real Git and filesystem operations.
External Codex and uv fixtures avoid paid calls and launch an independent fixture
app. They prove prompt transport, grading and runner lifecycle behavior; use a
separate live eval to assess model generation or judge quality.
