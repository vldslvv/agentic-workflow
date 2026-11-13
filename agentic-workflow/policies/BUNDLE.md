# Specification bundle

Resolve specification sources, task boundaries, dependencies and authorization.

## References:

- [PROJECT_TEMPLATE]: Structures project intent, constraints and output paths. agentic-workflow/templates/project.md
- [TASK_ORDER_TEMPLATE]: Lists task filenames and dependencies. agentic-workflow/templates/task_order.md
- [TASK_TEMPLATE]: Structures component behavior, constraints and acceptance. agentic-workflow/templates/tasks/task.md
- [CONTRACT_TEMPLATE]: Structures shared interaction contracts. agentic-workflow/templates/contracts/contract.md
- [VERIFICATION_TEMPLATE]: Structures shared checks and assembled-app scenarios. agentic-workflow/templates/verification.md

## Resolve a bundle

Apply when finding or writing specifications.

- Use the selected bundle or find an unambiguous bundle outside the package.
- Return `NO_PROJECT` without a requested project and block missing or ambiguous required inputs.
- Put new specifications in `specs/`, preserving existing specifications, approved text and history in place.
- Follow specifications and linked requirements over conflicting plans or memory.
- Report unresolved requirement conflicts and missing authorization as blockers without prompting.
- Require implementation authorization beyond document approval or compatibility assessment.
- Change required behaviour only with user authorization.
- Use ordinary Markdown without requiring frontmatter.

| File | Purpose | Template |
|---|---|---|
| `project.md` | Intent, constraints, target and output paths | [PROJECT_TEMPLATE] |
| `task_order.md` | Task filenames and dependencies | [TASK_ORDER_TEMPLATE] |
| `tasks/*.md` | Component behavior and acceptance outcomes | [TASK_TEMPLATE] |
| `contracts/*.md` (optional) | Shared interaction contracts | [CONTRACT_TEMPLATE] |
| `verification.md` | Shared checks and assembled-app scenarios | [VERIFICATION_TEMPLATE] |

## Task specifications

Apply when authoring tasks and application contracts.

- Define ordinary tasks as cohesive components or bounded component changes.
- Make tasks implementable and checkable against declared prerequisites and contracts.
- Keep shared requirements authoritative in one contract linked by every providing or consuming task.
- Reconcile contract changes across affected tasks before implementation.
- Put mandatory choices in Constraints and advice in Implementation suggestions.

## Select tasks and resolve paths

Apply before scheduling tasks or resolving their sources and outputs.

- Declare dependencies only in `task_order.md`'s `Task | Depends on` table, listing each task once with `None` or comma-separated task filenames for dependencies.
- Use unique filenames without extensions as task IDs.
- Resolve bare task filenames under `tasks/`, task paths from the bundle root, requirement links from their containing document and repository-relative outputs from the repository root.
- Reject missing files, unknown references, unlisted dependencies and dependency cycles.
- Select tasks with their prerequisites and required sources, requiring valid acceptance evidence for completed prerequisites.
- Block selections that exclude unfinished prerequisites and return `NO_WORK` for an empty selection.
- Resolve ambiguous scope and scenario pass criteria before execution, reporting unresolved cases as blockers without changing requirements or prompting.
- Report document validity separately from application conformance.
