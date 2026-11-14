---
name: agentic-workflow-implementer
description: Author documents, maintain workflow instructions, plan and implement authorized work.
disable-model-invocation: true
---

# Implementer

Execute authorized document authoring, workflow maintenance or implementation assignments.

## References:

- [AGENTS]: Routes work to role instructions and shared policies. agentic-workflow/AGENTS.md
- [IMPLEMENTER]: Defines work execution and authorization boundaries. agentic-workflow/roles/IMPLEMENTER.md
- [WORK_INPUT]: Defines the assignment description, sources and workspace. agentic-workflow/contracts/WORK_INPUT.md
- [RECORDS]: Defines saved work and returns. agentic-workflow/policies/RECORDS.md

## Execute work

- Context: when explicitly invoked, read [AGENTS] and follow [IMPLEMENTER].
- Inputs: [WORK_INPUT], loading only allowed sources and triggered branches.
- Effects: execute the authorized work under [IMPLEMENTER] and save work under [RECORDS].
- Outputs: requested documents or implementation, check evidence and saved Result.
- Next: preserve document-only and plan-only boundaries and any explicit approval requirement.
