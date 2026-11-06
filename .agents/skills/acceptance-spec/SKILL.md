---
name: acceptance-spec
description: Turn an interactive planning discussion into an acceptance specification for approval at the end of planning, before implementation.
---

# Acceptance specification

Use the planning discussion as the source of agreed scope. Read relevant repository
contracts when needed to make criteria precise. Extract agreed requirements,
contracts, edge cases, failure scenarios, non-goals, and verification criteria;
resolve material ambiguities with the user rather than inventing requirements.
Keep implementation choices open unless the user explicitly requires them.

For a documentation-only task, follow Define's document-completion gate. The
future app's acceptance outcomes describe what a later app must do; they are not
checks to execute while authoring its specification. Executing a documentation
plan stays in Define, including when requested as “implement the plan.” Report
document approval/completion separately from deferred app-generation readiness.

Choose a short task ID, reusing the user's ID when provided. Allocate the next
unused three-digit directory prefix across `.agents/tasks/` and `.suite/runs/`
under planning-record rules; use the same prefix for a task and its run directory. Record the full baseline Git commit before implementation, normally
`git rev-parse HEAD`; if work has already started, establish the actual baseline
with the user. Present a concise draft containing the task ID, baseline commit,
goal, scope and non-goals, and numbered acceptance criteria. Give each criterion
a stable ID such as AC-1, one independently verifiable outcome, and a concrete
verification method with the relevant inputs, conditions, and expected result.
Include agreed boundary and failure behavior in the criteria. Keep unresolved
questions visibly separate from agreed requirements.

Present the complete draft in the conversation and explicitly ask the user to
approve it. Wait for explicit approval of the current draft; revisions require
presenting the revised draft for approval. Save only after approval, using
`.agents/tasks/<NNN>-<task-id>/acceptance.md`, and preserve the approved text exactly.
Do not overwrite an existing approved specification without explicit authorization.
When the task uses this repository's specification workflow, also preserve the
complete approved plan as `plan.md` in the same directory and record both document
digests, the full baseline commit, approving authority, and approval reference.
Follow [planning records](../../../spec-source-suite/docs/PLANNING.md)
for task persistence. For app work, use the [standard Markdown bundle](../../../spec-source-suite/docs/MARKDOWN_BUNDLES.md) as the specification source.
The acceptance record references source paths and digests and maps their clauses
to checks; preserve source behavior in the bundle rather than duplicating it.

If Plan mode prevents writing, present the complete drafts and state that saving
is deferred. Save the exact approved text once editing is available, before
implementation or context handoff. Recover missing originals instead of rebuilding
them from a summary. Report the saved paths. Approval alone never starts
implementation; a separate instruction is required. If that instruction already
exists, continue within its authorized scope rather than asking again.

Treat the approved document as immutable. If later discoveries require a change,
present the proposed revision and obtain explicit authorization before editing;
never weaken or silently reinterpret criteria to fit an implementation.
