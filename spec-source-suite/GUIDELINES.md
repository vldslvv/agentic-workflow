# Engineering guidelines

- Prefer a **functional core**: represent state explicitly and express business rules as functions transforming inputs into outputs.
- Use stateful objects when they protect invariants, manage resource lifetimes, or satisfy framework requirements.
- Localize side effects behind explicit boundaries; keep domain logic independent of infrastructure and hidden mutable state.
- Build cohesive, composable modules with small public interfaces and one clear responsibility.
- Express processing as readable pipelines with explicit inputs, outputs, and dependencies.
- Make pipeline stages substitutable: replacements must accept supported inputs and preserve promised outputs, behavior, errors, and side-effect guarantees.
- Test observable behavior through public interfaces; tests should survive internal refactoring.
- Prefer real implementations and isolated, disposable infrastructure in tests. Use test doubles when real dependencies are costly, destructive, unreliable, or impractical; document meaningful coverage limits.
- Treat these as design defaults. Explain material departures with a concrete benefit or constraint.
- Do not create unnecessary validations, locks, checksums and manifests unless explicitly requested.
- Do not create backwards-compatible functionality unless explicitly requested.
- Use simple language in comments and documents and avoid dense tech jargon typical for LLM outputs.
