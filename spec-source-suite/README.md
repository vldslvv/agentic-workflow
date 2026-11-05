# Spec Source Suite

Reusable, instruction-driven workflows for building an app from approved subsystem specifications. Version: 0.2-draft.

Start at [AGENTS.md](AGENTS.md) and the [shared contract](docs/SUITE_CONTRACT.md). This package supplies guidance, skills, and blank templates. It contains no selected app, target stack, or automated runner.

| Workflow | Responsibility | Completion |
|---|---|---|
| [Define](docs/DEFINE.md) | Author app documents and verification descriptions; prepare executable checks only within authorized handoff scope | Documents: approved, saved, validated. Implementation handoff: executable checks available and inputs frozen |
| [Generate](docs/GENERATE.md) | Supervisor derives the DAG and dispatches ready tasks | Subsystems accepted and assembled-app checks pass |
| [Implement](docs/IMPLEMENT.md) | Implementer builds, spawns fresh review, and repairs | Candidate passes checks, independent review, and applicable integration |

Each app implementation task uses planner, implementer, and reviewer agents. Documentation-only tasks stay in Define and use its document-completion gate, even when requested as “implement the plan.” Supervisor is the parent's coordination responsibility; verifier means the check set/execution arrangement. The ordinary app workflow is serial and procedurally separated. The shared contract defines authority, ownership, evidence, and the initial candidate plus two repair rounds.

## Add a project

Keep project files outside this suite. Use `specs/` for a small [project brief](templates/PROJECT.md), [manifest](templates/project.yaml), and selected [target profile](templates/target.yaml). Save each task's complete approved [plan](templates/PLAN.md) and [acceptance](templates/SPEC.md) under `.agents/tasks/<NNN>-<task-id>/` with baseline commit and approval references. Register a subsystem's acceptance file directly in the manifest. Its `depends_on` defines prerequisites; no second graph is needed.

Keep checks alongside project inputs, frozen before implementation. Acceptance can contain the verification mapping; a separate [verification plan](templates/VERIFICATION.md) is optional. Keep raw results and review findings in one configured run directory outside the suite. See [RUN_REPORT.md](templates/RUN_REPORT.md).

The nested skills can be read directly or invoked when installed as `$spec-define`, `$spec-generate`, and `$spec-implement`. They are instructions, not shell commands. Runtime invocation conventions are sourced in [SOURCES.md](docs/SOURCES.md); no particular worker CLI is required. Missing fresh-review or execution capability blocks the corresponding gate.

## Conditional branches

- For regeneration or cross-target reconstruction, read [REGENERATION.md](docs/REGENERATION.md). It preserves input export, retained-state, isolation, and comparison safeguards.
- When enforced isolation is required, read [STRONG_ISOLATION.md](docs/STRONG_ISOLATION.md). Missing required enforcement blocks that run.
- Only when asked to build an automated runner, use [CODEX_START.md](CODEX_START.md) and [BUILD_THE_SUITE.md](docs/BUILD_THE_SUITE.md). Their tooling requirements are not app requirements.

Approved plans and acceptance are durable task records, even though plans do not define behavior. Source/build output may be replaced within authorized scope. Audit records and old plans stay outside regeneration exports.

Package structural results are recorded in `PACKAGE_CHECKS.json`. Documentation walkthroughs do not demonstrate successful app generation or enforced isolation.
