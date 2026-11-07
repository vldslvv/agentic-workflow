---
name: acceptance-spec
description: Turn an interactive planning discussion into an acceptance specification for approval before implementation.
---

# Acceptance specification

1. Extract agreed requirements, constraints, boundaries, failure behavior and non-goals from the discussion. Give each criterion a stable ID, source reference, observable outcome and concrete verification method. Keep implementation choices open unless explicitly required; surface material conflicts.
2. Present the complete plan and acceptance draft for approval when approval is still needed. An existing request to implement supplied scope already authorizes derived records and ordinary choices; do not ask again. Preserve explicitly approved text.
3. Save full `plan.md` and `acceptance.md` under `.suite/tasks/<NNN>-<task-id>/`, following [shared record rules](../../../spec-source-suite/AGENTS.md#records) and the [planner outlines](../../../spec-source-suite/PLANNER.md). In Plan mode state deferred saving; save approved drafts once editing is available. Recover missing originals instead of reconstructing them from summaries. Keep acceptance independent of plans, conversations and memory for reviewer access.
4. For app work, use the [Markdown bundle](../../../spec-source-suite/AGENTS.md#markdown-bundle) as source authority. Document-only work uses the planner routine and ends with validated documents; report app-generation readiness separately. Authorized single-task or whole-app execution enters through the [supervisor](../../../spec-source-suite/SUPERVISOR.md), which dispatches task planners and implementers. Approval alone does not start implementation, but an existing implementation instruction does. The explicit suite skill entry points are `spec-planner` and `spec-supervisor`.

Preserve historical records. Changes to required behavior need user authority; ordinary derived details do not require separate receipts or approval steps.
