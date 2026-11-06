# Planning records and check authorship

Planning reference for the supervisor or an explicitly delegated planner, reached from [Define](DEFINE.md). [Shared contract](SUITE_CONTRACT.md) governs authority and acceptance.

## Task records

Keep the complete plan and authoritative source-linked acceptance in `.suite/tasks/<NNN>-<task-id>/`, plus approval record identifying the full baseline Git commit, both document digests, normative source digests, authority and conversation/decision reference. Direct implementation requests authorize agent-authored derived handoffs; label them accordingly. For explicitly reviewed documents preserve exact approved bytes. Plans explain implementation, never replace requirements.

Allocate the next shared three-digit sequence across immediate directory names in `.suite/tasks/` and `.suite/runs/`; do not read earlier documents for allocation. Logical task IDs remain separate from storage prefixes. Resolve a supplied ID by its numbered suffix and ask on ambiguity. Relocation preserves approved text/history and records old-to-new references.

For continuing work use identified records and relevant state only. If approved originals are missing, recover complete text and approval from that task's known conversation/local transcript; a summary cannot replace it. If unavailable, state locations checked and request missing inputs. Fresh work uses current sources without history discovery.

In Plan mode present complete plan and acceptance drafts; state when saving is deferred. On entering editing mode save approved text exactly and bind approval before implementation/handoff. Approval alone does not start execution; an existing explicit implementation instruction does. Changes need authority and versioned digests; use [CHANGE](../templates/CHANGE.md), invalidate affected evidence and preserve prior records.

## Check authorship

Create plans and checks only when a task is ready, using current accepted dependency contracts. A planner can read relevant normative sources and inspect authorized existing interfaces without importing unrelated task narratives. Acceptance references exact clauses/digests and derived prerequisites. Describe normal, boundary, failure and interaction checks as applicable; a passing command alone cannot establish coverage.

Keep task, regression and final end-to-end checks distinct. Link shared scenarios from `verification.md`; avoid duplicating assertions in handoffs. Freeze versioned content inventories of source documents, checks, fixtures and adapters. Setup/check/cleanup manifests can use the [check helper](HELPERS.md#check-execution); this is execution plumbing, not acceptance authority.

For a reviewer coverage reproduction, validate the link to an existing requirement, propose an additive check revision to the supervisor, retain old frozen bytes and record authorization/new digests. Execute against the defective candidate and repaired candidate where available. Requirement changes, weakened expectations and other corrections remain outside delegated additive authority.

The supervisor retains planning decisions and records paths, digests, readiness and unresolved decisions. A delegated planner returns those references; the supervisor reads the complete plan/acceptance before dispatch. Implementer receives the full approved plan/acceptance through explicit read paths; reviewer receives acceptance and normative inputs through a separate manifest that excludes plans/conversations.
