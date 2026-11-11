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
  - Report requirement, authority and capability blockers under [BUNDLE] and [CHECKS] without prompting.
  - Stop on [BUNDLE]'s `NO_PROJECT`, `NO_WORK` or blocked inputs.
  - Use new paths for initial work.
  - Extend selected code for incremental work.
  - Allocate or resume records under [RECORDS] before dispatch.
  - Maintain [execution state](#execution-state) throughout coordination.
  - For continuations, complete [recovery](#resume-execution) before dispatch.
  - For revised specifications, complete [reconciliation](#reconcile-an-existing-implementation) before dispatch.
  - Select the [task mode](#task-mode) before dispatching each new task whose prerequisites are accepted.
  - Prepare the Assignment with [IMPLEMENTER]'s named inputs and role instructions under [RECORDS] (“Hand off work”).
  - Spawn a fresh Implementer without inherited conversation for every new task, including single-task scopes.
  - Run ready tasks concurrently while reserving capacity for full-task Reviewers and final validation.
  - Break ties by table order.
  - Blocked tasks do not hold unrelated work.
  - Resolve overlapping edits and interface changes before writing.
  - Return affected plans, checks and reviews to their owners under [RECORDS].
  - Route plan-review handoffs through [Review a task](#review-a-task).
  - Read each worker's saved Result and any required independent review before accepting the task.
  - Inspect detailed evidence when those records are incomplete, conflict or leave an acceptance question open.
  - Accept tasks under [CHECKS] before unlocking their dependents.
  - Return defects to the same Implementer for correction and rechecks.
  - Reassess affected downstream evidence under [CHECKS].
  - Stop when all remaining tasks are blocked.
  - After all selected tasks pass in either mode, [validate the assembled app](#validate-the-assembled-app).
  - Use [TRACING] (“Report usage”) when finished, blocked or requested, and for trace issues.
  - Save Result and available Evidence under [RECORDS] (“Return work”) when finished, blocked, cancelled or limited.
  - Distinguish selected-scope from whole-app acceptance in Result.
- Outputs: Assignments, Execution state and Result.

## Review a task

- Context: apply when a plan-review Implementer returns a Result ready for review.
- Inputs: Implementer handle, saved Result and Evidence, and the named inputs in [REVIEWER].
- Effects:
  1. Confirm the Implementer's turn has ended and all other affected writers are paused.
  2. Record the review phase in [execution state](#execution-state) and retain the Implementer handle.
  3. Spawn a fresh Reviewer with the permitted inputs under [RECORDS] and [CHECKS] and confirmation that affected writers are paused.
  4. When the Reviewer returns, read the saved Result and record its path in [execution state](#execution-state).
  5. Record the acceptance or correction decision and any blockers under [CHECKS] using both saved Results.
  6. Explicitly release affected writers before further edits.
- Outputs: Reviewer Result and updated Execution state.
- Next:
  - Resume the same Implementer session only for actionable review findings.
  - Use the host's follow-up action with the findings, Result path and explicit release to edit.
  - If the original Implementer is unavailable, apply [Resume execution](#resume-execution) when assigning corrections.
  - Start a fresh review after the corrected candidate is handed off.

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

## Execution state

Apply when coordinating an implementation or recovering its execution.

- Keep one `execution-state.md` at the implementation root allocated under [RECORDS].
- Keep the Supervisor as its sole writer.
- Record the specification bundle location and selected task scope.
- Record each task's status, mode, workspace, last execution phase and available worker handles.
- Record interfaces and file ownership, including shared configuration.
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
  3. Recover missing or incomplete state from saved sources and results, including results saved before checkpoint updates.
  4. Reconcile task statuses with files, results and available workers, marking stopped, incomplete work as interrupted.
  5. Reassess affected tasks, dependents and final validation under [CHECKS], preserving acceptance where evidence remains current.
  6. Resolve uncertain worker ownership before allowing a replacement writer.
  7. Inspect failed or interrupted work before choosing its continuation phase.
  8. Resolve uncertain persistent or external effects before retrying.
  9. Have Validator reuse the saved result and repair reservation to complete only missing publication parts before dispatch.
  10. Refresh the graph after repair publication changes the dependency table.
  11. Give replacements specifications, permitted saved artifacts, findings and continuation notes under [RECORDS].
  12. Save reconciled state before resuming from the recorded phase when prerequisites are accepted and blockers resolved.
- Outputs: continuation Assignments, reconciled Execution state and Result.
- Next: continue coordination and outstanding validation under the existing acceptance rules.

### Recovery rules

Apply throughout recovery.

- Reuse available owners, task IDs, workspaces, approved documents and implementation records.
- Treat dependent tasks waiting for prerequisites as blocked rather than failed.
- Make repeated resume against unchanged files and evidence preserve acceptance without duplicate dispatch, repairs or unnecessary checks.
- Report unresolved scope, conflicting evidence or missing workspaces as blockers for affected work.

## Validate the assembled app

- Context: apply [CHECKS] and [VALIDATOR].
- Inputs: Assignment, Project specification, selected Task specifications, Task order, Contracts, Verification, Implementation, Results and Evidence; Acceptance for plan-review tasks.
- Effects:
  - Confirm affected writers paused.
  - Spawn a fresh Validator with an Assignment and its named inputs under [RECORDS] and [CHECKS].
  - Read the saved Validator Result and inspect detailed evidence when it is incomplete, conflicts with other records or leaves an acceptance question open.
  - Explicitly release affected writers after validation and before further edits.
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

- Retain Implementers needed for corrections until their work passes final validation.
- Close completed workers through the host's close action after saving results and resolving correction needs.
- Record closed worker handles in execution state.
- Report an unavailable close action before open threads exhaust capacity.
- Wait for workers only through the host's native worker wait when the next decision depends on them.
- Resume waiting after a timeout unless a deadline, blocker or ready task calls for action.
- Use host progress reports unless a specific decision or blocker requires contacting workers or inspecting unfinished work.

## Task mode

Apply when choosing the assigned Implementer's procedure under [IMPLEMENTER].

- Use the task's `Workflow: plan-review` or `Workflow: direct` field when present.
- When the field is omitted, choose the mode below independently of model choice.

| Condition | Mode |
|---|---|
| Required planning/review, complex work, or uncertainty | `plan-review` |
| Simple, bounded work with clear source criteria | `direct` |
