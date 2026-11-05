# Verification plan — <PROJECT ID / baseline>

## Authority and baseline

<Approved spec digests, acceptance owner, verifier revision, visibility policy, and protected storage/execution boundary.>

## Candidate interface

<How the verifier observes actual behavior without relying on internal classes. Define target-specific adapter responsibilities and limits.>

## Requirement coverage

| Requirement IDs | Check ID | Type | Mandatory? | Pass rule | Evidence | Execution owner |
|---|---|---|---|---|---|---|
| <IDs> | <CHECK-ID> | <scenario/property/model/eval/inspection> | yes | <predicate/threshold> | <artifact> | <owner> |

## Check definition — <CHECK-ID>

**Requirements:** <IDs.>

**Setup and inputs:** <Initial state and environment.>

**Stimulus:** <Actions, sequence, concurrency, or input generation.>

**Oracle:** <Expected observable outcomes, errors, effects, and allowed variation, derived from the approved requirements.>

**Reset/cleanup:** <How tests avoid interfering with one another.>

**Evidence:** <Actual outputs or observations retained.>

**Sampling:** <For nondeterministic behavior: sample count, seeds/control, metric, threshold, uncertainty treatment, and retry policy. Otherwise not applicable.>

**Visibility:** <Public or held-out. No hidden requirement is permitted.>

## Integration and regression selection

<Checks needed after combining capabilities and after shared behavior changes.>

## Manual gates and unavailable checks

<Identify authorized manual criteria separately. Missing mandatory executable checks remain BLOCKED/NOT_RUN, not manually “passed” by inference.>

## Verifier and adapter change policy

<Approval, revision, independent validation, and baseline invalidation rules. Assertions may not be weakened by the implementation worker.>
