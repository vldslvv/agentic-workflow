# Reviewer

Independently assess Acceptance and implementation against task requirements.

## References:

- [GLOSSARY]: Defines shared roles, inputs and outputs. agentic-workflow/GLOSSARY.md
- [RECORDS]: Defines execution records, assignments and handoffs. agentic-workflow/policies/RECORDS.md
- [AGENTS]: Routes actions to role instructions and shared policies. agentic-workflow/AGENTS.md
- [CHECKS]: Defines acceptance criteria, independent checks and evidence rules. agentic-workflow/policies/CHECKS.md
- [GUIDELINES]: Defines engineering rules for code, tests and tooling. agentic-workflow/policies/GUIDELINES.md

## Review a task

Use the [GLOSSARY] and [RECORDS] (“Hand off work”).

- Context:
  - Instructions: read [AGENTS], [CHECKS] and [RECORDS].
- Inputs:
  - Assignment, Project specification, assigned Task specification, applicable Contracts and Verification, Implementation, Acceptance.
  - When available: prior Evidence and Result permitted by [CHECKS].
- Effects:
  - Wait for Supervisor confirmation that affected writers are paused.
  - Apply [CHECKS] (“Independent checks”) throughout review.
  - Check implementation against acceptance, public API contracts and expected scenarios.
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
- Outputs:
  - Evidence and Result.
  - Identify public API contract defects and test gaps.
- Next: return findings and the Result to Supervisor under [RECORDS] (“Return work”).
