# Spec Source Suite — shared rules

This package supplies instructions, blank templates and a usage helper, not a selected app or automated runner. Keep app inputs, code, memory and evidence outside it. Read this file plus exactly your role routine as operative suite guidance:

| Role | Routine | Responsibility |
|---|---|---|
| Supervisor | [SUPERVISOR.md](SUPERVISOR.md) | Schedule and collect outcomes |
| Planner | [PLANNER.md](PLANNER.md) | Author documents or prepare one ready task |
| Implementer | [IMPLEMENTER.md](IMPLEMENTER.md) | Implement, check and own fresh reviews |
| Reviewer | [REVIEWER.md](REVIEWER.md) | Independently check one candidate |
| Validator | [VALIDATOR.md](VALIDATOR.md) | Independently check the assembled app and specify repairs |

Spec implementation always uses the Supervisor's full project workflow, including single-task selections. Load roles directly; named skills are optional. Explicit `spec-planner` and `spec-supervisor` invocations use `.agents/skills/`. Document-only work uses the Planner and stops before execution. Only requested automated-runner work reads [RUNNER.md](RUNNER.md). Suite maintenance follows user acceptance and checks links, entry points and relevant tests. Documentation walkthroughs are not live app experiments. When adopting these procedures, merge repository instructions and verify worker capabilities; CLI flags and isolation are host-dependent.

## Workflow maintenance

For suite changes, keep operative guidance in this file plus one routine per role. Put common rules here and role-specific procedures with their role. Give each rule one authoritative home; reference it instead of repeating it. Prefer replacing or removing instructions when adding guidance. Add a file only when existing boundaries cannot accommodate its responsibility, and explain why.

Before completion, run `python spec-source-suite/helpers/check_package.py` from the repository root to check required guidance/templates, skill entry points/policies and local links/anchors. Additional valid files are allowed; no Git history is required. Legacy `--base VALUE` is accepted with a removal notice and performs no baseline comparison.

Review changed instructions for behavior, duplication and role placement. Confirm each role can operate with shared guidance, its own routine and routing configuration; record material exceptions in the result.

Index only persistent Markdown documentation, with explicit relative-path links and short purposes or read conditions. Update the applicable index when documentation is added, moved, renamed, or removed. Exclude transient task plans, acceptance records, run artifacts and review reports from indexes.

Workflow guidance belongs in the root file index. Persistent project documents and memory belong in their applicable scoped indexes. Create a scoped index only when none exists, and link it from its parent index. Indexing does not authorize loading material excluded from a role's context.

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

Save the task plan and separate source-linked acceptance before implementation, with depth appropriate to its workflow below. Required unavailable capabilities block acceptance; skipped checks are NOT_RUN or BLOCKED, observed violations are FAIL, never weakened expectations. Use proportionate observable checks, relevant regressions and required manual/real-dependency checks. Reuse meaningful tests and cover gaps through public interfaces; avoid tests that assert their own mock outputs, implementation details, or test-only production hooks. Record substitute limits and remaining coverage gaps.

A task passes only with successful required checks, adequate requirement coverage and no unresolved actionable findings. Where task review is required, it must be fresh and independent; missing review is INDEPENDENT_REVIEW_NOT_RUN and blocks acceptance. Failed or blocked prerequisites never unlock consumers. Changed sources, dependencies or implementation require reassessing affected results and repeating applicable checks/review. Final independent validation is required after scheduled tasks pass in either task workflow; task passes alone do not establish whole-app acceptance. Cancellation, applicable limits, conflicts or unavailable capabilities preserve unfinished results and blockers.

## Task workflows

Before implementation, the implementer assesses logic, component interactions, compatibility/data-loss risks and verification effort. Complex tasks require `full` regardless of certainty; only simple tasks qualify for `lightweight`. Default to `full` and honor explicit source/user requirements. Record the assessment and mode in the plan and results; report them to the supervisor. Unresolved requirements block either mode. Model profiles do not select workflows.

| Mode | Planning owner | Task review |
|---|---|---|
| `full` | Separate fresh planner; full plan and acceptance | Fresh independent review required |
| `lightweight` | Implementer; concise plan and separate acceptance, unless a planner is assigned | Optional unless explicitly required; a chosen optional review needs a concrete reason; omission is not a review PASS |

