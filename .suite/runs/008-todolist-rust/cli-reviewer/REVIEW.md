# Independent conformance review — 02_cli, attempt 0

**Outcome: PASS.** C1–C5 and business regressions B1–B5 passed independent execution. No blocking implementation findings remain. This is subsystem review, not final PostgreSQL or assembled-app acceptance.

**Spec bundle and requirement IDs:** `specs/todolist_rust`, C1–C5; prerequisite regressions B1–B5. Source SHA256 identities are recorded in `../frozen-inventory.json` and `.agents/tasks/009-rust-02_cli/approval.json`. The acceptance digest is `55db6d0be1d60a5b9de88860b583965821a63edce107282ebe9095c4af3454fb`; frozen verifier digest is `ba719bf41eacc570baf59aa01695889475b9e38df11e96fb7377442bb3d05482`.

**Candidate:** `apps/todolist_rust`, SHA256 `6739545cf7ccabd8e5facd48e01d51c75b987f8ea92b5cb1fd98392def9788a9`, using the frozen identity function (excludes target/, tasks.json and .git). Before/after per-file identities match. Accepted business prerequisite: `e0ddd6462a8e828d624f137d75f400676bb4b2a4458d2f734ae361a8a415281e`; every prerequisite candidate file remains byte-identical.

**Reviewer/session:** `/root/rust_cli/cli_reviewer`; spawned by implementer with `fork_turns=none`. No inherited conversation or plan contents read. Review kind: **INDEPENDENT_REVIEW**. Isolation is procedural, not an enforced filesystem boundary.

## Inputs actually inspected

- Root `AGENTS.md`; suite `AGENTS.md`, shared contract, Markdown bundle standard, Implement workflow/skill, reviewer/verifier prompts and review template.
- All six Markdown files in `specs/todolist_rust` (project, task order, verification, and the three selected task sources); CLI acceptance and approval; shared execution `inputs.md` from `.agents/tasks/008-rust-01_business_logic`.
- Frozen inventory and `checks/verify.py`; `business-acceptance.json`; allowlisted implementer before identity, attempt-0 build record, CLI results and command logs.
- Candidate `.gitignore`, `Cargo.toml`, `Cargo.lock`, `README.md`, `src/lib.rs`, `src/main.rs`. No target code/artifact contents inspected.
- Reviewer-owned evidence generated below. Protected files outside this textual allowlist, including plans, were hashed only by the frozen inventory routine.

## Integrity and execution

All 29 frozen input digests passed before and after execution. Evidence: `before/results.json`, `attempt-0/cli/results.json`, `after/results.json`.

Approved baseline `07fd1484a33826b53c9e669b7490175bce1bd11a` exists as a commit (`git cat-file -t`, exit 0) and is an ancestor of current HEAD (`git merge-base --is-ancestor`, exit 0). Current HEAD was `9eba8882bbcafd477059e9db3d98e364586af42f` (`git rev-parse HEAD`, exit 0). Review is bound to actual candidate content and protected source digests, not an assumption that HEAD still equals the initial baseline.

Commands independently executed from repository root, all exit 0:

1. `python3 .suite/runs/008-todolist-rust/checks/verify.py identity --evidence .suite/runs/008-todolist-rust/cli-reviewer/before`
2. `CARGO_NET_OFFLINE=true python3 .suite/runs/008-todolist-rust/checks/verify.py cli --evidence .suite/runs/008-todolist-rust/cli-reviewer/attempt-0/cli`
3. `python3 .suite/runs/008-todolist-rust/cli-reviewer/formatting.py`
4. `python3 .suite/runs/008-todolist-rust/checks/verify.py identity --evidence .suite/runs/008-todolist-rust/cli-reviewer/after`

Raw subprocess commands, working directories, stdout/stderr and exits are preserved in `attempt-0/cli/commands.json` and `attempt-0/formatting.json`. Frozen CLI execution compiled a fresh external business consumer, built the production binary with `cargo build --locked`, and invoked independent CLI processes from a temporary working directory. Expected invalid-command/operation exits were 1 with explanatory stderr; successful operations exited 0. Tests preserved/restored app-root data; supplementary restoration is explicitly recorded. The external frozen consumer emits an unused-mut warning, without affecting success.

## Requirements and evidence

| Requirement | Disposition | Independently observed evidence |
|---|---|---|
| C1 | PASS | Quoted Unicode and punctuation descriptions persist; trimming and blank rejection work. Add stdout reports the assigned ID. Frozen CLI logs and supplemental formatting logs. |
| C2 | PASS | Deletion removes the row; invalid, unknown and already-deleted IDs fail with stderr. Frozen CLI logs. |
| C3 | PASS | Completion persists across processes, is repeatable, reports success and displays Completed. Frozen and supplemental logs. |
| C4 | PASS | Empty list succeeds; exact tab-separated header, ordered rows and correct statuses are observed. Supplement exercises embedded tab/newline/carriage return/backslash escaping while preserving one physical row per task. |
| C5 | PASS | No arguments, help and --help show usage; unknown commands, missing/extra arguments and malformed IDs fail with explanatory stderr. Invocation from another directory stores only at app-root tasks.json; corrupt data is rejected without overwrite. |
| B1–B5 | PASS | Frozen external production-library consumer reran all five regression IDs successfully: creation/validation/IDs, listing, deletion, completion, and persistent reopen/error behavior. Prerequisite source files also remain unchanged. |
| Independent review | PASS | Fresh context, coverage/code inspection and independently executed checks, with reviewer-owned raw evidence. |
| Integrity | PASS | 29 protected digests and candidate identities unchanged before/after; accepted prerequisite file digests retained. |

No manual acceptance applies. Database and assembled-app checks were outside this phase and were not run.

## Findings and coverage gaps

No blocking findings. The frozen suite exercises standard descriptions and records confirmation text, but does not explicitly assert confirmation output or execute escaped control characters. Reviewer-owned `formatting.py` closes those disclosed C1/C3/C4 coverage gaps for this candidate, with exact raw outputs retained in `attempt-0/formatting.json`. Frozen expectations and source documents were not modified. This supplemental evidence must accompany review reuse.

Code inspection confirms a small Rust command dispatcher calling the unchanged business library, strict command arity, positive integer IDs, sorted active rows, escaped descriptions, and nonzero stderr failures. It adds no storage or dependency substitution. JSON remains the explicitly authorized interim storage; Docker/PostgreSQL belongs to task 03. No new normative requirement, mandatory manual gate, or unexecuted CLI acceptance clause was introduced.

## Outcome

**PASS for attempt 0, C1–C5 plus B1–B5 regressions**, against candidate `6739545cf7ccabd8e5facd48e01d51c75b987f8ea92b5cb1fd98392def9788a9`. Supervisor acceptance remains a separate responsibility. No behavioral repair round was consumed.
