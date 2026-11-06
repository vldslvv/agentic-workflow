# Run — <RUN ID>

**Task/scope/mode:** <Selected spec and requirement IDs; baseline commit; approval references.>
**Input identities:** <Document/check inventory, dependencies, target, suite/prompts, adapters, retained inputs and their digests.>
**Ownership and isolation:** <Allowed candidate paths, protected inputs, reviewer paths; requested/actual isolation, integrity observations and limitations.>
**Context and usage:** <Role manifest paths and suite-controlled bytes; per-role cached/uncached input, output/reasoning, response/tool counts, elapsed time; unavailable fields explicit; outer-driver overhead separate.>
**Agents and handoffs:** <Planner, implementer, reviewer identities/session IDs when available; actual input references; fresh reviewer context excludes plan/conversation.>
**Environment and limits:** <Tools/versions, timestamps, explicit cancellation/resource/infrastructure/specification stops; attempts continue until accepted; cost if available.>

## Attempts and results

| Attempt | Candidate revision/digest | Requirement/gate | PASS / FAIL / BLOCKED / NOT_RUN | Method and raw evidence | Review findings / next action |
|---|---|---|---|---|---|
| 0 | <Identity> | <ID> | <Result> | <Commands, exit codes, outputs or manual observation> | <Reference> |

Retain failed attempts and infrastructure incidents. Include independent review, integrity, dependency integration, manual gates, and assembled-app acceptance where applicable. Keep initial and repaired outcomes distinct. Record interventions and stale-evidence invalidation. Review details may be inline or use REVIEW.md; raw evidence remains linked.

**Coverage assessment:** <Per-requirement public-interface check execution, coverage judgment, and review outcome separately; inventory versions and additive-check authorizations. Link testing exceptions with obstacles, affected IDs, remaining evidence, gaps and supervisor-authorized revisions; preserve skipped/blocked results and original failures.>

**Supervisor decision:** <Scoped acceptance or remaining blockers; actual integrated candidate; reuse eligibility and missing checks.>

## Only for regeneration / cross-target

<Export inventory/digest, retained boundaries, new target/adapter identities, enforced controls or procedural limits, leakage, resumed provenance, and precise reconstruction claim. Ordinary runs omit this section.>
