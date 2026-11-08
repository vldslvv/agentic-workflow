# Native trace reference

Read for tracing operation or troubleshooting.

## Capture and collection

- Context: apply [Records](../policies/RECORDS.md) for assignments and disclosure.
- Inputs: implementation name or identified implementation/task, native host storage or selected saved exports.
- Effects:
  1. Allocate with `python3 agentic-workflow/helpers/records.py allocate NAME`; resume with `python3 agentic-workflow/helpers/records.py resolve IMPLEMENTATION TASK`. Allocation resolves `CODEX_THREAD_ID` through the SQLite index under `CODEX_HOME` (default `~/.codex`) and saves metadata plus the active turn under `native/<session-id>/<turn-id>.jsonl`. Missing telemetry is diagnosed on stderr without blocking allocation.
  2. To import existing work, place selected native files under `IMPLEMENTATION/native/`. Each Codex file selects its native turns; restrict scope by supplying metadata and only the intended turn's original records. No migration or legacy inventory reader is provided; historical implementations remain untouched.
  3. For OpenCode, supply saved `opencode export SESSION_ID` JSON under `native/`. Native user-message IDs select turns; structured text-part tags assign tasks/roles. Supply only intended work. No live OpenCode integration is provided.
  4. Run `python3 agentic-workflow/helpers/trace_view.py IMPLEMENTATION` for collection, reports and dashboard, or `python3 agentic-workflow/helpers/usage_report.py IMPLEMENTATION` for reports alone.
- Outputs: selected native files and `reports/usage.json`, `usage.md`, `events.json` and `timeline.json`; coverage diagnostics for missing or ambiguous evidence.

## Collection guidelines

Apply to capture, refresh and offline analysis.

- Keep native capture running throughout the work.
- Use adapters to calculate usage.
- Do not create trace inventories or count tokens manually.
- When assignment tags are missing, leave task and role unavailable but keep measured usage.
- Refresh saved selected turns, follow selected spawn/follow-up/message dispatches and save proven descendants. Native parent metadata corroborates returned agent paths; known IDs resolve through the index. Workspace/recency never establish inclusion. Fork history and unrelated turns remain excluded.
- Resolve follow-ups using returned turn/message IDs or delivered-message matches. A unique new turn within the dispatch interval can resolve an already proven identity; multiple candidates produce coverage diagnostics. Sources supply versions, session identities, selected turns and stable agent runs; dispatches supply requested settings, native turn context supplies observed settings.
- Keep native bytes, including partial active tails; host storage stays read-only. Copies/reports are replaced atomically per file, not as one transaction. Repeated collection deduplicates measurements. Offline analysis uses saved files and reports unavailable host storage; ambiguity, missing versions/measurements, unfinished turns and malformed tails remain diagnosed.
- Use Python's standard library on local POSIX filesystems. `flock` on the records directory serializes allocation; `.records.lock` per implementation serializes capture/collection/report refresh. Interrupted allocations stay reserved; distributed locking is outside the contract.
- Use the helper boundaries: `records.py` allocates/resolves; `native_traces.py` collects/resolves assignments; `trace_adapters.py` parses measurements/content; `usage_report.py` accounts for them. Discovery is separate from accounting. No source/bind commands, normalized trace copies, registration, launch wrappers, hooks or recorders are required.

## Assignment recovery

- Context: apply [Records](../policies/RECORDS.md) assignment rules. Some hosts encrypt dispatch arguments and delivered messages; recipients' local commentary tags remain readable.
- Inputs: selected native turns and verified task/role records for opaque handoffs.
- Effects: use plaintext delivered tags only for their native recipient; match native `SubAgentActivity` agent paths by session ID. Prose never establishes an assignment. For opaque handoffs, create `IMPLEMENTATION/assignment-annotations.json` using the format below.
- Outputs: explicit assignment annotations with evidence paths, preserved with native exports for offline analysis.

```json
{"version":1,"assignments":[{"adapter":"codex","session_id":"SESSION","turn_id":"TURN","task":"01_business_logic","role":"implementer","purpose":"Implement business logic","evidence":["runs/01_business_logic/build/result.md"]}]}
```

## Annotation guidelines

Apply when creating or consuming assignment annotations.

- Fill only missing assignments on exact selected turns. Keep session/turn selection, tags and observed settings/counters unchanged; do not inherit annotations to other turns. Fail refresh on duplicate, conflicting or unselected entries.
- Require evidence paths to identify existing files inside the implementation. Treat annotations as explicit assertions, not conclusions verified from file contents. Label their source `annotation` in reports/dashboard and retain evidence paths in JSON. Serve neither annotations nor native exports through the viewer.

