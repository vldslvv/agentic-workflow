# CLI task acceptance

Sources: `specs/todolist/tasks/02_cli.md` (commands), `specs/todolist/project.md` (simplicity, uv/pyproject, target), `specs/todolist/verification.md` (end-to-end task lifecycle), `/home/vv/ccode/generate-prototype/guidelines.md` (explicit side effects and public-interface verification). Accepted dependency: `.suite/003_todolist/runs/01_business_logic/business/result.md`.

| ID | Requirement and pass rule | Check |
|---|---|---|
| C1 | Add a task through the CLI and display its ID/title; later invocation lists it | Subprocess lifecycle test and app-root smoke |
| C2 | Delete by task ID; later list omits it | Subprocess lifecycle and smoke |
| C3 | Complete by task ID; later list visibly marks completion | Subprocess lifecycle and smoke |
| C4 | List shows active tasks with IDs, title, completion; empty list is intelligible | Subprocess lifecycle |
| C5 | Help explains all five commands; malformed input gives nonzero exit and useful usage/error | Subprocess help/error checks; inspect help text |
| C6 | App is in apps/todolist, uses uv/pyproject and keeps implementation simple | uv invocation; inspect CLI, README and project config |
| C7 | Business behavior remains correct; assembled add/complete/delete sequence persists between real CLI processes | Full unittest suite and app-root smoke |
| C8 | Domain rules stay behind service, tests use public behavior and real disposable storage | Code/test inspection against guidelines |

Commands: from `apps/todolist`, `uv run python -m unittest discover -s tests -v` and documented CLI invocations. Evidence destination `.suite/003_todolist/runs/02_cli/cli/result.md`. CLI process tests copy production modules to temporary app roots to exercise the real default storage path without touching user data; smoke uses actual target path and restores prior contents. No external service/manual UI is required. Final independent validation is a separate project gate.
