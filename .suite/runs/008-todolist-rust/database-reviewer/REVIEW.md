# Independent conformance review — 03_database, attempt 0

**Spec bundle and requirement IDs:** `specs/todolist_rust`, D1–D5; retained B1–B4/C1–C5 operation behavior, with JSON storage explicitly superseded. Source and acceptance digests match `../frozen-inventory.json` and `.agents/tasks/010-rust-03_database/approval.json`. Authority baseline: `07fd1484a33826b53c9e669b7490175bce1bd11a`.

**Candidate:** `apps/todolist_rust`, content SHA256 `3890639c8b52adc24f23c761ead2364c18f88b22a1fc6aa77db63f020d5e389a`. Accepted CLI prerequisite content identity `6739545cf7ccabd8e5facd48e01d51c75b987f8ea92b5cb1fd98392def9788a9`, as recorded in `../cli-acceptance.json`.

**Reviewer/session:** `/root/rust_database/database_review`, spawned with fresh context and an explicit restricted handoff. No planner/implementer conversation or plan text inspected. Plan bytes were hashed solely by the frozen integrity check.

**Review kind:** INDEPENDENT_REVIEW.

**Inputs actually inspected:** Root/suite AGENTS; suite contract, Markdown bundle and Implement procedures/skill; REVIEWER, VERIFIER and REVIEW template; selected six bundle documents; database acceptance/approval, business inputs/acceptance and CLI acceptance; frozen inventory and complete verifier; business/CLI acceptance receipts; all seven candidate files including Cargo.lock; implementer attempt-0 scope/environment raw result. Test-audit skill and audit guidance were read for coverage assessment. The suggested top-level `input-identity` directory was absent; independently computed before/after identity establishes the supplied candidate identity instead. No historical task discovery occurred.

**Integrity and execution:** All 29 protected inventory entries matched before and after. Candidate identity matched the supplied SHA256 both times (`before/results.json`, `after/results.json`). Independent frozen command `python3 .suite/runs/008-todolist-rust/checks/verify.py database --evidence .suite/runs/008-todolist-rust/database-reviewer/attempt-0/database` exited 0. Its 52 commands, exits and raw outputs are in `attempt-0/database/commands.json`; results are in the sibling results.json. Real Docker PostgreSQL was independently provisioned, restarted, stopped and removed, including only the isolated project volume/network. Docker execution required approved sandbox escalation. Additional real-DB observations ran via `python3 .suite/runs/008-todolist-rust/database-reviewer/observe.py`, exit 0, with commands and assertions recorded in `attempt-0/supplemental.json`. These checks use the public executable and SQL boundaries without changing source or frozen checks. No manual acceptance gate applies.

## Findings

| Finding ID | Requirement IDs | Observation and evidence | Severity | Required resolution |
|---|---|---|---|---|
| DB-01 | D2 | `Store::open` sets a TCP connect timeout, but CLI startup has no bound around PostgreSQL session establishment. With DATABASE_URL pointed at an isolated localhost socket that accepts TCP and sends no PostgreSQL startup response, `todolist help` was still running after 11.0068 seconds with empty stdout/stderr. The reviewer killed the process at 11 seconds. Raw observation: `attempt-0/connection-stall.json`. The required failure deadline is under 10 seconds. | blocking, implementation defect | Bound the CLI's live-connection/startup check so an endpoint that cannot establish a PostgreSQL session fails within 10 seconds, nonzero with explanatory stderr. Re-execute the frozen scenario and this failure case on the repaired candidate. |

## Coverage and evidence gaps

| Requirements | Disposition and evidence |
|---|---|
| D1 | PASS: real Compose PostgreSQL, named volume/healthcheck, DATABASE_URL-selected isolated port, no JSON writes; source and README establish local default. |
| D2 | FAIL: stopped-database cases pass for every command, help variants and no arguments, but session-establishment stall exceeds deadline. Frozen verifier covers refused connections only and therefore misses DB-01. |
| D3 | PASS: fresh schema, integer identity/primary key, enum labels, text and timestamp types inspected through PostgreSQL; monotonic IDs and added/update behavior executed. Supplemental SQL verifies generated-always identity and primary key. |
| D4 | PASS: New → Completed/Deleted, hidden deleted rows, missing/deleted mutation failure, repeat completion executed. Supplemental SQL verifies repeat completion preserves timestamps and deletion preserves added while advancing update. |
| D5 | PASS for prescribed E2E scenario: separate CLI processes, SQL/schema inspection, restart persistence, bad inputs and stopped database; overall acceptance still fails D2. |
| B1–B4, C1–C5 retained behavior | PASS within PostgreSQL scope: ordered active listing including Completed, trimming/blank rejection, increasing IDs, mutation failures, help forms and malformed commands all execute in frozen operations. Supplemental checks verify escaped tabs/newlines/backslashes/carriage returns and add/complete/delete confirmations. Superseded JSON business/CLI harnesses intentionally not rerun. |

All scoped production code was inspected, including status conversion, parameterized SQL, atomic mutations, initialization transaction/advisory lock, CLI argument branches and escape formatting. No additional defect found. The supplemental timeout fixture supplies a nonresponsive transport endpoint, not a substitute database implementation; it directly observes the disclosed live-connection failure bound. Frozen checks remain untouched.

## Scope and unintended behavior

No candidate or protected input modifications were made. Shared Git index was not modified. Identity is pinned to file content rather than current HEAD, because other repository work may advance HEAD. Isolation is procedural; digest checks are not an enforced write sandbox. JSON retention/migration was not required. An unrelated missing test-audit documentation link did not prevent execution or substantive coverage review.

## Outcome

**FAIL**, initial candidate attempt 0. Mandatory frozen execution passes, but independently reproduced DB-01 violates D2 and blocks acceptance. Preserve this attempt and repair within the remaining contract allowance; fresh review is required for any changed candidate.
