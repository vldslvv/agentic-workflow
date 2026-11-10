# Validator

Validate the assembled application and publish repair tasks for failures.

## References:

- [GLOSSARY]: Defines shared roles, inputs and outputs. agentic-workflow/GLOSSARY.md
- [RECORDS]: Defines execution records, assignments and handoffs. agentic-workflow/policies/RECORDS.md
- [AGENTS]: Routes actions to role instructions and shared policies. agentic-workflow/AGENTS.md
- [CHECKS]: Defines acceptance criteria, independent checks and evidence rules. agentic-workflow/policies/CHECKS.md
- [BUNDLE]: Defines specification files, task selection and path resolution. agentic-workflow/policies/BUNDLE.md

## Validate the app

Use the [GLOSSARY] and [RECORDS] (“Hand off work”).

- Context:
  - Instructions: read [AGENTS], [CHECKS], [BUNDLE] and [RECORDS].
- Inputs:
  - Assignment, Project specification, selected Task specifications, Task order, applicable Contracts, Verification, Implementation, Results and Evidence.
  - Plan-review tasks: Acceptance.
- Effects:
  - Wait for Supervisor confirmation that affected writers are paused.
  - Use source criteria for direct tasks.
  - Apply [CHECKS]' fresh-context, permitted-input and inspection-order rules.
  - Independently check final scenarios, task interactions and real dependencies.
  - Run required manual checks.
  - Reproduce gaps where feasible.
  - Keep the candidate unchanged.
  - Save status, source-linked findings, coverage and guideline exceptions under `runs/validation/<agent-run-id>/`.
  - Distinguish plan/acceptance defects from implementation failures.
  - Identify missing capabilities and unresolved requirements.
  - For implementation failures, publish one repair per failed pass below.
  - Report blockers promptly.
  - Return work under [RECORDS] (“Return work”).
- Outputs:
  - Evidence and Result.
  - After implementation failure: repair Task specification and updated Task order.
- Next:
  - Return result to Supervisor.
  - Supervisor releases writers.
  - Supervisor routes the validation result.

## Publish repair

- Context: apply [BUNDLE] and [RECORDS].
- Inputs: Assignment, failed validation Result and Evidence, Project specification, selected Task specifications, Task order, applicable Contracts and Verification.
- Effects:
  - Check bundle files and table rows before reserving a repair path.
  - Reserve the next unused `tasks/repair-NNN.md`.
  - Include all actionable findings and sources.
  - Describe expected/observed behavior, reproductions, scope and rechecks.
  - Depend on every validated task, including earlier repairs.
  - Include other required prerequisites.
  - Save result, reserved path and dependencies before publication.
  - Then write the repair and its `task_order.md` row.
  - Preserve existing specs and code.
  - On resume, complete only missing publication parts.
  - Recover dependencies from validated scope.
  - Block on ambiguity or conflicting files/rows.
  - Use a new number for each later failed pass.
- Outputs: repair Task specification, updated Task order and Result recording publication or blockers.
