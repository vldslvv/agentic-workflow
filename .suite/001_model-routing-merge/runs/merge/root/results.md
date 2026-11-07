# Model-routing merge results

Scope: [merge acceptance](../../../tasks/merge/acceptance.md). Implementation root `.suite/001_model-routing-merge`; candidate in `/tmp/generate-prototype-model-routing`, integrating main `535edd6096d9d344f5d5d57fb4b00cd52c4b8c49` and routing `60b1432`. Main was clean before integration. Implementation checks PASS; independent standards/spec review and delivery pending.

M1–M3: main-relative diff contains only root/shared routing and index additions, MODELS.md, checker inventory and package maintenance, plus required records. Every existing main file outside those five integration paths matches main byte-for-byte ([preservation](preservation.json)); MODELS.md exactly matches the reviewed source, including the concise 42-word fallback paragraph. Main's native telemetry/records rules and all role routines, tests, fixtures, tracing code and Makefile remain. Historical source records retain their original layout; new merge records use the current implementation-root convention. The rejected shared fallback expansion was not restored.

M4: only PACKAGE_CHECKS.json and SHA256SUMS conflicted. Metadata resolution starts from main's newer tracing metadata, adds current routing/integration checks and preserves disclosed live-validation gaps. Prior metadata from both parents is archived in [main metadata](package-checks-main.json) and [routing metadata](package-checks-routing.json). Historical tracing evidence was already absent in main's checkout; inherited claims are labelled and not presented as current execution. Checksums were regenerated from the integrated files.

M5 checks executed in the integration worktree:

- `PERFETTO_TRACE_PROCESSOR=/tmp/suite-trace-processor-shell python -m unittest discover -s spec-source-suite/tests -v`: exit 0, all 28 tests PASS, no skips, including the real Perfetto parser and Make/HTTP lifecycle ([log](tests.log)).
- `python spec-source-suite/helpers/check_package.py --base 535edd6096d9d344f5d5d57fb4b00cd52c4b8c49`: exit 0, PASS, 46 local links ([report](package-check.json)).
- `sha256sum -c SHA256SUMS` from `spec-source-suite/`: [checksum log](checksums.log).
- Main-file byte comparisons and reviewed MODELS equality: PASS. `git diff --check` and fresh standards/spec reviews complete the candidate checks.

Instruction growth against current main: 28 → 29 files, 11 directories unchanged, 6320 → 6844 Markdown words (+524). Shared-plus-role counts: Supervisor 2897, Planner 2757, Implementer 2570, Reviewer 2519, Validator 2681 (+312 each). MODELS.md adds 212 words beyond those metrics, so effective per-role growth is +524. The growth is the already reviewed routing/indexing guidance and concise clarification; integration adds no further operative prose. Configuration, selection procedure and existing tracing code retain their separate responsibilities; no engineering exception.

M6 delivery remains pending until independent review passes. Reviews: [standards](../standards/review.md), [spec](../spec/review.md). No push or worktree removal is authorized.

Routing: careful for integration preservation across changed guidance; requested `gpt-6.1-sol` / `high`. Top-level settings cannot be changed through exposed controls, so existing settings are retained; actual model/reasoning and native session/turn IDs are unavailable. Team identity `/root`. No invented native source bindings or token totals. Documentation walkthroughs do not demonstrate model/provider switching; current tests do not recreate missing historical live OpenCode or browser evidence.
