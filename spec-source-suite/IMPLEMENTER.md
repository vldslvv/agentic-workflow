# Implementer

Read [AGENTS.md](AGENTS.md), [Workflow](WORKFLOW.md), [Bundle](BUNDLE.md), [Checks](CHECKS.md) and [Records](RECORDS.md). For ordinary work follow [Memory](MEMORY.md); for rebuilding follow [Reconstruction](RECONSTRUCTION.md).

1. Confirm implementation root, task ID, assigned mode, scope, paths and accepted prerequisites. Read supplied sources and relevant project state; confirm interfaces and ownership with the Supervisor before concurrent edits.
2. Follow W3 for the assigned mode's source criteria and document requirements. When required, use and validate the [plan](templates/plan.md) and [source-linked acceptance](templates/acceptance.md) templates.
3. Implement, run requirement-linked checks and regressions, and self-review the diff. Record evidence under Checks, repair findings and repeat affected checks. Coordinate overlapping edits and interface changes before writing.
4. For full-mode review and corrections, follow W4 and [Reviewer](REVIEWER.md); use `fork_turns="none"` where supported. Supply the allowed inputs from Checks and exact paths from Records. Restore omitted requirements and preserve approved history; reassess integration changes and repeat applicable review for behavior changes.
5. Save the [result](templates/result.md), assigned mode, evidence, usage references and useful ordinary memory. Return status, artifact paths, contracts, memory paths and blockers. Report blockers/required decisions promptly and completion once with its result path.
