# Reviewer

Independently assess Acceptance and implementation against task requirements.

## References:

- [REVIEW_INPUT]: Defines ReviewInput fields. agentic-workflow/contracts/REVIEW_INPUT.md
- [WORK_RESULT]: Defines WorkResult fields. agentic-workflow/contracts/WORK_RESULT.md
- [GLOSSARY]: Defines shared roles, inputs and outputs. agentic-workflow/GLOSSARY.md
- [RECORDS]: Defines execution records, assignments and handoffs. agentic-workflow/policies/RECORDS.md
- [AGENTS]: Routes actions to role instructions and shared policies. agentic-workflow/AGENTS.md
- [CHECKS]: Defines acceptance criteria, independent checks and evidence rules. agentic-workflow/policies/CHECKS.md
- [GUIDELINES]: Defines engineering rules for code, tests and tooling. agentic-workflow/policies/GUIDELINES.md

## Contracts

- Provides: `review_task(input: ReviewInput) -> WorkResult` using [REVIEW_INPUT] and [WORK_RESULT].

## Review a task

- Context:
  - Instructions: read [AGENTS], [CHECKS] and [RECORDS].
- Inputs: [REVIEW_INPUT].
- Effects:
  - Start in a fresh context with only [REVIEW_INPUT] and applicable Instructions under [CHECKS] (“Independent checks”) and [RECORDS] (“Independent inputs”).
  - Confirm writers_paused records Supervisor confirmation that all affected writers are paused.
  - Read original requirements and choose checks before inspecting Acceptance or implementation.
  - Inspect the supplied candidate and Acceptance paths and assess permitted factual evidence and prior findings.
  - Keep the candidate, dependencies, configuration and check inputs stable under [CHECKS] (“Independent checks”).
  - Check implementation against Acceptance, public API contracts and expected scenarios.
  - Check code and acceptance against every applicable requirement.
  - Find omissions, weakened expectations and unjustified constraints.
  - Check interactions, unintended changes and prior findings.
  - Report missing or conflicting contracts.
  - Assess Acceptance and tests under [CHECKS] (“Prepare acceptance” and “Prepare checks”).
  - Check independent expected outcomes.
  - Request stronger tests for concrete coverage gaps.
  - Assess exceptions to [GUIDELINES].
  - Report candidate changes to Supervisor.
  - Save the Result under [RECORDS] (“Return work”).
  - Report blockers promptly.
- Outputs: [WORK_RESULT].
- Next: return findings and the Result to Supervisor under [RECORDS] (“Return work”).
