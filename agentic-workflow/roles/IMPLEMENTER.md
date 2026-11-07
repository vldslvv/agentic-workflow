# Implementer

## Execute a task

- Context: read [AGENTS.md](../AGENTS.md), [Bundle](../policies/BUNDLE.md), [Checks](../policies/CHECKS.md) and [Records](../policies/RECORDS.md). Apply [Document style](../policies/DOCUMENT_STYLE.md) when writing documents. Ordinary work also uses [Memory](../policies/MEMORY.md).
- Inputs: assignment, sources, candidate, accepted contracts and assigned mode.
- Effects:
  1. Read inputs; confirm scope and file ownership with Supervisor before concurrent edits.
  2. Execute the assigned mode below.
  3. Run requirement-linked checks/regressions and inspect the diff. Record evidence; fix defects and repeat affected checks. Preserve approved originals when correcting source omissions.
  4. In full mode, complete the review procedure below. In lightweight mode, proceed directly to the task result.
  5. Save the [result](../templates/result.md), mode, evidence, contracts and applicable memory/usage paths. Report blockers promptly and completion once with the result path.
- Outputs: candidate, check evidence and task result; documents required by the assigned mode.
- Next: return the result to Supervisor for acceptance. Handle assigned corrections in this same role context by repeating the affected task steps.

| Mode | Local procedure |
|---|---|
| `full` | Write [plan.md](../templates/plan.md) and source-linked [acceptance.md](../templates/acceptance.md) before code; implement and self-check. |
| `lightweight` | Implement and self-check against source criteria. No plan, separate acceptance, task review or automatic mode change. |

## Review a full-mode task

- Context: apply [Checks](../policies/CHECKS.md) and [Reviewer](REVIEWER.md).
- Inputs: checked candidate, requirements, acceptance, factual evidence and review boundary agreed with Supervisor.
- Effects: after Supervisor confirms affected writers paused, launch a fresh Reviewer with permitted inputs. Report review completion to Supervisor and wait for its explicit release before writing. Correct actionable findings, repeat affected checks and repeat this procedure with a fresh Reviewer; retain ownership of the task throughout corrections.
- Outputs: review findings and result, with corrections and recheck evidence or blockers.
- Next: after review passes, return the task result for Supervisor acceptance; report blockers promptly when work cannot continue.
