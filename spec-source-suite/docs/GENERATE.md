# Generate — supervise the selected graph

Read [shared contract](SUITE_CONTRACT.md) once and [bundle format](MARKDOWN_BUNDLES.md). The supervisor owns planning and acceptance as well as coordination. Retain source requirements, graph, shared constraints, plan/acceptance decisions, interfaces, dependency identities and blockers. Load [Define](DEFINE.md) when the first task is ready; implementer/reviewer procedures belong to their worker contexts.

## G1. Establish inputs and mode

Resolve selected bundle, scope, target, outputs, retained inputs, verification arrangement and evidence root. Initial work uses a new authorized output directory; incremental work uses declared existing paths. Missing inputs yield BLOCKED; no intent yields NO_PROJECT. Only for regeneration/cross-target read [Regeneration](REGENERATION.md); only for required enforcement read [Strong isolation](STRONG_ISOLATION.md). Record actual controls and limitations.

Record the selected project root for [memory](PROJECT_MEMORY.md); select notes through Define when planning ordinary tasks. Regeneration contexts use its exclusion rules.

## G2. Validate graph and prepare final verification

Validate ordered tasks plus explicit dependencies, prerequisite closure and already accepted revisions under contract §3. Record project-level assembled-app scenarios before execution. Do not create every task's plan/checks up front.

## G3. Plan and dispatch each ready task

For each ready task, follow Define in this context using its normative sources, shared constraints and accepted dependency contracts. Save the complete plan/acceptance, authority, executable checks and frozen identities before dispatch. Record readiness in the task receipt; the implementation-handoff gate must pass. Keep the decisions available for downstream planning and repairs. Explicitly delegated planning follows contract §2.

Dispatch a fresh implementer with [Implement](IMPLEMENT.md) and explicit role manifest. It receives the complete approved plan/acceptance and owns its repair loop/reviewer spawning. Keep it alive through repairs. Accept from execution, coverage, review, integrity and dependency evidence under contract §5; inspect raw logs for failures/disputes. As planner, validate the requirement mapping of coverage additions before authorizing them under contract §4. Failed prerequisites keep consumers blocked.

Use completion/blocker messages and supported waits, bounded by the platform's progress-update interval. Report new findings, decisions or blockers at meaningful checkpoints; keep required interim updates concise. Reuse known decisions and digest checks rather than repeatedly loading unchanged documents. Helpers validate manifests and retain evidence; they do not schedule agents.

## G4. Verify assembled app

After all selected tasks are accepted, independently execute the declared final end-to-end scenarios on the actual assembled candidate, including cross-task interactions and applicable manual gates. Preserve identity and execution evidence. Task passes do not replace this execution. Assembly defects route under contract §4 and invalidate affected node/downstream evidence before renewed final execution.

## G5. Report

Return concise scope status, accepted identities, attempts and evidence paths using [run report](../templates/RUN_REPORT.md). Distinguish first-attempt and eventual outcomes, partial scope, actual isolation and blocked gates. For measured runs retain explicit root/descendant session references and [usage report](HELPERS.md#usage-reporting), including per-role usage, unavailable counters and outer-driver overhead separately.

Apply [memory maintenance](PROJECT_MEMORY.md#completing-and-maintaining) for supported project-level lessons, including a blocked stop.
