# Spec Source Suite

Reusable, instruction-driven workflows for building an app from approved subsystem specifications. Version: 0.3-draft.

Start at [AGENTS.md](AGENTS.md) and the [shared contract](docs/SUITE_CONTRACT.md). This package supplies guidance, skills, and blank templates. It contains no selected app, target stack, or automated runner.

| Workflow | Responsibility | Completion |
|---|---|---|
| [Define](docs/DEFINE.md) | Author app documents and verification descriptions; prepare executable checks only within authorized handoff scope | Documents: approved, saved, validated. Implementation handoff: executable checks available and inputs frozen |
| [Generate](docs/GENERATE.md) | Supervisor derives the DAG, plans each ready task through Define and dispatches implementation | Subsystems accepted and assembled-app checks pass |
| [Implement](docs/IMPLEMENT.md) | Implementer builds, spawns fresh review, and repairs | Candidate passes checks, independent review, and applicable integration |

Each app implementation task uses the supervisor as planner, a fresh implementer, and an independent reviewer. Documentation-only tasks stay in Define and use its document-completion gate, even when requested as “implement the plan.” The supervisor retains planning and acceptance context across tasks; verifier means the check set/execution arrangement. The ordinary app workflow is serial and procedurally separated. The shared contract defines authority, ownership, evidence, and repairs until accepted under explicit stop conditions.

## Add a project

The sole app specification format is the [Markdown task bundle](docs/MARKDOWN_BUNDLES.md). Keep it outside the suite, under `specs/` by default, and preserve an existing bundle's location. The blank [bundle templates](templates/bundle/project.md) mirror its layout:

- [project.md](templates/bundle/project.md): shared rules, target constraints, and output location.
- [task_order.md](templates/bundle/task_order.md): ordered task filenames.
- [tasks/task.md](templates/bundle/tasks/task.md): one file per task's required behavior.
- [verification.md](templates/bundle/verification.md): shared verification and assembled-app scenarios.

Before execution, save each task's complete approved [plan](templates/PLAN.md) and source-linked [acceptance record](templates/ACCEPTANCE.md) under `.suite/tasks/<NNN>-<task-id>/`, with baseline commit and digest-bound approval references. The bundle defines behavior and order; these records hold the derived requirement/check mapping and prerequisites. Prepare `inputs.md` as the execution inventory and freeze checks before implementation. Keep raw results and review findings in the configured run directory outside the suite. See [RUN_REPORT.md](templates/RUN_REPORT.md).

The nested skills can be read directly or invoked when installed as `$spec-define`, `$spec-generate`, and `$spec-implement`. They are instructions, not shell commands. Runtime invocation conventions are sourced in [SOURCES.md](docs/SOURCES.md); no particular worker CLI is required. Missing fresh-review or execution capability blocks the corresponding gate.

## Conditional branches

- For regeneration or cross-target reconstruction, read [REGENERATION.md](docs/REGENERATION.md). It preserves input export, retained-state, isolation, and comparison safeguards.
- When enforced isolation is required, read [STRONG_ISOLATION.md](docs/STRONG_ISOLATION.md). Missing required enforcement blocks that run.
- Only when asked to build an automated runner, use [CODEX_START.md](CODEX_START.md) and [BUILD_THE_SUITE.md](docs/BUILD_THE_SUITE.md). Their tooling requirements are not app requirements.

Approved plans and acceptance are durable task records, even though plans do not define behavior. Source/build output may be replaced within authorized scope. Audit records and old plans stay outside regeneration exports.

Package structural results are recorded in `PACKAGE_CHECKS.json`. Documentation walkthroughs do not demonstrate successful app generation or enforced isolation.

Small standard-library [helpers](docs/HELPERS.md) validate role manifests, execute frozen checks, and report scoped usage. They do not launch workers or schedule tasks. The supervisor prepares each ready task in its existing context; implementers retain repair context and spawn fresh reviewers for every changed candidate.

[Project memory](docs/PROJECT_MEMORY.md) keeps short curated notes outside the suite, selected during ordinary planning and maintained by the completing agent. The memory helper validates their format; existing handoffs retain selected copies and exclude notes from review and regeneration.
