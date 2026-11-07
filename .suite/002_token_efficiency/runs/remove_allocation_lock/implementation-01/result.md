# Allocation lock removal implementation

Implementation checks: PASS. Candidate ready for required fresh independent review; task acceptance remains pending that review. Scope: [acceptance](../../../tasks/remove_allocation_lock/acceptance.md), repository `/home/vv/ccode/generate-prototype`, unstaged incremental changes against the preserved staged cleanup.

The extra `.suite/.allocation.lock` file was removed. Existing OS coordination remains: allocation applies `flock` to the suite directory; native capture and report refresh retain their per-implementation `.records.lock`. The shared helper closes either descriptor on normal completion or exceptions. No replacement files, reservation scheme or additional locking layer were added.

Incremental candidate paths:

- `spec-source-suite/helpers/records.py`: lock existing directories as well as record lock files; allocate using the suite directory.
- `spec-source-suite/AGENTS.md` and `spec-source-suite/helpers/TRACING.md`: describe directory coordination.
- `spec-source-suite/tests/test_usage_report.py`: extend the existing real concurrent CLI allocation regression to assert absence of `.allocation.lock`.
- `.suite/.allocation.lock`: removed local obsolete artifact.

Mode: full maintenance follow-up, with supervisor-supplied plan/acceptance and supervisor-owned fresh review. The change is small, but concurrent allocation and the shared capture/report locking boundary require compatibility checks. Guidelines: `/home/vv/ccode/generate-prototype/guidelines.md`; no material exceptions. Routing: careful, requested `gpt-6.1-sol` / `high` for those interactions. Observed host settings are unavailable.

All commands ran from the repository root:

| Check | Outcome |
| --- | --- |
| `python -m unittest discover -s spec-source-suite/tests -p test_usage_report.py -k concurrent_allocations` before the repair | Expected FAIL: the added public filesystem assertion found `.allocation.lock`. |
| `python -m unittest discover -s spec-source-suite/tests -p test_usage_report.py` after repair | PASS: 21 tests run, 20 passed, one optional Perfetto parser check skipped. Includes eight real CLI allocations with different names, unique consecutive numbers, retained roots, scoped task resolution, and absence of the extra lock file. |
| `python -m unittest discover -s spec-source-suite/tests -p test_native_collection.py` | PASS: seven tests, including capture/resume and simultaneous CLI report refresh preserving reports/native bytes. |
| `python spec-source-suite/helpers/check_package.py` | PASS, 50 local links checked. |
| `git diff --check`; inspect incremental `git diff`; compare `git diff --cached --stat`; `test ! -e .suite/.allocation.lock` | PASS. Four incremental tracked paths, 10 insertions/5 deletions; staged cleanup preserved. Unrelated files left untouched. |

Coverage: disposable real local POSIX processes and native indexes exercise the retained filesystem contract. No distributed-filesystem claim. Optional real Perfetto parser unavailable; unrelated to the changed coordination. No unresolved implementation finding. Fresh independent review: NOT_RUN here, assigned to the supervisor's next worker. No usage refresh performed for this follow-up.
