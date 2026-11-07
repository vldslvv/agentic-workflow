# Allocation lock removal independent review

**PASS — no actionable candidate findings.** Reviewed the paused unstaged incremental candidate against [acceptance](../../../tasks/remove_allocation_lock/acceptance.md), using `/home/vv/ccode/generate-prototype/guidelines.md`, shared suite rules and the Reviewer routine. The candidate comprises `records.py`, shared `AGENTS.md`, `helpers/TRACING.md`, and one assertion in `tests/test_usage_report.py`; its baseline is the existing staged cleanup. Plans, memory, conversations and unrelated research were excluded. No candidate edits or commits were made.

The extra `.suite/.allocation.lock` file is absent. Allocation locks the existing suite directory with OS `flock`; no new file, reservation scheme or locking layer replaces it. The same helper still opens each implementation's `.records.lock` for capture and report collection. Descriptor closure in `finally` retains release on normal completion and exceptions. Documentation accurately distinguishes these scopes. Existing staged cleanup and unrelated files were left untouched.

All checks ran independently from `/home/vv/ccode/generate-prototype`:

| Acceptance coverage | Command / inspection | Outcome |
| --- | --- | --- |
| Concurrent numbering, preserved roots, scoped resolution, extra-file absence | `python -m unittest discover -s spec-source-suite/tests -p test_usage_report.py` | Exit 0; 21 tests, 20 passed and one optional Perfetto parser check skipped. The existing regression runs eight real concurrent CLI allocations with different names and checks consecutive unique numbers, retained roots and resolution. |
| Capture/resume, shared record locking and report refresh | `python -m unittest discover -s spec-source-suite/tests -p test_native_collection.py` | Exit 0; seven passed, including simultaneous real CLI refreshes with preserved report/native bytes. |
| Suite guidance and links | `python spec-source-suite/helpers/check_package.py` | Exit 0; PASS, 50 local links. |
| Candidate whitespace | `git diff --check -- spec-source-suite/AGENTS.md spec-source-suite/helpers/TRACING.md spec-source-suite/helpers/records.py spec-source-suite/tests/test_usage_report.py` | Exit 0. |
| Actual obsolete artifact and incremental scope | `test ! -e .suite/.allocation.lock`; inspect `git diff`, `git diff --name-status -- spec-source-suite`, `git status --short`, and staged diff statistics | Exit 0 for absence; four incremental suite paths, no new candidate files. Existing staged changes remain staged. |

The added assertion protects an explicit observable filesystem contract at the existing real CLI concurrency boundary, with independent expectations and no production test seam or duplicated test. The implementer supplied pre-fix failure evidence for this assertion; I independently executed the repaired regression. No material engineering-guideline exception was found.

**Limits:** whole-tree `git diff --check` exited 2 solely for unrelated `TODOs.txt:6: new blank line at EOF`; the scoped candidate check passes. This is outside the assigned candidate and was reported to the supervisor without editing it. Local POSIX process behavior is covered; distributed filesystems are outside the documented contract. The optional Perfetto parser is unavailable and unrelated to allocation. Auxiliary `test-audit` links to `/home/vv/docs/help/testing/writing-tests.md` and `/home/vv/.agents/skills/openclaw-testing/SKILL.md` were unavailable; the available skill's core audit rules and repository guidelines were applied. No app benchmark or assembled-app validation was required for this task.

**Routing:** careful profile, requested `gpt-6.1-sol` / `high`, appropriate to allocation concurrency and shared capture/report locking. Observed host model/reasoning settings are unavailable; no settings substitution is claimed. Usage aggregation was not refreshed; this review makes no token-total claim. Supervisor acceptance remains separate from this independent review verdict.