## Adapter contract and accounting

Apply when parsing native evidence and deriving reports.

- Return normalized events and coverage diagnostics from `read_source(source, path)`. Add parsers to `ADAPTERS` without changing accounting. Measurement events identify agent/model/tool kind; separate message/instruction/tool-result observations retain content without affecting usage, call counts, durations or accounting coverage.
- Carry native session/turn/event IDs, provenance, available parent/call relations, settings, outcome, timing and canonical usage in events. Add implementation/task/role IDs during analysis, along with, native session run IDs, derived assignment IDs and stable event IDs. Missing fields are null with omissions disclosed.
- Group reports by task, run, role, model, reasoning effort, model+effort, task+model/effort, tool and task/tool. Model tables contain model measurements; tool tables contain tool observations. Model-only groups retain usage when effort is unavailable. Native spawn/fork/continuation edges survive without selecting the parent; reused sessions retain identity and selected turns.

| Pinned profile | Measurement scope | Meaning and limits |
|---|---|---|
| `codex-rollout-0.167.0` | CLI 0.167.0 `token_usage_record` by thread/response; function/custom calls by thread/call | Input includes cached input; output includes reasoning. Ignore legacy snapshots and turn/thread aggregates. Turn context gives observed settings. Structured command-end establishes failure; plain returns establish return, not success. Model duration needs a start. Native metadata retains spawn/fork parentage. |
| `opencode-export-1.2.27` | `step-finish` part ID, otherwise latest-step message snapshot | Canonical input adds cache reads/writes to native input; output includes reasoning. Prefer step usage: message tokens repeat only the latest step. A successful message without steps is partial latest-step evidence; failed/unfinished messages without steps are unmeasured, even with zero counters. Retain `variant` without translating it to reasoning effort. No step timings or fork/continuation relations; tool state gives duration/status and session `parentID` gives spawn parentage. |

- Calculate uncached input as input minus cache reads; keep cache writes included. Total = input plus output; never add reasoning again. Missing operands stay missing. Deduplicate at native measurement scope; conflicting duplicates fail.
- Identify content by native message/part IDs where available; use fingerprint plus occurrence within the selected turn for ID-less Codex records. Merge provenance for saved copies; identical ID-less occurrences within one source remain distinct. Keep response items and event notifications separate without shared native identity, even if text matches.
- Link tool results by session, turn and call ID, retaining multiple results, errors and orphans. Unfinished calls lack outputs. Wrapper calls and explicitly parented nested calls count separately; absent parent metadata cannot prove a wrapper had no nested operations.
- Exclude unknown measurements from subtotals; an all-unknown subtotal is null. Incomplete evidence prevents complete totals, including affected groups. Source-wide gaps propagate to their assignments; unresolved gap scope conservatively prevents completeness. Unattributed events stay in overall accounting and are omitted only from affected groupings. Operation time may overlap; it is not wall-clock, CPU or billed time.
- Derive versions from native metadata; missing/mismatched versions are unverified. Diagnose missing files, selected turns, counters, truncated JSONL, unfinished turns and unknown attribution. Structurally invalid exports fail import. After interrupted report replacement, rerun from saved native inputs.

## Viewer

- Context: use collected native evidence and the accounting contracts above.
- Inputs: explicit implementation path, refresh interval and available browser.
- Effects:
  1. Run `python3 agentic-workflow/helpers/trace_view.py IMPLEMENTATION --interval 5` with an explicit implementation path. Collection runs immediately, then waits after each completed attempt; passes never overlap. Repeated commands/tabs reuse the viewer. Restart its owner to change the interval.
  2. Use **Group by** to compare tasks, agents, models, effort or tools and **Find in this table** to filter rows. Assignments show native names, purpose, observed model/effort and lineage. Missing effort stays unavailable; requested settings remain separate in usage JSON. Tool tables show calls, outcomes and measured durations; coverage/attribution gaps stay visible.
  3. Inspect **Recorded content**, which lists timed observations chronologically, then untimed ones. Filter by agent, task, event type or tool and search full content; select an event for complete content, relationships, status and provenance.
  4. Keep the foreground terminal running; `Ctrl+C` stops collection/HTTP. Use loopback port 9001 for Perfetto integration; report unrelated occupants without disturbing them. Browser/tab reuse depends on the browser; failed launch prints the URL. Stop older viewers once before using the upgraded command.
  5. Select **Open timeline in Perfetto** to open the published snapshot matching successful `reports/timeline.json`; empty timelines explain missing evidence. Reopen for newer timing: an open Perfetto timeline does not live-update. Lanes show agent/assignment/observed settings; slices show purpose and turn settings. Dashboard agents retain observed setting changes without inferring requests.
