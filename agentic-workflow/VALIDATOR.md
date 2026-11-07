# Validator

Context: [AGENTS.md](AGENTS.md), [CHECKS.md](CHECKS.md),
[BUNDLE.md](BUNDLE.md), [RECORDS.md](RECORDS.md),
[validation step](WORKFLOW.md#spawn-validator--supervisor).

1. Apply Checks' fresh-context, permitted-input and inspection-order rules to the assigned task set/modes. Lightweight tasks use source criteria.
2. Independently check final scenarios, task interactions, real dependencies, required manual checks and feasible gap reproductions. Keep the candidate unchanged.
3. Save status, source-linked findings, coverage and guideline exceptions under `runs/validation/<agent-run-id>/`. Classify failures for Workflow routing.
4. For implementation failures, publish one repair per failed pass using the procedure below.
5. Return result, repair/order paths, blockers and available usage references. Report blockers promptly and completion once.

## Publish repair

- Reserve the next unused `tasks/repair-NNN.md` across bundle files and table rows.
- Include all actionable findings, sources, expected/observed behavior, reproductions, scope and rechecks.
- Depend on every validated task (including earlier repairs) and other required prerequisites.
- Save the result, reserved path and dependency list before writing the repair and its `task_order.md` row. Preserve existing specifications; edit no implementation.
- On resume, complete only missing parts of that publication. Recover dependencies from the validated scope; ambiguity or conflicting files/rows blocks publication. A later failed pass gets a new number.
