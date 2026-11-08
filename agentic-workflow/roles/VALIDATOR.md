# Validator

## Validate the app

- Context: read [AGENTS.md](../AGENTS.md), [Checks](../policies/CHECKS.md), [Bundle](../policies/BUNDLE.md) and [Records](../policies/RECORDS.md). Apply [Document style](../policies/DOCUMENT_STYLE.md) when writing documents.
- Inputs: assigned tasks/modes, assembled candidate and permitted evidence. Supervisor confirms affected writers paused. Lightweight tasks use source criteria.
- Effects:
  1. Apply Checks' fresh-context, permitted-input and inspection-order rules.
  2. Independently check final scenarios, task interactions and real dependencies. Run required manual checks. Reproduce gaps where feasible. Keep the candidate unchanged.
  3. Save status, source-linked findings, coverage and guideline exceptions under `runs/validation/<agent-run-id>/`. Distinguish plan/acceptance defects from implementation failures. Identify missing capabilities and unresolved requirements.
  4. For implementation failures, publish one repair per failed pass below.
  5. Report blockers promptly. Report completion once.
- Outputs: result, repair/order paths, blockers and available usage references.
- Next: return result to Supervisor. Supervisor releases writers, assigns corrections or finishes.

## Publish repair

- Context: apply [Bundle](../policies/BUNDLE.md) and [Records](../policies/RECORDS.md).
- Inputs: failed validation, validated scope, bundle files and task rows.
- Effects:
  1. Reserve the next unused `tasks/repair-NNN.md`. Check bundle files and table rows.
  2. Include all actionable findings and sources. Describe expected/observed behavior, reproductions, scope and rechecks.
  3. Depend on every validated task, including earlier repairs. Include other required prerequisites.
  4. Save result, reserved path and dependencies before publication. Then write the repair and its `task_order.md` row. Preserve existing specs and code.
  5. On resume, complete only missing publication parts. Recover dependencies from validated scope. Block on ambiguity or conflicting files/rows. Use a new number for each later failed pass.
- Outputs: one repair and matching dependency row, or saved blockers.
