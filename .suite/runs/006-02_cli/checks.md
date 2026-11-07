# CLI check evidence

Candidate: current files under apps/todolist. CLI scope: todolist/cli.py,
todolist/__main__.py, README.md, tests/test_cli.py. Accepted business code,
manifest, lockfile and business tests were not changed in this task.

Sources: specs/todolist/project.md, task_order.md, tasks/02_cli.md,
verification.md. Acceptance: .suite/tasks/006-02_cli/acceptance.md.
Accepted dependency contract and evidence:
.suite/runs/005-01_business_logic/checks.md and review.md. No prior findings.

## Commands and outcomes

- `uv sync` in apps/todolist: PASS, exit 0, one package resolved and environment checked.
- `uv run python -m unittest discover -s tests -v` in apps/todolist: PASS,
  exit 0, eight tests (four CLI and four unchanged business tests), 0.730s.
- `uv run python -m todolist --help` in apps/todolist: PASS, exit 0;
  usage lists add/list/complete/delete/help and describes each command.
- `git diff --check -- apps/todolist` from repository root: PASS, exit 0.
- Candidate code and change-scope inspection: PASS; argparse delegates to
  TaskStore, standard library only, business files unchanged, README documents
  setup, commands, storage location and single-user/ID-reuse behavior.

## Requirement coverage

CLI1–CLI4: test_lifecycle_across_processes starts a fresh Python module process
for every command, verifies empty state, two adds with multiword titles,
pending/completed status and IDs, selected completion/deletion, persistent JSON,
and final empty state. It copies the actual package into a temporary application
directory, runs from another directory, and verifies no cwd storage file. These
tests own command transport and process lifecycle, not detailed business schema.

CLI5: test_help_and_no_command checks help, --help and no arguments show usage
and every command without touching storage. Error table exercises missing
arguments, invalid integer and positive-ID parsing, unknown commands, blank
titles and unknown IDs: stderr, nonzero exit, no traceback or mutation.
test_storage_errors_are_concise_failures checks malformed JSON and a real
filesystem error (directory at tasks.json) are concise nonzero failures; corrupt
bytes remain unchanged. Business tests retain detailed schema/error coverage.

SH1–SH2: uv sync, uv module execution and all tests pass; manual source/README
inspection supports location, simplicity and command documentation.

E2E1: subprocess integration covers assembled behavior in an isolated temporary
copy. Supervisor must still run the separate final actual application scenario
and record assembled.md; that final execution is NOT_RUN by this implementer.

## Test audit and limits

Applied test-audit: four tests own CLI transport, process persistence, discovery,
and error translation. Real subprocesses/files, literal observable expected
states, no mocks or production testing flags/hooks. Detailed store semantics stay
owned by accepted store tests. Referenced boundary guide unavailable (inherited
disclosed skill-reference limitation); main skill used. This is new capability
coverage, not a claimed pre-fix bug reproduction. No required external service.

Usage: implementer `/root/cli`, supervisor `/root`; platform session/turn IDs,
log paths, token and tool counters unavailable. No totals inferred.
