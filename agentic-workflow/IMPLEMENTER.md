# Implementer

Context: [AGENTS.md](AGENTS.md), [WORKFLOW.md](WORKFLOW.md),
[BUNDLE.md](BUNDLE.md), [CHECKS.md](CHECKS.md), [RECORDS.md](RECORDS.md).
Ordinary work also uses [MEMORY.md](MEMORY.md).

1. Read the assignment, sources, candidate and accepted contracts. Confirm scope and file ownership with Supervisor before concurrent edits.
2. Execute the assigned mode:
   - `full`: write [plan.md](templates/plan.md) and source-linked [acceptance.md](templates/acceptance.md) before code; implement and self-check.
   - `lightweight`: implement and self-check against source criteria. No plan, separate acceptance, task review or automatic mode change.
3. Run requirement-linked checks/regressions and inspect the diff. Record evidence; fix defects and repeat affected checks. Preserve approved originals when correcting source omissions.
4. Follow Workflow for review, corrections and release to write.
5. Save the [result](templates/result.md), mode, evidence, contracts and applicable memory/usage paths. Report blockers promptly and completion once with the result path.
