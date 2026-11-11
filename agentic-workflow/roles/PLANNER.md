# Planner

Author project documents and maintain workflow instructions.

## References:

- [DOCUMENT_INPUT]: Defines DocumentInput fields. agentic-workflow/contracts/DocumentInput.md
- [WORK_RESULT]: Defines WorkResult fields. agentic-workflow/contracts/WorkResult.md
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

## Contracts

- Provides: `author_documents(input: DocumentInput) -> WorkResult` using [DOCUMENT_INPUT] and [WORK_RESULT].

## Author documents

- Context:
  - Instructions: read [AGENTS], [CHECKS], [RECORDS] and [MEMORY].
- Inputs: [DOCUMENT_INPUT].
- Effects:
  - Resolve inputs.
  - Write authorized documents using templates from [BUNDLE], [PLAN_TEMPLATE] or [ACCEPTANCE_TEMPLATE].
  - Apply [CHECKS] (“Prepare acceptance”) when authoring or correcting Acceptance.
  - Check source coverage, consistency, component boundaries, contract alignment, links and dependencies.
  - Check that pass rules are observable.
  - Report unresolved requirements and unavailable checks.
  - Return work under [RECORDS] (“Return work”).
- Outputs: [WORK_RESULT].
- Next: stop before implementation unless separately authorized.

## Workflow maintenance

Apply when changing workflow instructions or tooling.

- Index referenced documents under [DOCUMENT_STYLE] with explicit read conditions.
- Exclude transient execution artifacts.
- Indexes do not expand role permissions.
- Check preserved behavior and complete role reading paths.
- Run package checks and relevant tests from [README] (“Requirements and portable commands”).
- Include the integration check for root/skill changes.
- Use [WORKFLOW_REVIEW] for requested document conformance reviews.
- Report documentation checks separately from live app experiments.
