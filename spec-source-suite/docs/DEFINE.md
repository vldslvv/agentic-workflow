# Define — author specifications and acceptance together

Read [SUITE_CONTRACT](SUITE_CONTRACT.md) first. Use [SPEC.md](../templates/SPEC.md) as a starting point, not as a requirement to produce unnecessary prose.

## Purpose and entry paths

Define produces the durable description of the user's project. It does not select an application, architecture, or stack on the user's behalf.

| Entry path | Method | Additional safeguard |
|---|---|---|
| New intent | Turn the user's goal into capability boundaries, observable contracts, and acceptance clauses | Mark proposals and unresolved decisions; do not present invented details as user requirements |
| Existing specifications | Import and normalize documents, preserve their meaning, add IDs and acceptance mappings | Maintain provenance and surface conflicting source documents |
| Existing implementation | With explicit authorization, characterize public behavior and extract candidate specifications | Label observations separately from approved requirements; decide whether quirks are intentional |
| Change to an approved project | Write a scoped change proposal, impact analysis, and revised acceptance mapping | Preserve the prior approved snapshot; invalidate affected downstream evidence |

## Ways to express behavior

Use the smallest representation that removes the relevant ambiguity. Several forms can coexist in one spec or be referenced from it.

| Form | Useful for | Must make explicit |
|---|---|---|
| Structured prose with stable requirement IDs | General capabilities and rules | Preconditions, required outcomes, failure cases, and allowed variation |
| Given/When/Then scenarios or decision tables | Boundary cases and branching rules | Inputs, initial state, observable result, and side effects |
| Schemas and interface contracts | APIs, files, events, CLIs, or callable interfaces | Semantics and error behavior in addition to data shape |
| State-transition model | Stateful or asynchronous behavior | Legal transitions, terminal states, conflicts, retries, and recovery |
| Properties and invariants | General behavior across many inputs or histories | Domain, quantification, limits, and how counterexamples are assessed |
| Operational measurements or evaluation rubrics | Latency, resource limits, generated content, or other nonexact outputs | Environment, sample design, metrics, tolerances, aggregation, and pass thresholds |

No form is mandatory for every project. A small deterministic tool may need only precise prose, input/output examples, and a few properties. A nondeterministic system needs an explicit evaluation protocol; exact string matching is not the default.

## Procedure

### D1. Establish the observation boundary

Read the project brief or supplied material. Identify consumers, supported operations, outputs, externally visible effects, state that survives restarts, and environment assumptions. Define what is outside the preservation target. Distinguish behavior preservation from byte-identical output, identical internals, or preservation of existing data.

Capture unresolved behavior in an open-questions section. It is permissible to draft alternatives, but not to approve an arbitrary answer as if supplied by the user. Ask for decisions only where the missing answer changes the contract; leave unrelated drafting work unblocked.

### D2. Choose acceptance-sized capabilities

Split by independently assessable behavior, not by source files or framework layers. A single spec may be sufficient. Put genuinely shared terms and invariants into referenced shared contracts rather than copying them into every document.

Assign stable spec IDs and stable requirement IDs. Define dependencies in each spec's `depends_on`. Derive and validate the DAG. Record the effects of changing a shared contract on all consumers.

### D3. Write the specification as its acceptance document

For each mandatory requirement, include its observable rule and an acceptance clause that an independent reviewer can assess. Specify relevant normal, boundary, failure, and interaction behavior. Explicitly distinguish REQUIRED, ALLOWED_VARIATION, and OUT_OF_SCOPE.

Address time, randomness, ordering, persistence, retries, concurrency, authorization, and external dependencies only as applicable. For each relevant topic, define the semantics rather than writing “handle correctly.” Record “not applicable” with a reason where omission could otherwise be mistaken for an unanswered question.

Internal design decisions belong in a target profile or transient implementation plan unless they are truly mandated. A technology-independent spec may still require a stable external protocol, format, or performance bound.

### D4. Design verification before implementation

Map requirement IDs to check definitions in [VERIFICATION.md](../templates/VERIFICATION.md). One scenario may cover several requirements; avoid duplicating tests merely to achieve a one-to-one mapping.

For each check define setup, stimulus, observable assertions, reset/cleanup, evaluation method, pass rule, and evidence. Identify whether it is automated, manually inspected, or not yet executable. A missing required check blocks the corresponding acceptance gate even when the prose is clear.

Public examples teach the contract. Protected checks assess it. Additional held-out cases may exercise composed behavior, but may not invent requirements. When behavior is stochastic, predeclare sample size, seeds if applicable, aggregation, uncertainty treatment, and allowed retry policy.

### D5. Review the spec before approval

Perform a contradiction and completeness review against the following questions:

- Can an independent worker tell what is mandatory, allowed, and out of scope?
- Is each mandatory requirement observable and linked to a meaningful acceptance method?
- Are IDs, references, and dependencies valid, with no unresolved prerequisite cycles?
- Are conflicts, failure behavior, and cross-capability interactions addressed where relevant?
- Have essential assets, external contracts, and state requirements been retained explicitly?
- Are target choices separated from behavior, and are unresolved normative questions visible?

A reviewer can find gaps; approval belongs to the designated authority. Record approval of exact content digests, not just an editable status label.

### D6. Freeze the implementation input

Export or identify the approved specification bundle, acceptance baseline, dependency revisions, and required retained inputs. It is acceptable for a spec to be approved while its automated verifier is still being built, but record acceptance readiness separately; implementation acceptance cannot pass until all mandatory checks are available.

## Outputs and stop conditions

Output capability specs, the project manifest, a derived DAG, a requirement-to-check mapping, an approval record, and any unresolved change proposals. Use [CHANGE.md](../templates/CHANGE.md) for behavior changes.

No project intent or specs: report NO_PROJECT. Unresolved mandatory behavior: leave the affected specs DRAFT or PROPOSED. Invalid dependencies or contradictions: report BLOCKED with exact references. Never generate an application merely to fill those gaps.
