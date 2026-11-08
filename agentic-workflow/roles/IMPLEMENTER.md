# Implementer

## Execute a task

- Context: read [AGENTS.md](../AGENTS.md), [Bundle](../policies/BUNDLE.md), [Checks](../policies/CHECKS.md) and [Records](../policies/RECORDS.md). Apply [Document style](../policies/DOCUMENT_STYLE.md) when writing documents. Ordinary work also uses [Memory](../policies/MEMORY.md).
- Inputs: assignment, sources, candidate, accepted contracts and mode.
- Effects:
  1. Read inputs. Agree on scope and file ownership with Supervisor before concurrent edits.
  2. Follow the assigned mode below.
  3. Check requirements and regressions. Inspect the diff and record evidence. Fix defects and rerun affected checks. Preserve approved originals when fixing source omissions.
  4. Full: complete review below. Lightweight: write the task result.
  5. Save the [result](../templates/result.md), mode, evidence and contracts. Include applicable memory/usage paths. Report blockers promptly. Report completion once with the result path.
- Outputs: candidate, evidence, task result and required documents.
- Next: return result to Supervisor for acceptance. Keep this context for corrections. Repeat affected task steps.

| Mode | Local procedure |
|---|---|
| `full` | Write [plan.md](../templates/plan.md) and [acceptance.md](../templates/acceptance.md) before code. Link acceptance to sources. Include public API contracts and expected test scenarios under Checks. Implement and run checks. Spawn fresh Reviewer as described below. |
| `lightweight` | Implement and run checks against source criteria. No plan, separate acceptance, task review or automatic mode change. |

## Review a full-mode task

- Context: apply [Checks](../policies/CHECKS.md) and [Reviewer](REVIEWER.md).
- Inputs: checked candidate, requirements, acceptance, factual evidence and agreed review boundary.
- Effects:
  1. Agree on review boundary with Supervisor. Wait for confirmation that affected writers are paused.
  2. Spawn fresh Reviewer with permitted inputs.
  3. Report review completion to Supervisor. Wait for explicit release before writing.
  4. Fix actionable findings and rerun affected checks. Repeat with fresh Reviewer. Keep task ownership through corrections.
- Outputs: review result, findings, corrections, recheck evidence or blockers.
- Next: after review passes, return task result to Supervisor. Report blockers promptly.
