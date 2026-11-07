# Model routing and Markdown indexing in an isolated worktree

## Summary and worktree

Implement one Markdown routing file and small workflow-document changes, using a separate Git worktree based on committed `main`.

- Base commit: `0d6dabf7203c05254632ddfd103225e91cb58b42`.
- New branch: `suite/model-routing`.
- Worktree: `/tmp/generate-prototype-model-routing`.
- Create the worktree when implementation begins; run all edits and checks there.
- Leave the original checkout and its uncommitted changes untouched. Do not import the in-progress tracing changes or depend on their APIs.
- Leave the completed worktree available for review; merging is outside this implementation.

## Routing configuration

Add `spec-source-suite/MODELS.md`. Keep concrete model names and native reasoning settings in one profile table:

| Profile | Model | Reasoning |
|---|---|---|
| coordination | `gpt-6.1-sol` | `low` |
| standard | `gpt-6.1-sol` | `medium` |
| careful | `gpt-6.1-sol` | `high` |
| small-change | `gpt-6-luna` | `high` |
| escalation | `gpt-6-astra` | `medium` |

Allow `default` reasoning to use the host’s setting. Treat model identifiers as opaque strings, including provider-qualified names. Provider switching changes these names and, where necessary, native reasoning values.

A second table specifies routing:

| Role | Default | Demanding work |
|---|---|---|
| Supervisor | coordination | standard |
| Planner | standard | careful |
| Implementer | standard | careful |
| Reviewer | careful | escalation |
| Validator | careful | escalation |

Apply exceptions in this order:

1. After two consecutive implementation repair attempts reproduce the same failure without new diagnostic evidence, request escalation.
2. Use the demanding route for conflicting requirements, complex component interactions, or correctness decisions involving security, data loss, or compatibility.
3. Use small-change for local implementation with explicit expected behavior, an established pattern, and no interface or dependency changes.
4. Otherwise use the role default.

Missing infrastructure, credentials, and unresolved requirements remain blockers.

## Workflow integration

- Put the routing procedure in shared guidance. Agents read the configuration when entering a role and before launching workers; role documents do not duplicate model names.
- Read configuration edits for subsequent dispatches. Change retained-worker settings only through supported host controls, preserving contexts and fresh-review requirements.
- If the host cannot apply a requested setting, continue with host defaults and report the fallback.
- Treat the top-level route as launch guidance when the existing session cannot change settings; disclose known mismatches.
- Record the chosen profile, selection reason, requested settings, and fallback in existing Markdown results. Distinguish requests from observed settings without changing telemetry code or schemas.
- Undefined profiles or malformed routing entries require correction.

Provider authentication and connectivity remain host configuration. No dispatcher, provider adapters, or Markdown parser is added.

## File indexing

Add an explicit link to `MODELS.md` in the root `AGENTS.md` file index, with the read condition: entering a role or selecting settings for a worker.

Add one authoritative shared rule:

> Whenever a Markdown file is added, register it with an explicit relative-path link in the applicable index in the same change. Include a short purpose or read condition. Update the index when the file is moved, renamed, or removed.

Workflow guidance belongs in the root file index. Generated project documents, task records, and memory belong in their applicable scoped indexes. Create a scoped index only when none exists, and link it from its parent index. Indexing does not authorize loading material excluded from a role’s context.

## Validation and delivery

- Save the plan and separate acceptance using the committed baseline’s record conventions.
- Walk through every default and exception route, provider-name replacement, native/default reasoning, unsupported-setting fallback, and retained-worker limitations.
- Verify the root index links directly to `MODELS.md` with its read condition.
- Walk through Markdown additions, moves, and removals to verify index maintenance is part of completion.
- Update the package inventory and run the existing package checker against the pinned base commit, plus retained usage-report tests.
- Refresh package metadata and checksums. Report instruction-size changes and distinguish documentation walkthroughs from live execution evidence.
- Inspect the final diff against the pinned base to confirm it contains only routing, indexing, and necessary package-maintenance changes.

## Execution record

Authority: the user's direct request to implement the supplied plan above. No app generation or merge is authorized. No prerequisites beyond the pinned baseline and local tools. Applicable engineering guidance: [guidelines.md](../../../guidelines.md), resolved as `/tmp/generate-prototype-model-routing/guidelines.md`; apply cohesive responsibilities, explicit boundaries and observable verification. No material exceptions planned.

Separate acceptance: [acceptance.md](acceptance.md). Outputs are the named workflow files and necessary inventory/metadata/checksum edits. Evidence: [run directory](../../runs/001-model-routing/results.md); all records use this baseline's task/run convention. No ordinary project memory exists. Save records before workflow edits. Keep the configuration as data, the selection procedure in shared guidance, and index records through one scoped index. Run the existing checker and unittest suite, perform documented route/index walkthroughs, then obtain fresh independent review under the shared acceptance rule. Preserve historical package metadata in the run directory before refreshing it. No dispatcher, parser, adapter, telemetry changes or new automated tests are needed for these documentation changes.
