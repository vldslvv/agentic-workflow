# Markdown task bundles

Keep app inputs outside the suite, under `specs/` for new authorized authoring. Preserve existing locations and approved text. Ordinary Markdown needs no frontmatter.

| File | Purpose |
|---|---|
| `project.md` | Project intent, shared constraints, target and output paths |
| `task_order.md` | Ordered task filenames |
| `tasks/*.md` | Required behavior; explicit additional prerequisites |
| `verification.md` | Shared verification and assembled-app scenarios |

1. Use the selected bundle; ask if several are plausible. No project intent yields NO_PROJECT. Missing required files block generation; prepare them through Define only when authoring is authorized.
2. Resolve bare task filenames under `tasks/`, explicit relative task paths from the bundle root, and normative references from their containing document. Only listed tasks are selected; include referenced prerequisites and normative inputs. Require each listed file once and unique filename stems as task IDs.
3. Each listed task waits for the preceding task's acceptance plus explicitly declared prerequisites. Reject unknown references and cycles. Do not infer extra dependencies from names. Scope controls cannot bypass prerequisites.
4. Use [Define](DEFINE.md) to save the full plan and acceptance in the existing task-record locations. Map stable requirement IDs to exact source clauses, observable outcomes and checks. Record derived prerequisites, target, output/evidence paths and ordinary defaults. Repository-relative output paths resolve from the repository root; resolve material ambiguity before execution.
5. Shared constraints stay in `project.md`; shared/final scenarios stay in `verification.md`. Clarify pass rules for broad scenarios before executing them. Implementation may develop checks without a separate input inventory or approval step. Preserve explicit requirements and required manual/integration checks.

Compatibility assessment alone does not authorize generation. A direct implementation request authorizes derived plans and acceptance; a plan cannot override the source bundle. Format validity and app acceptance are separate conclusions.
