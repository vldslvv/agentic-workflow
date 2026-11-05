# Future generation order — TODO CLI

This is an execution-order document, not authorization to execute it. The current task produces documents only. The [documentation plan](../.agents/tasks/002-todo-cli/plan.md) remains unchanged; a later generation task needs its own approved implementation plan and must not reinterpret that document as implementation permission.

## Inputs and dependency order

Load [project.yaml](project.yaml), the registered authoritative acceptance and approval record, and the selected target. There is one subsystem, `TODO-CLI`, with `depends_on: []`; its selected scope is TODO-R001 through TODO-R012. No retained assets or accepted prerequisite subsystems are required.

The reserved run location for this task is `.suite/runs/002-todo-cli/` relative to the repository root; documentation work does not create it. A separately numbered generation task must allocate the next unused shared sequence for its task and matching run directories, and select the existing specification rather than copy requirements.

## Sequence and exit gates

1. **Approve the documentation.** Resolve review changes, record approval and document digests, and verify baseline and guidance identities. Exit when the exact acceptance and target contents are approved. Approval alone does not start generation.
2. **Prepare the handoff under separate authorization.** Read the Generate and Implement skills/workflows identified by repository AGENTS.md. Prepare the later implementation plan and requirement-linked executable C01–C12 checks, fixtures, execution adapter, and offline/filesystem-failure arrangements. Register executable checks and assembled-app C12 in the manifest. Freeze normative inputs and obtain the approvals required by the suite. Exit only when readiness is satisfied; missing mechanisms remain BLOCKED.
3. **Generate the initial candidate.** Dispatch the implementer with approved requirements, target, ownership, baseline identities, and checks. Candidate ownership is `app/`; planner-owned documentation and checks stay protected. Exit with an identified candidate, local results, and input-integrity comparison.
4. **Review independently.** The implementer spawns a fresh-context reviewer with a narrow allowlist: acceptance and normative references, approval identities, selected IDs, target, candidate, frozen checks, and raw results. Exclude plans and prior conversation. The reviewer executes acceptance against the candidate and owns its result files. Exit with requirement-linked findings, raw evidence, and integrity results.
5. **Resolve findings within the suite bounds.** Permit candidate 0 and two repair rounds. Modified candidates require renewed review and affected acceptance evidence. Specification conflicts, verifier defects, missing infrastructure, and significant plan deviations return to the supervisor; they are not silently repaired by changing acceptance. Exit on acceptance or an explicit FAIL/BLOCKED outcome with retained evidence.
6. **Accept the assembled app and report.** Require all mandatory checks, independent review, C12 assembled-app execution, and integrity gates to pass. No manual app gate applies. Record actual isolation, limitations, candidate identities, first-attempt results, eventual outcome, and unexecuted gates in the suite's run-report/review formats.
7. **Assess the workflow.** Conduct a separate user walkthrough of the procedure and collect friction. Propose changes to suite guidance in a separate task. App acceptance does not depend on this walkthrough; workflow assessment remains pending until feedback is collected.

## Ownership and evidence

The planner owns acceptance, target, executable checks, fixtures, adapters, and frozen inventory. The implementer owns candidate files and implementation logs. The reviewer owns review reports and independent acceptance results. The parent coordinates approvals and acceptance from evidence. Use procedural isolation and serial execution; a digest check detects writes but is not an enforced sandbox.

The documentation inventory records saved document and guidance identities only. It is not the future frozen handoff inventory. Current app acceptance, independent review, and assembled-app checks are NOT_RUN; generation readiness is BLOCKED.
