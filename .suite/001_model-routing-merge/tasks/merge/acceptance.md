# Merge acceptance

Authority: user request “Merge this work into main worktree. Make sure to review the merge to avoid breaking anything.” This authorizes commits and merge, superseding earlier no-merge restrictions. Original requirements: [routing acceptance](../../../tasks/001-model-routing/acceptance.md) and [concise fallback correction](../../../tasks/001-model-routing/acceptance-fallback.md). Engineering constraints: [guidelines](../../../../guidelines.md).

Starting main: `535edd6096d9d344f5d5d57fb4b00cd52c4b8c49`; source routing commit `60b1432`. Main checkout `/home/vv/ccode/generate-prototype`; integration worktree `/tmp/generate-prototype-model-routing`; implementation root `.suite/001_model-routing-merge`.

| ID | Required result | Verification |
|---|---|---|
| M1 | Main contains both committed tracing work and routing/fallback changes, with original work preserved. | Inspect ancestry and final tree; both starting commits are ancestors, main/worktree trees match, no unrelated changes. |
| M2 | Retain main's records/native telemetry rules, tracing helpers, fixtures, tests, role routines and Makefile. Add routing profile/index guidance and MODELS inventory entry. | Compare main-relative diff; tracing executable sources/tests are byte-identical; shared guidance includes both sets of rules. |
| M3 | Keep concise fallback in MODELS.md and do not reintroduce the rejected shared fallback expansion. | MODELS equals the reviewed source version; original profile/role routing and root read condition remain. |
| M4 | Resolve package metadata/checksums coherently, preserving historical evidence and disclosed gaps. | Checker passes against pinned main; current metadata points at executed checks, prior metadata archived, checksum verification passes. Do not claim missing historical tracing evidence was rerun. |
| M5 | Full current regression suite passes, including real Perfetto parser when available; merge independently reviewed for standards and spec. | `PERFETTO_TRACE_PROCESSOR=/tmp/suite-trace-processor-shell python -m unittest discover -s spec-source-suite/tests -v`; fresh independent reviews have no actionable findings. |
| M6 | Deliver into main worktree with clean Git state; retain source worktree; no push or deletion. | Confirm branch, ancestry, tree identity and status after merge. |

Document walkthroughs do not establish live model/provider switching. Existing tracing live-provider validation gaps remain disclosed. Test and package commands run in the integration worktree before delivery; final main tree must match the reviewed candidate. No new app execution is required.
