# Shared suite contract

Version: 0.2-draft. Normative for Define, Generate, and Implement. MUST marks a gate. This is an instruction-driven procedure; it requires no automated scheduler.

## Applicability: documents and app execution

Choose the procedure from the authorized deliverable. Authoring specification bundles, acceptance criteria, target constraints, or task-order documents is Define work, even when the user says “implement the plan.” Describing future implementation or verification does not authorize executing it.

A documentation-only task completes when its requested documents are approved, saved with approval/baseline identities, and validated for consistency, coverage, references, and dependency structure. It does not require executable app checks, a candidate, an implementer/reviewer cycle, repair rounds, or generation-run evidence. Report deferred execution prerequisites as generation readiness, separately from document completion. Honor existing explicit approvals; request approval only for content not already approved.

Executable-check preparation and freezing require authorized implementation-handoff scope. App implementation/generation requires authorization for that scope; an existing instruction may already provide it. Candidate-oriented roles and gates in §§3–7 apply to app execution. Document approval, reference/DAG validation, and integrity rules continue to apply during Define. A documentation inventory records document identities but does not substitute for the future frozen verifier inventory.

## 1. Authority and project inputs

The suite supplies reusable guidance. A project supplies behavior and constraints in the [standard Markdown bundle](MARKDOWN_BUNDLES.md): `project.md`, `task_order.md`, `tasks/*.md`, and `verification.md`. Keep bundles outside the suite, under `specs/` by default. Keep task handoffs in `.agents/tasks/<NNN>-<task-id>/` and run evidence at the evidence root recorded in `inputs.md`.

Approved task files and their explicitly normative references define behavior. Shared constraints and target choices live in `project.md`; `task_order.md` selects and orders tasks; `verification.md` describes shared checks and assembled-app scenarios. Each task's `acceptance.md` maps source clauses to stable requirement IDs and approved observable checks, referencing source paths and digests. It is a handoff record, not a replacement specification. Freeze the sources and mapping together. Plans explain implementation; they cannot override behavior or acceptance.

Before implementation, require the approved bundle, selected requirement IDs, accepted dependencies, approved target constraints, required assets/retained inputs, frozen checks, authorized output paths, and approval references. Record their identities in the execution input inventory described by the bundle standard. Missing required execution inputs yield BLOCKED; no project intent or specifications yields NO_PROJECT. Blank templates are not approved inputs. Resolve missing choices with the user rather than inventing a domain, stack, or deployment model.

## 2. Task records and approval

Prefix task and run directories with a shared three-digit sequence (`001-`, `002-`, …), allocated from the next unused number across both roots. Keep the logical task ID separate from this storage prefix. Resolve an unprefixed task ID by its directory suffix; use explicit paths to resolve any ambiguity. A relocation preserves approved document bytes and historical evidence, records old-to-new paths, and updates active references.

The planner preserves the complete agreed `plan.md` and authoritative `acceptance.md` under `.agents/tasks/<NNN>-<task-id>/`, plus an approval record identifying the full baseline Git commit, the digests of both documents, approving authority, and the conversation/decision reference. Store the actual approved text, not a handoff summary. Bind referenced normative source digests in the approval record too. Each acceptance record identifies its source task, requirement mapping, and derived prerequisites; a follow-up task references the same source baseline and exact selected requirements.

In Plan mode, present both complete drafts for approval. If writing is unavailable, state that saving is deferred. On entering editing mode, save the approved text exactly and record its approval before implementation or context handoff. If a draft is lost, recover it or ask for it; never recreate it from a summary and label it approved. Approval alone does not start implementation: a separate instruction is required. Existing explicit approvals and implementation instructions remain valid across handoffs.

Approved documents are immutable. Changes require explicit user authorization (or an already explicit delegated approval policy), versioned digests, and invalidation of affected evidence. A worker-written `approved` label is not approval. Significant deviations from the approved plan return to the supervisor before proceeding. Use [CHANGE.md](../templates/CHANGE.md) only when a change is needed.

