# Spec Source Suite compared with current agent engineering

Assessment date: 2026-11-07. Scope: orchestration, planning, decomposition, context, memory, model routing, and development efficiency. Acceptance integrity and tamper detection are outside this assessment's focus. This is a source-grounded architecture assessment, not a benchmark of the suite.

The workflow is well aligned with modern context engineering and persistent agent work. Its main opportunity is to make coordination more adaptive: keep a capable worker moving through related work, introduce separate specialists when they contribute something specific, and measure whether each handoff pays for itself. The evidence does not establish a universally best agent count or justify a wholesale single-agent rewrite.

The assessment reads the current [shared rules](../spec-source-suite/AGENTS.md), [Supervisor](../spec-source-suite/SUPERVISOR.md), [Planner](../spec-source-suite/PLANNER.md), [Implementer](../spec-source-suite/IMPLEMENTER.md), [Reviewer](../spec-source-suite/REVIEWER.md), [Validator](../spec-source-suite/VALIDATOR.md), [model configuration](../spec-source-suite/MODELS.md), [engineering guidelines](../spec-source-suite/GUIDELINES.md), and [tracing reference](../spec-source-suite/helpers/TRACING.md). The inspected checkout was at `867440e0c8272d59b02ad8e9b81d29eabf590b04`. Prior assessment documents were not treated as descriptions of current behavior. No app execution histories were inspected.

**What the workflow actually does**

The supervisor starts a fresh implementer for each ready task. The implementer assesses difficulty. In full mode, a separate fresh planner prepares that task's plan and acceptance, then the original implementer resumes. Lightweight mode lets the implementer do its own concise planning. Full mode is mandatory for complex tasks; simple tasks can use lightweight mode. The supervisor retains owners for corrections, and workers communicate through exact source paths, contracts, results, and selected memory. Task order imposes a predecessor dependency, so execution is serial unless parallelism is explicitly authorized. Independent review and final evaluation complete the process, but they are not the main subject here. [Current orchestration](../spec-source-suite/SUPERVISOR.md), [task modes](../spec-source-suite/AGENTS.md#task-workflows), [task ordering](../spec-source-suite/AGENTS.md#markdown-bundle).

This is a predefined multi-agent workflow containing autonomous coding loops. It already has several adaptations often recommended for agents: a lighter path, targeted source loading, durable artifacts, retained repair owners, and escalation after repeated failure. The question is how well those choices fit the workload and model, rather than whether the workflow has enough named roles.

**Where it matches current practice, and where I would experiment**

