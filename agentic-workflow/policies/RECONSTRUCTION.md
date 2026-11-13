# Reconstruction

Rebuild from authorized inputs while excluding prior implementation and execution evidence.

## References:

- [CHECKS]: Defines independent checks and evidence requirements. agentic-workflow/policies/CHECKS.md
- [RECORDS]: Defines execution records and handoffs. agentic-workflow/policies/RECORDS.md

## Rebuild from allowed inputs

Apply before any role starts reconstruction and throughout its execution.

- Use a new workspace and fresh contexts for every role, including Supervisor.
- Filter each role's input contract to approved requirements, acceptance, public contracts, examples, reusable inputs and applicable guidance.
- Exclude prior code, build products, repository history, old plans, conversations, caches containing prior code and project memory, including copies.
- Inspect exports and possible access through files, symlinks, parent instructions, session memory, caches, remotes and network.
- Keep exports within the allowed directory, excluding credentials from exports and logs.
- Preserve required outcomes, thresholds and fixtures when adapting commands to the new target.
- Check real dependencies that will be reused.
- Preserve the source workspace and historical evidence, resuming only this reconstruction and labeling resumed work.
- Allow new plans and code only where the role permits, applying [CHECKS] to independent workers.
- Use separation by instructions unless enforced isolation is required.
- For required isolation, apply and test access controls over excluded inputs and reviewer results, blocking when controls are unavailable.
- Replace workers exposed to excluded material and withdraw reconstruction claims if prior code reaches the workspace or a worker's context.
- Describe work using prior code as a port.
- Record reused inputs, target changes, achieved separation, controls and limits under [RECORDS].
- Report requirement conformance separately from reconstruction claims, without claiming enforced isolation from instructions or guaranteed equivalence from finite checks.
