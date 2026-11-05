**`plan.md` — Simplify the specification-driven workflow**

**Task:** `simplify-spec-workflow`  
**Baseline commit:** `0da44c5e4533f42abcc3f405a7c9a6c3c3413cef`

**Goal.** Make the suite’s ordinary app-generation procedure easy to follow while retaining subsystem dependencies, approved contracts, isolated agent contexts, and acceptance-driven correction.

**Scope.** Revise the suite guidance, skill instructions, prompts, and templates, plus the repository’s routing instructions and local acceptance-spec skill. Preserve existing staged work. This task produces no TODO implementation or executable orchestration framework.

**Architecture and procedure.**

1. **Keep three workflow stages.** Define establishes subsystem contracts and acceptance; Generate derives and supervises the DAG; Implement runs one task’s planner–implementer–reviewer cycle. Put shared rules in the shared contract and reference them from the procedures.
2. **Make subsystem specs the graph nodes.** Each registered spec has a stable ID, `depends_on`, observable contracts, and requirement-linked acceptance criteria. Derive the DAG from these declarations. Reject missing prerequisites and cycles. Use one subsystem per task by default; additional implementation tasks reference its requirements without creating competing specifications.
3. **Preserve the two task documents.** Store the complete agreed plan and authoritative acceptance document under `.agents/tasks/<task-id>/`. Register a subsystem’s `acceptance.md` directly as its spec. Keep project metadata and target profiles outside the suite, using `specs/` by default. Record the baseline commit and approval of both document digests before implementation.
4. **Use three agent roles per task.** The planner prepares the documents and requirement-linked executable checks. After document approval, freeze the checks before implementation. The implementer receives both documents and accepted dependency inputs. It spawns a reviewer with fresh context and no inherited conversation, providing acceptance, baseline, candidate location, and checks—but not the plan. The reviewer examines coverage and executes acceptance against the candidate.
5. **Bound the correction loop.** Allow the initial candidate and two repair rounds. Confirmed implementation defects return to the implementer. Specification ambiguity, verifier defects, significant plan deviations, and infrastructure blockers return to the supervisor immediately. Changes to approved documents require user authorization.
6. **Advance through evidence.** The supervisor accepts a node only when its required checks and independent review pass. Execute nodes serially; blocked nodes cannot unlock consumers. Run whole-app acceptance against the assembled candidate. Changes to accepted dependencies invalidate affected downstream evidence.
7. **Keep isolation claims accurate.** The initial procedure uses fresh contexts, scoped write ownership, and baseline-integrity checks. Label this procedural separation. Preserve enforced isolation as an explicit stronger policy, with unavailable enforcement reported as blocked when that policy is required.
8. **Reduce mandatory paperwork.** Keep short spec and plan templates, a manifest, a target profile, executable checks, and one run directory containing raw check results and review findings. Record identities, approval references, candidate revisions, attempts, and outcomes there. Make a separate verification-design document optional when the acceptance document already supplies the necessary mapping. Move regeneration and cross-target details behind conditional references while preserving their safeguards.

**Implementation order.** Update the shared contract and workflows first; align skills, prompts, templates, and repository instructions next; then validate consistency and obtain fresh review. Use the available fresh-context subagent mechanism for the reviewer role rather than require a runtime-specific TOML file.

**Validation.** Check local links, template metadata, requirement references, and package checksums. Walk through a two-node dependency graph, a failed prerequisite, a cycle, a repair, and a specification conflict. Label these as procedure walkthroughs, not app-generation evidence. Refresh package-check records only for checks actually executed. Have an independent reviewer evaluate the final changes against the acceptance document.

**Deferred example.** The later TODO exercise uses persistence → task-management CLI, `uv` with a basic `pyproject.toml`, and `apps/todo/tasks.json`. Its detailed contracts will be planned and approved using the revised procedure.
