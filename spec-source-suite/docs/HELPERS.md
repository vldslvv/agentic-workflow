# Usage helper

The retained standard-library CLI reads explicitly selected session/turn logs. It does not discover history, launch agents or decide acceptance.

## Usage reporting

1. Capture session IDs, turn IDs, role, parent session and available log paths as supervisor, implementers and reviewers run. Include repairs and blocked work. Keep these source references beside the results; they select measurements only and require no hashes or approval.
2. When logs are available, run:

   `python spec-source-suite/helpers/usage_report.py sessions.json --root WORKSPACE --output usage.json`

   The existing version 1 input format is:

   ```json
   {
     "version": 1,
     "root": {"session_id": "supervisor-id", "path": "supervisor.jsonl", "turn_ids": ["turn-id"], "role": "supervisor"},
     "descendants": [
       {"session_id": "implementer-id", "path": "implementer.jsonl", "turn_ids": ["turn-id"], "role": "implementer", "parent_session_id": "supervisor-id"},
       {"session_id": "reviewer-id", "path": "reviewer.jsonl", "turn_ids": ["turn-id"], "role": "reviewer", "parent_session_id": "implementer-id"}
     ]
   }
   ```

   Paths resolve from `--root`; absolute read-only source paths and a single `turn_id` remain supported. Keep outputs separate from source logs.
3. Link the source references and report from the result record. Report execution totals and per-role/per-session tokens and tool calls, cached/uncached input, output/reasoning where available, known subtotals, missing counters and counting limits. When a source or counter is unavailable, say so; label any partial report's scope. Never invent IDs, zero usage or complete totals. Missing telemetry does not block app acceptance.

The helper supports Codex JSONL and normalized events documented in its docstring. It deduplicates responses by session/response ID and calls by session/call ID. Cached input is part of input; reasoning is part of output; total tokens are input plus output. Legacy token snapshots cannot establish deduplicated totals. Nested operations need explicit parent call IDs; execution batches and observed nested calls are reported separately. Elapsed time is the selected event span, not CPU or billed time. Outer benchmark-driver overhead belongs in a separate report from the execution supervisor.

Optional `verification_subprocesses` entries use `session_id`, `turn_id`, `call_id`, `count` and `evidence_path` referencing an included call and existing evidence. Do not infer subprocess counts from tool names. The helper reads source logs without changing them; its CLI and output schema are retained for compatibility.

Run retained tests with `python -m unittest discover -s spec-source-suite/tests -v`.
