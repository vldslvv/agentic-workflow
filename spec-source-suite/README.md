# Spec Source Suite

Instruction-driven Define, Implement and Generate workflows. Version: 0.4-draft.

Start with [AGENTS.md](AGENTS.md), the shared rules and your role routine. This package supplies guidance, blank templates and a usage helper; it contains no selected app or automated runner.

- [Define](docs/DEFINE.md): save and validate documents, or prepare a ready task's plan and source-linked acceptance.
- [Implement](docs/IMPLEMENT.md): build, check, request independent review and repair until accepted.
- [Generate](docs/GENERATE.md): plan tasks as prerequisites pass, retain implementers through repairs and verify the assembled app.
- [Reviewer](prompts/REVIEWER.md): inspect and execute independently using restricted inputs.

Add a project with the [Markdown bundle](docs/MARKDOWN_BUNDLES.md) outside the suite, normally under `specs/`. Copy the blank [project](templates/bundle/project.md), [task order](templates/bundle/task_order.md), [task](templates/bundle/tasks/task.md) and [verification](templates/bundle/verification.md) templates. Save complete [plans](templates/PLAN.md) and [acceptance](templates/ACCEPTANCE.md) in `.suite/tasks/<NNN>-<task-id>/`; save [results](templates/RUN_REPORT.md) and [usage statistics](docs/HELPERS.md#usage-reporting) in `.suite/runs/<NNN>-<task-id>/`.

[Project memory](docs/PROJECT_MEMORY.md) carries useful lessons between ordinary tasks. [Regeneration](docs/REGENERATION.md) describes reconstruction exclusions and isolation limits. Only when building a future automated runner, use the separate [assignment](CODEX_START.md) and [acceptance list](docs/BUILD_THE_SUITE.md).

The nested skills are instruction entry points: [spec-define](.agents/skills/spec-define/SKILL.md), [spec-implement](.agents/skills/spec-implement/SKILL.md), and [spec-generate](.agents/skills/spec-generate/SKILL.md). See [integration conventions](docs/SOURCES.md). Unavailable execution or fresh review blocks the corresponding acceptance requirement.

`PACKAGE_CHECKS.json` records actual package validation; `SHA256SUMS` inventories package files. These describe the distribution, not app execution gates. Documentation walkthroughs do not demonstrate successful app generation.
