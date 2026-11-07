# Model-routing maintenance results

Scope: [acceptance](../../tasks/001-model-routing/acceptance.md), candidate `/tmp/generate-prototype-model-routing` on `suite/model-routing`, based on `0d6dabf7203c05254632ddfd103225e91cb58b42`. Engineering source: [guidelines](../../../guidelines.md). No app was selected or generated.

Role/status: PASS. Required documentation checks and [fresh independent review](review.md) passed with no actionable findings; this maintenance task is accepted.

Model routing: standard, for ordinary document implementation that introduces new configuration rather than following an established small-change pattern. Requested profile resolves to `gpt-6.1-sol` / `medium`. This top-level host session exposes no setting-change control; its route is launch guidance, and execution continues with host defaults. Actual model/reasoning settings are unavailable; no known mismatch can be verified and no switch is claimed. Native root session/turn identifiers and token counters are unavailable; team task identity is `/root`. No telemetry schema or code was changed.

## Checks and coverage

Commands run in the worktree unless noted:

- R1, R11: `git diff --check` passed; branch and HEAD match the requested branch and baseline. Final diff and all new files are inspected for scope. Worktree creation required host permission for shared Git metadata; checkout files were not edited.
- R2–R10: [25 documentation walkthroughs](walkthroughs.md) PASS. They cover each default/demanding role route, ordered exceptions and boundaries, blockers, provider/native/default reasoning, setting controls, fallbacks, malformed configuration and index lifecycle.
- R11: `python spec-source-suite/helpers/check_package.py --base 0d6dabf7203c05254632ddfd103225e91cb58b42` exited 0: [package report](package-check.json), 42 local links, no errors.
- R11: `python -m unittest discover -s spec-source-suite/tests -v` exited 0: [test log](usage-tests.log), all 7 retained usage-report tests pass. Test and usage-report source files remain unchanged.
- R11: package metadata refreshed after validation; prior metadata retained as [JSON evidence](package-checks-before.json). `sha256sum -c SHA256SUMS` from the suite directory exited 0 for all 20 entries: [checksum log](checksums.log). An initial invocation from the repository root exited 1 because checksum paths are suite-relative; rerunning from the specified directory resolved the command error without artifact changes.
- R12: fresh independent reviewer `/root/routing_review` returned PASS with no actionable findings, independently rerunning the package checker, seven tests, twenty checksum checks, index consistency and scope checks. Requested profile was careful (`gpt-6.1-sol` / `high`); observed settings were unavailable. Its [review](review.md) records the independent conclusion and limits. No assembled-app validation applies to this documentation task.

## Maintenance assessment

The only new reusable guidance file is MODELS.md, needed to keep editable concrete settings and role mappings together, separate from the shared procedure. Each addition changes requested behavior: configuration profiles/routes, ordered selection, dispatch rereads, supported-control limitations, fallback disclosure, invalid-configuration correction, result provenance and Markdown lifecycle indexing. Shared guidance owns the procedure and indexing rule; result fields reference its reporting behavior. Role routines remain unchanged and do not duplicate model names or routing steps. The two root pointers supply precise read conditions; record pointers belong to the scoped index. No additional supporting procedure files are required.

The role-load sufficiency statement now accounts for routing configuration: shared guidance plus one routine and MODELS.md. The checker retains its existing literal shared-plus-role metric; configuration overhead is reported separately below so the actual load is visible. Engineering boundaries remain cohesive, with no executable dispatcher, provider adapter, parser or tracing dependency. No material guideline exception was needed.

| Measure | Before | After | Change |
|---|---:|---:|---:|
| Package files | 20 | 21 | +1 |
| Package directories (excluding root) | 10 | 10 | 0 |
| All package Markdown words | 4953 | 5433 | +480 |
| Shared + Supervisor | 2648 | 2960 | +312 |
| Shared + Planner | 2343 | 2655 | +312 |
| Shared + Implementer | 2154 | 2466 | +312 |
| Shared + Reviewer | 2105 | 2417 | +312 |
| Shared + Validator | 2266 | 2578 | +312 |

MODELS.md adds 168 words to each role-entry/dispatch context beyond the checker’s shared-plus-role totals: Supervisor 3128, Planner 2823, Implementer 2634, Reviewer 2585, Validator 2746. Effective per-role growth is +480 words. These package metrics exclude root instructions, guidelines and task evidence. Root instructions separately grow from 348 to 376 words (+28) for the two index entries. The growth implements the requested routing and indexing behavior; no instruction was weakened to reduce it.

## Evidence limits

Manual walkthroughs establish document consistency, not reliable model selection, live provider connectivity, retained-session reconfiguration or app correctness. The package checker, retained unit tests and checksum verification are actual local executions. The fresh reviewer is a real independent worker; its requested settings are not proof of observed execution settings. No new behavioral tests were added for prose-only rules or the inventory entry. Original tracing work remains outside this worktree. The worktree remains available; no merge is performed.
