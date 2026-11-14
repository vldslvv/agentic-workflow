# Implementation workflow

Define how tasks move through implementation, review and final validation.

## References:

- [WORKFLOW_STYLE]: Defines how to maintain the workflow contract. agentic-workflow/WORKFLOW_STYLE.md
- [GLOSSARY]: Defines shared workflow inputs and outputs. agentic-workflow/GLOSSARY.md

## Context

When editing this document, read and apply [WORKFLOW_STYLE].
Use [GLOSSARY] for shared terms.

Supervisor executes the selected scope autonomously without interactive prompts.

## Starting points

- From scratch: implement the Project specification and Task specifications following Task order.
- Existing project: dispatch new tasks against the existing Implementation.
- Revised specifications: Supervisor assesses the Implementation and dispatches affected tasks to reconcile it.

All three follow the same execution flow.

## Task execution

1. Supervisor reads Task order and resolves dependencies.
2. Supervisor assigns each task direct or plan-review mode.
3. Supervisor spawns an Implementer for each new task when its prerequisites are accepted.
4. Independent tasks execute in parallel.

Each Implementer follows its assigned mode:

- Direct: implement, check against requirements and iterate without a separate Plan, Acceptance or Reviewer.
- Plan-review: create Plan and Acceptance before implementation, implement, check, record review readiness and hand off to Supervisor for review, ending the Implementer's turn.
- Supervisor starts a fresh Reviewer to check Acceptance and Implementation against requirements.
- Supervisor resumes the same Implementer session only when review finds work to fix.
- Supervisor releases the Implementer to fix findings and hand off for fresh review.

Supervisor accepts completed tasks before unlocking their dependents.
Task corrections return to the same Implementer.
Interrupted execution resumes unfinished tasks, reusing available Implementers.

## Final validation

Once all selected tasks are accepted, Supervisor spawns a separate Validator.

- Pass: complete the selected scope.
- Implementation failure: Validator publishes a new repair Task specification and updates Task order; Supervisor dispatches a new Implementer.
- Plan or Acceptance defect: return affected work to the original Implementers.
- Blocker: report what prevents completion.

Repairs follow the same task flow.
After corrections are accepted, Supervisor repeats final validation.
