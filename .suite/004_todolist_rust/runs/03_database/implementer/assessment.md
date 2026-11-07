# Implementer assessment — 03_database

Mode: **full**. Implementation has not begun; awaiting a fresh Planner's validated plan/acceptance and explicit Supervisor resume.

Authority: `specs/todolist_rust/{project.md,task_order.md,verification.md,tasks/03_database.md}`, inherited `tasks/01_business_logic.md` and `tasks/02_cli.md` as amended by task 03. Candidate: `apps/todolist_rust`. Engineering: `/home/vv/ccode/generate-prototype/guidelines.md`. Prerequisite tasks 01 and 02 are accepted by Supervisor.

Assessment: replacement of JSON with Docker PostgreSQL changes the persistence boundary, public domain representation, schema initialization, error propagation, runtime configuration and fixture lifecycle. Required timestamps, PostgreSQL enum, integer sequential IDs, soft deletion and startup connection checks interact with existing CLI behavior; backend replacement introduces data-loss/component-correctness risks. Verification requires actual PostgreSQL and CLI processes, direct schema/data observations, failure controls, cross-process persistence and container restart. This is complex regardless of implementation confidence.

Planning must concretize connection configuration/startup, `id` integer domain and CLI parsing, actual SQL enum values `Completed/New/Deleted`, datetime meaning and update rules, soft-delete/list/not-found semantics, and how inherited public API/CLI behavior is reassessed. Every invocation must check an alive database, including help/no-argument/invalid usage forms; JSON persistence and migration are outside scope. Keep source behavior and required acceptance expectations intact; no backwards-compatibility feature is requested.

Routing: careful, selected for backend replacement/data-loss/component correctness; requested `gpt-6.1-sol` high. Observed host settings unavailable; no known fallback.

Read shared/Implementer/model guidance, resolved guidelines, selected source files, candidate source/README/manifest/business tests/example, and handed-off task02 results. No other implementation inspected. Test-audit main skill applies; its auxiliary `/home/vv/docs/help/testing/writing-tests.md` is unavailable. No dependency or infrastructure check run during assessment; handoff states real Docker available via approved escalation. No production files changed.
