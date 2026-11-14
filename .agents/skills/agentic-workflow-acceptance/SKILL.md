---
name: agentic-workflow-acceptance
description: Turn an interactive planning discussion into an acceptance specification for approval before implementation.
disable-model-invocation: true
---

# Acceptance specification

Turn agreed requirements into authorized Plan and Acceptance documents.

## References:

- [AGENTS]: Routes work to role instructions and shared policies. agentic-workflow/AGENTS.md
- [IMPLEMENTER]: Defines document authoring and work execution. agentic-workflow/roles/IMPLEMENTER.md
- [SUPERVISOR]: Coordinates authorized specification implementation. agentic-workflow/roles/SUPERVISOR.md
- [CHECKS]: Defines observable criteria and checking rules. agentic-workflow/policies/CHECKS.md
- [BUNDLE]: Defines source authority and implementation authorization. agentic-workflow/policies/BUNDLE.md
- [PLAN_TEMPLATE]: Structures implementation plans. agentic-workflow/templates/PLAN.md
- [ACCEPTANCE_TEMPLATE]: Structures acceptance criteria and checks. agentic-workflow/templates/ACCEPTANCE.md
- [RECORDS]: Defines saving and recovering approved originals. agentic-workflow/policies/RECORDS.md

## Author acceptance

- Context: when explicitly invoked, read [AGENTS] and follow [IMPLEMENTER] for document authoring.
- Inputs: interactive planning discussion, agreed requirements, constraints, boundaries, failure behavior and non-goals.
- Effects:
  1. Extract source-linked criteria with stable IDs, observable outcomes and concrete checks under [CHECKS].
  2. Keep design choices open unless explicitly required.
  3. Surface material conflicts.
  4. Apply [BUNDLE] to approvals and implementation authorization.
  5. Present complete Plan and Acceptance drafts when approval is needed.
  6. Preserve explicitly approved text.
  7. Use [PLAN_TEMPLATE] and [ACCEPTANCE_TEMPLATE].
  8. Save and recover originals under [RECORDS], including its Plan-mode rules.
- Outputs: complete Plan and Acceptance drafts or saved approved documents, as authorized.
- Next: route authorized app execution to [SUPERVISOR].

## Guidelines

Apply when choosing this skill for acceptance authoring.

- Keep this skill optional for direct work under [IMPLEMENTER].
