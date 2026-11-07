# CLI task plan

Authority: `specs/todolist/tasks/02_cli.md`, `specs/todolist/project.md`, `specs/todolist/verification.md`, ordered by `specs/todolist/task_order.md`. Guidelines: `/home/vv/ccode/generate-prototype/guidelines.md`. Implementation: `.suite/003_todolist`; target: `apps/todolist`; evidence: `.suite/003_todolist/runs/02_cli/cli/result.md`.

Prerequisite: task 01 accepted PASS by supervisor; public contract in `.suite/003_todolist/runs/01_business_logic/business/result.md` and existing `todolist.py`.

Workflow: lightweight. Five argparse commands delegate to the existing service with no new domain/storage behavior or external dependencies. Logic and interactions are simple; storage risk stays behind the accepted service. Standard profile (`gpt-6.1-sol`, medium) applies because this adds a user interface; retained host settings cannot be changed here, observed settings unavailable.

Implement `cli.py` with add TITLE, delete ID, complete ID, list, help and standard argparse help. Show IDs and completion status; present operation errors without traceback. Keep business logic in TaskService. Document `uv run python cli.py ...` and app-root storage. Add subprocess tests in disposable app copies for command dispatch/output/exit status and help/errors; retain business regression tests. Run all tests plus a real app-root CLI lifecycle with cleanup, then inspect all changed files and whitespace. No optional task review: simple interface and public-boundary checks suffice for this task; final independent assembled-app validation remains required.
