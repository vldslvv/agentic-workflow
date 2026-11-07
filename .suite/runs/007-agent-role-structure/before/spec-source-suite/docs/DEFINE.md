# Define — documents and ready-task planning

1. Resolve current intent, selected sources, scope and accepted prerequisites. Read the [bundle format](MARKDOWN_BUNDLES.md) and relevant [memory](PROJECT_MEMORY.md). Preserve explicit constraints; choose reasonable defaults for unspecified details and surface material conflicts.
2. Author requested documents using the bundle templates, or prepare source-linked [acceptance](../templates/ACCEPTANCE.md) for a ready task. Give requirements stable IDs, observable outcomes and proportionate check methods covering relevant normal, boundary, failure and interaction behavior. Link shared verification rather than copying it.
3. Save the complete [plan](../templates/PLAN.md): approach, interfaces, dependency contracts, output paths, checks, evidence destination and relevant memory paths. Checks may be developed during implementation; describe expected outcomes now. Distinguish task checks, regressions and assembled-app scenarios. Record unavailable checks and remaining coverage gaps.
4. Validate document consistency, source coverage, links, task order/prerequisites and verification descriptions. Document-only work finishes here with saved, validated documents; report generation readiness separately. App environments or implementation review are unnecessary for document authoring.
5. For authorized implementation, hand the implementer the full plan, acceptance, sources, dependency contracts and relevant memory paths. A direct implementation request already authorizes derived records. On completion or a blocked stop, save concise results, usage and useful memory.

## Records

- Keep `plan.md` and `acceptance.md` in `.suite/tasks/<NNN>-<task-id>/`; default run evidence is `.suite/runs/<NNN>-<task-id>/`. Allocate the next shared three-digit number by listing immediate directory names in both roots, without reading prior records.
- Record the authorizing request or decision in the task documents. Preserve complete explicitly approved text. Ordinary derived details need no separate approval receipt. Required behavior changes need user authority; retain earlier approved versions when revising them.
- Continuing work loads the identified complete records and relevant current state. Recover missing approved originals from that task's known source/conversation; if unavailable, report locations checked and request them instead of inventing text from a summary.
- In Plan mode, present complete drafts and state when saving is deferred. Save approved text once editing is available, before implementation or handoff. Approval alone does not authorize execution, but an existing implementation instruction does.
