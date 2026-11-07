# Task 02 check evidence

Candidate: `/home/vv/ccode/generate-prototype/apps/todolist_rust`, unchanged during review. No Git revision: candidate app is currently untracked in the enclosing repository. Task changes: `src/main.rs` (new CLI), `tests/cli_e2e.py` (new public-process check), `README.md` (CLI documentation). Existing library, manifest, dependencies and business tests unchanged.

Sources: `specs/todolist_rust/{project.md,tasks/02_cli.md,verification.md}`; acceptance `.suite/004_todolist_rust/tasks/02_cli/acceptance.md`; engineering `/home/vv/ccode/generate-prototype/guidelines.md`.

Checks from `apps/todolist_rust`, all exit 0:
- `cargo fmt --check`
- `cargo check --offline`
- `cargo test --offline` (existing public library coverage plus doc tests)
- `cargo clippy --offline --all-targets -- -D warnings`
- `python3 tests/cli_e2e.py` (final invocation from repository root as `python3 apps/todolist_rust/tests/cli_e2e.py`; script resolves its own source root).

Rust command output is in `checks-initial.log`; final process output is in `cli-e2e.log`. Initial process run failed solely because its fixture asserted the substring `storage` for a directory at tasks.json. The existing library reports that I/O error through serde as `invalid task JSON: Is a directory`; the test now checks explanatory directory text. Initial failure preserved in `checks-initial.log`. No production change was needed.

CLI-01: simple Rust binary, standard library parser and existing TodoStore only. CLI-02–05/08: disposable project build, actual persistent JSON and process launches outside the project root cover empty→add A/B→mixed completion twice→delete B/A→empty→C, including exact description preservation and increasing IDs. CLI-06: four help forms with absent, valid and corrupt storage. CLI-07: unknown commands/options, every wrong arity, invalid numeric input including max+1, u64 maximum/zero not-found, leading-zero valid ID, non-UTF-8 command/description on POSIX, actual corrupt JSON and directory errors, unchanged storage and empty stdout on failures.

Test-audit: strongest owner is the public binary for process status/output, transport and storage-root lifecycle. Existing API tests retain domain coverage; no parallel parser unit tests or production test hooks were added. Temporary source copy/target/storage are deleted by TemporaryDirectory. Auxiliary `/home/vv/docs/help/testing/writing-tests.md` is unavailable; main skill applied. New-feature baseline failure not separately executed before coding; no prior binary existed. No guideline departures. Concurrent writers/crash durability remain outside accepted scope; task03 database work deferred.
