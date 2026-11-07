# Acceptance — 02_cli
Baseline: e63405b4205b0f965879f37e739e3a161ab7f47a. Authority: user “Implement specs/todolist”, derived handoff under contract §1.
Sources: specs/todolist/tasks/02_cli.md command list; project.md output and uv constraints; task_order.md; verification.md. Digests: approval.json/frozen-v1.json.
Prerequisite: 01_business_logic ACCEPTED at dd770c472c384f4747c8f6056496c91212200199a6253e2426b3ca7c9ea6b85e; evidence .suite/runs/001-01_business_logic/business-accepted.json. Ordered dependency gate PASS before planning.

| ID | Source clause and observable criterion | Check |
|---|---|---|
| CLI-ADD | “add tasks”: `todo add TITLE` creates via accepted business layer; quoted multiword/Unicode titles supported | cli.py routing/display |
| CLI-DELETE | “delete tasks”: `todo delete ID` removes task by numeric ID | cli.py routing/display |
| CLI-COMPLETE | “complete tasks”: `todo complete ID` completes task | cli.py routing/display |
| CLI-LIST | “list tasks”: `todo list` displays IDs, titles and [ ]/[x] state; empty output says “No tasks” | cli.py routing/display |
| CLI-HELP | “help”: `todo help`, `todo --help`, no arguments show available commands and exit 0 without storage writes | cli.py help |
| CLI-ERROR | User-facing CLI: bad syntax, empty title, unknown ID, corrupted/unreadable storage produce useful stderr and nonzero exit without traceback or data loss | cli.py errors |
| CLI-UV | project.md uv + pyproject.toml at apps/todolist: `uv run --project apps/todolist todo ...` installs and runs console entry point | uv sync/task invocation; reviewer source inspection |

Public command defaults are derived simple choices; do not add flags/features beyond needed help. Accepted business source and API stay unchanged. Packaging/README changes are shared integration paths; business checks rerun as declared regression to confirm real dependency integration. Task checks: checks/task-v1.json, regression: checks/regression-v1.json. Final shared scenarios stay .suite/runs/001-01_business_logic/checks/final.json, executed separately by supervisor after task acceptance. All subprocess assertions must pass. Disposable copied app uses real editable install and default storage, cleans itself; no live data touched. Manual reviewer checks readability of help/list/errors and simplicity plus packaging. No user-only manual checks. No memory inputs. No unresolved decisions. Approval: approval.json; frozen identities: frozen-v1.json.
