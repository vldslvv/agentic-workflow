---
name: acceptance-spec
description: Turn an interactive planning discussion into an acceptance specification for approval before implementation.
---

# Acceptance specification

1. Extract agreed requirements, constraints, boundaries, failure behavior and non-goals from the discussion. Give each criterion a stable ID, source reference, observable outcome and concrete verification method. Keep implementation choices open unless explicitly required; surface material conflicts.
2. Present the complete plan and acceptance draft for approval when approval is still needed. An existing request to implement supplied scope already authorizes derived records and ordinary choices; do not ask again. Preserve explicitly approved text.
3. Save full `plan.md` and `acceptance.md` under `.suite/tasks/<NNN>-<task-id>/`, following [Define records](../../../spec-source-suite/docs/DEFINE.md#records). In Plan mode state deferred saving; save approved drafts once editing is available. Recover missing originals instead of reconstructing them from summaries.
4. For app work, use the [Markdown bundle](../../../spec-source-suite/docs/MARKDOWN_BUNDLES.md) as source authority. Document-only work ends with Define's validated documents; report app-generation readiness separately. Approval alone does not start implementation, but an existing implementation instruction does.

Preserve historical records. Changes to required behavior need user authority; ordinary derived details do not require separate receipts or approval steps.
