# Final independent validation: PASS

Scope: assembled `apps/todolist`, both scheduled tasks and acceptances. Sources read directly: `specs/todolist/{project,task_order,verification}.md`, `specs/todolist/tasks/{01_business_logic,02_cli}.md`, `.suite/003_todolist/tasks/{01_business_logic,02_cli}/acceptance.md`, and repository `guidelines.md`. Allowed implementation results read from `runs/01_business_logic/business/result.md` and `runs/02_cli/cli/result.md`. Both lightweight tasks accepted; optional reviews omitted, not claimed PASS. Plans, conversations and project memory excluded.

Candidate: `apps/todolist` untracked working-tree files at repository HEAD `867440e0c8272d59b02ad8e9b81d29eabf590b04`; read all production modules, tests, README, pyproject and uv lock directly. No candidate code changed. Unrelated staged root/suite/research work preserved.

Model routing: Validator default careful profile; requested `gpt-6.1-sol`, high reasoning. Existing host session offers no setting control; observed model/reasoning unavailable, host defaults retained.

## Requirement-linked checks

| Coverage | Independent method, working directory and outcome |
| --- | --- |
| B1–B4, B5 restart persistence; C1–C5/C7 | `uv run python -m unittest discover -s tests -v`, cwd `apps/todolist`, exit 0: all five public-service and real-subprocess tests PASS. |
| B5, B7, C1–C4/C7; shared final lifecycle | `uv run python -` validation script, cwd `apps/todolist`, exit 0. Invoked actual absolute `cli.py` from a temporary external working directory in separate processes: empty list, two additions, list, complete twice, completed list, delete one while retaining the other, delete final task and empty list. Explicit JSON assertions verified IDs, titles and completion at actual `apps/todolist/tasks.json`. |
| Chosen error contracts, C5 | Suite checks help, absent/malformed arguments, unknown IDs and blank titles; actual-app script also checked blank-title/unknown-ID exits 2 with useful errors and unchanged bytes, then malformed JSON failed without overwrite. Help describes all five commands. |
| B6, C6/C8, guidelines | Direct inspection: uv + pyproject with no external dependencies; pure state transformations, immutable Task values, explicit JSON service boundary, CLI delegation. README invocations match actual CLI. No material guideline exceptions. |
| Candidate whitespace | `git diff --check -- apps/todolist specs/todolist .suite/003_todolist`, cwd repository root, exit 0. New untracked files were inspected directly. |

Execution output: [checks.txt](checks.txt). Actual-storage cleanup PASS: storage originally absent; temporary `tasks.json` removed in `finally`. No smoke data remains.

Test-audit skill applied read-only: public business/storage contracts retain ownership of domain details; CLI tests cover transport/process lifecycle and real default storage at disposable copied app roots. No mocks supplying asserted behavior, test-only production seams, or implementation-coupled assertions found. The linked optional guide `/home/vv/docs/help/testing/writing-tests.md` is unavailable; local skill gates and audit checklist were applied.

## Findings and coverage

Zero unresolved actionable findings; no repair specification or task-order change required. Required assembled scenarios and acceptance coverage are sufficient. No external dependency or manual UI is required. Concurrency and filesystem-failure guarantees are neither specified nor claimed; finite checks do not prove them.

Records helper `resolve .suite/003_todolist validation` reported reserved task absent (exit 2); `validation` has no ordinary task document. This is record-tool behavior, not an app failure; assigned SUITE attribution and this evidence use the required reserved validation role/path.

Fresh final validation complete: PASS. Usage counters unavailable in this session; supervisor aggregate usage report pending.

