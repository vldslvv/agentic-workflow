---
name: agentic-workflow-acceptance
description: Turn an interactive planning discussion into an acceptance specification for approval before implementation.
disable-model-invocation: true
---

# Acceptance specification

When explicitly invoked, read [workflow entry points](../../../agentic-workflow/AGENTS.md).

1. Extract agreed requirements, constraints, boundaries, failure behavior and non-goals. Give criteria stable IDs, source references, observable outcomes and concrete checks under [Checks](../../../agentic-workflow/CHECKS.md). Keep design choices open unless explicitly required; surface material conflicts.
2. Apply [source authority](../../../agentic-workflow/BUNDLE.md) to approvals and implementation authorization. Present complete plan/acceptance drafts when approval is needed; preserve explicitly approved text.
3. Use the [plan](../../../agentic-workflow/templates/plan.md) and [acceptance](../../../agentic-workflow/templates/acceptance.md) templates. Save and recover originals under [Records](../../../agentic-workflow/RECORDS.md), including its Plan-mode rules.
4. Route document-only work to [Planner](../../../agentic-workflow/PLANNER.md) and authorized app execution to [Supervisor](../../../agentic-workflow/SUPERVISOR.md). This skill is not a prerequisite for the [lightweight execution workflow](../../../agentic-workflow/IMPLEMENTER.md).