The planning owner handles planning/acceptance corrections. Both modes follow all shared acceptance, engineering, record and usage rules. Concise plans retain authority, sources, prerequisites, approach, target and evidence paths; acceptance maps every requirement to checks/pass rules, including shared verification and coverage limits. Reassess changed scope or implementation demands; complexity requires escalation to full, preserving records and completing its gates. Explicit approval/review requirements remain binding.

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

One implementation owns `.suite/<NNN>_<name>/`: `native/<session-id>/<turn-id>.jsonl`, `tasks/<task-id>/{plan,acceptance}.md`, `runs/<task-id>/<agent-run-id>/` and `reports/`. Allocate before task work with `python spec-source-suite/helpers/records.py allocate NAME` (serialized locally by locking the suite directory). Fresh implementations receive new numbers; resumes and repairs reuse their root. Keep new records there, using source filename stems as task IDs in documents, assignments and run paths. Preserve approved originals and history in place. Reserve `orchestration` for supervisor activity and `validation` for final validation, not planning stages. Task documents identify authority, sources, prerequisites, target and destinations.

Allocation saves the current session metadata and active native turn; on resume, run `python spec-source-suite/helpers/records.py resolve IMPLEMENTATION TASK` to resolve the task and save that turn. Pass the implementation root through every handoff and include one structured line, substituting its implementation name, source task ID and recipient role:

```text
SUITE {"implementation":"001_todolist","task":"01_business_logic","role":"implementer"}
```

