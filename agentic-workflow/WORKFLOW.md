# Implementation workflow

This document is the source of truth for how the system works.
It defines responsibilities, inputs, outputs, decisions and transitions independently
of the documents that provide execution instructions.

## References

- Apply [Workflow style](policies/WORKFLOW_STYLE.md) when changing workflow behavior or its documentation.
- Use the [Glossary](GLOSSARY.md) for shared terms.

## Shared responsibilities

Apply to every role and handoff.

- Follow applicable Instructions and the authorized Assignment.
- Give every worker an Assignment stating objective, selected scope, task mode, target, record location and ownership constraints.
- Pass named inputs by path and read them before planning, editing or checking.
- Let each output owner create its record directories before saving outputs.
- Preserve approved requirements and history during corrections.
- Obtain user authority before changing required behavior.
- Save a Result containing status, completed scope, Evidence references, findings, limits and unfinished work.
- Return a short status, Result path and any required decision or blocker.
- Preserve Results and Evidence when finished, blocked, cancelled or limited.
- Select worker settings from the applicable model routing Instructions independently of task mode.
- Record requested and observed settings separately and report unsupported controls.
- Capture available native execution and usage information without blocking acceptance for missing telemetry.
- Keep project specifications, Implementation, Memory and execution records outside the workflow package.

## Author documents — when requested

- Context: Planner applies Instructions for the authorized document work.
- Inputs:
  - Assignment.
  - Relevant existing Project specification, Task specifications, Task order, Contracts, Verification, Plan, Acceptance or Instructions.
  - Implementation and prior Result when applicable.
  - Memory for ordinary work.
- Effects:
  - Planner authors the requested specification types, Plan, Acceptance or Instructions.
  - Define component boundaries and shared Contracts where required.
  - Map Acceptance to original requirements, Contract guarantees and observable check scenarios.
  - Check coverage, consistency, dependencies, links and observable pass criteria.
  - Report unresolved requirements and unavailable checks.
  - For workflow maintenance, check preserved behavior, complete role reading paths and package validity.
- Outputs:
  - Requested Project specification, Task specifications, Task order, Contracts, Verification, Plan, Acceptance or Instructions.
  - Result reporting document validity and generation readiness separately.
  - Memory when useful lessons are saved.
- Next: stop before implementation unless separately authorized.

## Coordinate implementation

- Context: Supervisor applies Instructions and reads subordinate input/output contracts.
- Inputs:
  - Assignment, Project specification, Task specifications, Task order, Contracts and Verification.
  - Results, Evidence and Execution state when available.
  - Memory index for ordinary work.
- Effects:
  - Supervisor resolves the authorized scope, target and task prerequisites.
  - Stop when no project or work is selected, or required inputs are missing or ambiguous.
  - Reject missing tasks, unknown dependencies and dependency cycles.
  - Select tasks with their prerequisites and require current Evidence for accepted prerequisites.
  - Allocate records for new work and resolve existing task records for continuations.
  - Record Supervisor’s orchestration assignment and assign task IDs before dispatch.
  - Start initial Implementation at new paths and extend the selected Implementation for incremental work.
  - Reconcile revised specifications and recover continuations before dispatch.
  - Maintain Execution state for task status, mode, workspace, ownership, worker handles, acceptance and continuation.
  - Track final validation and unfinished repair publication separately from task acceptance.
  - Honor explicit task modes and block unresolved conflicts.
  - Use `plan-review` for required planning/review, complexity or uncertainty.
  - Use `direct` for simple bounded tasks with clear criteria.
  - Dispatch ready tasks with accepted prerequisites concurrently within capacity reserved for review and validation.
  - Break scheduling ties by Task order table order.
  - Resolve overlapping ownership, shared configuration ownership and Contract changes before edits.
  - Return affected Plans, Acceptance, checks and reviews to their owners.
  - Let unrelated work continue when a task is blocked or writers are paused elsewhere.
- Outputs: Assignments, Execution state and Result.

## Implement a task

- Context: Implementer applies Instructions and retains task ownership through corrections.
- Inputs:
  - Assignment, Project specification, assigned Task specification, applicable Contracts and Verification, Implementation.
  - Prior Result and existing Plan and Acceptance when continuing.
  - Memory for ordinary work.
- Effects:
  - Supervisor starts a fresh Implementer per new task without inherited conversation.
  - Implementer agrees on scope and file ownership before concurrent edits.
  - In `plan-review`, write Plan and source-linked Acceptance before Implementation.
  - Include public API Contracts and expected test scenarios in Acceptance.
  - In `direct`, implement and check source criteria without separate Plan, Acceptance or task review.
  - Keep the assigned mode.
  - Implementer checks requirements and regressions, inspects the diff, records Evidence and fixes defects.
  - Rerun checks affected by corrections.
