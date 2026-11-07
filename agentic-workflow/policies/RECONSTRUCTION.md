# Reconstruction

## Rebuild from allowed inputs

- Context: read before rebuilding without prior implementation; apply [Checks](CHECKS.md), [Records](RECORDS.md) and the [separation guidelines](#separation-guidelines). Porting with prior code is a different claim.
- Inputs: approved behavior, target, retained assets/data/services and compatibility checks.
- Effects:
  1. Define the approved behavior and retained boundary. Preserve outcomes, thresholds and fixtures; target-specific invocation may change without weakening them.
  2. Use a new workspace and fresh allowed-input contexts for every role, including the Supervisor. Export only approved requirements, acceptance, public contracts/examples, permitted retained inputs and applicable workflow guidance and engineering guidelines.
  3. Inspect exports and actual separation across filesystem access, parent instructions, session memory, caches, remotes and network.
  4. If enforced isolation is required, apply and test controls for the declared boundary, including excluded inputs and reviewer results. Unavailable controls block that requirement.
  5. Replace any worker that read excluded material; check retained real dependencies.
- Outputs: target changes, retained boundaries, controls, limits and observed conformance reported using Records, including the actual separation achieved.

## Separation guidelines

Apply to every reconstruction role, export and claim.

- Distinguish retained inputs from reconstructed outputs.
- Exclude prior code, build products, repository history, old plans, conversations, caches containing prior code, and all memory/copies. Reject traversal and symlink escapes; keep credentials out of exports and logs. Preserve the source workspace and historical evidence.
- Allow new plans and code produced within this reconstruction for their ordinary roles; apply Checks to independent workers.
- Treat procedural separation as the default; instructions or a new directory do not enforce isolation.
- Invalidate reconstruction claims on known prior-code leakage; report ordinary conformance separately when appropriate.
- Resume only this reconstruction's work and label it resumed.
- Limit conclusions to observed evidence; finite checks do not prove universal equivalence or reconstruction reliability.
