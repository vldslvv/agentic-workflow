---
name: acceptance-spec
description: Turn an interactive planning discussion into an acceptance specification for approval before implementation.
---

# Acceptance specification

1. Extract agreed requirements, constraints, boundaries, failure behavior and non-goals. Give criteria stable IDs, source references, observable outcomes and concrete checks under [Checks](../../../spec-source-suite/CHECKS.md). Keep design choices open unless explicitly required; surface material conflicts.
2. Apply [source authority](../../../spec-source-suite/BUNDLE.md) to approvals and implementation authorization. Present complete plan/acceptance drafts when approval is needed; preserve explicitly approved text.
3. Use the [plan](../../../spec-source-suite/templates/plan.md) and [acceptance](../../../spec-source-suite/templates/acceptance.md) templates. Save and recover originals under [Records](../../../spec-source-suite/RECORDS.md), including its Plan-mode rules.
4. Route document-only work to [Planner](../../../spec-source-suite/PLANNER.md) and authorized app execution to [Supervisor](../../../spec-source-suite/SUPERVISOR.md). This skill is not a prerequisite for the [lightweight execution workflow](../../../spec-source-suite/IMPLEMENTER.md).