- Outputs: local dashboard and published report snapshot; optional Perfetto timeline and visible coverage/refresh diagnostics.

## Viewer guidelines

Apply to live collection, presentation and serving.

- Build one report bundle per refresh, write four exports, render the dashboard and publish a completed in-memory snapshot. HTTP serves that snapshot without reading reports or rendering again. Editing individually atomic export files does not change the page. Failed refreshes retain successful JSON/timestamp, display an error and retry; initial failures remain command errors.
- Poll from the browser at the configured interval, preserving grouping, search, expansion, scroll and recorded-content filters/selection. Collection and polling default to five seconds: normal latency is 5–10 seconds plus processing. Connection failures retain data and retry. Collection continues while idle until `Ctrl+C`, rebuilding full reports with unchanged accounting.
- Apply [collection guidelines](#collection-guidelines) to live evidence, including new children. Capture or supply unrelated turns and later root turns explicitly; use supplied exports for OpenCode. Missing measurements stay unavailable; unfinished evidence does not establish current agent activity.
- Render values as inert text with preserved whitespace; never fetch/render external attachments.
- Serve only the dashboard and generated usage/events/timeline JSON through the tokenized boundary. Native logs, annotations, arbitrary files and directory traversal are excluded. Collection/analysis stay local; only optional Perfetto UI needs internet. If prompted, allow local-device access for `ui.perfetto.dev`; the command never changes browser permissions. Viewer health is separate from Perfetto's reserved `/status` probe.

## Evidence and interoperability

Apply when exporting content, interpreting evidence or checking integrations.

- Include complete recorded prompts, messages, handoffs, instructions and tool inputs/outputs in content exports/dashboard by default, with no preview limit or opt-in flag. Include IDs, paths, measurements and assignment descriptions in usage JSON/Markdown. Full content can enlarge exports; refresh rebuilds it from saved evidence. Follow [Records](../policies/RECORDS.md) disclosure boundaries.
- Include matching dashboard IDs, native identity, tool-call relations and available counters in Perfetto event details. Tool arguments contain full inputs and associated outputs; timestamped messages are instants and agent turns retain recorded instruction context. Structured arguments are JSON strings preserving complete arrays/nested payloads.
- Distinguish empty, missing, encrypted and explicitly upstream-truncated content in labels. No decryption, text truncation or exact assembled-model-request reconstruction occurs; unmarked upstream omissions cannot be detected.
- Export Chrome Trace metadata (`M`), complete operations (`X`), thread instants (`i`) and spawn flows (`s`/`f`). Complete durations need both observed endpoints; single timestamps become instants. Untimed events remain in the dashboard/content report with timeline omissions. Never invent timestamps.
- Require native session-creation time and a selected parent lane for spawn flows; creation instants anchor both endpoints without invented durations. Missing relationship timing produces no arrow.
- Treat fixtures as synthetic reductions of pinned schemas, not recordings or live-integration evidence. Set `PERFETTO_TRACE_PROCESSOR` to official `trace_processor_shell` for optional real-parser regressions. Set `PLAYWRIGHT_MODULE` to installed Playwright with Chromium for optional browser regressions. Record real capture/import and parser/visual evidence in run evidence and package metadata; disclose skipped checks.
- Account for OpenCode replacing provider-missing counters with zero upstream; exports cannot recover them. Fork exports copy messages under new IDs and omit fork provenance: select only known new-work turns. A pinned profile does not imply support for every release/provider.
- Follow [OpenTelemetry agent/model/tool examples](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/non-normative/examples-agent-calls.md) without an SDK/collector. Viewer format follows [Perfetto external traces](https://perfetto.dev/docs/getting-started/other-formats).
- Use these pinned contracts: [Codex protocol](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/protocol/src/protocol.rs), [OpenCode messages](https://github.com/anomalyco/opencode/blob/v1.2.27/packages/opencode/src/session/message-v2.ts), [usage normalization](https://github.com/anomalyco/opencode/blob/v1.2.27/packages/opencode/src/session/index.ts), [export](https://github.com/anomalyco/opencode/blob/v1.2.27/packages/opencode/src/cli/cmd/export.ts) and [processor](https://github.com/anomalyco/opencode/blob/v1.2.27/packages/opencode/src/session/processor.ts). MLflow/Phoenix destinations, recorder plugins, automated runners, costs and mandatory services remain outside this implementation.
