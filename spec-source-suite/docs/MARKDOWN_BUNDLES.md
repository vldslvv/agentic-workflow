# Standard specification format — Markdown task bundles

All app specifications use this layout: `project.md`, `task_order.md`, `tasks/*.md`, and `verification.md`. Define authors it; Generate and Implement consume it. The files use ordinary Markdown prose and lists, with no required frontmatter. The [shared contract](SUITE_CONTRACT.md) governs approval, frozen checks, review, and acceptance. Specification loaders support only this layout; historical records remain audit evidence, not an alternative app input format.

## Resolve the supplied bundle

| Source | Meaning |
|---|---|
| `project.md` | Shared constraints, target choices, and output location |
| `task_order.md` | Selected task files and their required execution order |
| `tasks/*.md` | Authoritative task behavior |
| `verification.md` | Shared verification intent and assembled-app scenarios |

Resolve a bare task filename in `task_order.md` under the bundle's `tasks/` directory; resolve an explicit relative path from the bundle root to a Markdown file under `tasks/`. Resolve normative references within task documents from their containing document. Validate that every listed file exists and occurs once. Only listed tasks are selected; inspect other files when explicitly referenced as normative inputs or prerequisites. If multiple bundles are plausible, resolve the selected bundle before execution.

Keep existing source files in place and preserve their text. Use each task's filename stem as its stable ID, validate ID uniqueness, and map requirement IDs to exact source clauses in the task acceptance record. Pin source digests so line shifts or edits cannot silently change a requirement. Source numbering is an identifier, not the repository's task/run sequence.

Each task in the ordered list waits for the preceding task's acceptance. Record those ordering prerequisites in the acceptance records. Include prerequisites explicitly declared in task prose too. The union must be acyclic and reference known tasks; contradictory order and dependency declarations yield BLOCKED. Do not invent domain dependencies from filenames or remove declared edges. The source order and task declarations define the graph under contract §5; acceptance records preserve its derived form for execution. Freeze them together and reconcile any later change through Define.

## Prepare the execution handoff

Use [Define](DEFINE.md) to complete the acceptance and check mapping. Each `.agents/tasks/<NNN>-<task-id>/acceptance.md` references its original task file, shared project constraints, relevant verification intent, source digests, requirement IDs, and normalized dependencies. It adds approved observable criteria only where needed; it does not copy or replace the source behavior. Any conflict between the record and its sources must be resolved before approval. Preserve a complete plan and digest-bound approval record under contract §2, including the referenced source identities.

Put the execution input inventory in a shared, planner-owned `inputs.md` alongside those task records, outside the source bundle and generated output. It records:

- Bundle root and source paths/digests; selected task IDs and acceptance-record paths.
- Target constraints and explicitly delegated choices, taken from `project.md` and the task sources.
- Generated roots, protected paths, retained inputs, verification mapping, frozen inventory, approval references, and evidence root.

Declare paths in `inputs.md` relative to the repository root, with any controlled external verifier references identified explicitly. Use `.suite/runs/<NNN>-<task-id>/` by default for run evidence. Repository-relative output paths in `project.md` resolve from the repository root; clarify ambiguous output or data-root language before freezing it. Record technology and target constraints in `project.md`, with only constraints needed to execute and verify the selected work, using supplied choices and explicit delegation for the rest. The inventory pins those constraints and records the selected execution environment and check adapters.

The inventory and acceptance records are derived handoff artifacts, not alternative specifications. Keep the inventory separate from the implementation plan so it can be allowlisted for fresh review. Automated tooling must consume the same bundle layout and preserve these authority boundaries.

## Assess readiness separately from format

Natural-language tasks and broad verification suggestions may need clarification. Resolve observable interfaces, persisted-state semantics, applicable failures, and concrete pass rules before freezing checks. Preserve the user's requirements and distinguish proposals from approved behavior. Existing approvals apply only to their recorded documents and digests; an older similarly named app or task is not authority for the selected bundle.

An incomplete bundle is input for Define when authoring is authorized; missing required files block generation until prepared and approved. Other source material can inform authorized Define work, but execution requires the standard bundle. Report the missing layout explicitly rather than falling back to historical specification formats. No supplied project intent or specification material yields NO_PROJECT.

A compatibility-only request authorizes this assessment, not app generation or approval of missing behavior. Report format support separately from outstanding execution inputs. An authorized generation request can proceed through Define preparation and then Generate using the same request's implementation authorization once all gates pass; avoid asking again for authorization already given. Missing required decisions, approvals, or executable checks yield BLOCKED for execution, while an absent project yields NO_PROJECT. Broad scenario text alone is not a frozen executable verifier.
