# Spec Source Suite — shared rules

This package supplies instructions, blank templates and a usage helper, not a selected app or automated runner. Keep app inputs, code, memory and evidence outside it. Read this file plus exactly your role routine as operative suite guidance:

| Role | Routine | Responsibility |
|---|---|---|
| Supervisor | [SUPERVISOR.md](SUPERVISOR.md) | Schedule and collect outcomes |
| Planner | [PLANNER.md](PLANNER.md) | Author documents or prepare one ready task |
| Implementer | [IMPLEMENTER.md](IMPLEMENTER.md) | Implement, check and own fresh reviews |
| Reviewer | [REVIEWER.md](REVIEWER.md) | Independently check one candidate |
| Validator | [VALIDATOR.md](VALIDATOR.md) | Independently check the assembled app and specify repairs |

Document-only requests enter through `spec-planner`; single-task and whole-app execution through `spec-supervisor`. The two instruction-only skills under `.agents/skills/` require explicit invocation. Role dispatch may load the role files directly. Only requested automated-runner work reads [RUNNER.md](RUNNER.md). Suite tooling follows the user's acceptance and checks links, metadata and retained tests; documentation walkthroughs are distinct from live app experiments. These are proposed engineering procedures, not proven guarantees. When adopting the package, deliberately merge repository instructions and verify installed worker capabilities rather than assuming CLI flags or isolation.

## Workflow maintenance

For suite changes, keep operative guidance in this file plus one routine per role. Put common rules here and role-specific procedures with their role. Give each rule one authoritative home; reference it instead of repeating it. Prefer replacing or removing instructions when adding guidance. Add a file only when existing boundaries cannot accommodate its responsibility, and explain why.

Before completion, run `python spec-source-suite/helpers/check_package.py --base <starting-commit>` from the repository root. Check layout, links and skill entry points; report file/directory counts, instruction words and shared-plus-role context sizes. Explain increases as review signals, not automatic failures or reasons to weaken requirements. Update package metadata and checksums after validation.

Review each added instruction: does it change behavior, duplicate a rule, or force a role to load supporting procedure files? Confirm each role can operate with shared guidance, its own routine and the routing configuration below. Record the answers and any justified growth in the change's results.

Whenever a Markdown file is added, register it with an explicit relative-path link in the applicable index in the same change. Include a short purpose or read condition. Update the index when the file is moved, renamed, or removed.

Workflow guidance belongs in the root file index. Generated project documents, task records and memory belong in their applicable scoped indexes. Create a scoped index only when none exists, and link it from its parent index. Indexing does not authorize loading material excluded from a role's context.

## Model routing

Read [MODELS.md](MODELS.md) when entering a role and before launching workers; reread edits for subsequent dispatches. Resolve profiles and role routes from its tables; undefined profiles or malformed entries require correction before routing. Keep concrete model names and native reasoning settings in that configuration, not role routines.

Select the first applicable route:

1. After two consecutive implementation repair attempts reproduce the same failure without new diagnostic evidence, request the escalation profile.
2. Use the role's demanding route for conflicting requirements, complex component interactions, or correctness decisions involving security, data loss or compatibility.
3. Use small-change for local implementation with explicit expected behavior, an established pattern and no interface or dependency changes.
4. Otherwise use the role default.

Missing infrastructure, credentials and unresolved requirements remain blockers; routing does not resolve them.

Request the selected settings through supported host controls. If the host cannot apply a requested setting, continue with host defaults and report the fallback. Change retained-worker settings only through supported host controls, preserving contexts and fresh-review requirements. If an existing top-level session cannot change settings, treat its route as launch guidance and disclose known mismatches. Record requests separately from observed settings using the result outline below; unknown observations remain unavailable.

## Authority and acceptance

The selected bundle and normative references define behavior; plans and memory cannot override them. Preserve explicit requirements, complete approved text and history. A direct implementation request authorizes derived records and ordinary choices without routine reapproval. Required behavior changes and material conflicts need user authority. Approval of documents alone does not authorize execution.

Save a full plan and separate source-linked acceptance before implementation. Required unavailable capabilities block acceptance; skipped checks are NOT_RUN or BLOCKED, observed violations are FAIL, never weakened expectations. Use proportionate observable checks, relevant regressions and required manual/real-dependency checks. Reuse meaningful tests and cover gaps through public interfaces; avoid tests that assert their own mock outputs, implementation details, or test-only production hooks. Record substitute limits and remaining coverage gaps.

