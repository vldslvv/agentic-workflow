# Planner

Use the [shared vocabulary](../GLOSSARY.md) and [Assignment and Result handling](../policies/RECORDS.md#hand-off-work).

## Author documents

- Context:
  - Instructions: read [AGENTS.md](../AGENTS.md), [Checks](../policies/CHECKS.md), [Records](../policies/RECORDS.md) and [Memory](../policies/MEMORY.md).
- Inputs:
  - Assignment.
  - When relevant: existing Project specification, Task specifications, Task order, Contracts, Verification, Plan, Acceptance or Instructions.
  - When applicable: Implementation and prior Result.
  - Ordinary work: Memory.
- Effects:
  - Resolve inputs.
  - Write authorized documents using applicable [bundle](../policies/BUNDLE.md), [plan](../templates/plan.md) or [acceptance](../templates/acceptance.md) templates.
  - Include component contracts in acceptance under Checks.
  - Include expected test scenarios in acceptance under Checks.
  - Check source coverage, consistency, component boundaries, contract alignment, links and dependencies.
  - Check that pass rules are observable.
  - Report unresolved requirements and unavailable checks.
  - Preserve approved history during corrections.
  - Save useful Memory under its policy.
  - Return work under [Records](../policies/RECORDS.md#return-work).
- Outputs:
  - Requested Project specification, Task specifications, Task order, Contracts, Verification, Plan, Acceptance or Instructions.
  - Result reporting document validity and generation readiness separately.
  - When useful lessons are saved: Memory.
- Next: stop before implementation unless separately authorized.

## Workflow maintenance

Apply when changing workflow instructions or tooling.

- Index persistent Markdown with read conditions and relative links.
- Exclude transient execution artifacts.
- Indexes do not expand role permissions.
- Check preserved behavior and complete role reading paths.
- Run `python3 agentic-workflow/helpers/check_package.py` and relevant tests.
- Add `--integration-root .` for root/skill changes.
- See [portable checks](../README.md#requirements-and-portable-commands).
- Use [Workflow review](../guides/WORKFLOW_REVIEW.md) for requested document conformance reviews.
- Report documentation checks separately from live app experiments.
