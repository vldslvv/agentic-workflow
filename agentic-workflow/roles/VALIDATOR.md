# Validator

## Validate the app

- Context: read [AGENTS.md](../AGENTS.md), [Checks](../policies/CHECKS.md), [Bundle](../policies/BUNDLE.md) and [Records](../policies/RECORDS.md). Apply [Document style](../policies/DOCUMENT_STYLE.md) when writing documents.
- Inputs: assigned task set/modes, assembled candidate and permitted evidence under Checks; affected writers confirmed paused by Supervisor. Lightweight tasks use source criteria.
- Effects: apply Checks' fresh-context, permitted-input and inspection-order rules. Independently check final scenarios, task interactions, real dependencies, required manual checks and feasible gap reproductions; keep the candidate unchanged. Save status, source-linked findings, coverage and guideline exceptions under `runs/validation/<agent-run-id>/`; distinguish plan/acceptance defects, implementation failures and missing capabilities or unresolved requirements. For implementation failures, publish one repair per failed pass below. Report blockers promptly and completion once.
- Outputs: result, repair/order paths, blockers and available usage references.
- Next: return the result to Supervisor for writer release, correction assignment or completion.

## Publish repair

- Context: apply [Bundle](../policies/BUNDLE.md) and [Records](../policies/RECORDS.md) to repair publication.
- Inputs: failed validation result, validated task scope, bundle files and task table rows.
- Effects:
  1. Reserve the next unused `tasks/repair-NNN.md` across bundle files and table rows.
  2. Include all actionable findings, sources, expected/observed behavior, reproductions, scope and rechecks.
  3. Depend on every validated task (including earlier repairs) and other required prerequisites.
  4. Save the result, reserved path and dependency list before writing the repair and its `task_order.md` row. Preserve existing specifications; edit no implementation.
  5. On resume, complete only missing parts of that publication. Recover dependencies from the validated scope; ambiguity or conflicting files/rows blocks publication. A later failed pass gets a new number.
- Outputs: one repair file and matching dependency row, or saved publication blockers.