A task passes only with successful required checks, adequate requirement coverage and fresh independent review with no actionable findings. Missing fresh review is INDEPENDENT_REVIEW_NOT_RUN and blocks acceptance. Failed or blocked prerequisites never unlock consumers. Changed sources, dependencies or implementation require reassessing affected results and repeating checks/review. Final independent validation is required after scheduled tasks pass; task passes alone do not establish whole-app acceptance. Cancellation, applicable limits, conflicts or unavailable capabilities preserve unfinished results and blockers.

## Engineering guidelines

Every role must resolve and read applicable engineering guidelines before its work. Use sources required by repository instructions and those linked from the selected `project.md`; include repository-root `guidelines.md` when present. Resolve links from their containing document and pass resolved paths, not summaries. An explicitly required or handed-off file that is unavailable blocks work; an adopting repository with no guideline source has no additional guidelines. Keep project guidelines outside this reusable suite.

Treat these files as shared engineering constraints for planning, production code, tests, tooling and repairs. Plans and acceptance reference applicable clauses; implementation applies them; review and validation check conformance. Preserve each clause's strength: a preference permits a justified exception, while a requirement remains binding. Record material exceptions with their reason in review-visible results. Findings cite the clause and concrete consequence; stylistic preferences alone do not create new product requirements. Resolve conflicts under authority and acceptance above.

Every worker handoff includes the applicable guideline paths, including fresh reviewers, validators and replacement workers. Guidelines are allowed source inputs for independent checks, separate from excluded plans and memory. Reconstruction exports include the applicable guidelines within the allowed-input boundary; workers read the exported paths. Guideline changes require reassessing affected plans, checks and reviews under the ordinary changed-source rules.

## Markdown bundle

Use the selected bundle. Otherwise look outside the suite for these four file types and ask if multiple bundles are plausible. New authorized authoring uses `specs/`; preserve existing locations. No project intent yields NO_PROJECT; missing required inputs block generation. Compatibility assessment alone does not authorize generation.

| File | Content | Blank template |
|---|---|---|
| `project.md` | Intent, shared constraints, target and output paths | [project](templates/project.md) |
| `task_order.md` | Ordered task filenames | [task order](templates/task_order.md) |
| `tasks/*.md` | Observable required behavior and additional prerequisites | [task](templates/tasks/task.md) |
| `verification.md` | Shared checks and assembled-app scenarios | [verification](templates/verification.md) |

Ordinary Markdown needs no frontmatter. Resolve bare filenames under `tasks/`, explicit relative task paths from the bundle root, and normative references from the containing document. Require each listed file once and unique filename stems as task IDs. Only listed tasks are selected; include referenced prerequisites and normative inputs. Each task waits for the preceding listed task's acceptance plus explicit prerequisites. Reject unknown references and cycles; do not infer dependencies from names. Partial scope cannot bypass prerequisites; an empty selection is NO_WORK. Tasks are serial by default; parallel execution needs explicit authorization and coordinated ownership/interfaces.

Keep shared constraints in `project.md` and shared/final scenarios in `verification.md`. Clarify broad scenarios' pass rules before execution without changing requirements. Checks may be developed during implementation without frozen inventories or approval receipts. Repository-relative output paths resolve from the repository root; material ambiguity blocks execution. Format validity and app acceptance are separate conclusions.

## Records

One implementation effort owns `.suite/<NNN>_<name>/`: `implementation.json`, `tasks/<task-id>/{plan,acceptance}.md`, `runs/<task-id>/<agent-run-id>/` and `reports/`. Allocate once with `python spec-source-suite/helpers/records.py allocate NAME` (serialized local allocation); fresh implementations receive new numbers, while resumes and repairs reuse the identified root. Preserve historical records in place. Use `orchestration` for supervisor activity and `validation` for final validation; these are identities, not planning stages. Record authority, sources, prerequisites, target and destinations in task documents; preserve approved originals.

Pass the implementation root through every handoff. `implementation.json` version 2 records explicit native sources/selected turns and append-only task/role/session bindings; the [records helper](helpers/records.py) supplies source/bind commands. Record assignment changes for new turns, retaining native identity and agent-run ID across follow-ups. Replacements have distinct identities. Native evidence supplies spawn/fork/continuation relationships independently of workflow assignments.
Fresh work uses the current brief/bundle and relevant memory, without searching earlier tasks or conversations. Continuing work uses identified task paths or execution references. Resolve a bare task ID under the identified implementation’s immediate `tasks/` directory; ask if the implementation or task is absent, ambiguous, or continuation is unclear. Stop discovery once authority is resolved. Recover missing approved originals from that task's known source/conversation; if unavailable, report locations checked and request the originals rather than inventing them from summaries. Reviewers/validators receive recovered source requirements or acceptance only, never the recovery conversation. In Plan mode present full drafts and state deferred saving; save approved text once editing is available before implementation or handoff.

