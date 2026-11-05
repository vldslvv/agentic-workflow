# Generate — supervise the subsystem DAG

Read the [shared contract](SUITE_CONTRACT.md), [Implement skill](../.agents/skills/spec-implement/SKILL.md), and [Implement workflow](IMPLEMENT.md). Generate coordinates those task cycles; it does not define another worker loop.

**Inputs:** approved standard Markdown bundle, execution input inventory, target constraints, scope/mode, retained inputs, authorized outputs, and verification arrangement. **Outputs:** subsystem candidates and evidence plus assembled-app acceptance in one run directory. No specs yields NO_PROJECT.

Read the [standard bundle format](MARKDOWN_BUNDLES.md) before validating execution readiness. Resolve `project.md`, `task_order.md`, `tasks/*.md`, and `verification.md`; incomplete inputs require authorized Define preparation before dispatch.

## G1. Select mode and validate inputs

Use `initial` for new implementation or `incremental` for authorized changes with existing-code access. For `regenerate` or `cross-target`, read [REGENERATION.md](REGENERATION.md) before preparing work. If enforced isolation is required, also read [STRONG_ISOLATION.md](STRONG_ISOLATION.md). These are explicit branches, not prerequisites for ordinary generation.

For initial generation, use a new authorized output directory, possibly within the existing repository; leave other project files intact. Incremental work uses declared existing paths. Record retained assets/state and external boundaries; code generation does not recreate unavailable data or services.

## G2. Resolve the graph and handoffs

Derive and validate the DAG under contract §5. Select prerequisite closure or identify already accepted dependencies. Identify downstream impact separately. For each selected task, obtain the persisted planner handoff from [Define](DEFINE.md), target constraints, and integrity inventory. Record the project-level assembled-app checks before execution.

**Readiness gate:** no unresolved graph/input/approval/check requirements; ready nodes have current accepted prerequisites. The input inventory points to source-linked acceptance records; their prerequisite mapping must match the bundle's order and declarations.

## G3. Execute ready tasks

Run serially by default. Dispatch each ready task to [Implement](IMPLEMENT.md), with a fresh implementer context and only its approved inputs. The supervisor records node outcomes and identities in the run directory; it does not rely on worker memory. Apply contract §§5–7 to readiness, repair limits, failures, and reuse. Failed or blocked prerequisites keep consumers blocked.

## G4. Assess the assembled app

After selected nodes pass, execute the frozen project-level checks against the actual assembled candidate, including cross-subsystem interactions and required manual criteria. Preserve outputs, candidate identity, and environment. Individual node passes cannot satisfy this gate. Assembly failures follow contract §6; do not invent a separate unlimited repair loop. Changes to accepted nodes invalidate affected downstream and assembled evidence.

## G5. Record the scope result

Use [RUN_REPORT.md](../templates/RUN_REPORT.md) and the contract §7 completion policy. Record PASS only with all mandatory gates satisfied; otherwise retain FAIL, BLOCKED, and NOT_RUN dispositions and the next action. Distinguish partial scope from project acceptance and procedural separation from enforced isolation. Regeneration claims require the selected branch's additional evidence.
