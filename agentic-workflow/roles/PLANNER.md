# Planner

## Author documents

- Context: read [AGENTS.md](../AGENTS.md), [Checks](../policies/CHECKS.md), [Records](../policies/RECORDS.md) and [Memory](../policies/MEMORY.md). Apply [Document style](../policies/DOCUMENT_STYLE.md).
- Inputs: brief, scope, sources, target paths, relevant code and accepted contracts.
- Effects:
  1. Resolve inputs and write authorized documents. Use applicable [bundle](../policies/BUNDLE.md), [plan](../templates/plan.md) or [acceptance](../templates/acceptance.md) templates.
  2. Check source coverage, consistency, links and dependencies. Check that pass rules are observable.
  3. Report unresolved requirements and unavailable checks.
  4. Save results, usage references and useful memory. Preserve approved history during corrections.
- Outputs: document paths, document validity and generation readiness. Report validity and readiness separately.
- Next: stop before execution. App setup and review are not prerequisites.

## Workflow maintenance

Apply when changing workflow instructions or tooling.

- Index persistent Markdown with read conditions and relative links. Exclude transient execution artifacts. Indexes do not expand role permissions.
- Check preserved behavior and complete role reading paths.
- Run `python3 agentic-workflow/helpers/check_package.py` and relevant tests. Add `--integration-root .` for root/skill changes. See [portable checks](../README.md#requirements-and-portable-commands).
- Use [Workflow review](../guides/WORKFLOW_REVIEW.md) for requested document conformance reviews. Report documentation checks separately from live app experiments.
