# Planner

Author project documents and maintain workflow instructions.

## References:

- [GLOSSARY]: Defines shared roles, inputs and outputs. agentic-workflow/GLOSSARY.md
- [RECORDS]: Defines execution records, assignments and handoffs. agentic-workflow/policies/RECORDS.md
- [AGENTS]: Routes actions to role instructions and shared policies. agentic-workflow/AGENTS.md
- [DOCUMENT_STYLE]: Defines document structure and reference conventions. agentic-workflow/policies/DOCUMENT_STYLE.md
- [CHECKS]: Defines acceptance criteria, independent checks and evidence rules. agentic-workflow/policies/CHECKS.md
- [MEMORY]: Defines how to read and maintain project lessons. agentic-workflow/policies/MEMORY.md
- [BUNDLE]: Defines specification files, task selection and path resolution. agentic-workflow/policies/BUNDLE.md
- [PLAN_TEMPLATE]: Structures task implementation plans. agentic-workflow/templates/plan.md
- [ACCEPTANCE_TEMPLATE]: Maps requirements to observable checks and pass rules. agentic-workflow/templates/acceptance.md
- [README]: Explains installation, package ownership and portable commands. agentic-workflow/README.md
- [WORKFLOW_REVIEW]: Defines requested workflow conformance reviews. agentic-workflow/guides/WORKFLOW_REVIEW.md

## Author documents

Use the [GLOSSARY] and [RECORDS] (“Hand off work”).

- Context:
  - Instructions: read [AGENTS], [CHECKS], [RECORDS] and [MEMORY].
- Inputs:
  - Assignment.
  - When relevant: existing Project specification, Task specifications, Task order, Contracts, Verification, Plan, Acceptance or Instructions.
  - When applicable: Implementation and prior Result.
  - Ordinary work: Memory.
- Effects:
  - Resolve inputs.
  - Write authorized documents using templates from [BUNDLE], [PLAN_TEMPLATE] or [ACCEPTANCE_TEMPLATE].
  - Include component contracts in acceptance under [CHECKS].
  - Include expected test scenarios in acceptance under [CHECKS].
  - Check source coverage, consistency, component boundaries, contract alignment, links and dependencies.
  - Check that pass rules are observable.
  - Report unresolved requirements and unavailable checks.
  - Preserve approved history during corrections.
  - Save useful Memory under its policy.
  - Return work under [RECORDS] (“Return work”).
- Outputs:
  - Requested Project specification, Task specifications, Task order, Contracts, Verification, Plan, Acceptance or Instructions.
  - Result reporting document validity and generation readiness separately.
  - When useful lessons are saved: Memory.
- Next: stop before implementation unless separately authorized.

## Workflow maintenance

Apply when changing workflow instructions or tooling.

- Index referenced documents under [DOCUMENT_STYLE] with explicit read conditions.
- Exclude transient execution artifacts.
- Indexes do not expand role permissions.
- Check preserved behavior and complete role reading paths.
- Run `python3 agentic-workflow/helpers/check_package.py` and relevant tests.
- Add `--integration-root .` for root/skill changes.
- See [README] (“Requirements and portable commands”).
- Use [WORKFLOW_REVIEW] for requested document conformance reviews.
- Report documentation checks separately from live app experiments.
