# Independent model-routing maintenance review

Role/status: **Reviewer — PASS**, with no actionable findings. This is the independent review conclusion; final task acceptance remains the supervisor's decision.

Scope/candidate: working tree, including untracked artifacts, at `/tmp/generate-prototype-model-routing`, branch `suite/model-routing`, HEAD/base `0d6dabf7203c05254632ddfd103225e91cb58b42`. Authority: [acceptance](../../tasks/001-model-routing/acceptance.md); engineering constraints: [guidelines](../../../guidelines.md). Read the supplied root/shared/reviewer guidance and [model configuration](../../../spec-source-suite/MODELS.md) directly. Permitted implementation evidence was inspected. The plan, parent conversation, memory and unrelated task history were excluded. No implementation, requirements or retained tests were changed by this reviewer.

Model routing: **careful**, because this is normal independent review. The handoff requests `gpt-6.1-sol` / `high`, matching the configured Reviewer default. Observed runtime model/reasoning settings are unavailable. This worker has no exposed setting-change control, so it continues with host defaults; the requested route does not prove those settings were applied. No known mismatch can be independently established.

## Requirement-linked review

| Requirements | Independent method and outcome |
|---|---|
| R1 | `git worktree list --porcelain`, `git branch --show-current`, `git rev-parse HEAD`, baseline diff and untracked-file listing confirm the isolated target, requested branch and exact base. Changed production artifacts are root/shared instructions, the new configuration, the checker's inventory entry, metadata and checksums. Other additions are scoped task/evidence records. No tracing APIs, merge or commit were used. Original-checkout preservation limits are stated below. |
| R2–R3 | Manually compared every cell in the five-profile and five-role tables with acceptance: all exact model/reasoning pairs and all ten default/demanding routes match. Role routines are unchanged; targeted search finds no concrete model settings or duplicate routing procedure in them. |
| R4 | Independently walked the ordered branches: two consecutive repairs reproducing the same failure without new evidence select escalation; one repair, changed failures or new evidence do not satisfy that trigger. Demanding work wins over local small-change conditions. Small-change requires local implementation plus every listed condition, so routine review remains on its role route. Infrastructure, credentials and unresolved requirements remain blockers. |
| R5–R7 | Inspected opaque/provider-qualified identifiers, native reasoning and `default`; authentication/connectivity stay host concerns. Role entry and worker launch require current configuration, including edits. Supported retained-worker controls preserve context and fresh review. Unsupported host settings use reported defaults; existing top-level sessions disclose known mismatches. Undefined profiles/malformed entries require correction instead of that fallback. These are documentation walkthroughs. |
| R8 | The shared result outline adds the required routing provenance fields, and implementation results distinguish requests, observations and host fallback. Byte comparison against the base confirms `helpers/usage_report.py` and `tests/test_usage_report.py` are unchanged; no telemetry schema/code change is present. |
| R9–R10 | Root index directly links MODELS.md with the required read condition. Shared guidance contains the authoritative add/move/rename/remove rule, scoped placement, parent-link condition and context exclusion. Checked the root-to-scoped-index chain and explicit purpose-bearing links for all new Markdown artifacts, including this already indexed review. Allowed record links resolve; the excluded plan was checked for target existence only. |
| R11 | Independently executed all required commands successfully, as detailed below. Metadata evidence targets exist; archived prior metadata exactly matches the pinned base. Reported package/root counts agree with independent results. The checker's only change is the required MODELS.md inventory entry. |
| R12 | Fresh independent reviewer context used the acceptance, candidate, engineering guidance and permitted evidence, without plans/conversations/memory. No engineering departures or actionable defects were found. This record supplies the independent review outcome. |

## Executed checks

All commands used `/tmp/generate-prototype-model-routing`, except checksum verification, which used its `spec-source-suite/` directory.

- `python spec-source-suite/helpers/check_package.py --base 0d6dabf7203c05254632ddfd103225e91cb58b42` — exit 0, PASS, 42 local links, no errors. Independent output matches [package evidence](package-check.json): files 20 → 21, directories 10 → 10, Markdown words 4953 → 5433 (+480), each shared-plus-role context +312 words.
- `python -m unittest discover -s spec-source-suite/tests -v` — exit 0, all 7 retained usage-report tests pass. No test source was changed.
- `sha256sum -c SHA256SUMS` — exit 0, all 20 entries OK.
- `git diff --check` — exit 0; no whitespace errors.
- Read-only Python assertions — exit 0: current metadata references exist, previous metadata equals the base byte-for-byte, telemetry/tests equal the base, root word counts are 348 → 376 (+28), all added Markdown files have the correct index links, and permitted record links resolve. The plan body was not read.

The role-load accounting is explicit: MODELS.md contributes 168 additional words beyond the checker's shared-plus-role metric, producing effective role-entry totals of Supervisor 3128, Planner 2823, Implementer 2634, Reviewer 2585 and Validator 2746. Each role's effective increase is +480 words. Configuration has one cohesive responsibility; the shared file owns selection/reporting/indexing procedure, and role routines remain sufficient with shared guidance plus configuration. The additional file and growth implement the requested behavior without extra supporting procedures. No material exception to the engineering guidelines was needed.

The implementer reported a small results-only edit during review adding root word counts. This reviewer reread the changed results and independently verified those counts. No implementation/configuration change was reported or observed during review. No prior review findings required repair.

## Coverage and identity limits

These checks establish document consistency, package structure and retained-test behavior. They do not establish live provider connectivity, actual model switching, retained-worker reconfiguration, app behavior or enforced filesystem isolation; acceptance explicitly excludes those claims. Full plan content was excluded by the independent-review boundary; its existence and acceptance link were verified.

This reviewer worked only in the target worktree and made no writes to the original checkout. Worktree registration and scoped diffs were inspected, but this reviewer did not obtain independent before/after snapshots of the original checkout's uncommitted files. Original preservation therefore also relies on the implementation's supplied evidence. No claim of enforced isolation is made.

Available team identity: `/root/routing_review`; parent: `/root`. Native session/turn IDs, log paths and token counters are unavailable in this worker's exposed context. No conversation/log contents were read to obtain counters. This is a reporting limit, not invented zero usage.
