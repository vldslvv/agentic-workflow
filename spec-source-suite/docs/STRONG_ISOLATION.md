# Branch — enforced isolation

Read this only when the project requests enforced isolation. Return to the invoking workflow after establishing the controls. The [shared contract](SUITE_CONTRACT.md) defines the ordinary procedural path.

Declare the boundary and threat model: candidate writes, protected acceptance inputs/results, filesystem mounts, parent instructions, history, session memory, caches, network/remotes, and credentials. Apply and test the relevant sandbox/runner restrictions. A directory name, fresh context, or instruction cannot enforce a filesystem boundary.

Keep assertions, fixtures, approvals, and reviewer conclusions outside the implementer's write authority. Verify both permitted writes and rejected out-of-scope access. Record applied controls and observed results. Inject needed secrets through the environment; never serialize their values into specs, exports, or logs.

If required enforcement is unavailable, return BLOCKED. Do not silently substitute procedural separation; a policy change requires approval. Report `enforced` only for controls actually applied and evidenced at the declared boundary. Report ordinary procedural separation honestly, including any untested channels.
