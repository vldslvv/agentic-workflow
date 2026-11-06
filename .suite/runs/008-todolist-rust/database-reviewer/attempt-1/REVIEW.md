# Independent conformance review — Rust TODO database, repair attempt 1

**Spec bundle and requirement IDs:** `specs/todolist_rust`, selected D1–D5 with retained operational B1–B4/C1–C5. JSON persistence is explicitly superseded. Source, acceptance, approval and frozen check identities match `../../frozen-inventory.json`. Database authority: `.agents/tasks/010-rust-03_database/approval.json`, baseline `07fd1484a33826b53c9e669b7490175bce1bd11a`. Accepted CLI dependency: `6739545cf7ccabd8e5facd48e01d51c75b987f8ea92b5cb1fd98392def9788a9`, verified against its acceptance receipt and database implementer input-identity evidence.

**Candidate:** `apps/todolist_rust`, content SHA256 `1b2d9e006a54dfc3994fff4f7824844e1e88ae92f45f75c1ce62162e0dad21ee`.

**Reviewer/session:** `/root/rust_database/database_review_1`, fresh-context reviewer with a narrow allowlist. No plan text or planner/implementer conversation inspected. Frozen integrity verification hashes plan bytes without reading their text.

**Review kind:** INDEPENDENT_REVIEW.

**Inputs actually inspected:** root/suite AGENTS; shared contract, Markdown bundle and Implement procedure/skill; REVIEWER, VERIFIER and REVIEW template; all six selected bundle documents; database acceptance and approval; business execution inputs and acceptance; CLI acceptance; frozen inventory and full verifier; business/CLI acceptance receipts; all seven candidate files; implementer attempt-1 database results and handshake result, implementer input-identity; prior review, prior failed handshake evidence and prior supplemental scenario script. Test-audit skill used to assess supplemental behavioral proof. No history discovery or excluded conversation access occurred.

**Integrity and execution:** `before/results.json` and `after/results.json` independently establish identical candidate content and all 29 protected inputs matching the inventory. The frozen command `python3 .suite/runs/008-todolist-rust/checks/verify.py database --evidence .suite/runs/008-todolist-rust/database-reviewer/attempt-1/database` exited 0; its 52 subprocess commands, exits and raw output are retained in `database/commands.json`, with assertions summarized in `database/results.json`. It built with `cargo build --locked`, provisioned real Docker PostgreSQL, ran separate CLI processes, inspected SQL, restarted/stopped the database, and successfully removed only the isolated Compose resources.

Independent supplement commands `python3 .suite/runs/008-todolist-rust/database-reviewer/attempt-1/connection-stall.py` and `python3 .suite/runs/008-todolist-rust/database-reviewer/attempt-1/observe.py` both exited 0. `connection-stall.json` records TCP acceptance, 62 received startup bytes, no server response, CLI exit 1 in 5.001240364 seconds, empty stdout, and stderr `Error: database connection or initialization timed out`. `supplemental.json` records independently rerun real-database formatting, identity and timestamp observations. Docker and localhost listener execution used approved sandbox escalation. Environment versions are in `environment.json`. No manual acceptance gate applies.

## Findings

| Finding ID | Requirement IDs | Observation and evidence | Severity | Required resolution |
|---|---|---|---|---|
| DB-01, resolved | D2 | The previously failed PostgreSQL handshake scenario now exits nonzero with explanatory stderr in 5.001 seconds, below the required 10-second deadline. See `connection-stall.json`; prior failure remains preserved under `../attempt-0/connection-stall.json`. | resolved | None. |

No new blocking findings.

## Coverage and evidence gaps

| Requirements | Disposition and evidence |
|---|---|
| D1 | PASS. Real PostgreSQL Compose provisioning, volume, healthcheck, DATABASE_URL override and absence of JSON writes executed. Local default and connection selection inspected in source/README. |
| D2 | PASS. Frozen stopped-database checks cover add/list/complete/delete/help/--help/no arguments. Independent stalled-handshake observation establishes the repaired deadline. Source inspection confirms the same startup check precedes every argument branch, including invalid commands. |
| D3 | PASS. SQL execution verifies integer ID, text description, timestamp fields, exact enum labels, fresh schema, monotonic unique IDs and immutable added with advancing update. Supplemental SQL verifies GENERATED ALWAYS identity and primary key. |
| D4 | PASS. Add/New, complete/Completed, soft delete/Deleted, active listing, rejected missing/deleted IDs and repeat completion executed. Supplemental SQL verifies idempotent completion preserves timestamps and deletion preserves added while advancing update. |
| D5 | PASS. Full prescribed real-database E2E scenario passes, including separate CLI processes, persistence across restart, malformed inputs and unavailable database. |
| B1–B4/C1–C5 retained operations | PASS. Frozen operations cover trimming, blank rejection, ordered listing, completion, deletion, mutation failure, help forms and malformed commands; supplemental execution covers escaped control characters and mutation confirmations. |

Production source inspection covered the startup worker and bounded channel wait, process termination on timeout, parameterized SQL, schema initialization transaction/advisory lock, atomic mutation rules, status conversion, command parsing and display escaping. The frozen verifier alone misses accepted-TCP/session stalls; the independently executed supplemental observation closes that gap without changing its expectations. The original failed observation supplies pre-repair regression evidence. No mandatory scoped check remains unexecuted. Superseded JSON harnesses were not rerun; retained operations were re-executed through PostgreSQL.

## Scope and unintended behavior

The startup deadline covers connection and schema initialization. Command operations begin only after startup succeeds; the required startup bound does not claim a deadline for all later database queries. No extra contract obligation was inferred. Only reviewer attempt-1 outputs were written; candidate, protected sources/checks, earlier evidence and Git index were untouched. Isolation is procedural, not an enforced write sandbox. Candidate identity is content-pinned because unrelated work may advance HEAD. Existing acceptance receipts establish the prerequisite revision; this review does not replace the supervisor's final project acceptance step.

## Outcome

**PASS** for independent review and mandatory execution of database repair attempt 1, on the exact candidate identity above. D1–D5 and retained B1–B4/C1–C5 pass. Initial attempt 0 remains separately recorded as FAIL; DB-01 is resolved with independently observed evidence.
