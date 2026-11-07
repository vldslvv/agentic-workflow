# Business layer check evidence

Candidate: current files under apps/todolist/{pyproject.toml,uv.lock,todolist/__init__.py,todolist/store.py,tests/test_store.py,.gitignore}. Fresh business implementation; CLI and README are outside this task. Starting workspace had tracked app files deleted; these were not restored from history.

Sources: specs/todolist/project.md, specs/todolist/task_order.md, specs/todolist/tasks/01_business_logic.md, specs/todolist/verification.md. Acceptance: .suite/tasks/005-01_business_logic/acceptance.md. No prerequisites or prior review findings.

## Commands and outcomes

- `uv sync` from apps/todolist: PASS (exit 0), CPython 3.14.10, one package resolved, virtual environment and uv.lock created. No runtime dependencies.
- `uv run python -m unittest discover -s tests -v` from apps/todolist: PASS (exit 0), four tests. Persisted lifecycle establishes BL1–BL4 and real JSON persistence BL5. Separate tests cover current storage across consumers, invalid input/missing IDs without mutation, and malformed JSON/schema without mutation.
- Python default-path smoke check from /tmp with apps/todolist on sys.path: PASS (exit 0). Changed cwd to a fresh temporary directory; created via TaskStore(), confirmed apps/todolist/tasks.json exists and unrelated cwd/tasks.json does not, reloaded the task, deleted it and reloaded an empty list. Finally restored any preexisting storage bytes or removed smoke storage. Output: `PASS: default persistence uses application root from unrelated cwd`. Establishes BL5's default-path behavior independently of CLI, which remains a later task.
- `git diff --check -- apps/todolist`: PASS (exit 0). Inspected candidate files and change scope; preexisting CLI/README deletions remain pending the later task.

## API for consumers

`from todolist import TaskStore`; constructor `TaskStore(path=None)` defaults to application-root tasks.json and accepts an explicit Path/string. `create(title)` returns a task dictionary; `list()` returns task dictionaries; `complete(task_id)` returns the completed task; `delete(task_id)` returns None. Dictionaries have positive integer `id`, nonblank string `title` and boolean `completed`. Titles are stripped; new tasks start incomplete. Each operation reads current storage. IDs are allocated above the current maximum (deleted IDs may be reused). Invalid titles, invalid/unknown IDs and malformed storage raise ValueError; filesystem failures propagate as OSError. Missing storage lists empty. Mutation replaces the file atomically. No concurrency guarantees.

## Coverage judgment and limits

Public-interface tests use actual temporary files and independent expected states; no mocks or production test hooks. Lifecycle owns task semantics; multiple store instances test stale-state overwrite risk; error tables own preservation contracts. Default location has an actual-file smoke check. CLI transport and assembled lifecycle are not implemented or claimed in this task. The test-audit main skill was followed; its referenced boundary guide is unavailable. Atomic replacement is supported by direct candidate inspection of same-directory temporary output followed by os.replace; no crash/concurrency test is claimed.

Usage reference: implementer agent `/root/business`, parent `/root`. Platform session ID, turn ID, log paths and token/tool counters are unavailable; no telemetry totals are claimed.
