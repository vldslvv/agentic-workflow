# Independent review — simplify-suite

**Scope and candidate:** Current working-tree suite simplification, including final package metadata and checksums; requirements are `.suite/tasks/004-simplify-suite/acceptance.md` (AC-1–AC-7). Fresh reviewer context; no task plan, conversation, project memory or prior task/run history read. `docs/PROJECT_MEMORY.md` was inspected as changed workflow guidance, not project memory content.

**Role and status:** Reviewer — PASS. No actionable findings.

| Requirements | Independent inspection/check | Outcome |
|---|---|---|
| AC-1 | Inspected consolidated shared rules, four routines and removed instruction owners. Recounted all current suite Markdown/skill YAML plus root router/local acceptance skill: 4,703 words. Recorded baseline is 11,813; reduction is 60.2%, across the complete instruction surface rather than relocated text. | PASS |
| AC-2, AC-3 | Inspected routers, skills, bundle/plan/acceptance/result templates and separate future-runner assignment/acceptance. Walked document completion, repair/review, prerequisite and assembly-failure branches. Searched active guidance for retired obligations; remaining mentions prohibit them or describe distribution metadata. | PASS |
| AC-4 | Walked ordinary memory handoff and reconstruction routes: relevant live note paths, no prescribed memory metadata/copies/hashes, fresh allowed-input reconstruction workspace, excluded implementation/history/memory, preserved behavior and explicit actual isolation limits. | PASS |
| AC-5 | Confirmed three retired helpers and their owner tests are absent. Diff inspection and removal audit support explicit interface retirement rather than deletion of failing proof. Package inventory independently matches all 30 distribution files. | PASS |
| AC-6 | `python -m unittest discover -s spec-source-suite/tests -v` from repository root: exit 0, seven tests passed. Independently compared helper/test bytes with `git show HEAD:<path>`: identical. Usage guidance retains source selection, totals/breakdowns, missing-counter limits and blocked-run reporting without acceptance gates. | PASS |
| AC-7 | Independent Python local-link/heading check: 94 links, zero errors. Inspected three skill entry points/YAML and templates. `sha256sum -c SHA256SUMS` from `spec-source-suite/`: all 30 files OK. Independently checked complete inventory and metadata evidence paths. `git diff --check` from repository root: exit 0. | PASS |

**Findings and resolutions:** None. Final metadata was checked after the implementer declared the candidate stable. An initial metadata read used the wrong working directory and did not execute its chained checks; corrected reads and checks above succeeded.

**Coverage and limitations:** Independently walked all eight documented scenarios, including unavailable review/checks and missing telemetry, and inspected `walkthroughs.md`. These are documentation assessments and retained-helper execution, not live app generation, reconstruction, runner execution or enforced-isolation experiments. No new tests or production seams were added. Retained usage tests protect observable aggregation, missing counters, source scope and input-file integrity.

**Usage references:** Reviewer thread `01a1b210-edc4-7c80-a82e-dd6585e80585`; turn ID and log path unavailable through the provided context. Environment also exposes `CODEX_SESSION_ID=01a1b20b-0bad-7c41-adeb-0df6bf4c7a7a`, which may be inherited; do not treat it as this reviewer's identity without verification. Counters unavailable locally; supervisor may aggregate available telemetry. No conversation logs were read.