Resume from complete identified records, findings and current artifacts. Reassess stale or missing evidence; preserve useful failure evidence and resolutions. Retain role handles and artifact paths so corrections return to the same task planner and implementation repairs to the same implementer while available. If a session is unavailable, restore that role from its allowed saved inputs and disclose the replacement; never claim an unavailable session was retained.

Handoffs include the implementation root and supply exact paths, absolute or relative to an explicit root, for the recipient's shared/role guidance and allowed specifications, acceptance, candidate and evidence. Include plans and memory only for permitted roles. Recipients read supplied paths directly; discover only unresolved inputs under the selection/recovery rules above. Paths identify inputs; their contents still must be read.

## Project memory

Ordinary planners and implementers read `<project-root>/.agents/memory/index.md` and only relevant `entries/*.md`; missing memory means no notes yet. Use short retrieval hints and ordinary Markdown lessons with source pointers, without a required metadata schema. Requirements and current repository facts outrank advice; verify stale advice without searching unrelated history. At completion or a blocked stop save supported useful lessons, merge duplicates and correct stale advice. Initialize only for a useful lesson; omit transcripts, progress logs, speculation, secrets and copied configuration. Pass relevant paths to later ordinary task workers. Supervisors relay paths without loading detailed notes. Reviewers, validators and all reconstruction workers exclude memory and copies.

## Reconstruction

Rebuilding without prior implementation uses a new workspace and fresh allowed-input contexts for every role, including the supervisor. Cross-target reconstruction preserves required behavior; porting with prior code is a different claim. Define approved behavior, target, retained assets/data/services and compatibility checks. Retained inputs are not reconstructed outputs. Preserve required outcomes, thresholds and fixtures; invocation can change by target without weakening them.

Export only approved requirements, acceptance, public contracts/examples, permitted retained inputs and relevant suite guidance. Exclude prior implementation, build products, repository history, old plans, conversations, caches containing prior implementation and all memory/copies. Reject traversal and symlink escapes; keep credentials out of exports/logs. Preserve the source workspace and historical evidence. A worker that already read excluded material must be replaced by a fresh allowed-input context. New plans and code produced within this reconstruction are allowed for their ordinary roles; reviewers/validators still exclude all plans.

Inspect exports and report actual separation across filesystem access, parent instructions, session memory, caches, remotes and network. Procedural separation is the default claim. If enforced isolation is required, apply and test controls for the declared boundary, including excluded inputs and reviewer results; unavailable controls block that requirement. Instructions or a new directory do not enforce isolation. Known prior-code leakage invalidates reconstruction claims; ordinary conformance can be reported separately. Resume only this reconstruction's work and label it resumed. Check retained real dependencies and report target changes, retained boundaries, controls/limits and observed conformance. Finite checks do not establish universal equivalence or reconstruction reliability.

## Results and usage references

Every role returns available native session/turn IDs and source paths, including repairs and blocked work, for the manifest bindings. Supply workflow context absent from native evidence; tools capture execution details and adapters calculate usage. Keep review/validation inputs independent of conversations; the supervisor uses reports, not raw logs. Missing telemetry is a reporting limitation, never an app acceptance blocker; unknown measurements remain unavailable.
Use this common result outline, omitting inapplicable fields. Keep review/validation inputs free of plans, conversations and memory even when forwarding results.

- **Scope and candidate:** source/acceptance paths, implementation location/revision, dependencies.
- **Role and status:** PASS, FAIL, BLOCKED or NOT_RUN; rationale and unfinished work.
- **Model routing:** chosen profile, selection reason, requested model/reasoning, observed settings when available, and any host-default fallback or known mismatch.
- **Requirement-linked checks:** ID, command/method, working directory, exit/outcome and evidence; manual checks identify authority and inspected artifact. Separate execution outcomes from coverage judgment and cleanup errors from primary failures.
- **Findings and resolutions:** requirement, expected/observed behavior, reproduction, repair and remaining actionable findings. Preserve useful failures.
- **Coverage and blockers:** substitutes, skipped checks, remaining gaps and required decisions.
- **Independent review/validation:** fresh session/result paths, prior findings resolved; review findings remain distinct from the supervisor's acceptance decision.
- **Assembled app:** final execution evidence or why incomplete; omit for task-only/document results.
- **Usage:** source references/report links, known totals and per-role/session breakdowns, missing counters and limits.
- **Reconstruction:** allowed/retained inputs, target changes, actual isolation controls, exclusions/leakage and limits.

Document-only results describe document validation, not app execution. Historical records remain intact; new results identify the candidate actually checked.
