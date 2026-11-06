# Independent conformance review — 01_business_logic, attempt 0

**Spec bundle and requirement IDs:** `specs/todolist_rust`, task `01_business_logic`, B1–B5. Source SHA256 `1262a1da26f58cb390a87ac067f8775dc33c366e1da83ad3d2928ef96ad2556f`; acceptance SHA256 `33fd28afc0f8541ca09db80459320b7e1696ab122f50a40394c9ec04070b9b90`. Source and other protected digests are recorded in `../frozen-inventory.json` and verified before/after execution.

**Candidate:** `apps/todolist_rust`, SHA256 `e0ddd6462a8e828d624f137d75f400676bb4b2a4458d2f734ae361a8a415281e`. Baseline commit `07fd1484a33826b53c9e669b7490175bce1bd11a`. Identity includes Cargo.lock and excludes generated target contents and tasks.json. Authorization is `.agents/tasks/008-rust-01_business_logic/approval.json`, direct implementation request with derived agent-authored acceptance.

**Reviewer/session:** `/root/rust_business/review_business`, fresh independent child of implementer. No inherited implementation conversation was present; only the explicit task handoff was supplied. Review performed 2026-11-05.

**Review kind:** INDEPENDENT_REVIEW.

**Inputs actually inspected:** root/suite AGENTS.md, shared contract, Markdown bundle procedure, Implement skill/workflow, REVIEWER.md, VERIFIER.md, review template; business source task and shared project/task-order/verification documents; business acceptance/approval/inputs; frozen inventory and verifier; candidate Cargo.toml, src/lib.rs and .gitignore; implementer before/results.json, attempt-0 build.json/build-retry.json and business commands/results. Cargo.lock was digest-verified, not semantically reviewed. Test-audit skill was read for coverage assessment. Plans and all planner/implementer conversations were excluded; frozen integrity verification only hashed protected plans and other tasks' records.

**Integrity and execution:** `attempt-0/before/results.json` and `attempt-0/after/results.json` both match the supplied candidate SHA256 and all 29 frozen protected files. `attempt-0/business/commands.json` retains independent external-consumer execution, exit 0, and actual stdout/stderr. `attempt-0/business/results.json` records B1–B5 PASS and before/after integrity PASS. Run command: `CARGO_NET_OFFLINE=true python3 .suite/runs/008-todolist-rust/checks/verify.py business --evidence .suite/runs/008-todolist-rust/business-reviewer/attempt-0/business`. `attempt-0/build.json` records rustc/cargo 1.99.0, cargo fmt --check and cargo build --locked, all exit 0. Supplemental public-library observations and exact commands are preserved in `attempt-0/additional_observations.rs` and `attempt-0/additional-observations.json`; both compilation and execution exited 0. These observations use reviewer-owned data, cleaned on success. No manual acceptance gate applies.

## Findings

No blocking implementation discrepancy, protected-input change, or candidate change was observed.

| Finding ID | Requirement IDs | Observation and evidence | Severity | Required resolution |
|---|---|---|---|---|
| R1 | B1, B3, B4, B5 | Frozen business assertions do not explicitly exercise default_path or snapshot every field after rejected operations. Code inspection establishes early failure before saving and manifest-root path resolution; supplemental executed public-library observations additionally prove exact file-byte preservation after invalid add/unknown complete/unknown delete, repeated-completion idempotence, and default path from cwd `/`. | Nonblocking; coverage supplemented | No candidate change required. Preserve these observations with the frozen-check results. |

## Coverage and evidence gaps

| Requirement | Disposition | Independently observed evidence |
|---|---|---|
| B1 | PASS | Frozen external consumer opens missing JSON store, rejects blank description, creates trimmed Unicode description, New status and positive increasing IDs including after deletion. Supplemental invalid add preserves exact bytes. |
| B2 | PASS | Frozen external consumer verifies persistent listing, Completed task retention, deleted-task exclusion and increasing remaining IDs; code sorts by ID and filters Deleted. |
| B3 | PASS | Frozen external consumer rejects unknown delete, hides deleted task, retains other task and rejects completing deleted task; supplemental unknown delete preserves exact bytes. |
| B4 | PASS | Frozen external consumer sets Completed, repeats completion and rejects unknown ID; supplemental repeat completion and invalid completion preserve exact bytes. |
| B5 | PASS | Frozen consumer reopens persistent data and proves malformed JSON fails without overwrite; source inspection and executed default_path observation establish app-root tasks.json independent of cwd. |

All prescribed business checks executed. Supplemental observations strengthen narrow assertions without changing frozen expectations. Actual CLI default-path file creation is a later CLI gate, not claimed executed in this business-library review. The verifier emits an unused_mut warning in its consumer; candidate formatting and locked build pass. No dependent subsystem, manual criterion, or assembled-app gate is in this review scope.

## Scope and unintended behavior

Implementation uses Rust with serde JSON and temporary-file persistence. Deleted records remain internally with Deleted status, which is consistent with deletion from active listing and monotonically increasing IDs. Concurrent writers require external coordination as documented; concurrent writer support is not required by this scope. No additional runtime or UI requirements were inferred. Procedural isolation only: independent context, reviewer-owned evidence and before/after digests; no enforced write sandbox is claimed. Reviewer changed only reviewer-owned evidence and ephemeral build artifacts. Frozen checks and candidate source remained unchanged.

## Outcome

**PASS** for independent business review and acceptance execution, attempt 0, requirements B1–B5 at the recorded candidate identity. Every selected requirement has passing independent execution plus relevant code inspection; no unresolved blocking finding remains. This subsystem result does not establish later CLI/database or assembled-app acceptance.
