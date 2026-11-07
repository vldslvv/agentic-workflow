# Documentation walkthroughs

Method: manual tracing of instruction paths against the current edited files. These scenarios were not executed by live worker agents.

| Scenario | Trace and observed instruction outcome | Result |
|---|---|---|
| Direct code, test or tooling work | Root `AGENTS.md` requires reading and applying `guidelines.md` before planning, writing, changing or reviewing code. | PASS |
| Planner entry | The `spec-planner` skill loads shared rules and Planner. Shared rules require guideline reading; Planner includes source paths in plans and applicable clauses in acceptance. | PASS |
| Supervisor and implementer | The `spec-supervisor` skill loads shared rules and Supervisor. Every dispatched worker receives guideline paths; shared rules apply to implementation, tests and repairs. | PASS |
| Fresh independent reviewer | Implementer supplies resolved guideline paths and material exception reasons. Reviewer checks applicable guidelines. Source files are allowed independently of excluded plans, conversations and memory. | PASS |
| Final validator and replacements | Supervisor's every-worker handoff includes guidelines; shared rules explicitly cover validators and replacements. Validator checks conformance at the assembled-app stage. | PASS |
| Adoption and missing files | Shared rules combine repository-required sources, project-linked sources and an existing root `guidelines.md`. Explicitly required or handed-off missing files block work; a repository with no guideline source does not acquire a fictitious required file. Template prompts authors for relative source links. | PASS |
| Reconstruction | Shared rules require exporting applicable guidelines within the allowed-input boundary and using exported paths, preserving independent review exclusions. | PASS |
| Exceptions, conflicts and changes | Each clause retains its strength. Material preference exceptions include reasons visible to reviewers; binding requirements remain binding. Conflicts use existing authority rules; source changes require reassessing affected results. | PASS |

Limit: this establishes that instruction paths carry the guidelines, not that an agent will always comply or that a specific app conforms.
