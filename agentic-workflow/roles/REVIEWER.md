# Reviewer

Use the [shared vocabulary](../GLOSSARY.md) and [Assignment and Result handling](../policies/RECORDS.md#hand-off-work).

## Review a task

- Context:
  - Instructions: read [AGENTS.md](../AGENTS.md), [Checks](../policies/CHECKS.md) and [Records](../policies/RECORDS.md).
- Inputs:
  - Assignment, Project specification, assigned Task specification, applicable Contracts and Verification, Implementation, Acceptance.
  - When available: prior Evidence and Result permitted by Checks.
- Effects:
  - Wait for Supervisor confirmation that affected writers are paused.
  - Apply Checks' fresh-context, permitted-input and inspection-order rules.
  - Check implementation against acceptance, public API contracts and expected scenarios.
  - Check code and acceptance against every applicable requirement.
  - Find omissions, weakened expectations and unjustified constraints.
  - Check interactions, unintended changes and prior findings.
  - Report missing or conflicting contracts.
  - Inspect public API unit and integration tests.
  - Check scenario coverage and independent expected outcomes.
  - Assess internal tests and mock justifications under Checks.
  - Accept internal tests and mocks when they provide useful evidence.
  - Request stronger tests for concrete coverage gaps.
  - Check that each test layer covers a distinct risk.
  - Assess guideline exceptions.
  - Check for test-only production hooks.
  - Run relevant checks.
  - Reproduce findings where feasible.
  - Keep requirements and code unchanged.
  - Report candidate changes to Implementer and Supervisor.
  - Apply Checks' recheck rules.
  - Save and return the result under [Records](../policies/RECORDS.md#return-work).
  - Report blockers promptly.
- Outputs:
  - Evidence and Result.
  - Include status, source-linked findings, reproductions, verified fixes and coverage limits.
  - Identify public API contract defects and test gaps.
- Next:
  - Return findings and result to Implementer.
  - Supervisor releases paused writers.
