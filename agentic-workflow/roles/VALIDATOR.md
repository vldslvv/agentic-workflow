# Validator

Validate the assembled application and publish repair tasks for failures.

## References:

- [VALIDATION_INPUT]: Defines ValidationInput fields. agentic-workflow/contracts/VALIDATION_INPUT.md
- [WORK_RESULT]: Defines WorkResult fields. agentic-workflow/contracts/WORK_RESULT.md
- [GLOSSARY]: Defines shared roles, inputs and outputs. agentic-workflow/GLOSSARY.md
- [RECORDS]: Defines execution records, assignments and handoffs. agentic-workflow/policies/RECORDS.md
- [AGENTS]: Routes actions to role instructions and shared policies. agentic-workflow/AGENTS.md
- [CHECKS]: Defines acceptance criteria, independent checks and evidence rules. agentic-workflow/policies/CHECKS.md
- [BUNDLE]: Defines specification files, task selection and path resolution. agentic-workflow/policies/BUNDLE.md

## Contracts

- Provides: `validate_app(input: ValidationInput) -> WorkResult` using [VALIDATION_INPUT] and [WORK_RESULT].

Repair publication and its recovery remain part of this interface.

## Validate the app

- Context:
  - Instructions: read [AGENTS], [CHECKS], [BUNDLE] and [RECORDS].
- Inputs: [VALIDATION_INPUT].
- Effects:
  - Wait for Supervisor confirmation that affected writers are paused.
  - Use source criteria for direct tasks.
  - Apply [CHECKS] (“Independent checks”) throughout validation.
  - Independently check final scenarios, task interactions and real dependencies.
  - Run required manual checks under [CHECKS] (“Prepare checks”).
  - Distinguish plan/acceptance defects from implementation failures.
  - Report missing capabilities, unresolved requirements and other blockers promptly.
  - For implementation failures, publish one repair per failed pass below.
  - Return work under [RECORDS] (“Return work”).
- Outputs: [WORK_RESULT].
- Next: return the Result to Supervisor.

## Publish repair

- Context: apply [BUNDLE] and [RECORDS].
- Inputs: [VALIDATION_INPUT].
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
- Outputs: [WORK_RESULT].