## 3. Three agents and their handoffs

Each app implementation task uses three agents. Documentation-only Define work uses document review and does not dispatch this implementation cycle:

| Agent | Responsibility | Handoff |
|---|---|---|
| Planner | Prepare the plan, acceptance, and requirement-linked checks; resolve gaps and freeze checks after document approval, before implementation | Both approved documents, approval/baseline record, checks and their digest inventory, accepted dependency inputs, target and ownership |
| Implementer | Build the candidate, run local checks, repair implementation defects, and spawn its reviewer | Acceptance and normative references, baseline/approval identities, selected IDs, dependency evidence, target, candidate location/digest, frozen checks, raw results, reviewer output path |
| Reviewer | Independently assess coverage and execute acceptance on the actual candidate in fresh context | Requirement-linked results, raw execution evidence, review findings, candidate identity |

The supervisor is the coordinating responsibility of the parent session, not a required fourth agent. It schedules work and records acceptance from evidence; it cannot waive gates. The verifier is the frozen check set and its execution arrangement, not a required fourth agent either. The reviewer performs or observes independent execution through that arrangement.

The implementer MUST spawn the reviewer with no inherited conversation (for example, `fork_turns="none"` where supported). Use [REVIEWER.md](../prompts/REVIEWER.md). Exclude the implementation plan, planner/implementer conversation, and persuasive implementation summaries from reviewer inputs. The reviewer may inspect candidate code and raw results. Supply a narrow input allowlist; procedural access does not justify reading excluded files. Missing fresh-context capability yields INDEPENDENT_REVIEW_NOT_RUN and blocks acceptance. Same-session self-review cannot satisfy that gate. A fresh session separates context, not necessarily model reasoning errors.

## 4. Checks and procedural isolation

The planner derives checks from approved requirements and prepares executable checks wherever execution is required. Acceptance must specify setup, inputs, observable assertions, cleanup, pass rule, and evidence; sampling/thresholds must be fixed for nondeterministic behavior. Use the bundle's `verification.md` for shared and assembled-app checks, and task acceptance records for task-specific mappings; reference each mapping rather than duplicating it. Each manual criterion names its authorized authority and inspected artifact. Missing mandatory checks block readiness; an opinion cannot replace required execution.

Freeze a content-digest inventory of documents, checks, fixtures, adapters, and other normative inputs before handing off. Checks may be visible; hidden cases are optional and must test disclosed requirements. Declare any held-out feedback policy. Implementers may add local tests, but cannot edit frozen checks, fixtures, thresholds, approved documents, or reviewer-owned results to obtain a pass. Submit suspected check defects to the supervisor.

Default isolation is **procedural**: scoped file ownership, fresh contexts, and integrity checks. The implementer owns declared candidate paths and local logs; the planner owns acceptance/check inputs; the reviewer owns its reports and acceptance results. Record authorized shared integration paths explicitly. Compare the frozen inventory before and after each implementation/repair and review, and inspect the diff for out-of-scope writes. Any unauthorized baseline change invalidates the attempt; preserve the incident and restore/resolve through the supervisor before restarting evaluation. A digest match detects change; it is not a write sandbox.

Only when enforced isolation is requested, read [STRONG_ISOLATION.md](STRONG_ISOLATION.md). Only for regeneration or a target-changing reconstruction, also read [REGENERATION.md](REGENERATION.md). Ordinary initial and incremental work need neither branch.

## 5. DAG and readiness

Derive the subsystem DAG from `task_order.md` and prerequisites explicitly declared in task prose, following the bundle standard. Persist the derived prerequisites in acceptance records and verify agreement with their source digests. Validate unique IDs, references, required mappings, missing prerequisites, and cycles before dispatch. Unknown dependencies or cycles yield BLOCKED; resolve cycles by approved boundary changes, never by silently removing edges. A semantic cross-reference is not automatically a prerequisite.