- Outputs:
  - Implementation, Evidence and Result.
  - Plan and Acceptance in `plan-review`.
  - Memory when useful lessons are saved.
- Next:
  - In `plan-review`, Implementer leads independent review.
  - In `direct`, return Result to Supervisor for acceptance.

## Review a plan-review task

- Context: Implementer reads Reviewer’s input/output contract and Supervisor controls writer pauses.
- Inputs:
  - Assignment, Project specification, assigned Task specification, applicable Contracts and Verification, Implementation, Acceptance.
  - Permitted prior Evidence and Result when available.
- Effects:
  - Implementer agrees on the review boundary with Supervisor.
  - Supervisor confirms affected writers paused before Implementer starts a fresh Reviewer.
  - Reviewer checks Implementation and Acceptance against every applicable requirement, Contract and expected scenario.
  - Check omissions, weakened expectations, unjustified constraints, interactions and unintended changes.
  - Assess test coverage, independent expected outcomes, mock justifications and prior fixes.
  - Run relevant checks and reproduce findings where feasible.
  - Keep requirements and Implementation unchanged.
  - Return source-linked findings, reproductions, verified fixes and coverage limits to Implementer.
  - Implementer reports review completion to Supervisor.
  - Supervisor explicitly releases paused writers before corrections.
- Outputs: Evidence and Result.
- Next:
  - The same Implementer corrects actionable findings, reruns affected checks and repeats fresh review.
  - After review passes, Implementer returns Result to Supervisor for acceptance.

## Check and accept work

Apply to check preparation, independent checks and acceptance decisions.

- Derive checks from original requirements, including normal use, boundaries, failures, interactions and lifecycle guarantees.
- Check public API Contracts and use unit and integration tests where they cover distinct risks.
- Run required manual checks and checks against real dependencies.
- Assess internal tests and mocks by the failures they detect and record mock justifications and coverage limits.
- Reject production hooks added only for tests.
- Start every independent review and validation with a fresh context and no inherited conversation.
- Choose independent checks from requirements and Instructions before reading Acceptance or Implementation.
- Limit independent inputs to the assigned requirements, Contracts, Verification, applicable Acceptance, Implementation and factual Results and Evidence.
- Permit focused mock justifications, justified guideline exceptions and prior findings as Evidence.
- Exclude Plans, implementation suggestions, conversations, Memory, design explanations and claims of correctness from independent inputs, including copies in other files.
- Keep the checked Implementation, dependencies, configuration and check inputs unchanged during independent checks.
- Report changes during checking and repeat affected independent checks in a fresh context.
- Require passing checks, adequate requirement coverage and no actionable findings for `PASS`.
- Use `FAIL` for violated requirements or applicable rules and `BLOCKED` for unresolved requirements or unavailable required capabilities.
- Report skipped checks as `NOT_RUN`, or `BLOCKED` when their absence prevents acceptance.
- Block acceptance when required independent review has not run.
- Supervisor reads saved task Results and required independent Results before accepting work.
- Inspect detailed Evidence when Results are insufficient for the acceptance decision.
- Return defects to the same Implementer and reassess affected downstream Evidence.
- Unlock dependents only after Supervisor accepts their prerequisites.
- Reassess affected acceptance when requirements, Instructions, dependencies or Implementation change.
- Repeat successful checks only for relevant changes, failures, new concerns or required independent checks.

## Validate the assembled application

- Context: Supervisor starts fresh validation after all selected tasks pass, in either task mode.
- Inputs:
  - Assignment, Project specification, selected Task specifications, Task order, applicable Contracts, Verification, Implementation, Results and Evidence.
  - Acceptance for plan-review tasks.
- Effects:
  - Supervisor confirms affected writers paused before starting Validator.
  - Validator independently checks assembled-application scenarios, task interactions, real dependencies and required manual checks.
  - Use source criteria for direct tasks.
  - Keep Implementation unchanged and reproduce gaps where feasible.
  - Distinguish Plan or Acceptance defects, implementation failures and unresolved requirements.
  - Publish a repair Task specification and update Task order after implementation failure.
  - Supervisor releases writers after validation and routes the Result.
- Outputs:
  - Evidence and Result.
  - Repair Task specification and updated Task order after implementation failure.
