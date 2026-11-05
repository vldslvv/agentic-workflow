# App generation

This repository uses `spec-source-suite/` as reusable guidance for generating an app. The app's specification bundle lives outside that directory and defines what to build. Keep app specifications, target constraints, retained assets, generated code, and run evidence outside the suite. Modify the suite itself only when the user requests changes to the workflow tooling or guidance.

## Locate existing task documents first

When implementing, resuming, or receiving a task handoff, resolve its approved documents before asking the user to supply them:

Use a shared three-digit sequence for each task and its run directory: `.agents/tasks/001-example/` and `.suite/runs/001-example/`, then `002-…`. Allocate the next unused number across both roots; preserve existing task IDs and approved text when renaming directories. For lookup by an unprefixed task ID, match the numbered directory suffix.

1. Read any explicit task paths or execution-inventory task-record references. A user-selected Markdown bundle is authoritative for input discovery; use [Markdown bundles](spec-source-suite/docs/MARKDOWN_BUNDLES.md) to prepare its handoff rather than substituting historical task documents. Otherwise use the task ID from the request to open `.agents/tasks/<NNN>-<task-id>/plan.md`, `acceptance.md`, and the accompanying approval record, relative to this repository root.
2. If the ID or files are missing, search hidden task directories explicitly with `rg --files --hidden .agents/tasks` and inspect matching task IDs, titles, and approval references. Default file searches can omit `.agents/`; an empty default search is not evidence that documents are absent.
3. If saving was deferred or documents are still missing, inspect the identified prior task's available conversation history or local transcript to recover the complete approved originals and approval reference. Preserve exact text; a handoff summary cannot replace it.

Ask the user only after these available sources are exhausted or conflicting records leave authority unresolved. State which locations were checked and what remains missing. Independent reviewers retain their restricted input boundary: read acceptance and approval records, never the plan or prior conversation.

## Load the workflow

Before defining, implementing, or generating an app, read [the suite instructions](spec-source-suite/AGENTS.md) and [the shared contract](spec-source-suite/docs/SUITE_CONTRACT.md). Their workflow boundaries and acceptance gates apply to app work throughout this repository. Resolve relative paths in suite documents from the containing document, not from this project root.

Select the procedure by the requested deliverable, not by verbs such as “implement the plan.” Creating specification-bundle, acceptance, target-constraint, or task-order documents is Define work, including execution of an approved documentation plan. Read both its skill file and workflow document directly; the nested skills need not be installed or automatically discovered:

| Requested work | Skill instructions | Workflow |
|---|---|---|
| Author app documents or define/revise behavior and acceptance criteria | [spec-define](spec-source-suite/.agents/skills/spec-define/SKILL.md) | [Define](spec-source-suite/docs/DEFINE.md) |
| Implement an approved app capability or assess an app candidate | [spec-implement](spec-source-suite/.agents/skills/spec-implement/SKILL.md) | [Implement](spec-source-suite/docs/IMPLEMENT.md) |
| Generate an app, update it incrementally, regenerate it, or change its target technology | [spec-generate](spec-source-suite/.agents/skills/spec-generate/SKILL.md) | [Generate](spec-source-suite/docs/GENERATE.md) |

For generation, also read the Implement skill and workflow: Generate orchestrates that procedure for each selected capability. Read `spec-source-suite/CODEX_START.md` and `spec-source-suite/docs/BUILD_THE_SUITE.md` only when explicitly asked to build the suite's tooling; they are not the app specification.

## Locate the app inputs

1. Use the specification bundle identified by the user. Otherwise inspect the repository outside `spec-source-suite/` for `project.md`, `task_order.md`, `tasks/*.md`, and `verification.md`. If multiple bundles are plausible, ask which one is authoritative before implementing.
2. Follow the [standard bundle format](spec-source-suite/docs/MARKDOWN_BUNDLES.md) for task selection, path resolution, dependencies, and target constraints. Read all selected task files, prerequisite tasks, and normative references.
3. If the user supplies a brief or incomplete source material, follow Define to author the standard bundle when authorized. Use `specs/` at the project root for a new bundle with no established location. Copy the [bundle templates](spec-source-suite/templates/bundle/project.md) and fill them from the user's requirements. Preserve an existing standard bundle's location and approved text.
4. Treat suite templates as blank scaffolding and `BUILD_THE_SUITE.md` as a tooling specification. Neither supplies app requirements. Keep source-linked task acceptance, the approved `plan.md`, baseline commit, and digest-bound approval references under `.agents/tasks/<NNN>-<task-id>/`; record their paths in `inputs.md`. Historical task notes are audit records, not alternative app specifications. Missing required bundle files block generation; no supplied project intent or specification material yields `NO_PROJECT`.

## Execute and finish

For documentation-only work, use Define's document-completion gate: approved, saved, internally consistent documents with verification descriptions. Report deferred app execution prerequisites separately as generation readiness. Writing an implementation-order document does not trigger its steps. The execution gates below apply to app implementation and generation, not document authoring.

Before app implementation, establish the approved specification baseline, selected requirement IDs and scope, dependency graph, target constraints, verification arrangement, retained inputs, and authorized output paths required by the shared contract. Use existing approvals and delegated choices where applicable. Resolve missing decisions with the user instead of inventing a domain, stack, or deployment model. Missing required execution inputs yield `BLOCKED`.

Follow Generate's mode-specific workspace rules and Implement's review and verification loop. Keep the app bundle and acceptance baseline protected from implementation changes. Persist run state and requirement-linked evidence in the execution inventory's configured evidence directory, outside `spec-source-suite/`. Use the suite’s concise run-report and review templates when those steps are reached; the bundle's `verification.md` holds shared scenarios and acceptance records link task-specific checks. Follow the shared contract for planner-authored frozen checks, the implementer-spawned fresh reviewer, and the bounded correction loop. Initial and incremental work use procedural separation unless stronger isolation is explicitly required.

Completion requires every mandatory gate for the selected scope to pass, including independent review, applicable manual acceptance, and assembled-app checks for project acceptance. Report actual checks, unmet requirements, evidence paths, and any isolation or execution limitations. When a required capability is unavailable, preserve partial evidence and report the blocked gate rather than claiming success.
