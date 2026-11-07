# Allocation lock file removal acceptance

Authority: the user requested removal of `.allocation.lock`; existing allocation behavior is retained. Applicable guidelines: `/home/vv/ccode/generate-prototype/guidelines.md`. Target: records helper, its relevant tests and allocation documentation. Records: `.suite/002_token_efficiency/runs/remove_allocation_lock/<run>/`.

- Allocating a run does not create or use `.allocation.lock`; the obsolete repository file is removed.
- Existing OS coordination uses the suite directory itself, with no new lock files, reservation files or locking service.
- Concurrent allocations with different names retain distinct sequential numbers, existing folders are preserved, and task resolution still works. Verify through real disposable CLI processes.
- Per-implementation locking, native capture and report collection remain correct; run the relevant existing regressions if the shared helper changes.
- Documentation accurately describes the directory-based coordination. Package checks pass; prior staged cleanup and unrelated files remain intact.
- A fresh independent reviewer checks the changed candidate and relevant behavior. Finish only with successful required checks and no actionable findings. The final explanation explicitly states that the extra file was removed while OS coordination remains.
