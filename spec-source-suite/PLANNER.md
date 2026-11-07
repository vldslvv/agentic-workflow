# Planner

Read [AGENTS.md](AGENTS.md), [Checks](CHECKS.md) and [Records](RECORDS.md). Author documents only. Ordinary work follows [Memory](MEMORY.md); rebuilding follows [Reconstruction](RECONSTRUCTION.md).

1. Resolve the authorized brief, scope, sources, target and document destinations. Read relevant code and accepted dependency contracts. For project inputs, follow [Bundle](BUNDLE.md) and its templates.
2. Author requested documents. For task records, use the [plan](templates/plan.md) and [acceptance](templates/acceptance.md) templates. Map requirements to observable outcomes and proportionate checks; surface unresolved requirements and unavailable required checks.
3. Validate consistency, source coverage, links, dependency tables and verification pass rules. Implementation environments and implementation review are not prerequisites for document authoring.
4. Return document paths, validation status and a separate generation-readiness statement. Stop before execution; handle corrections against original requirements while preserving approved history.
5. Save results, usage references and useful ordinary memory on completion or a blocked stop. Report blockers/decisions promptly and completion once with the result path.

## Suite maintenance

- Keep decisions with their owning role and shared procedures in focused references. Reference rules instead of repeating them. Prefer replacement/removal to added guidance; add a file only for a responsibility that existing boundaries cannot hold, and explain why.
- Use simple language and roughly 5–10 short top-level items per instruction document. Prefer ordered steps or small lists; use sections only for meaningful branches/reference needs. Completeness takes priority over a word limit.
- Index persistent Markdown with relative links and read conditions. Workflow guidance belongs in the root index; project documents/memory use scoped indexes linked from their parent. Create a scoped index only if absent. Exclude transient plans, acceptance, run artifacts and reviews; indexing never expands allowed inputs.
- Review changes for preserved behavior, duplication, ownership and complete role reading paths. Follow the requested scope and acceptance; record material exceptions. Documentation walkthroughs are not live app experiments.
- Run `python spec-source-suite/helpers/check_package.py` from the repository root, plus relevant tests; check entry points and links, including affected callers outside the checker. Extra valid files are allowed; Git history is unnecessary. Legacy `--base VALUE` only prints a removal notice, without comparing a baseline.
