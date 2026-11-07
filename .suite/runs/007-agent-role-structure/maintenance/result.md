# Workflow maintenance guardrails

Implemented the user's “Do it” instruction following the proposal to keep few files, minimal instructions and role-based grouping.

The existing shared AGENTS.md now holds the maintenance rules and review questions. The root router points suite changes to them. One new executable helper, `helpers/check_package.py`, validates the expected package layout, local inline Markdown links/anchors and role/skill entry points. It compares package file/directory counts, all Markdown words and shared-plus-role words against a resolved starting Git commit. Positive deltas are review signals; structural errors fail. It requires a valid baseline and prints that commit in its JSON report.

## Maintenance review

- **Behavior added:** Future suite changes must run the structural check, explain growth, and assess duplication and role sufficiency before completion. Root routing makes these rules discoverable for tooling work.
- **Single authoritative home:** The rules and review questions live in shared AGENTS.md. Root guidance supplies a pointer; role files do not repeat them. The checker owns the expected package layout.
- **Role grouping:** No new operative instruction document or supporting procedure chain was added. Shared guidance plus the assigned role remains the operative context; task inputs and authoring templates remain separate inputs.
- **Justified growth:** One helper file is added because executable checks are a separate responsibility from role instructions and the compatibility-preserved usage helper. The maintenance block adds 148 words of operative guidance; directories are unchanged. No numeric word cap or new approval gate is imposed. Duplication, semantic role sufficiency and whether an instruction earns its place remain manual review judgments.
- **Concurrent work:** Engineering-guideline changes appeared in the same working tree during this task. They were preserved. The machine comparison against starting commit `4aa4b7a7ed9d2ac96a750f26497f823b8a61d629` reports the combined working tree, not solely this task's word delta. Existing package-check entries and historical evidence were preserved; the workflow-maintenance entry was added to current metadata.

## Actual verification

- [Structural report](package-check.json): PASS; expected layout, 20 package-local Markdown links, and role/skill entry points validated. Reports before/after counts, added/removed paths and growth signals.
- [CLI scenarios](cli-checks.json): nine PASS results using a real temporary Git repository. Covers a valid package, extra supporting file, missing role, broken link, missing anchor, wrong shared entry point, implicit skill invocation, non-failing word growth, and unavailable baseline. Reproduction: `python .suite/runs/007-agent-role-structure/maintenance/check-cli.py`.
- [Usage tests](usage-tests.log): all seven retained tests passed. The usage helper and its tests remain byte-identical to HEAD.
- [Checksums](checksums.log): all 19 inventory entries passed; SHA256SUMS itself is excluded from its inventory.
- `git diff --check`: PASS.

No live app generation or automatic semantic review is claimed. The checker validates the current package's inline links and ATX heading anchors, not arbitrary Markdown syntax or external URLs. Its layout contract must be deliberately revised for justified structural changes; adding an unexpected instruction file cannot silently pass.