- Next:
  - Pass completes the validated scope.
  - Plan or Acceptance defects return to original Implementers for affected task steps.
  - Implementation failures go to a fresh Implementer through the task workflow.
  - Missing capabilities or unresolved requirements block affected work.
  - Corrections require affected checks, required fresh review and acceptance before fresh validation.

## Publish a repair

- Context: Validator publishes one repair per failed validation pass.
- Inputs: Assignment, failed validation Result and Evidence, validated Task specifications, Task order and applicable requirements.
- Effects:
  - Reserve the next unused repair task number across existing Task specifications and Task order rows.
  - Include all actionable findings, source requirements, expected and observed behavior, reproductions, scope and rechecks.
  - Depend on every validated task, including earlier repairs, and any other required prerequisites.
  - Save Result, reserved path and dependencies before publishing the repair Task specification and its Task order row.
  - Preserve existing specifications and Implementation.
  - On resume, complete only missing publication parts using the saved reservation and validated scope.
  - Block on ambiguous dependencies or conflicting files and rows.
  - Use a new repair number for each later failed validation pass.
- Outputs: repair Task specification, updated Task order and Result recording publication or blockers.
- Next: Supervisor dispatches the repair after publication is complete.

## Reconcile and resume

- Context: Supervisor handles revised specifications and interrupted executions.
- Inputs: Assignment, Implementation, current specifications, Task order, Contracts and Verification; saved Execution state, Results and Evidence when available.
- Effects:
  - Recover from saved files even when the original conversation is unavailable.
  - Reconstruct dependencies from current Task order and reconcile saved status with files, Evidence and available workers.
  - Reuse task IDs, workspaces, approved documents, records and available owners.
  - Resolve uncertain ownership before allowing a replacement writer.
  - Inspect existing effects before retrying interrupted operations.
  - Reopen affected tasks and final validation when revised requirements or changed inputs invalidate their Evidence.
  - Preserve unaffected work, current acceptance and previous Results.
  - Give replacement workers only their role’s permitted inputs and continuation information.
  - Have Validator finish incomplete repair publication before dispatch and refresh dependencies afterward.
  - Save reconciled Execution state before resuming ready work.
  - Avoid duplicate dispatch, repair publication and unnecessary checks when files and Evidence are unchanged.
- Outputs: continuation Assignments, reconciled Execution state and Result.
- Next: resume unfinished work with accepted prerequisites and resolved blockers, including outstanding validation.

## Reconstruct without prior implementation

- Context: every role uses a fresh context within the agreed reconstruction boundary.
- Inputs: Assignment, approved requirements, Contracts, Acceptance, examples and explicitly reusable assets, data and services.
- Effects:
  - Use a new workspace and preserve the source workspace and historical Evidence.
  - Exclude prior code, build products, repository history, old Plans, conversations, caches and all Memory, including copies.
  - Inspect exported inputs and possible access paths for excluded material.
  - Preserve expected outcomes, thresholds and fixtures while adapting checks to the new target.
  - Test required isolation controls and block when enforced isolation is required but unavailable.
  - Replace any worker that reads excluded material and withdraw reconstruction claims if prior code enters the workspace or worker context.
  - Permit new reconstruction Plans and Implementation only where each role allows them.
  - Follow the same implementation, independent review, acceptance and validation transitions.
  - Resume only work from this reconstruction.
- Outputs: Implementation, Evidence and Result reporting reused inputs, achieved separation and limits.

## Memory, completion and worker lifetime

Apply during ordinary work, coordination and shutdown.

- Planner and Implementer read the Memory index and relevant entries during ordinary work.
- Supervisor reads only the Memory index and forwards relevant paths without reading detailed entries.
- Exclude Memory from Reviewer, Validator and every reconstruction role.
- Prefer current requirements and repository facts over conflicting Memory.
- Save only useful, source-backed lessons and merge duplicate or outdated notes.
- Save worker Results before closing their threads.
- Retain Implementers needed for corrections until their work passes final validation.
- Close completed workers when corrections are no longer needed and record closed handles in Execution state.
- Use native agent waits and continue waiting after timeouts while work remains active.
- Inspect worker status or unfinished files only to resolve actionable uncertainty.
- Save dispatch intent before launch, worker handles after launch and Execution state after returned Results and before stopping.
- Save Results before recording their references or acceptance in Execution state.
- Treat Execution state as a checkpoint to reconcile, rather than proof of acceptance.
- Stop when all remaining tasks are blocked and report blockers promptly.
- Supervisor distinguishes selected-scope from whole-application acceptance and identifies unfinished work.
- Produce usage reports when finished, blocked or requested and report unavailable telemetry as a reporting limit.
