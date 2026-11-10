# Specification bundle

Apply when finding or writing specifications or selecting tasks.

## References:

- [PROJECT_TEMPLATE]: Structures project intent, constraints and output paths. agentic-workflow/templates/project.md
- [TASK_ORDER_TEMPLATE]: Lists task filenames and dependencies. agentic-workflow/templates/task_order.md
- [TASK_TEMPLATE]: Structures component behavior, constraints and acceptance. agentic-workflow/templates/tasks/task.md
- [CONTRACT_TEMPLATE]: Structures shared interaction contracts. agentic-workflow/templates/contracts/contract.md
- [VERIFICATION_TEMPLATE]: Structures shared checks and assembled-app scenarios. agentic-workflow/templates/verification.md
- [VALIDATOR]: Validates the assembled app and publishes repair tasks. agentic-workflow/roles/VALIDATOR.md
- [SUPERVISOR]: Coordinates implementation, recovery and acceptance. agentic-workflow/roles/SUPERVISOR.md

## Resolve a bundle

- Use the selected bundle.
- Without a selected bundle, look for these files outside the package.
- Ask when more than one bundle fits.
- Put authorized new specifications in `specs/`.
- Keep existing specifications in their current locations.
- Return `NO_PROJECT` when no project has been requested.
- Block generation when required inputs are missing.
- Do not generate apps from compatibility assessment requests.
- Follow the bundle and linked requirements over conflicting plans or memory.
- Preserve explicit requirements, the full approved text and its history.
- Make ordinary implementation choices when implementation is requested.
- Create needed records for requested implementation.
- Ask the user to resolve significant requirement conflicts.
- Get user approval before changing required behaviour.
- Require implementation permission beyond document approval.
- Use ordinary Markdown without requiring frontmatter.

A bundle contains the project files listed below.

| File | Purpose | Template |
|---|---|---|
| `project.md` | Intent, constraints, target and output paths | [PROJECT_TEMPLATE] |
| `task_order.md` | Task filenames and dependencies | [TASK_ORDER_TEMPLATE] |
| `tasks/*.md` | Component responsibilities, behavior and acceptance outcomes | [TASK_TEMPLATE] |
| `contracts/*.md` (optional) | Shared interaction contracts | [CONTRACT_TEMPLATE] |
| `verification.md` | Shared checks and assembled-app scenarios | [VERIFICATION_TEMPLATE] |

## Task specifications

Apply when authoring tasks and interaction contracts.

- Define each ordinary task as a cohesive component or bounded component change.
- Follow [VALIDATOR] (“Publish repair”) for cross-component validation repairs.
- Make tasks implementable and checkable against agreed contracts and declared prerequisites.
- Keep responsibility, boundaries, behavior and acceptance, omitting other inapplicable fields.
- Keep shared requirements in one authoritative contract or interface definition.
- Link shared contracts from every task that provides or consumes them.
- Reconcile contract changes across affected tasks before implementation.
- Put required choices in Constraints and advisory choices in Implementation suggestions.

## Select tasks and resolve paths

Apply before scheduling selected tasks under [SUPERVISOR].

- Declare dependencies only in the `Task | Depends on` table in `task_order.md`.
- List each task once.
- Use `None` or comma-separated task filenames for dependencies.
- Do not infer dependencies from runtime interactions, shared contracts, names or row order.
- Use unique filenames without extensions as task IDs.
- Resolve bare task filenames under `tasks/`.
- Resolve task paths or links from the bundle root.
- Resolve requirement links from the containing document.
- Reject missing files, unlisted dependencies, unknown references and dependency cycles, including self-dependencies.
- Select listed tasks together with their prerequisites and required source documents.
- Block selections that exclude unfinished prerequisites.
- Require valid evidence for accepted prerequisites.
- Return `NO_WORK` for an empty selection.
- Resolve repository-relative output paths from the repository root.
- Stop execution when ambiguity could affect the work.
- Clarify broad scenarios' pass criteria before execution without changing requirements.
- Allow checks to develop during implementation.
- Do not require a fixed check inventory or approval receipt.
- Report document validity separately from app conformance.
