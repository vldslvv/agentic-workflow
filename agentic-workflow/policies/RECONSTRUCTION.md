# Reconstruction

## Rebuild from allowed inputs

- Context: read before rebuilding without access to the previous implementation. Apply [Checks](CHECKS.md), [Records](RECORDS.md) and the [separation guidelines](#separation-guidelines). Describe work that uses prior code as a port.
- Inputs: approved behaviour, target, assets, data and services allowed for reuse, and compatibility checks.
- Effects:
  1. Define the required behaviour and which inputs may be reused. Preserve expected outcomes, thresholds and fixtures. Commands may change for the new target; the checks must remain just as strong.
  2. Use a new workspace and fresh contexts for every role, including the Supervisor. Give each role only allowed inputs.
  3. Export only approved requirements, acceptance criteria, public contracts and examples, inputs allowed for reuse, and applicable workflow and engineering guidance.
  4. Inspect exports for excluded material. Check whether it is accessible through files, parent instructions, session memory, caches, remotes or the network.
  5. If enforced isolation is required, apply and test access controls for the agreed boundary. Include excluded inputs and reviewer results. Block the isolation requirement if the controls are unavailable.
  6. Replace any worker that read excluded material. Check real dependencies that will be reused.
- Outputs: use Records to report target changes, reused inputs, access controls, limits and observed results. State what separation was actually achieved.

## Separation guidelines

Apply to every role and export when rebuilding without prior code.

- State which inputs were reused and which outputs were rebuilt.
- Exclude prior code, build products, repository history, old plans, conversations, caches containing prior code, and all project memory and copies of it.
- Reject paths or symlinks that escape the allowed directory.
- Keep credentials out of exports and logs. Preserve the source workspace and historical evidence.
- Allow roles to use new plans and code made during this reconstruction when their role permits it. Follow Checks for independent workers.
- Use separation by instructions unless enforced isolation is required. Instructions and a new directory alone do not enforce isolation.
- Withdraw claims of reconstruction without prior code if that code reached the workspace or a worker's context. Report whether the result meets requirements separately, when appropriate.
- Resume only work from this reconstruction and label it as resumed.
- Limit conclusions to what was checked. A finite set of checks cannot prove equivalence in every case or that reconstruction will always work.
