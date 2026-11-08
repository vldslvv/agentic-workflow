# Implementation workflow

## Author documents — when requested

- Context: [PLANNER.md](roles/PLANNER.md), authorized brief and sources.
- Inputs: requested documents, target paths, relevant code and accepted contracts.
- Effects: Planner writes and checks documents. For workflow changes, check behavior, role reading paths and package validity. Preserve approved history.
- Outputs: document paths, blockers and check gaps. Report document validity and generation readiness separately.
- Next: stop before execution. App setup and review are not prerequisites. Implementation needs authorization under [BUNDLE.md](policies/BUNDLE.md).

## Start Supervisor

- Context: [SUPERVISOR.md](roles/SUPERVISOR.md), project files, [BUNDLE.md](policies/BUNDLE.md), [RECORDS.md](policies/RECORDS.md). All roles apply [AGENTS.md](AGENTS.md) and [model routing](policies/MODELS.md).
- Inputs: spec directory or identified continuation.
- Effects:
  1. Resolve work. Stop on `NO_PROJECT`, `NO_WORK` or blocked inputs. Start at new paths; extend selected code for incremental work.
  2. Allocate/resume records and assign task IDs before dispatch. Record modes, interfaces, file owners, worker handles and output paths. Include shared configuration ownership.
  3. Choose modes independently of models. Use full for required planning/review, complexity or uncertainty. Use lightweight for simple, bounded tasks with clear criteria. Honor user/source requirements; block on conflicts.
  4. Dispatch tasks with accepted prerequisites. Run ready tasks concurrently; reserve Reviewer capacity. Break ties by table order. Blocked tasks do not hold unrelated work.
- Outputs: accepted task results or blockers.

## Spawn Implementer — per task

- Context: [IMPLEMENTER.md](roles/IMPLEMENTER.md), task sources, accepted dependency contracts.
- Inputs: assignment, mode, candidate, owned files.
- Effects:
  1. Supervisor spawns Implementer in a fresh session. Use handoff rules in [RECORDS.md](policies/RECORDS.md).
  2. Implementer reads inputs and agrees on concurrent edits with Supervisor, including scope and file ownership. Supervisor resolves overlaps and interface changes before edits. Return affected plans/checks/reviews to owners.
  3. Full: write plan and source-linked acceptance before code. Lightweight: use source criteria; skip plan, separate acceptance and review. Keep the assigned mode.
  4. Implement, check requirements and regressions, and inspect the diff. Fix defects and rerun affected checks. Preserve approved originals.
- Outputs: candidate, evidence, task result; full mode adds plan and acceptance.
- Next: full → review; lightweight → accept.

## Spawn Reviewer — full mode

- Context: [REVIEWER.md](roles/REVIEWER.md), requirements, acceptance, candidate, factual evidence. Apply independent-check rules in [CHECKS.md](policies/CHECKS.md).
- Inputs: checked candidate and agreed review boundary. Supervisor confirms affected writers paused.
- Effects: Implementer launches fresh Reviewer. Reviewer checks code against acceptance criteria and both against requirements. Check test quality and prior fixes. Run relevant checks and feasible reproductions. Keep requirements and code unchanged. Report candidate changes to Implementer and Supervisor; apply Checks' recheck rules.
- Outputs: result, source-linked findings, reproductions, verified fixes and coverage gaps.
- Next: Implementer reports review completion. Wait for Supervisor's explicit release before writing. Findings → same Implementer fixes, rechecks and repeats fresh review. Pass → task result and acceptance.

## Accept task — Supervisor

- Context: [CHECKS.md](policies/CHECKS.md).
- Inputs: task result, mode, required evidence.
- Effects: pass unlocks dependents. Return defects to the same Implementer for correction.
- Outputs: acceptance or findings; reassess affected downstream evidence.
- Next: ready tasks → implement; all accepted → validate; all remaining blocked → stop.

## Spawn Validator — Supervisor

- Context: [VALIDATOR.md](roles/VALIDATOR.md), requirements, acceptance, contracts, factual evidence. Apply independent-check rules in [CHECKS.md](policies/CHECKS.md).
- Inputs: assembled candidate, exact task set and modes; affected writers paused.
- Effects: after all selected tasks pass, Supervisor launches fresh Validator in either mode. Check final scenarios, interactions, real dependencies and required manual checks. Reproduce gaps where feasible. Keep the candidate unchanged. Use source criteria for lightweight tasks.
- Outputs: final result; repair task for implementation failures.
- Next: Supervisor releases writers and routes the result:

| Result | Next |
|---|---|
| Pass | Finish |
| Plan/acceptance defect | Original Implementers repeat affected steps; then fresh validation |
| Implementation failure | Publish repair; fresh Implementer executes it; then fresh validation |
| Missing capability or unresolved requirement | Record blockers; behavior changes need user authority |

## Publish repair — Validator

- Context: [VALIDATOR.md](roles/VALIDATOR.md), [BUNDLE.md](policies/BUNDLE.md), [RECORDS.md](policies/RECORDS.md).
- Inputs: failed validation, validated scope, bundle files and task rows.
- Effects: publish one repair per failed pass. Include actionable findings and recheck details from the Validator procedure. Reserve the next unused `tasks/repair-NNN.md` across files and rows. Depend on all validated tasks, earlier repairs and other prerequisites. Save result, path and dependencies before publishing the repair and `task_order.md` row. Preserve existing specs and code.
- Outputs: repair and dependency row, or blockers.
- Next: Supervisor assigns repair to fresh Implementer. On resume, Validator completes missing publication parts before dispatch. Recover dependencies from validated scope; block on ambiguity or conflicts. Use a new number for each later failed pass.

## Finish, stop or resume

- Context: [RECORDS.md](policies/RECORDS.md).
- Inputs: results, findings, current artifacts.
- Effects: save results and evidence when finished, blocked, cancelled or limited. Apply each role's memory and usage rules. Report blockers promptly. Implementer and Validator report completion once. Supervisor builds usage reports when finished, blocked or requested.
- Outputs: final/partial result, accepted scope and unfinished work. Distinguish selected-scope from whole-app acceptance.
- Resume: reuse records and available owners. Reassess evidence; finish repair publication before dispatch.

## Coordination guidelines

Apply while workers are active.

- Wait for notifications with the longest timeout compatible with host/user updates. Keep waiting after timeouts.
- Message for decisions or new information. Inspect status only to resolve concrete uncertainty.
- Supervisor pauses and releases writers for review and validation. Unrelated work may continue.
