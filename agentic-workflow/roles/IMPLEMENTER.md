# Implementer

## Execute a task

- Context:
  - Read [AGENTS.md](../AGENTS.md), [Bundle](../policies/BUNDLE.md), [Checks](../policies/CHECKS.md) and [Records](../policies/RECORDS.md).
  - Apply [Document style](../policies/DOCUMENT_STYLE.md) when writing documents.
  - Ordinary work also uses [Memory](../policies/MEMORY.md).
- Inputs: assignment, sources, candidate, accepted contracts and mode.
- Effects:
  - Read inputs.
  - Agree on scope and file ownership with Supervisor before concurrent edits.
  - Follow the assigned mode below.
  - Check requirements and regressions.
  - Inspect the diff.
  - Record check evidence.
  - Include mock justifications under Checks.
  - Fix defects.
  - Rerun affected checks.
  - Preserve approved originals when fixing source omissions.
  - Full: complete review below.
  - Lightweight: write the task result.
  - Save the [result](../templates/result.md), mode, evidence and contracts.
  - Include applicable memory/usage paths.
  - Report blockers promptly.
  - Report completion once with the result path.
- Outputs: candidate, evidence, task result and required documents.
- Next:
  - Return result to Supervisor for acceptance.
  - Keep this context for corrections.
  - Repeat affected task steps.

## Full mode

Apply when assigned `full` mode.

- Write [plan.md](../templates/plan.md) before code.
- Write [acceptance.md](../templates/acceptance.md) before code.
- Link acceptance to sources.
- Include public API contracts under Checks.
- Include expected test scenarios under Checks.
- Implement the task.
- Run checks.
- Spawn fresh Reviewer using the procedure below.

## Lightweight mode

Apply when assigned `lightweight` mode.

- Implement against source criteria.
- Run checks against source criteria.
- Skip plan, separate acceptance and task review.
- Keep the assigned mode.

## Review a full-mode task

- Context: apply [Checks](../policies/CHECKS.md) and [Reviewer](REVIEWER.md).
- Inputs: checked candidate, requirements, acceptance, factual evidence and agreed review boundary.
- Effects:
  - Agree on review boundary with Supervisor.
  - Wait for confirmation that affected writers are paused.
  - Spawn fresh Reviewer with permitted inputs.
  - Pass mock justifications with check evidence.
  - Report review completion to Supervisor.
  - Wait for explicit release before writing.
  - Fix actionable findings.
  - Rerun affected checks.
  - Repeat with fresh Reviewer.
  - Keep task ownership through corrections.
- Outputs: review result, findings, corrections, recheck evidence or blockers.
- Next:
  - After review passes, return task result to Supervisor.
  - Report blockers promptly.
