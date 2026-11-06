# Spec Source Suite agentic development conclusions

Assessment date: 2026-11-06.

Spec Source Suite has strong verification and provenance rules, but delegates too much mechanical coordination to a supervising LLM. The highest-priority improvements are machine-checkable specifications and a deterministic execution runner. Moving independent review from every task to the completed application is a separate optimization that should be evaluated against the current policy.

## Preserve the verification foundation

The suite already separates authoritative requirements from implementation plans, freezes checks before implementation, links evidence to requirements and candidate identities, retains failed attempts, and requires final assembled-app verification. These are useful foundations for reliable automation. [Shared contract](../spec-source-suite/docs/SUITE_CONTRACT.md).

Fresh reviewers and restricted handoffs help separate evaluation from the implementer's narrative. Their frequency should be measured, while preserving the distinction between passing commands, adequate requirement coverage, and an independent review outcome. [Reviewer procedure](../spec-source-suite/prompts/REVIEWER.md).

## Add deterministic specification validation

The current bundle uses ordinary Markdown without required structured metadata. Dependencies can appear in prose, leaving the supervisor responsible for deriving and validating the execution graph. Existing helpers validate role and check manifests, but do not provide a complete source-bundle preflight. [Bundle format](../spec-source-suite/docs/MARKDOWN_BUNDLES.md), [helper capabilities](../spec-source-suite/docs/HELPERS.md).

OpenSpec is a suitable candidate for specification authoring and structural validation. Its CLI supports noninteractive validation with machine-readable output:

```sh
openspec validate --all --strict --json --no-interactive
```

It checks specification structure and change consistency. Its workflow schemas validate artifact dependencies, including unknown references and cycles. These checks do not establish semantic completeness, execute application behavior, or automatically represent the suite's implementation-task graph. The inspected source is pinned to commit `3e4d5f0769e2857c8eb54f149cbf5e4f703fa04c`; package adoption should pin and verify a corresponding release. [OpenSpec CLI](https://github.com/Fission-AI/OpenSpec/blob/3e4d5f0769e2857c8eb54f149cbf5e4f703fa04c/docs/cli.md), [schema validation](https://github.com/Fission-AI/OpenSpec/blob/3e4d5f0769e2857c8eb54f149cbf5e4f703fa04c/src/core/artifact-graph/schema.ts).

Use a versioned execution manifest to capture the suite-specific fields:

- Task IDs and explicit prerequisites.
- Source requirement references and digests.
- Owned and protected paths.
- Required interface and dependency identities.
- Frozen check inventories and requirement mappings.
- Review policy, manual gates, and resource limits.

Validate explicit metadata before model calls. Validate complete handoffs again before implementation. Resolving ambiguous requirements and defining missing acceptance criteria still requires reasoning.

Keep one authoritative specification source. If OpenSpec becomes authoritative, generate any compatibility views instead of maintaining two editable specifications. Typed metadata alongside existing Markdown is a lower-disruption alternative.

## Replace routine supervision with a deterministic runner

[Generate](../spec-source-suite/docs/GENERATE.md) currently assigns planning, graph validation, dispatch, and acceptance to the supervisor. Separate mechanical execution from decisions that require judgment:

| Runner responsibilities | Agent responsibilities |
|---|---|
| Validate metadata, references, and hashes | Resolve unclear requirements |
| Select ready tasks and launch workers | Design missing interfaces and implementation approaches |
| Execute declared checks and collect receipts | Diagnose failures and implement repairs |
| Persist attempts and resume execution | Assess coverage gaps and disputed findings |
| Enforce explicit acceptance gates | Evaluate behavior without mechanical pass rules |

Start with a serial loop around the existing helpers. The current bundle already makes each task depend on its predecessor; eliminating the supervising LLM does not require parallel execution.

Persist shared constraints, interface decisions, accepted dependency identities, and evidence so workers do not depend on a continuing supervisor conversation. Invoke planning on demand when a handoff is incomplete. A worker's exit code or completion message must not substitute for required evidence.

This direction follows the distinction between predefined workflows and model-directed orchestration in Anthropic's guidance. [Building effective agents](https://www.anthropic.com/research/building-effective-agents).

## Evaluate review after the completed build

The proposed task loop followed by an independent E2E evaluator has direct supporting experience: Anthropic's March 2026 application-development report moved evaluation from every sprint to the end of the build with a stronger model. Failed evaluations still led to repair rounds. This supports experimentation, rather than establishing equal quality for every workload. [Application harness report](https://www.anthropic.com/research/harness-design-long-running-apps).

Retain task-level behavioral, interface, and regression checks when deferring the review agent. Final evaluation should combine frozen assembled-app scenarios with exploratory assessment and relevant code-level checks. A browser journey alone cannot establish every requirement.

Distinguish a provisional task whose checks passed from an independently accepted task. The current contract forbids unreviewed prerequisites from unlocking consumers, so deferred review requires an explicit policy revision. Removing central LLM coordination can preserve the existing gates; changing review frequency changes acceptance semantics. [Contract §§3–5](../spec-source-suite/docs/SUITE_CONTRACT.md).

## Reduce overhead through measured changes

Current research supports choosing architecture by workload. A controlled study of 260 configurations found that collaboration benefits depend on task structure and that coordination can add overhead. Recent Anthropic guidance also recommends evaluating the removal of unnecessary agent boundaries incrementally. Neither establishes a universal best workflow. [Scaling-agent study](https://arxiv.org/abs/2512.08296v3), [October 2026 guidance](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop).

Repeated instructions are another candidate for reduction. Move enforceable rules into the runner and retain concise role-specific guidance. Research on repository context files found increased inference cost without general success improvements in its studied settings, motivating evaluation of instruction content rather than assuming more guidance helps. [Evaluating AGENTS.md, v3](https://arxiv.org/abs/2602.11988v3).

For unattended execution, apply and test access controls where isolation is required. Report actual limits. [Reconstruction and isolation](../spec-source-suite/docs/REGENERATION.md).

## Recommended implementation order

1. Add a specification/execution schema and deterministic preflight.
2. Introduce a serial runner while retaining current per-task reviews.
3. Compare per-task review with final or selective review.
4. Reduce repeated instructions and unnecessary handoff overhead.
5. Consider parallelism only for explicitly independent tasks with coordinated ownership.

Compare representative CLI, stateful API, and UI builds using equivalent briefs, models, verification, and budgets. Run repeated trials and measure first-attempt and eventual success, escaped defects, total tokens and cost, repair effort, elapsed time, and human intervention. Include failed and blocked runs. Evaluate on held-out cases so the workflow is not optimized only for its own checks.

The immediate investment should be a typed preflight and a small runner built around existing helpers. Token savings and acceptable review frequency remain empirical questions; this assessment did not benchmark the suite.

The [full suite assessment](../research/spec-source-suite-sota-assessment-2026-11-06.md) contains implementation considerations and an architecture diagram. The [research evidence review](../research/agentic-development-evidence.md) records primary sources, publication dates, and methodological limitations.
