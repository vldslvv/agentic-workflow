# Plan — 01_business_logic

Status: Authorized derived handoff under the user’s implementation request and instruction to proceed without approval prompts.
Baseline: `07fd1484a33826b53c9e669b7490175bce1bd11a`.
Acceptance: `.agents/tasks/006-01_business_logic/acceptance.md`, all mapped requirements.

Implement a small JSON-backed public business API for create/list/delete/complete plus uv packaging. Use Python standard library and uv + pyproject.toml in `apps/todolist`, validating on available Python 3.14.10 and uv 0.13.6. Include uv.lock and an app-local ignore rule for runtime data. The bundle remains unchanged.

Planner owns task records, input inventory, and frozen checks. Implementer owns `apps/todolist/` and its per-task logs. Reviewers own their report/result directories. Protect source specifications, suite guidance, historical records, and frozen inputs. No external assets or services are needed.

Executable checks and their commands, API, adapters, and source identities are prepared and frozen before implementation. Dispatch fresh implementers serially: business logic first, CLI only after accepted business evidence. Each implementer spawns a fresh reviewer with acceptance, sources, inventory, candidate identity, and checks; exclude plans and prior conversation. Verify input/candidate integrity around execution and review. Use procedural isolation and initial candidate plus at most two repairs per task. Escalate specification, verifier, or infrastructure conflicts.

After both tasks pass, run assembled A1 and record requirement-linked results, raw commands/output, candidate hashes, actual agent identities, reviews, and limitations in `.suite/runs/006-01_business_logic/`. Shared inventory: `.agents/tasks/006-01_business_logic/inputs.md`. Authorization binds this complete plan and acceptance text to the user’s implementation request and delegation.
