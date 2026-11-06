# Plan — 01_business_logic

Baseline: 07fd1484a33826b53c9e669b7490175bce1bd11a. Acceptance: sibling acceptance.md.

Create a small Rust crate named todolist with production library Store::open(path), add(&str) -> Result<Task>, list() -> Result<Vec<Task>>, complete(i32) -> Result<()>, delete(i32) -> Result<()>. Task exposes id, description, status; Status has New/Completed/Deleted and Debug. JSON persists an increasing next-id counter and tasks, propagates I/O/parse errors, and writes safely. Keep operations usable by the forthcoming CLI.

Own only apps/todolist_rust and .suite/runs/008-todolist-rust/business-implementer/. Planner owns handoffs/checks/inventory. Reviewer owns .suite/runs/008-todolist-rust/business-reviewer/. Dependency: none, via supervisor acceptance evidence. Initial candidate plus two repairs. Infrastructure/verifier defects escalate immediately. Procedural isolation; compare protected and candidate hashes.

Run frozen business checks, cargo fmt/build, retain results. Spawn reviewer with fork_turns=none using spec-source-suite/prompts/REVIEWER.md; supply acceptance, sources, approval, checks, inputs, dependency evidence, candidate identity and raw results; exclude plan and conversations. Final database checks cover assembled app. Approval: sibling approval.json.