| Dimension | Current suite | Assessment and next experiment |
|---|---|---|
| Context selection | Shared rules plus one role; explicit input paths; supervisor avoids detailed worker conversations. | Strong alignment with focused context and progressive disclosure. Measure repeated discovery and handoff loss before changing these boundaries. [Context engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents). |
| Separate planning | Fresh planner for every full-mode task, after implementer assessment. | Plausible for difficult design decisions; its benefit for all complex implementation is unproven. Compare implementer-owned planning with a separate planner while holding the rest of the workflow fixed. [October 2026 practice](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop). |
| Task boundaries | Fresh implementer per task; accepted contracts and memory carry continuity. | Resetting context reduces accumulated noise, but can repeat repository discovery. Compare several tightly related small tasks in one worker session against the current fresh-worker policy. Preserve new contexts for independent investigations. [Context engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents). |
| Scheduling | Every listed task waits for its predecessor; parallelism requires authorization. | Sensible for coupled changes. Independent work can inherit avoidable waiting. Determine actual dependency and ownership boundaries before experimenting with concurrency. Multi-agent gains depend strongly on task structure. [Scaling study](https://arxiv.org/abs/2512.08296v3). |
| Memory | Indexed, selective, source-linked lessons; stale advice must be checked; useful notes survive sessions. | A strong foundation. Measure whether notes prevent rediscovery or repeated failures. Prefer concrete commands, interface decisions, environment facts, and resolved failure causes over general advice. [Local memory rules](../spec-source-suite/AGENTS.md#project-memory). |
| Model routing | Role defaults, demanding routes, a small-change route, and repeated-failure escalation. | Sensible heuristics, but not a demonstrated optimum. Compare models on complete task cost and outcome, including repairs, rather than price per token. [Current routes](../spec-source-suite/MODELS.md). |
| Learning from runs | Native measurements by role, task, model, effort, tool, and timing; unknown measurements remain unknown. | Useful infrastructure for controlled workflow experiments. Add a small outcome comparison alongside existing usage, then change one workflow component at a time. [Tracing](../spec-source-suite/helpers/TRACING.md), [AHE study](https://arxiv.org/abs/2604.25850v4). |

The comparisons above are engineering inferences from the inspected design and the cited evidence; they are not measured weaknesses of this repository.

**OpenSpec and deterministic preflight before model handoff**

Follow-up recommendation: use OpenSpec as a candidate specification-authoring front end, with a small deterministic adapter that prepares task handoffs. This directly reduces mechanical work assigned to the supervisor and can be introduced independently of changing agent roles. I inspected the latest release, [v1.16.1](https://github.com/Fission-AI/OpenSpec/releases/tag/v1.16.1), published 2026-11-07, and its source. No installation, migration, or CLI execution was performed.

The proposed flow is: author requirements and tasks → validate the selected change → check suite task metadata → assemble the selected task's inputs → launch its worker. Invalid input returns actionable file/field diagnostics to the author; implementation dispatch does not start.

OpenSpec's current validator checks specification structure, requirement/scenario conventions, delta rules, and task-checkbox/numbering issues. Strict mode rejects warnings as well as errors. Its separate workflow-schema validation checks artifact IDs, dependency references, and cycles. That graph represents authoring artifacts such as proposal, specs, design, and tasks; it does not automatically represent dependencies between implementation tasks. [Validator](https://github.com/Fission-AI/OpenSpec/blob/v1.16.1/src/core/validation/validator.ts), [artifact schema](https://github.com/Fission-AI/OpenSpec/blob/v1.16.1/src/core/artifact-graph/schema.ts).

For the selected change, the preflight can invoke:

```sh
openspec validate add-todo-search --type change --strict --json --no-interactive
openspec status --change add-todo-search --json
```

The wrapper must evaluate the outputs and required artifacts before dispatch. Status reports artifact existence, not content quality. Prefer explicit selected-change validation for handoff; bulk `--all` is useful for repository-wide maintenance, but its empty-item case exits successfully. [CLI reference](https://github.com/Fission-AI/OpenSpec/blob/v1.16.1/docs/cli.md), [command implementation](https://github.com/Fission-AI/OpenSpec/blob/v1.16.1/src/commands/validate.ts).

The suite-specific adapter should check unique task IDs, explicit prerequisite references and cycles, requirement references that resolve, required input files, output locations, and recognized workflow/model-profile values when specified. It can emit a ready task's exact source paths and scheduling metadata without asking a model to rediscover them. Checking that a requirement is referenced does not prove the task implements it completely; omitted dependencies and contradictory prose still need judgment.

Keep behavioral requirements in OpenSpec specs and implementation steps in its task list. Existing suite task files describe observable behavior, so they should not simply be pasted into OpenSpec's implementation checklist. Add only scheduling metadata the handoff needs. OpenSpec supports `x-` extension keys in change metadata, which could hold task-ID mappings and prerequisites; OpenSpec deliberately ignores those keys, so their schema and validation belong to the adapter. An OpenSpec custom workflow schema can organize these artifacts, but does not itself validate arbitrary task metadata. [Built-in workflow](https://github.com/Fission-AI/OpenSpec/blob/v1.16.1/schemas/spec-driven/schema.yaml), [metadata extensions](https://github.com/Fission-AI/OpenSpec/blob/v1.16.1/docs/cli.md).

Maintain one editable source for each fact. If the existing Markdown bundle remains needed during adoption, generate its compatibility view. The useful first deliverable is a small preflight plus handoff builder, before a large runner or role redesign.

**The most relevant current signals**

Anthropic's October 22, 2026 guidance describes enterprise deployments where folding planner, router, and domain subagents into a main loop improved quality and often cost or latency. It still identifies useful reasons for separate contexts, including parallel work and context pressure. This is first-party deployment experience, not a controlled demonstration that this suite should collapse its roles. Its relevant lesson here is to require a concrete benefit from each boundary. [Article](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop).

The March 24, 2026 application-development case study changed its orchestration when a stronger model became available, removing sprint scaffolding while retaining useful planning. The author removed components incrementally after a broad simplification failed. That supports periodically revisiting the suite's task granularity and role allocation when models change. [Application harness case study](https://www.anthropic.com/research/harness-design-long-running-apps).

OpenAI's February 11, 2026 engineering account emphasizes repository-local knowledge, a small entry-point map, and direct access to the running application, logs, and metrics. This supports the suite's source maps and persistent records. It also suggests a useful allocation of effort: make the worker's environment easier to understand and operate, rather than putting every recurring difficulty into more orchestration prose. [Engineering account](https://openai.com/index/harness-engineering/).

Controlled studies summarized below qualify these practitioner reports. In particular, multi-agent performance depends on the workload, a strong minimal agent is a necessary baseline, and additional repository instructions do not automatically improve outcomes. None supplies a transferable numeric efficiency estimate for this suite.

**Recommended priorities**

1. **Measure the separate planner's contribution first.** On representative work, compare the current full-mode path with the same worker producing and updating its own plan. Keep other conditions unchanged. Track time before the first useful implementation, duplicated discovery, total cost, and resulting functionality. The suite already supports self-planning for simple tasks; the useful experiment concerns the boundary between simple and complex work. Broadening it would be a proposed workflow policy change, not something this assessment implements.

2. **Choose task size around coherent work.** A user-visible capability or a module with a clear interface is a useful candidate boundary. If adjacent tasks share nearly all their context and continually revise one another, keeping an implementer across them may save more than adding parallel workers. If tasks use separate contexts and independent interfaces, bounded parallel work may help. Do not infer independence merely from different filenames. Compare these options separately so their effects remain attributable.

3. **Make planning adaptive without losing architectural continuity.** Keep shared interface decisions and cross-cutting constraints concise and accessible. Ask a specialist to resolve an architectural question or compare alternatives when needed. Let the implementation owner refine the local approach as execution teaches it more. Avoid requiring a second agent to rediscover routine implementation details solely because a task has been labelled complex. This is a proposed direction to test, not a claim that all separate planning is wasteful.

4. **Reduce repeated context work.** The shared file is 2,542 whitespace-delimited words; shared-plus-role totals range from 2,771 to 3,024 words, excluding root instructions, model configuration, project inputs, and tool descriptions. The role files themselves are already short. Use the existing traces to locate repeated reads and searches before trimming rules. Test conditional loading of specialized guidance, such as reconstruction procedures when reconstruction is not being performed, while preserving the constraints applicable to the actual task. Word counts are a loading proxy, not measured token cost or evidence of degraded performance.

5. **Tune routing against complete task outcomes.** Retain the present distinction between coordination, implementation, and demanding reasoning, but calibrate it with actual tasks. A cheaper model can be more expensive after extra attempts; a stronger model may need fewer planning handoffs. Revisit the choice after model upgrades and record which failures were caused by missing information or tooling, since those are not solved merely by escalation.

6. **Improve tools and feedback where runs show friction.** Helpers for preparing handoffs, finding relevant context, starting disposable environments, or summarizing actionable failures can remove mechanical work. The suite is intentionally reusable guidance running on a host harness; the absence of its own runner is not by itself a defect. A large runner or framework migration should follow a demonstrated operational need. For this assessment, it is a lower priority than understanding role cost and context continuity.

**A practical comparison**

Use representative UI, CLI, API, and cross-component tasks at several difficulty levels. Establish the current workflow as the baseline. Change only one factor at a time: separate versus worker-owned planning; fresh versus retained workers across related tasks; current versus selectively loaded guidance; then model routing. Keep starting repository, requested behavior, tools, model settings, and available budget comparable. Repeat trials and report variability; a small pilot can reveal large effects but cannot establish small differences reliably.

Record completed functionality, human intervention, elapsed time, available token/cost measurements, repair effort, repeated discovery, handoff count, and time spent waiting for another role. Include unsuccessful and blocked runs. Choose changes that improve the quality/time/cost tradeoff on the intended workload. Usage totals alone cannot tell whether planning helped, and a single impressive build cannot establish reliability. [Evaluation methodology](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).

No workflow or application code was changed. The accompanying empirical evidence is a literature review; no comparative application runs were performed for this assessment.


## Empirical evidence

### 1. Coordination should follow task structure

**Source:** [Towards a Science of Scaling Agent Systems, v3](https://arxiv.org/html/2512.08296v3), first submitted 2025-12-09; revised 2026-04-08.

Across 260 configurations, six benchmarks, five architectures, and three model families, the authors controlled tools, prompts, and compute. Relative gains over single-agent baselines ranged from +80.8% on decomposable financial work to −70.0% on sequential planning. Coordination had diminishing returns as baseline capability rose; tool-heavy work incurred overhead. The revised study includes SWE-bench Verified and Terminal-Bench, beyond the four domains in earlier coverage.

**Limits:** Canonical architectures are not every production workflow. The fitted model's cross-validated R² was 0.373, or 0.413 with the task-grounded capability measure; the reported 87% architecture-selection result concerns held-out configurations, not universal unseen-task prediction.

**Workflow inference:** Keep clear integration ownership and dispatch separable work selectively. These results do not establish that a sequential implementation/review/validation pipeline should become a single agent.

### 2. Instruction compliance does not imply improved task success

**Source:** [Evaluating AGENTS.md, v3](https://arxiv.org/html/2602.11988v3), first submitted 2026-02-12; revised 2026-09-29.

The study evaluates 300 SWE-bench Lite tasks and 138 CTXbench tasks using four model/agent configurations. Context files did not generally improve success, while inference cost increased by over 20% on average. Instructions were followed; repository overviews did not provide the expected benefit. In the revised analysis, success differences between no context and generated/developer context were not statistically significant. Each configuration used one completion per task.

**Limits:** This is repository issue resolution with test-based scoring, not a controlled evaluation of specification authority, handoff provenance, or required engineering conventions. Extra instructed checks may impose costs that a benchmark does not reward.

**Workflow inference:** Measure shared and role-specific instruction overhead; retain necessary conventions and authority rules, and trim duplicated discoverable facts. The paper does not justify deleting AGENTS.md wholesale.

### 3. Strong models can make elaborate domain harnesses redundant

**Source:** [How Much of a Harness Does a Strong Agent Need for Autonomous ML Engineering?, v1](https://arxiv.org/html/2609.40303v1), submitted 2026-09-30.

Under matched backbones and time budgets, a minimal single-session coding agent matches or exceeds four specialized open-source ML engineering harnesses across tested frontier backbones. The comparison covers 30 MLE-bench tasks and 40 NatureBench tasks. A weaker Gemma backbone benefits more from a specialized harness, qualifying the general result.

**Limits:** This concerns autonomous ML experimentation and competitive benchmark outcomes, not application delivery, reviewability, or organizational controls. Some confidence intervals are broad. MLE-bench has public-task contamination and preparation concerns; the authors repair identified tasks and add NatureBench as a second benchmark.

**Workflow inference:** Include a strong model with a simple workflow as an ablation baseline. Do not infer that every planning, review, or validation stage is unnecessary.

### 4. Useful harness complexity can be discovered through measured failures

**Source:** [Agentic Harness Engineering, v4](https://arxiv.org/html/2604.25850v4), first submitted 2026-04-28; revised 2026-05-18.

The authors evolve a harness using inspectable components, summarized trajectories, and predictions attached to changes. Ten iterations raise Terminal-Bench 2 pass@1 from 69.7% to 77.0%. The frozen result transfers to SWE-bench Verified and alternate model families. Ablations attribute gains to tools, middleware, and memory more than the system prompt.

**Limits:** The headline result selects the best configuration from evolution on all 89 Terminal-Bench tasks, rather than an untouched test split. Transfer is stronger evidence of generality. One evolution campaign and model-specific timeout/step settings limit conclusions. Regression prediction remains weak.

**Workflow inference:** Convert execution evidence into explicit, testable workflow changes. Stored logs alone do not demonstrate an improvement loop; compare revisions against a fixed task set and retain rollback information.

### 5. Routing benefits from measured task-specific performance

**Source:** [Agent-as-a-Router, v3](https://arxiv.org/html/2606.22902v3), first submitted 2026-06-22; revised 2026-06-26.

CodeRouterBench contains 10,111 tasks and eight candidate models. A router that accumulates verified execution experience outperforms static alternatives on the authors' comparisons, including 176 held-out agentic programming tasks. Supplying task-dimension performance statistics improves a basic model router by 15.3% relative. No tested model dominates every coding dimension.

**Limits:** Most tasks are single-turn coding; three dimensions use proxy metrics and model judges. The agentic subset uses a 40-step cap instead of the standard 250. Monetary estimates use listed token prices without observable provider cache-hit rates. This does not establish durable model rankings or validate a particular role-to-model assignment.

**Workflow inference:** Treat model and reasoning-effort defaults as hypotheses to update from local outcomes, rather than deriving them only from model reputation or role labels.

### 6. A fresh specialist can help without receiving the whole history

**Source:** [Rethinking Verification in Agent Harnesses, v1](https://arxiv.org/html/2610.34577v1), submitted 2026-10-25.

In this preprint's comparison of 17 designs across seven coding models, a fresh critic improves average task accuracy. Supplying the entire execution trajectory does not consistently improve outcomes and increases critic cost by 29–43%; the authors recommend task requirements and changes as default context.

**Limits:** Selected task subsets and one fixed critic model limit generalization. This is supporting evidence for bounded specialist handoffs, not proof that each extra workflow stage is worthwhile.
