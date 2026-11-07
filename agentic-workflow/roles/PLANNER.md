# Planner

## Author documents

- Context: read [AGENTS.md](../AGENTS.md), [Checks](../policies/CHECKS.md), [Records](../policies/RECORDS.md), [Memory](../policies/MEMORY.md) and apply [Document style](../policies/DOCUMENT_STYLE.md).
- Inputs: brief, authorized scope, sources, target and document paths; relevant code and accepted contracts.
- Effects: resolve inputs; author requested documents using [bundle templates](../policies/BUNDLE.md), [plan](../templates/plan.md) or [acceptance](../templates/acceptance.md) as applicable. Check source coverage, consistency, links, dependencies and observable pass rules; report unresolved requirements and unavailable checks. Save results, usage references and useful memory; preserve approved history during corrections.
- Outputs: document paths, document-validation status and generation readiness reported separately. Document authoring stops before execution; implementation environments/review are not prerequisites.

## Workflow maintenance

Apply when changing workflow instructions or tooling.

- Index persistent Markdown with read conditions and relative links. Exclude transient execution artifacts; indexes do not expand role permissions.
- Inspect changes for preserved behavior and complete role reading paths. Run `python3 agentic-workflow/helpers/check_package.py` and relevant tests; add `--integration-root .` for root/skill changes. See [portable checks](../README.md#requirements-and-portable-commands).
- Use [Workflow review](../guides/WORKFLOW_REVIEW.md) for requested document conformance reviews. Report documentation checks separately from live app experiments.
