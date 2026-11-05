**`acceptance.md` — Simplify the specification-driven workflow**

**Task:** `simplify-spec-workflow`  
**Baseline commit:** `0da44c5e4533f42abcc3f405a7c9a6c3c3413cef`

**Goal.** Provide a compact, coherent procedure for generating an app from approved subsystem specifications and demonstrating agreement with them.

**Scope.** Workflow documentation, skills, prompts, templates, and their consistency checks. App implementation, an automated runner, and regeneration experiments are out of scope.

| ID | Required outcome | Verification |
|---|---|---|
| AC-1 | Define, Generate, and Implement have explicit inputs, responsibilities, outputs, and completion gates; shared rules have one authoritative definition. | Inspect the entrypoints and follow their references through the ordinary initial-generation path. |
| AC-2 | Registered subsystem specifications define the DAG through `depends_on`; unmet prerequisites and invalid graphs prevent dependent execution. | Walk through persistence → CLI, a failed persistence node, an unresolved dependency, and a cycle; verify the prescribed outcomes. |
| AC-3 | Each task preserves its complete approved plan, authoritative acceptance document, baseline commit, and approval references under `.agents/tasks/<task-id>/` before implementation or context handoff. | Inspect the task workflow and templates, including Plan-mode deferral and authorization for later changes. |
| AC-4 | Each task uses a planner, an implementer, and a reviewer spawned by the implementer with fresh context; reviewer inputs exclude the plan and implementation conversation. | Trace the documented handoffs and inspect reviewer instructions for independent acceptance execution and coverage assessment. |
| AC-5 | Planner-authored checks trace to approved requirements and are frozen before implementation; implementation workers cannot legitimately change the acceptance baseline to obtain a pass. | Trace check preparation, baseline-integrity checking, and the specification/verifier-change path. |
| AC-6 | The repair loop permits the initial candidate plus two repairs, retains failed attempts, and escalates contract or infrastructure problems immediately. | Walk through a successful repair, exhausted repairs, and a specification conflict. |
| AC-7 | Node acceptance requires passing checks and independent review; project acceptance additionally requires checks against the assembled app. | Inspect completion rules, downstream invalidation, and reporting of FAIL, BLOCKED, and NOT_RUN. |
| AC-8 | The common procedure supports concise human-editable specs and clearly reports procedural isolation; stronger isolation and regeneration requirements remain available through explicit branches. | Follow the ordinary path and inspect the conditional branches for unsupported claims or weakened safeguards. |
| AC-9 | Revised guidance and templates have valid local references and accurate validation records; existing staged work is preserved. | Run structural checks, review the diff, and obtain fresh independent review of the final candidate. |

**Open questions:** None for this milestone.
