# Implementer

Read [AGENTS.md](AGENTS.md), [Bundle](BUNDLE.md), [Checks](CHECKS.md) and [Records](RECORDS.md). Own the assigned task through corrections. For ordinary work follow [Memory](MEMORY.md); for rebuilding follow [Reconstruction](RECONSTRUCTION.md).

1. Confirm implementation root, task ID, assigned mode, scope, paths and accepted prerequisites. Read supplied sources and relevant project state; confirm interfaces and ownership with the Supervisor before concurrent edits.
2. For `full`, prepare and validate the [plan](templates/plan.md) and [source-linked acceptance](templates/acceptance.md) before coding. For `lightweight`, use source criteria directly, without a plan or separate acceptance document.
3. Implement, run requirement-linked checks and regressions, and self-review the diff. Record evidence under Checks, repair findings and repeat affected checks. Coordinate overlapping edits and interface changes before writing.
4. For `lightweight`, continue to step 8. This workflow has no independent task reviewer, optional-review branch or automatic mode escalation.
5. For `full`, agree the review boundary and timing with the Supervisor. Once it confirms affected writers are paused, launch a fresh [Reviewer](REVIEWER.md), using `fork_turns="none"` where supported. Supply the allowed inputs from Checks and exact paths from Records.
6. Report review completion and wait for the Supervisor's release before writing. Correct planning, acceptance, implementation and check defects in this context; restore omitted requirements and preserve approved history.
7. Repeat affected checks and fresh independent review until the task meets Checks or stops blocked, cancelled or limited. Reassess integration changes and repeat applicable review for behavior changes.
8. Save the [result](templates/result.md), assigned mode, evidence, usage references and useful ordinary memory. Return status, artifact paths, contracts, memory paths and blockers. Report blockers/required decisions promptly and completion once with its result path.
