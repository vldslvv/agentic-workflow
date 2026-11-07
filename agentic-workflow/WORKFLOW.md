# Implementation workflow

## Start Supervisor

- Context: [SUPERVISOR.md](roles/SUPERVISOR.md), project files.
- Inputs: spec directory or identified continuation.
- Effects: resolve work; allocate/resume records; run the task steps below for ready tasks.
- Outputs: accepted task results or blockers.

## Spawn Implementer — per task

- Context: [IMPLEMENTER.md](roles/IMPLEMENTER.md), task sources, accepted dependency contracts.
- Inputs: assignment, mode, candidate, owned files.
- Effects: Supervisor spawns an Implementer without inherited conversation to execute the assigned mode.
- Outputs: candidate, check evidence, task result; full mode also produces plan and acceptance.
- Next: full → review; lightweight → accept.

## Spawn Reviewer — full mode

- Context: [REVIEWER.md](roles/REVIEWER.md), requirements, acceptance, candidate, factual evidence.
- Inputs: review boundary confirmed paused by Supervisor.
- Effects: Implementer launches a fresh Reviewer.
- Outputs: findings and review result.
- Next: Implementer reports completion; Supervisor releases writers. Findings → same Implementer corrects, rechecks and repeats fresh review; pass → accept.

## Accept task — Supervisor

- Context: [CHECKS.md](policies/CHECKS.md).
- Inputs: task result, mode, required evidence.
- Effects: pass unlocks dependents; defects return to the same Implementer through its task steps.
- Outputs: acceptance or findings; reassess affected downstream evidence.
- Next: remaining ready tasks → implement; all accepted → validate; all remaining blocked → stop.

## Spawn Validator — Supervisor

- Context: [VALIDATOR.md](roles/VALIDATOR.md), requirements, applicable acceptance, contracts, factual evidence.
- Inputs: assembled candidate, exact task set and modes; affected writers paused.
- Effects: fresh Validator checks the app in either mode.
- Outputs: final result; implementation failures also produce a repair task.
- Next: Supervisor releases writers and routes the result:

| Result | Next |
|---|---|
| Pass | Finish |
| Plan/acceptance defect | Original Implementers correct; repeat affected task steps, then fresh validation |
| Implementation failure | Fresh Implementer runs the repair through task steps, then fresh validation |
| Missing capability or unresolved requirement | Record blockers; required behavior changes need user authority |

## Finish, stop or resume

- Context: [RECORDS.md](policies/RECORDS.md).
- Inputs: results, findings, current artifacts.
- Effects: each role saves evidence on completion, blockers, cancellation or limits; Supervisor builds usage reports.
- Outputs: final/partial result stating selected-scope versus whole-app acceptance and unfinished work.
- Resume: reuse records and available owners, reassess evidence, and complete interrupted repair publication before dispatch.
