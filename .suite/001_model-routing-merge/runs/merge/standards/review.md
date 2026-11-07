# Standards review

PASS — no actionable documented violations or heuristic code smells.

Scope: [merge acceptance](../../../tasks/merge/acceptance.md), candidate `272ef356c25e8d0bfb961e7925b45b7a744a35b1`, fixed point `535edd6096d9d344f5d5d57fb4b00cd52c4b8c49`; worktree `/tmp/generate-prototype-model-routing`. Reviewed root `AGENTS.md`, resolved `/tmp/generate-prototype-model-routing/guidelines.md`, suite shared/reviewer guidance and `MODELS.md`. Plans, conversations and memory were excluded. This is the Standards axis; final delivery remains outside this review.

Independent checks, all exit 0:

- Root: `python spec-source-suite/helpers/check_package.py --base 535edd6096d9d344f5d5d57fb4b00cd52c4b8c49`: PASS, 46 links; independently reproduced recorded metrics.
- Suite directory: `sha256sum -c SHA256SUMS`: all 28 entries OK.
- Root: `git diff --check 535edd6096d9d344f5d5d57fb4b00cd52c4b8c49...HEAD`: clean.
- Root: independent Python/Git blob comparisons verified both parents' ancestry, unchanged main files outside the five declared integration paths, exact source-record preservation, exact archived parent metadata, source-identical MODELS and explicit index links for every added Markdown file. Index purposes and exclusions were inspected without following plan links.

Manual maintenance judgment: shared guidance owns routing selection and Markdown lifecycle rules; MODELS owns concrete settings and role tables; root/scoped indexes own discovery. This satisfies shared “one authoritative home” and engineering “one clear responsibility” guidance. Configuration warrants its new file because tables can change independently of procedures. Added instructions change dispatch/index behavior, preserve context exclusions and distinguish requests from observations; no further procedural documents become mandatory. Shared guidance, each unchanged role routine and routing configuration remain sufficient. Concise MODELS fallback restates the shared boundary for configuration readers without introducing a conflicting rule or separate mechanism.

Growth is justified and accurately disclosed: 28→29 package files, 11 directories, 6320→6844 words; shared-plus-role +312 each, plus 212 configuration words. Metadata separates current checks from inherited unavailable historical evidence. No functional-core or test-interface departure; executable tracing/test sources remain identical. The supplied 28-pass regression log includes real Perfetto; redundant full execution was not repeated. Live provider/model switching remains unproven and is not claimed.

Routing: careful/default Standards review; requested `gpt-6.1-sol`/`high`; observed settings unavailable, existing host settings retained. Identity `/root/merge_standards`; native session/turn IDs unavailable.
