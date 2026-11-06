# Acceptance record — <TASK ID>

Save under `.agents/tasks/<NNN>-<task-id>/acceptance.md`. This record maps the standard bundle's behavior to checks. The task ID is the source filename stem; source files remain the specification authority.

**Baseline commit:** <Full pre-implementation Git commit.>
**Source identities:** <Task file, project.md, task_order.md, verification.md, normative references, and their digests.>
**Scope:** <Selected source clauses, boundary, and exclusions.>
**Prerequisites:** <Task IDs derived from source order and explicit declarations; accepted revisions required for execution.>

## Requirements and checks

| Requirement ID | Source clause and observable acceptance criterion | Check ID and method | Setup, inputs, pass rule, cleanup, evidence |
|---|---|---|---|
| <TASK-ID>-R001 | <Exact source reference and approved criterion> | <CHECK-ID; command or authorized manual criterion> | <Concrete assessment> |

Reference shared scenarios in the bundle's verification.md. Include applicable dependency integration and regression checks. Record approved clarifications without copying source requirements; resolve conflicts before approval. The planner freezes executable checks and normative inputs before implementation.

## Retained inputs and approval

<Required assets/data/services; unresolved decisions or none; approval reference binding this record, plan, and source digests to the baseline, authority, and decision. Follow shared contract §1 and planning-record rules for changes.>

**Check sets:** <Task checks; declared regression set; separate final end-to-end scenarios.>
**Coverage:** <Check execution, coverage assessment and independent review outcome are separate dispositions.>
**Verifier revisions:** <Frozen inventory versions and authorized additive coverage, retaining earlier bytes.>
