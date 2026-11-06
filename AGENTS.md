# App generation

`spec-source-suite/` is reusable guidance, changed only for requested workflow/tooling work. Keep app specifications, constraints, assets, generated code and evidence outside it.

Classify the request before discovery:

- Fresh work: current brief or selected bundle; never search prior task records/runs/conversations.
- Continuing work: identified task paths or execution-inventory references only. Resolve a bare task ID by immediate `.agents/tasks/` directory suffix; ask if absent/ambiguous. If continuation itself is unclear, ask before searching history.
- Advice/guidance changes: requested files and relevant references; no task-history discovery.

Before app work read [suite router](spec-source-suite/AGENTS.md) and [shared contract](spec-source-suite/docs/SUITE_CONTRACT.md) once. Load your role procedure through that router. Skills are short entry points: [Define](spec-source-suite/.agents/skills/spec-define/SKILL.md), [Implement](spec-source-suite/.agents/skills/spec-implement/SKILL.md), [Generate](spec-source-suite/.agents/skills/spec-generate/SKILL.md). Reviewers use their restricted handoff instead of loading plans or other role procedures.

For app inputs use the user-selected [standard bundle](spec-source-suite/docs/MARKDOWN_BUNDLES.md). Otherwise inspect outside the suite for `project.md`, `task_order.md`, `tasks/*.md`, `verification.md`; ask if multiple bundles are plausible. New authorized authoring uses `specs/` and suite bundle templates; templates and BUILD_THE_SUITE are not app requirements. Missing required bundle inputs block generation; no intent yields NO_PROJECT. A supplied implementation request authorizes derived handoffs under the contract; choose reasonable defaults without routine reapproval.

Route by deliverable: authoring specification/acceptance/constraint/order documents is Define work and uses its document-completion gate. Generating an app uses Generate; one capability uses Implement. The supervisor plans each ready task through Define, retaining shared constraints, acceptance decisions and dependency contracts; it hands paths/identities to fresh implementers and independent reviewers through role manifests. Allocate shared task/run numbers by listing immediate directory names across both roots only; preserve approved text and historical evidence.

Continuing work loads complete approved records and relevant state. Missing originals follow [planning-record recovery](spec-source-suite/docs/PLANNING.md#task-records); reviewers retain their exclusion boundary. Stop discovery when authority is resolved.

App execution requires every contract gate: frozen inputs, prerequisite acceptance, independent review, applicable manual checks and final assembled-app execution. Persist requirement-linked evidence outside the suite; report actual checks and blocked gates. Load [CODEX_START](spec-source-suite/CODEX_START.md) and [BUILD_THE_SUITE](spec-source-suite/docs/BUILD_THE_SUITE.md) only for explicitly requested suite tooling, not app requirements.
