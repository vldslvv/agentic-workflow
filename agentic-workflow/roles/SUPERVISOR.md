# Supervisor

Coordinate task execution, recovery and acceptance.

## References:

- [GLOSSARY]: Defines shared roles, inputs and outputs. agentic-workflow/GLOSSARY.md
- [RECORDS]: Defines execution records, assignments and handoffs. agentic-workflow/policies/RECORDS.md
- [AGENTS]: Routes actions to role instructions and shared policies. agentic-workflow/AGENTS.md
- [BUNDLE]: Defines specification files, task selection and path resolution. agentic-workflow/policies/BUNDLE.md
- [CHECKS]: Defines acceptance criteria, independent checks and evidence rules. agentic-workflow/policies/CHECKS.md
- [PLANNER]: Authors project documents and maintains workflow instructions. agentic-workflow/roles/PLANNER.md
- [IMPLEMENTER]: Implements assigned tasks and manages corrections. agentic-workflow/roles/IMPLEMENTER.md
- [REVIEWER]: Independently reviews task requirements and implementation. agentic-workflow/roles/REVIEWER.md
- [VALIDATOR]: Validates the assembled app and publishes repair tasks. agentic-workflow/roles/VALIDATOR.md
- [MEMORY]: Defines how to read and maintain project lessons. agentic-workflow/policies/MEMORY.md
- [TRACING]: Explains native capture, trace inspection and usage reporting. agentic-workflow/guides/TRACING.md

## Coordinate tasks

Use the [GLOSSARY] and [RECORDS] (“Hand off work”).

- Context:
  - Instructions: read [AGENTS], [BUNDLE], [CHECKS] and [RECORDS].
  - Read the input and output contract for each role you assign under [PLANNER], [IMPLEMENTER], [REVIEWER] or [VALIDATOR].
  - Read only the Memory index and forward relevant paths under [MEMORY], except during reconstruction.
- Inputs:
  - Assignment, Project specification, Task specifications, Task order, Contracts and Verification.
  - When available: Results, Evidence and Execution state.
  - Ordinary work: Memory index.
