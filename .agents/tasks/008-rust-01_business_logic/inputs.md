# Execution inputs — todolist_rust

Mode initial; selected specs/todolist_rust, all three ordered tasks. Baseline 07fd1484a33826b53c9e669b7490175bce1bd11a; current working-tree source bytes authoritative, including uncommitted inputs. Authority: “Implement specs/todolist_rust”. No historical records inspected.

Records: .agents/tasks/008-rust-01_business_logic, .agents/tasks/009-rust-02_cli, .agents/tasks/010-rust-03_database. DAG 01_business_logic → 02_cli → 03_database. Each record has plan.md, acceptance.md, approval.json.

Target Rust CLI; candidate apps/todolist_rust, initially absent. Final storage Docker PostgreSQL. Interim data root means apps/todolist_rust. No retained assets/data. Other repository work protected. Simple defaults recorded in acceptance.

Evidence root .suite/runs/008-todolist-rust; frozen inventory .suite/runs/008-todolist-rust/frozen-inventory.json; checks .suite/runs/008-todolist-rust/checks/verify.py. Sources: all six Markdown files under specs/todolist_rust. All source, handoff, check and procedural identities pinned in frozen inventory.

Planner/supervisor /root; fresh implementer per task; implementer spawns fresh reviewer. Procedural isolation only, no enforced sandbox. Reviewer allowlist excludes plans/conversations; reviewer owns phase-reviewer evidence. Candidate hashes exclude target/ and tasks.json, include Cargo.lock.

Verification: business consumer → CLI plus business regressions → real Docker PostgreSQL/CLI, schema, restart persistence, unavailable DB. Final assembled scenario reruns database acceptance after node 03 passes. No manual gate. Initial candidate plus two repairs per phase. Escalate check defects/infrastructure without consuming behavioral repairs.
