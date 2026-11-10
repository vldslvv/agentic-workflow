# <Task ID> — acceptance

Define observable checks and pass rules for task requirements.

## References:

- [CHECKS]: Defines acceptance criteria, independent checks and evidence rules. agentic-workflow/policies/CHECKS.md

## Acceptance

- **Request, sources and scope:** <Authorizing request, exact source clauses, applicable guideline clauses, shared constraints and selected behavior.>
- **Prerequisites:** <Link to applicable task_order.md entries.>
- **Target and paths:** <Required target, implementation destination and evidence destination.>
- **Contracts:** <Authoritative contract references or task-specific interface definitions under [CHECKS] (“Prepare acceptance”).>

| Requirement ID | Source / contract | Check scenario and pass rule |
|---|---|---|
| <Stable ID> | <Exact source clause or contract reference> | <Method, setup, action, observable outcome and cleanup> |

- **Shared/regression/final checks:** <References, including required real-dependency integration and manual criteria.>
- **Limits and decisions:** <Unavailable checks, substitutes/fidelity, coverage gaps and material conflicts, or none.>

- Derive this document from authorized requirements and sources, including source discussions, under [CHECKS].
- Apply [CHECKS] (“Independent checks”) during independent review and validation.
