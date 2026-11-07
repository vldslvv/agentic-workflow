# Organize the suite around five agent roles

## Summary

Replace the scattered workflow documents with one shared instruction file and five self-contained role files. Each agent reads shared rules plus its own routine.

The supervisor only orchestrates. Separate task planners prepare implementation work, implementers own review loops, and an independent final validator can generate repair tasks.

## File structure and entry points

Use this structure:

```text
spec-source-suite/
  AGENTS.md
  SUPERVISOR.md
  PLANNER.md
  IMPLEMENTER.md
  REVIEWER.md
  VALIDATOR.md
  RUNNER.md
  templates/
    project.md
    task_order.md
    tasks/task.md
    verification.md
  .agents/skills/
    spec-planner/
    spec-supervisor/
  helpers/usage_report.py
  tests/test_usage_report.py
  PACKAGE_CHECKS.json
  SHA256SUMS
```

- Merge shared authority, bundle format, record locations, memory conventions, reconstruction boundaries, and the common result outline into `AGENTS.md`.
- Put planning instructions and plan/acceptance outlines in `PLANNER.md`; orchestration and usage aggregation in `SUPERVISOR.md`; implementation and review procedures in their respective files.
- Merge the future-runner assignment and acceptance list into optional `RUNNER.md`, excluded from ordinary startup.
- Remove the superseded README, supporting guides, `docs/`, `prompts/`, and separate record templates. Flatten the bundle templates without changing their four-file format.
- Replace the three existing suite skills with `spec-planner` and `spec-supervisor`, retaining explicit invocation policy. Update root instructions, the local acceptance-spec skill, references, and package metadata. Do not retain old skill aliases.

## Agent workflow and context

| Agent | Inputs and responsibility |
|---|---|
| Supervisor | Task order, dependency status, agent handles, artifact paths, and usage references. Schedules ready tasks, retains task agents, collects outcomes, and launches final validation. Does not prepare task plans or load detailed implementation discussions. |
| Planner | Fresh context per task: original specifications, relevant current code, accepted dependency contracts, and relevant memory. Produces the complete plan and source-linked acceptance. Remains available for planning corrections within that task. |
| Implementer | Specifications, plan, acceptance, relevant project state, memory, and its planner’s handle. Implements, runs proportionate checks, maintains useful memory, and launches fresh reviewers until no actionable findings remain. |
| Reviewer | Original requirements, acceptance, implementation, check results, relevant contracts, and prior findings. Independently inspects and checks the candidate. Excludes plans, conversations, and memory. |
| Validator | Project requirements, all task acceptances, assembled implementation, check results, and prior validation findings. Independently checks whole-app behavior, interactions, and coverage. Excludes plans, conversations, and memory. |

Tasks remain serial and prerequisite-gated by default. Planning or acceptance defects return to the retained task planner; changes to required behavior need user authority. Document-only requests enter through `spec-planner` and finish after document validation. Single-task and whole-app execution enter through `spec-supervisor`.

After all scheduled tasks pass, launch a fresh validator. If it finds actionable failures:

1. The validator creates one `tasks/repair-NNN.md` specification for that validation pass and appends it to the selected bundle’s `task_order.md`, using the next unused repair number.
2. Each finding links existing requirements to expected behavior, observed failure, and reproduction evidence. The validator changes neither implementation nor existing specifications.
3. The supervisor schedules the repair through a new planner, new implementer, and ordinary fresh-review loop.
4. After acceptance, launch a fresh final validator.

Resume an already recorded repair task instead of creating a duplicate. Unavailable capabilities and unresolved requirements remain blockers; they do not become invented product requirements.

## Preservation and verification

Preserve existing task/run locations, full approved records, historical evidence, memory storage, reconstruction exclusions, and requirement-linked results. Reconstruction workers continue to use fresh allowed-input contexts and report actual isolation limits.

Keep the usage helper’s implementation, CLI, output schema, and tests unchanged. Capture references for supervisors, planners, implementers, reviewers, and validators, including repair and blocked work. Missing telemetry does not block acceptance.

Verify:

- All active links, skill metadata, package inventories, and entry points match the new structure; obsolete instructions are removed rather than relocated.
- Every role’s operative instructions fit within its shared-plus-role context.
- Retained usage tests pass and the diff contains no unrelated app changes.
- Walkthroughs cover document authoring, task planning corrections, repeated fresh reviews, dependency/memory handoffs, generated repair tasks, repair resumption, unavailable capabilities, reconstruction exclusions, and missing telemetry.
- Before/after instruction words, file counts, and directory counts demonstrate consolidation without imposing a numeric reduction target.

Report checks actually performed. Documentation walkthroughs do not establish successful live app generation.

## Defaults

Existing app bundles and historical records remain untouched during this refactor. Only future execution of the validator repair workflow extends a selected bundle. Bundle-template cleanup stays limited to removing redundant guidance and nesting.

---

## Saved-record context

The plan above preserves the complete proposed plan from this conversation. The user confirmed the shared design in Q16 (“Yes, finalize plan (Recommended)”) and then requested: “Save the plan and acceptance doc.” This request authorizes saving these documents; it does not request execution of the refactor.

**Task:** `007-agent-role-structure`.
**Acceptance:** [acceptance.md](acceptance.md), ARS-001–ARS-019.
**Implementation scope:** `spec-source-suite/`, root `AGENTS.md`, `.agents/skills/acceptance-spec/SKILL.md`, and relevant references outside the suite. Existing app changes are outside scope.
**Future evidence destination:** `.suite/runs/007-agent-role-structure/` (repository-relative; not created by this save-only request).
**Prerequisites:** No prior task acceptance is required for saving these documents. Future implementation uses the current suite as its baseline; it must preserve unrelated working-tree changes.
