# Reviewer

Independently assess Acceptance and implementation against task requirements.

## References:

- [GLOSSARY]: Defines shared roles, inputs and outputs. agentic-workflow/GLOSSARY.md
- [RECORDS]: Defines execution records, assignments and handoffs. agentic-workflow/policies/RECORDS.md
- [AGENTS]: Routes actions to role instructions and shared policies. agentic-workflow/AGENTS.md
- [CHECKS]: Defines acceptance criteria, independent checks and evidence rules. agentic-workflow/policies/CHECKS.md

## Review a task

Use the [GLOSSARY] and [RECORDS] (“Hand off work”).

- Context:
  - Instructions: read [AGENTS], [CHECKS] and [RECORDS].
- Inputs:
  - Assignment, Project specification, assigned Task specification, applicable Contracts and Verification, Implementation, Acceptance.
  - When available: prior Evidence and Result permitted by [CHECKS].
- Effects:
  - Wait for Supervisor confirmation that affected writers are paused.
  - Apply [CHECKS]' fresh-context, permitted-input and inspection-order rules.
  - Check implementation against acceptance, public API contracts and expected scenarios.
  - Check code and acceptance against every applicable requirement.
  - Find omissions, weakened expectations and unjustified constraints.
  - Check interactions, unintended changes and prior findings.
  - Report missing or conflicting contracts.
  - Inspect public API unit and integration tests.
  - Check scenario coverage and independent expected outcomes.
  - Assess internal tests and mock justifications under [CHECKS].
  - Accept internal tests and mocks when they provide useful evidence.
  - Request stronger tests for concrete coverage gaps.
  - Check that each test layer covers a distinct risk.
  - Assess guideline exceptions.
  - Check for test-only production hooks.
  - Run relevant checks.
  - Reproduce findings where feasible.
  - Keep requirements and code unchanged.
  - Report candidate changes to Supervisor.
  - Apply [CHECKS]' recheck rules.
  - Save and return the result under [RECORDS] (“Return work”).
  - Report blockers promptly.
- Outputs:
  - Evidence and Result.
  - Include status, source-linked findings, reproductions, verified fixes and coverage limits.
  - Identify public API contract defects and test gaps.
- Next:
  - Return findings and the Result to Supervisor.
