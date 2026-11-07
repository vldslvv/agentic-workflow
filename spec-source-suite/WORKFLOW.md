# Implementation workflow

- Read for any spec implementation, including one task. This contract owns the sequence, role handoffs and shared state; role documents explain how to perform assigned work. Standalone document authoring uses [Planner](PLANNER.md).
- The numbered rules below and their applicable linked policies are the reference for [document review](WORKFLOW_REVIEW.md). Detailed policies stay with their linked owners; this contract adds no app requirements or automatic runner.

## Flow

```text
Supervisor resolves the bundle; stop on NO_PROJECT, NO_WORK or blocked inputs
Supervisor allocates or resumes records and owners
while selected tasks remain:
    Supervisor dispatches dependency-ready tasks, concurrently where possible
    for each task, its Implementer follows the assigned mode:
        full: plan + acceptance -> implement + self-check -> fresh Reviewer
              findings -> same Implementer repairs -> fresh Reviewer again
        lightweight: source criteria -> implement + self-check
    Supervisor accepts results before releasing dependent tasks
    if remaining tasks are blocked: save blockers and stop
Supervisor launches fresh Validator for the assembled app, in either mode
    planning/acceptance defects -> original Implementers -> recheck
    implementation failures -> repair task -> fresh Implementer -> task gates
    after corrections are accepted -> fresh Validator again
save results on completion, blockers, cancellation or limits
```

## Steps

| Rule / owner | Inputs | Outputs | Completion and next step |
|---|---|---|---|
| W1 · Supervisor: resolve | Brief or identified continuation; [Bundle](BUNDLE.md) | Selected tasks, sources, dependencies, target, final-scenario pass rules and [Records](RECORDS.md) root | Resolve required inputs before W2. Bundle defines `NO_PROJECT`, `NO_WORK` and blocked selections. Apply S5 before any reconstruction dispatch. |
| W2 · Supervisor: dispatch | Selected tasks and accepted prerequisite evidence | Assigned mode under [Supervisor](SUPERVISOR.md#task-mode), agreed interfaces/file ownership and a handoff under S1 | Only tasks whose declared dependencies passed acceptance are ready. New tasks get fresh Implementers without inherited conversation; resume existing owners under W8. There is no separate execution planner. Run ready tasks concurrently within capacity, reserving room for full-task reviewers; table order breaks capacity ties. Blocked/failed prerequisites hold consumers while unrelated work continues. |
| W3 · Implementer: execute | Assignment, original requirements, relevant candidate and accepted contracts | Checked candidate and requirement-linked evidence | For full mode, prepare plan and source-linked acceptance before code, then implement/self-check and enter W4. Lightweight uses source criteria directly and goes to W5: no plan, separate acceptance, task reviewer, optional-review branch or automatic mode escalation. |
| W4 · Implementer / Reviewer / Supervisor: review | Full-task candidate, applicable acceptance and S3 inputs | Independent findings and review result | Implementer agrees the boundary with Supervisor; after Supervisor confirms affected writers paused, Implementer launches a fresh [Reviewer](REVIEWER.md). After review, Implementer reports completion and waits for Supervisor's explicit release before writing. Findings return to that Implementer; repeat affected checks and fresh review until ready for W5 or stopped. |
| W5 · Supervisor: accept | Task result, assigned mode and required evidence | Acceptance decision or findings/blockers | Apply [Checks](CHECKS.md). A pass unlocks dependents; ordinary task defects return to the retained Implementer through W3/W4. Reassess affected downstream evidence. All scheduled tasks passing leads to W6, not whole-app acceptance. |
| W6 · Supervisor / Validator: validate | Exact task set/modes, assembled candidate, requirements, applicable acceptance, contracts and factual evidence | Independent final-scenario results | Supervisor launches a fresh [Validator](VALIDATOR.md) in either task mode under S2/S3. Pass completes app validation; findings enter W7. Lightweight tasks need no acceptance document or task-review result. |
| W7 · Validator / Supervisor: route findings | Failed validation and source-grounded findings | Corrections, one repair task per failed pass, or blockers | Missing capabilities/unresolved requirements block; behavior changes need user authority. Planning/acceptance defects return to original Implementers. Implementation failures become one Validator-authored repair depending on every validated task, including earlier repairs, and other required prerequisites. Supervisor assigns that repair a fresh Implementer through W2–W5, then repeats W6. After planning/acceptance corrections, repeat affected task gates and W6 too. |
| W8 · Supervisor / current owners: resume or stop | Identified records, findings and current artifacts | Recovered assignments or final/partial results | Reuse the implementation root and available owners under Records; reassess stale evidence. Validator completes interrupted repair-file/table publication before dispatch. On completion or stopping, each role saves results, evidence and available usage references; preserve unfinished work/blockers. Supervisor distinguishes selected-scope from whole-app acceptance. |

## Shared state

- **S1 · Sources and artifacts:** [Bundle](BUNDLE.md) owns source authority; [Records](RECORDS.md) owns paths, handoff fields and persistence. Create task identities before dispatch. Pass exact paths to sources, guidance, accepted contracts, evidence and outputs; role permissions still apply. Preserve approved originals and history.
- **S2 · Candidate and coordination:** Implementers edit their agreed areas; Supervisor tracks interfaces, owners, agent handles, pauses and artifacts. Resolve overlaps/interface changes before edits and return affected plans/checks/reviews to their owners. Supervisor pauses affected writers for independent checks and explicitly releases them afterward; unrelated work may continue. [Checks](CHECKS.md) defines the stable candidate boundary and fresh rechecks after changes.
- **S3 · Worker context:** Retain Implementers for ordinary corrections; W7 creates a new owner for each validation repair. Unavailable owners are replaced from permitted saved inputs with the replacement disclosed. Independent workers use the fresh-context, inspection-order and allowed-input rules in [Checks](CHECKS.md); handoffs and telemetry cannot bypass those limits.
- **S4 · Project memory:** Carry useful lessons between ordinary tasks using [Memory](MEMORY.md), which defines role access, required reads and permitted updates. Relay paths through Records; memory never changes source authority or independent-worker permissions.
- **S5 · Reconstruction:** Apply [Reconstruction](RECONSTRUCTION.md) to every role before work. Its export, fresh-workspace/context and exclusion rules replace ordinary access to prior implementation state; resume only this reconstruction's records. Report the separation actually achieved.