An optional `purpose` describes the assignment. Recipients also emit their assigned line in local commentary so encrypted handoffs retain readable attribution. Follow-ups retain assignments unless explicitly retagged; replacements retain their distinct native identities. For selected Supervisor turns, emit the line with `supervisor` / `orchestration`; final validation uses `validator` / `validation`. The helper discovers descendants through native dispatches and identities. Missing tags leave task/role unavailable unless explicitly recovered through [assignment annotations](helpers/TRACING.md#assignment-recovery), without discarding measured usage. Keep native logs local; reports contain measurements and metadata, not prompts or tool content.

Fresh work uses the current brief/bundle and relevant memory, without searching earlier tasks or conversations. Continuing work uses identified task paths or execution references. Resolve a bare task ID under the identified implementation’s immediate `tasks/` directory; ask if the implementation or task is absent, ambiguous, or continuation is unclear. Stop discovery once authority is resolved. Recover missing approved originals from that task's known source/conversation; if unavailable, report locations checked and request the originals rather than inventing them from summaries. Reviewers/validators receive recovered source requirements or acceptance only, never the recovery conversation. In Plan mode present full drafts and state deferred saving; save approved text once editing is available before implementation or handoff.

Resume from complete identified records, findings and current artifacts. Reassess stale or missing evidence; preserve useful failure evidence and resolutions. Retain role handles and artifact paths so corrections return to the same task planner and implementation repairs to the same implementer while available. If a session is unavailable, restore that role from its allowed saved inputs and disclose the replacement; never claim an unavailable session was retained.

Handoffs include the implementation root and supply exact paths, absolute or relative to an explicit root, for the recipient's shared/role guidance and allowed specifications, acceptance, candidate and evidence. Include plans and memory only for permitted roles. Recipients read supplied paths directly; discover only unresolved inputs under the selection/recovery rules above. Paths identify inputs; their contents still must be read.

## Coordination and checking

Use native waits and completion notifications, choosing the longest wait allowed by host limits and required user-update intervals. A timeout alone calls for continued waiting, not worker prompting or escalation. Routine status prompts, short polling loops, sleep-based monitoring and repeated agent-list checks are excluded. Use a runtime status snapshot only to resolve concrete uncertainty, such as a failed operation or missing completion notification. Host scheduling may still wake the parent.

Send worker messages for inputs, decisions, assignment changes, blockers and repairs. Workers report blockers and required decisions promptly; report completion once with the result path. Keep required user updates brief and based on known information.

Batch independent reads and commands; print only needed matches, fields and tool descriptions. Pass paths instead of copied documents. Supervisors consume concise results; workers read their allowed sources directly. Run each role's required checks together; repeat successful checks only after relevant changes, failures, new concerns or a required independent check. Reviewers and validators still perform their own independent inspections and executions.

Keep the candidate unchanged during review and validation, identified by location and revision when available. Changes invalidate affected results under the acceptance rules. Use existing version information without forcing commits or adding a locking service.

## Project memory

Ordinary planners and implementers read `<project-root>/.agents/memory/index.md` and only relevant `entries/*.md`; missing memory means no notes yet. Use short retrieval hints and ordinary Markdown lessons with source pointers, without a required metadata schema. Requirements and current repository facts outrank advice; verify stale advice without searching unrelated history. At completion or a blocked stop save supported useful lessons, merge duplicates and correct stale advice. Initialize only for a useful lesson; omit transcripts, progress logs, speculation, secrets and copied configuration. Pass relevant paths to later ordinary task workers. Supervisors relay paths without loading detailed notes. Reviewers, validators and all reconstruction workers exclude memory and copies.

## Reconstruction

Rebuilding without prior implementation uses a new workspace and fresh allowed-input contexts for every role, including the supervisor. Cross-target reconstruction preserves required behavior; porting with prior code is a different claim. Define approved behavior, target, retained assets/data/services and compatibility checks. Retained inputs are not reconstructed outputs. Preserve required outcomes, thresholds and fixtures; invocation can change by target without weakening them.

Export only approved requirements, acceptance, public contracts/examples, permitted retained inputs and relevant suite guidance. Exclude prior implementation, build products, repository history, old plans, conversations, caches containing prior implementation and all memory/copies. Reject traversal and symlink escapes; keep credentials out of exports/logs. Preserve the source workspace and historical evidence. A worker that already read excluded material must be replaced by a fresh allowed-input context. New plans and code produced within this reconstruction are allowed for their ordinary roles; reviewers/validators still exclude all plans.

Inspect exports and report actual separation across filesystem access, parent instructions, session memory, caches, remotes and network. Procedural separation is the default claim. If enforced isolation is required, apply and test controls for the declared boundary, including excluded inputs and reviewer results; unavailable controls block that requirement. Instructions or a new directory do not enforce isolation. Known prior-code leakage invalidates reconstruction claims; ordinary conformance can be reported separately. Resume only this reconstruction's work and label it resumed. Check retained real dependencies and report target changes, retained boundaries, controls/limits and observed conformance. Finite checks do not establish universal equivalence or reconstruction reliability.

## Results and usage references

Keep separate plan/acceptance documents and one concise result per role/run using the outline below; save extra logs and explanations when useful, preserving repair history and failures. Routine candidate manifests, checksum lists, duplicate check summaries and repeated hash sweeps are excluded; functional identity, deduplication and regression hashes remain valid.

Roles link derived usage reports and coverage limitations, including repairs and blocked work, without maintaining token totals. The supervisor generates aggregate reports at overall completion or a blocked stop; earlier refreshes are on request. Native capture and assignment handling continue throughout; adapters calculate usage. Missing telemetry is a reporting limitation, never an app acceptance blocker; unknown measurements remain unavailable. Omit inapplicable outline fields and keep forwarded review/validation results free of plans, conversations and memory.

- **Scope and candidate:** source/acceptance paths, implementation location/revision, dependencies.
- **Role and status:** PASS, FAIL, BLOCKED or NOT_RUN; rationale and unfinished work.
- **Model routing:** chosen profile, selection reason, requested model/reasoning, observed settings when available, and any host-default fallback or known mismatch.
- **Requirement-linked checks:** ID, command/method, working directory, exit/outcome and evidence; manual checks identify authority and inspected artifact. Separate execution outcomes from coverage judgment and cleanup errors from primary failures.
- **Findings and resolutions:** requirement, expected/observed behavior, reproduction, repair and remaining actionable findings. Preserve useful failures.
- **Coverage and blockers:** substitutes, skipped checks, remaining gaps and required decisions.
- **Independent review/validation:** fresh session/result paths, prior findings resolved; review findings remain distinct from the supervisor's acceptance decision.
- **Assembled app:** final execution evidence or why incomplete; omit for task-only/document results.
- **Usage:** aggregate report references when available, missing counters and coverage limits.
- **Reconstruction:** allowed/retained inputs, target changes, actual isolation controls, exclusions/leakage and limits.

Document-only results describe document validation, not app execution. Historical records remain intact; new results identify the candidate actually checked.
