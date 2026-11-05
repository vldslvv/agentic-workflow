# Run report — <RUN ID>

## Identity and scope

**Project:** <ID.>

**Workflow/mode:** <implement / initial / incremental / regenerate / cross-target.>

**Selected specs and requirement IDs:** <Exact scope.>

**Spec/dependency digests:** <Approved baseline.>

**Suite and prompt revisions:** <Exact versions/digests.>

**Target:** <Profile and digest.>

**Verifier/adapters:** <Exact versions and independent validation references.>

**Candidate:** <Revision/artifact digests.>

## Execution conditions

<Environment/tool versions; worker/reviewer identities and sessions; timestamps; attempt budget; feedback policy; manual interventions; resume provenance.>

## Retained inputs and isolation

**Export manifest:** <Path and digest.>

**Retained boundaries:** <Services, assets, data, binaries, or test doubles that survive.>

**Isolation requested / actual:** <enforced, procedural, or none.>

**Controls and evidence:** <Filesystem, network, history, memories, credentials, verifier protection.>

**Limitations or leakage:** <What could not be enforced or checked.>

## Requirement and gate results

| Requirement / gate | Result | Method | Evidence |
|---|---|---|---|
| <ID> | <PASS/FAIL/BLOCKED/NOT_RUN> | <automated/manual> | <actual artifact> |

## Attempts and accounting

**First-attempt result:** <Outcome.>

**Repair attempts and final result:** <All attempts retained.>

**Infrastructure errors:** <Separate from behavior failures.>

**Duration, cost, and resource use:** <Measured values or unavailable.>

**Scope controls:** <Skipped/completed/limited nodes and why prerequisites remain satisfied.>

## Conclusions

**Ordinary conformance:** <What passed for this exact scope and baseline.>

**Independent review:** <Actual result and independence limitations.>

**Regeneration evidence:** <Whether generated anew, same-baseline status, actual isolation, and retained boundaries.>

**Cross-target evidence:** <Applicable result or not attempted.>

**Unverified claims:** <Explicit gaps.>

**Next required action:** <Repair, spec change, environment fix, further test, or none.>
