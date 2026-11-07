# Planner

Read [AGENTS.md](AGENTS.md), [Checks](CHECKS.md) and [Records](RECORDS.md). Author documents only. Ordinary work follows [Memory](MEMORY.md); rebuilding follows [Reconstruction](RECONSTRUCTION.md).

1. Resolve the authorized brief, scope, sources, target and document destinations. Read relevant code and accepted dependency contracts. For project inputs, follow [Bundle](BUNDLE.md) and its templates.
2. Author requested documents. For task records, use the [plan](templates/plan.md) and [acceptance](templates/acceptance.md) templates. Map requirements to observable outcomes and proportionate checks; surface unresolved requirements and unavailable required checks.
3. Validate consistency, source coverage, links, dependency tables and verification pass rules. Implementation environments and implementation review are not prerequisites for document authoring.
4. Return document paths, validation status and a separate generation-readiness statement. Stop before execution; handle corrections against original requirements while preserving approved history.
5. Save results, usage references and useful ordinary memory on completion or a blocked stop. Report blockers/decisions promptly and completion once with the result path.

## Workflow maintenance

- Keep implementation sequence/handoffs in [Workflow](WORKFLOW.md), local decisions with their role and detailed policies in focused references. Reference rules instead of repeating them. Prefer replacement/removal to added guidance; add a file only for a responsibility that existing boundaries cannot hold, and explain why.
- Use simple language and roughly 5–10 short top-level items per instruction document. Prefer ordered steps or small lists; use sections only for meaningful branches/reference needs. Completeness takes priority over a word limit.
- Index persistent Markdown with relative links and read conditions. Workflow guidance belongs in the root index; project documents/memory use scoped indexes linked from their parent. Create a scoped index only if absent. Exclude transient plans, acceptance, run artifacts and reviews; indexing never expands allowed inputs.
- Review changes for preserved behavior, duplication, ownership and complete role reading paths. Follow the requested scope and acceptance; record material exceptions. Documentation walkthroughs are not live app experiments.
- When asked for workflow conformance review, use [Workflow review](WORKFLOW_REVIEW.md). Its sole purpose is judging document agreement; it adds no routine gate. Keep the reference fixed during a review and resolve intended workflow changes under the user's authorized scope.
- Run `python3 agentic-workflow/helpers/check_package.py` from the project root, plus relevant tests. Use `--integration-root .` when checking the root entry-point block and installed optional skills; check affected callers too. Extra valid files are allowed; Git history is unnecessary. Portable commands and copy boundaries are in [README](README.md).
