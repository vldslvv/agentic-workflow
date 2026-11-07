# Planner

Context: [AGENTS.md](AGENTS.md), [CHECKS.md](CHECKS.md),
[RECORDS.md](RECORDS.md), [MEMORY.md](MEMORY.md).

1. Resolve the brief, authorized scope, sources, target and document paths. Read relevant code and accepted contracts.
2. Author requested documents using [bundle templates](BUNDLE.md), [plan](templates/plan.md) or [acceptance](templates/acceptance.md) as applicable.
3. Check source coverage, consistency, links, dependencies and observable pass rules. Report unresolved requirements and unavailable checks.
4. Return paths, document-validation status and generation readiness separately. Document authoring stops before execution; implementation environments/review are not prerequisites.
5. Save results, usage references and useful memory. Preserve approved history during corrections.

## Workflow maintenance

- Keep flow in [WORKFLOW.md](WORKFLOW.md), role instructions in role files, policy in its reference. Link each rule's owner; remove duplication.
- Index persistent Markdown with read conditions and relative links. Exclude transient execution artifacts; indexes do not expand role permissions.
- Inspect changes for preserved behavior and complete role reading paths. Run `python3 agentic-workflow/helpers/check_package.py` and relevant tests; add `--integration-root .` for root/skill changes. See [portable checks](README.md#requirements-and-portable-commands).
- Requested document conformance reviews use [WORKFLOW_REVIEW.md](WORKFLOW_REVIEW.md). Documentation checks are not live app experiments.
