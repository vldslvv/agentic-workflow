# Direct path routing

The user's clarification confirms that avoiding path discovery, while retaining required reading, is the goal.

Root AGENTS.md now groups exact paths by read condition: engineering guidelines, shared rules, each of five roles, all four templates, package validation, usage reporting and optional runner work. Existing routing prose was consolidated into that table. The reusable suite retains its own navigation for standalone adoption; the root map provides repository-local entry points without copying procedures. Shared record guidance now requires exact paths with an explicit base for each recipient's permitted inputs; plans and memory remain role-restricted. Unknown selections and missing records still follow existing discovery/recovery rules.

The existing checker now validates root AGENTS.md links when present, as well as suite-local links. No new reusable file or supporting procedure document was added.

## Verification and maintenance review

- Package checker: PASS; 38 local links/anchors and the expected 20-file package layout validated. See [report](package-check.json). The Git baseline comparison includes existing concurrent engineering-guideline and maintenance changes.
- Existing checker CLI scenarios: all nine pass; see [CLI results](cli-checks.json).
- A real temporary Git repository accepted the complete root map and rejected a deliberately broken implementer path with the exact root-link error; see [root check](root-index-check.json). The first verification attempt used an incorrect hardcoded total-link assertion; that harness error was removed without changing production behavior.
- File and directory counts unchanged by this follow-up. [Word counts](instruction-counts.json) compare the exact working-tree files captured before this edit. Growth adds direct entry paths and an explicit handoff contract; it saves path discovery without omitting required reads.
- Shared instructions remain the authority for procedures. Repeated paths at repository and portable-suite entry points are navigation, checked for existence, rather than repeated operative rules. Each role still reads shared guidance plus its own routine and allowed task artifacts.
- `git diff --check` and package checksums pass. The usage helper and its tests were not changed; the checker was validated through its actual CLI.

Earlier evidence and unrelated working-tree changes were preserved. No live app generation or claim of automated semantic review is made.