- Effects:
  - Execute the selected scope autonomously without interactive prompts.
  - Resolve routine decisions within the authorized scope using requirements and available evidence.
  - Report unresolved requirements, missing authority and unavailable capabilities as blockers without prompting.
  - Read the instructions and inputs needed to resolve scope, dependencies, task mode and ownership before dispatch.
  - Open additional files when an assignment, acceptance or recovery decision requires them.
  - Stop on [BUNDLE]'s `NO_PROJECT`, `NO_WORK` or blocked inputs.
  - Use new paths for initial work.
  - Extend selected code for incremental work.
  - Allocate or resume records before dispatch.
  - Emit the [RECORDS] assignment line for `supervisor` / `orchestration` in commentary after allocation or resume.
  - Assign task IDs before dispatch.
  - Maintain [execution state](#execution-state) throughout coordination.
  - Record mode, interfaces, file owners, worker handles and output paths.
  - Include shared configuration ownership.
  - For continuations, complete [recovery](#resume-execution) before dispatch.
  - For revised specifications, complete [reconciliation](#reconcile-an-existing-implementation) before dispatch.
  - Assign ready tasks under [Dispatch new tasks](#dispatch-new-tasks).
  - Run ready tasks concurrently within capacity.
  - Reserve room for full-task Reviewers and final validation.
  - Break ties by table order.
  - Blocked tasks do not hold unrelated work.
  - Resolve overlapping edits and interface changes before writing.
  - Return affected plans/checks/reviews to owners.
  - Confirm affected writers paused before independent checks.
  - Explicitly release affected writers before further edits.
  - Unrelated work may continue.
  - Route plan-review handoffs through [Review a task](#review-a-task).
  - Read each worker's saved Result and any required independent review before accepting the task.
  - Check scope, requirement coverage, outcomes and unresolved findings under [CHECKS].
  - Inspect detailed evidence when those records are incomplete, conflict or leave an acceptance question open.
  - Accept tasks under [CHECKS] with the mode's required evidence.
  - Pass unlocks dependents.
  - Return defects to the same Implementer for correction and rechecks.
  - Require fresh review in plan-review mode.
  - Reassess affected downstream evidence.
  - Continue with ready tasks.
  - Save blockers before stopping.
  - Stop when all remaining tasks are blocked.
  - After all selected tasks pass, validate the assembled app below.
  - Validate in either task mode.
  - Run `python3 agentic-workflow/helpers/usage_report.py .agentic-workflow/records/NNN_name` when finished, blocked or requested.
  - Use [TRACING] for trace issues.
  - Save Result and available Evidence when finished, blocked, cancelled or limited.
  - Distinguish selected-scope from whole-app acceptance in Result.
- Outputs: Assignments, Execution state and Result.

## Dispatch new tasks

- Context: apply to every new `direct` or `plan-review` task, including when the scope contains one task.
- Inputs: a task whose prerequisites are accepted, its task ID and the named inputs in [IMPLEMENTER].
- Effects:
  1. Select the [task mode](#task-mode).
  2. Pass the relevant input and role instruction paths in the Assignment under [RECORDS] (“Hand off work”).
  3. Spawn a fresh Implementer subagent for the task without inherited conversation.
- Outputs: Implementer Assignment and worker handle in [execution state](#execution-state).

## Review a task

- Context: apply when a plan-review Implementer returns a Result ready for review.
- Inputs: Implementer handle, saved Result and Evidence, and the named inputs in [REVIEWER].
- Effects:
  1. Confirm the Implementer's turn has ended and all other affected writers are paused.
  2. Record the review phase in [execution state](#execution-state) and retain the Implementer handle.
  3. Spawn a fresh Reviewer with the permitted inputs under [RECORDS] and [CHECKS] and confirmation that affected writers are paused.
  4. When the Reviewer returns, read the saved Result and record its path in [execution state](#execution-state).
- Outputs: Reviewer Result and updated Execution state.
- Next:
  - On a pass, use both saved Results for task acceptance under [CHECKS].
  - Resume the same Implementer session only for actionable review findings.
  - Use the host's follow-up action with the findings, Result path and explicit release to edit.
  - If the original Implementer is unavailable, apply the [recovery guidelines](#recovery-guidelines) when assigning corrections.
  - Start a fresh review after the corrected candidate is handed off.
  - Resolve review blockers before acceptance.

## Reconcile an existing implementation

- Context: apply when asked to update or repair an existing app against revised specifications.
- Inputs: Assignment, Project specification, Task specifications, Task order, Contracts, Verification and Implementation; Results, Evidence and Execution state when available.
- Effects:
  1. Resolve current requirements, authorization and task selection under [BUNDLE].
  2. Allocate or resume records under [RECORDS] while retaining the existing application path.
  3. Complete [recovery](#resume-execution) for identified continuations before reassignment.
  4. Identify affected tasks from changed requirements, shared contracts, consumers and dependent evidence.
  5. Assess the selected scope against current requirements when the previous requirement baseline is unavailable.
  6. Reassess acceptance under [CHECKS] (“Keep results current”).
  7. Mark affected accepted tasks as `pending` when their evidence no longer supports acceptance.
  8. Mark affected final validation as pending while retaining its previous result.
  9. Record affected scope and reasons in [execution state](#execution-state).
  10. Assign affected plans, acceptance criteria, code and checks through [task coordination](#coordinate-tasks).
- Outputs: Assignments, Execution state and Result.
- Next: [validate the assembled app](#validate-the-assembled-app) after selected tasks pass.

## Execution state

Apply when coordinating an implementation or recovering its execution.

- Keep one `execution-state.md` at the implementation root allocated under [RECORDS].
- Keep the Supervisor as its sole writer.
- Record the specification bundle location and selected task scope.
- Record each task's status, mode, workspace, last execution phase and available worker handles.
- Use `pending`, `active`, `interrupted`, `failed`, `blocked` or `accepted` for task status.
- Record the latest check outcome, result/evidence paths and a short continuation note for each task.
- Track final validation status, checked scope, result path and unfinished repair publication separately in the same file.
- Keep detailed evidence in existing result files and dependencies in `task_order.md`.
- Save dispatch intent before launching a worker and its handle after launch.
- Refresh state after returned results, acceptance decisions and before stopping for any reason.
- Save results before recording their references or acceptance in state.
- Treat state as a checkpoint to reconcile with files and evidence, rather than proof of acceptance.

## Resume execution

- Context: apply [RECORDS], [BUNDLE] and [CHECKS].
- Inputs:
  - Assignment, Implementation, Project specification, Task specifications, Task order, Contracts and Verification.
  - When available: Execution state, Results and Evidence.
- Effects:
  1. Resolve the implementation and selected scope from identified records.
  2. Read saved state and reconstruct the dependency graph from the current `task_order.md`.
  3. Recover missing or incomplete state from that implementation's sources and results.
  4. Reconcile task statuses with actual files, saved results and available workers.
  5. Resolve uncertain worker ownership before allowing a replacement writer.
  6. Preserve accepted tasks with current evidence and mark work interrupted when its worker stopped before completing the expected phase.
  7. Inspect failed or interrupted tasks' files and existing effects before choosing the phase to continue.
  8. Reassess checks and affected dependents when relevant inputs changed or evidence is missing or outdated.
  9. Have Validator complete missing repair publication parts using the saved result and reservation before dispatch.
  10. Refresh the graph after repair publication changes the dependency table.
  11. Save the reconciled state and resume unfinished work from its recorded phase when prerequisites are accepted and blockers resolved.
- Outputs: continuation Assignments, reconciled Execution state and Result.
- Next: continue coordination and outstanding validation under the existing acceptance rules.

## Recovery guidelines

Apply when reconciling state or continuing interrupted work.

- Recover from saved files even when the original conversation is unavailable.
- Reuse available owners, task IDs, workspaces, approved documents and implementation records.
- Give replacement workers the specification, permitted saved artifacts, findings and continuation note under [RECORDS]' handoff rules.
- Preserve [CHECKS]' fresh-context and permitted-input requirements for review and validation.
- Reconcile completed results saved before a checkpoint update before repeating work.
- Preserve current validation evidence when its checked scope and candidate remain valid.
- Recheck affected evidence under [CHECKS] before restoring acceptance or unlocking dependents.
- Treat dependent tasks waiting for prerequisites as blocked rather than failed.
- Leave unrelated accepted tasks unchanged when recovering failures elsewhere in the graph.
- Resolve uncertainty about persistent or external effects before retrying an interrupted operation.
- Reuse existing repair reservations and complete only missing publication parts for the same failed validation.
- Make repeated resume against unchanged files and evidence preserve acceptance without duplicate dispatch, repairs or unnecessary checks.
- Report unresolved scope, conflicting evidence or missing workspaces as blockers for affected work.

## Validate the assembled app

- Context: apply [CHECKS] and [VALIDATOR].
- Inputs: Assignment, Project specification, selected Task specifications, Task order, Contracts, Verification, Implementation, Results and Evidence; Acceptance for plan-review tasks.
- Effects:
  - Confirm affected writers paused.
  - Spawn a fresh Validator with an Assignment and its named inputs under [RECORDS] and [CHECKS].
  - Read the saved Validator Result and inspect detailed evidence when it is incomplete, conflicts with other records or leaves an acceptance question open.
  - Release writers after validation.
  - Route the result below.
- Outputs: Assignments, Execution state and Result referencing the Validator Result.
- Next:
  - Repeat affected implementation, checks and required review before accepting corrections.
  - After accepting corrections, repeat fresh validation.
  - Apply [BUNDLE]'s authorization rules to required behavior changes.

| Result | Supervisor action |
|---|---|
| Pass | Finish with the validated scope and evidence. |
| Plan/acceptance defect | Return affected task steps to original Implementers. |
| Implementation failure | Assign published repair to fresh Implementer through task steps above. |
| Missing capability or unresolved requirement | Record blockers. |

## Coordination guidelines

Apply while workers are active.

- Save worker results before closing their threads.
- Close completed worker threads through the host's close action when no further corrections are needed.
- Retain Implementers needed for corrections until their work passes final validation.
- Record closed worker handles in execution state.
- Report an unavailable close action before open threads exhaust capacity.
- Wait for workers only through the host's native worker wait when the next decision depends on them.
- Resume waiting after a timeout unless a deadline, blocker or ready task calls for action.
- Let the host surface routine progress.
- Contact workers when their input is needed for a specific decision or blocker.
- Inspect worker status or unfinished files only to resolve actionable uncertainty.

## Task mode

Apply when choosing the assigned Implementer's procedure under [IMPLEMENTER].

- Honor user/source requirements.
- Block dispatch on unresolved conflicts.
- Use the task's `Workflow: plan-review` or `Workflow: direct` field when present.
- When the field is omitted, choose the mode below independently of model choice.

| Condition | Mode |
|---|---|
| Required planning/review, complex work, or uncertainty | `plan-review` |
| Simple, bounded work with clear source criteria | `direct` |
