# Engineering guidelines

Read before planning, production code, tests, tooling, review or repairs.

- Separate state and logic.
- Use classes that mix state and logic sparingly, only when required.
- Localize side effects.
- A top-level flow of each module should have a clear, functional-like flow.
- Prefer small, Unix-like modules.
- Give each module a public API with few responsibilities.
- Prioritize public behaviour tests.
- Internal tests can add useful coverage.
- Prefer real infrastructure.
- Justify mocks under [Checks](CHECKS.md).
- Build with small modules, composing larger architectural structures out of them.
- Test public behaviour for every eligible module.
- Test public contracts specified in the task.
- Do not create unnecessary validations, locks, checksums and manifests unless explicitly requested.
- Do not create backwards-compatible functionality unless explicitly requested.
- Use simple language in comments and documents.
- Avoid dense tech jargon and phrasing typical for LLM outputs.
