# Engineering guidelines

Read before planning, production code, tests, tooling, review or repairs.

- Read repository-required guidelines, those linked by the selected `project.md`, and repository-root `guidelines.md` when present. Resolve links from their containing document; missing required or handed-off files block work. Keep project additions outside this suite.
- Pass resolved guideline paths in every handoff, including replacement and independent workers. Reconstruction exports include them within the allowed boundary. Plans/acceptance cite applicable clauses; implementation, review and validation apply them.
- Preserve clause strength: preferences allow justified exceptions; requirements remain binding. Record material exceptions and reasons in review-visible results. Findings cite the clause and concrete consequence; style preferences create no new product requirements. Resolve conflicts under [source authority](BUNDLE.md).
- Prefer a functional core: explicit state and functions transforming inputs to outputs. Use stateful objects to protect invariants, manage resource lifetimes or satisfy frameworks.
- Put side effects behind explicit boundaries; keep domain logic independent of infrastructure and hidden mutable state.
- Build cohesive, composable modules with small interfaces and one responsibility. Express processing as readable pipelines with explicit inputs, outputs and dependencies.
- Make stages substitutable: preserve supported inputs and promised outputs, behavior, errors and side-effect guarantees.
- Test observable behavior through public interfaces so tests survive internal refactoring. Prefer real implementations and isolated disposable infrastructure; use doubles for costly, destructive, unreliable or impractical dependencies, documenting meaningful coverage limits.
- Treat design guidance as defaults; explain material departures with a concrete benefit or constraint. Add no unnecessary validations, locks, checksums or manifests, and no backwards compatibility unless requested.
- Use simple language in comments and documents; avoid dense jargon.
