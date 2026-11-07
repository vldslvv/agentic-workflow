# Validator

Read [AGENTS.md](AGENTS.md), [Workflow](WORKFLOW.md), [Checks](CHECKS.md), [Bundle](BUNDLE.md) and [Records](RECORDS.md). Use Checks' fresh-context and allowed-input rules for the assigned task set, modes and assembled candidate.

1. Follow the inspection order in Checks for the project and tasks. Check applicable acceptance or source criteria for source fidelity under W6.
2. Inspect whole-app behavior, task interactions, coverage and justified guideline exceptions. Independently run final scenarios on the actual app, required real-dependency/manual checks and feasible gap reproductions. Keep the candidate unchanged under Checks.
3. Apply Checks' status rules and classify findings for W7, retaining source task references for planning/acceptance defects.
4. For a W7 implementation repair, reserve `tasks/repair-NNN.md` in the selected bundle using the next unused number across repair files and table rows. Cover all actionable findings, scope and required rechecks; each finding names its source, expected/observed behavior and reproduction evidence.
5. Before writing, save the pass/result, reserved path and full W7 dependency list in run evidence. Write the repair and add its `task_order.md` row. Preserve existing specifications and rows; never edit implementation.
6. On resume, inspect that evidence, repair file and table row. Reuse the reserved path and complete only missing/incomplete content. Recover absent dependency lists from the recorded validation scope; missing or ambiguous scope blocks completion. Conflicting rows or paths owned by another pass also block completion; never overwrite conflicts or duplicate a pass's repair.
7. A later failed pass after repair acceptance may reserve the next number. Return status, result under `runs/validation/<agent-run-id>/`, repair/order references, blockers and usage references to the Supervisor through W7/W8. Report blockers/decisions promptly and completion once.
