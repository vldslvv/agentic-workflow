---
id: "<SPEC-ID>"
version: "0.1"
status: draft
title: "<Subsystem>"
depends_on: []
shared_contracts: []
---

# Acceptance — <TASK ID / subsystem>

Save as `.agents/tasks/<NNN>-<task-id>/acceptance.md` and register this file as the subsystem specification. Fill only relevant behavior; unresolved mandatory items block approval. Approval lives in a separate digest-bound record, not this status field.

**Baseline commit:** <Full pre-implementation Git commit.>
**Goal, boundary, and exclusions:** <Observable operations, interfaces, outputs, side effects, state, normative references, and non-goals.>

## Requirements and checks

| Requirement ID | Required observable outcome, boundaries/errors, allowed variation | Check ID and method | Inputs/setup, assertions/pass rule, cleanup, evidence |
|---|---|---|---|
| <SPEC-ID>-R001 | <Concrete contract> | <CHECK-ID; executable command or authorized manual criterion> | <Precise assessment> |

Checks may cover several requirements. Include required dependency integration and assembled-app checks, manual authorities, and any sampling/thresholds. Use a separate verification plan only when this table is insufficient. The planner freezes executable checks and normative inputs before implementation.

## Dependencies and retained inputs

<Explain depends_on prerequisites, shared contracts, assets/data/services, and integration expectations. No second graph.>

## Open decisions and approval reference

<Unresolved questions or none; approval record identifying this document's digest, plan digest, baseline commit, authority, and decision. Later changes require authorization under shared contract §2.>
