# Plan — 03_database

Baseline: 07fd1484a33826b53c9e669b7490175bce1bd11a. Acceptance: sibling acceptance.md.

Replace JSON with synchronous postgres crate-backed storage, preserving CLI operations. Bound connection timeout and connect before all commands. Initialize schema transactionally and safely on repeat invocations, with native enum, identity id, timestamps and parameterized SQL. Add compose.yaml and README. Use postgres:17, service db, named volume, healthcheck, localhost binding and POSTGRES_PORT override for isolated verification. Default postgres://todolist:todolist@127.0.0.1:5432/todolist, DATABASE_URL override. No migration is needed for this new app; test-stage files are temporary.

Own only apps/todolist_rust and .suite/runs/008-todolist-rust/database-implementer/. Planner owns handoffs/checks/inventory. Reviewer owns .suite/runs/008-todolist-rust/database-reviewer/. Dependency: 02_cli, via supervisor acceptance evidence. Initial candidate plus two repairs. Infrastructure/verifier defects escalate immediately. Procedural isolation; compare protected and candidate hashes.

Run frozen database checks, cargo fmt/build, retain results. Spawn reviewer with fork_turns=none using spec-source-suite/prompts/REVIEWER.md; supply acceptance, sources, approval, checks, inputs, dependency evidence, candidate identity and raw results; exclude plan and conversations. Final database checks cover assembled app. Approval: sibling approval.json.
