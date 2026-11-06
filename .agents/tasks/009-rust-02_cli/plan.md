# Plan — 02_cli

Baseline: 07fd1484a33826b53c9e669b7490175bce1bd11a. Acceptance: sibling acceptance.md.

Add a thin synchronous parser and binary named todolist using the accepted library. Use CARGO_MANIFEST_DIR for default app-root data. Document cargo build/run and commands. Preserve dependency behavior; run business and CLI checks.

Own only apps/todolist_rust and .suite/runs/008-todolist-rust/cli-implementer/. Planner owns handoffs/checks/inventory. Reviewer owns .suite/runs/008-todolist-rust/cli-reviewer/. Dependency: 01_business_logic, via supervisor acceptance evidence. Initial candidate plus two repairs. Infrastructure/verifier defects escalate immediately. Procedural isolation; compare protected and candidate hashes.

Run frozen cli checks, cargo fmt/build, retain results. Spawn reviewer with fork_turns=none using spec-source-suite/prompts/REVIEWER.md; supply acceptance, sources, approval, checks, inputs, dependency evidence, candidate identity and raw results; exclude plan and conversations. Final database checks cover assembled app. Approval: sibling approval.json.