Use one subsystem per task and serial execution by default. A node is ready only when every prerequisite is accepted at the required revision and its evidence still applies. FAIL, BLOCKED, NOT_RUN, a stub, or an unreviewed candidate cannot unlock consumers. Scope controls (`only`, `skip`, `start-after`, limits, resume) cannot bypass prerequisites. An empty selection is NO_WORK, not project acceptance.

If explicitly authorized, contract-first parallel work may use approved contracts and coordinated write ownership, but real-dependency integration remains mandatory. Record this exception; do not report stub acceptance as prerequisite acceptance.

## 6. Attempts and failure routing

A task permits **the initial candidate plus two repair rounds**: attempts 0, 1, and 2. Smaller time/cost limits can stop work earlier. There is no automatic attempt 3, and relaunching a session does not reset the count. Preserve each candidate digest, failed checks, findings, and outcome. Every modified candidate needs new review and acceptance evidence, including affected checks and the declared regression set; identify any unchanged checks reused and why their scope is unaffected.

| Finding | Action |
|---|---|
| Confirmed implementation defect | Repair within the remaining two-round allowance; exhausted allowance stops as FAIL with partial evidence |
| Ambiguous or conflicting requirements | Immediately hold affected work as SPEC_CONFLICT/BLOCKED and return to Define through the supervisor |
| Defective or contradictory verifier | Immediately preserve failure and escalate; authorize and freeze a corrected baseline before evaluation resumes |
| Significant plan deviation | Immediately escalate to the supervisor for user resolution before continuing |
| Missing tool/service, timeout, or infrastructure problem | Immediately record INFRA_ERROR/BLOCKED and escalate; do not spend behavioral repair rounds or infer a pass |
| Target incompatible with behavior | BLOCKED pending an explicit decision; no silent downgrade |
| Budget exhaustion/cancellation | Stop with partial evidence and explicit unexecuted gates |

A changed baseline starts a versioned evaluation; it does not erase earlier attempts. Extra work beyond the repair allowance needs explicit authorization recorded by the supervisor.

## 7. Acceptance and evidence

For each mandatory requirement and gate, record PASS, FAIL, BLOCKED, or NOT_RUN with method and evidence. FAIL means an observed mismatch; BLOCKED means a known unmet precondition; NOT_RUN means no assessment occurred. Manual judgments stay distinct from automated results. Empty coverage or zero executed mandatory checks cannot pass.

The supervisor accepts a subsystem only when its prescribed checks, independent review, applicable real-dependency integration, manual gates, and baseline-integrity checks all pass for the actual candidate. No unresolved blocking finding may remain. The project additionally requires acceptance against the assembled app, including cross-subsystem interactions. Passing every node is insufficient if the assembled candidate fails. A partial-scope result names its boundary and retained dependencies.

Keep one run directory outside the suite. A concise [RUN_REPORT.md](../templates/RUN_REPORT.md) with raw outputs and [review findings](../templates/REVIEW.md) is enough; separate logs, JSONL, prompt transcripts, and verification-design reports are optional. Record:

- Task, baseline commit, approval references, selected spec/requirement IDs, and document/check/input digests.
- Dependency revisions, target, suite/prompt revisions, retained inputs, authorized paths, environment/tool versions, actual isolation, and limitations.
- Planner/implementer/reviewer identities and session IDs when available; handoff inputs; timestamps and attempt/resource limits.
- Every candidate revision/digest, executed commands and exit codes or manual observations, requirement/gate results, review findings, failed attempts, interventions, and next action. Cost is optional when unavailable.

Resume only after verifying that relevant spec, dependency, target, checks/adapters, suite/prompts, retained inputs, candidate outputs, and evidence still exist and match recorded identities. A change invalidates affected evidence, including downstream consumers and assembled-app acceptance. Reassess those gates before unlocking work; an old “done” message is insufficient. Report first-attempt results separately from eventual acceptance. Never claim app generation, enforced isolation, or regeneration from documentation walkthroughs.
