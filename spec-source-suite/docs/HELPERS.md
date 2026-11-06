# Small workflow helpers

These Python standard-library CLIs validate explicit jobs and retain evidence. They do not launch agents, schedule work, or grant acceptance. Run them from any workspace with absolute paths or the documented root. Failed validation exits nonzero. Keep manifests and outputs outside the reusable suite. Sample placeholders below describe schemas, not approved application inputs.

## Role context

`python spec-source-suite/helpers/role_context.py job.json --root WORKSPACE --output reading.json`

A version 1 JSON job declares `role` (`supervisor`, `planner`, `implementer`, `reviewer`), `reads` entries with `path`, full-file `sha256`, optional exact Markdown `section` heading and `category`, plus `owned_paths` and `forbidden_paths`. Paths resolve against `--root`. Canonical role procedures, shared contract and routers must be listed as complete files. Named sections are permitted only for supplemental normative references; full-file digests still validate their integrity. The result lists paths/sections, identities and suite-controlled byte sizes, not file contents. Missing references/digest mismatches fail explicitly. Reviewer lists exclude plans and conversations; declare sensitive inputs as forbidden as well. Procedural manifests are not access-control sandboxes. Record extra relevant inspection in the role receipt.

For a supervisor that also plans, use `role: supervisor` and include complete `docs/DEFINE.md` and `docs/PLANNING.md` reads alongside its supervisor inputs (paths relative to `spec-source-suite/`). These additional reads use the existing manifest schema. Use `role: planner` for explicitly delegated planning; a separate manifest does not require a separate agent.

## Check execution

`python spec-source-suite/helpers/check_execution.py checks-v1.json --output NEW_EVIDENCE_DIRECTORY`

Version 1 manifests declare `requirements` (IDs), and `setup`, `checks`, `cleanup` arrays. Each step has `id`, `argv` (literal argument array; no shell), `cwd` (manifest-relative or absolute), `timeout_seconds`, `expected_exit_codes`, `timeout_kind` (`behavioral` or `infrastructure`). Check steps additionally declare `requirements` and `mandatory`. All mandatory requirements need mapped mandatory execution. Use distinct manifests for task checks, regressions and final end-to-end scenarios. Frozen inventory versions pin manifest/check/fixture/adapter digests; the executor does not freeze them for you.

The new evidence directory receives invocation/start records before processes, step stdout/stderr and results, and `summary.json`. Exit 0 = PASS, 1 = FAIL, 2 = BLOCKED. Expected nonzero exits can pass. Declared behavioral deadline timeouts fail; infrastructure timeout/missing executable/interruption block. Cleanup runs even after failure and its errors remain distinct from primary results. Zero executed mandatory checks or incomplete mappings cannot pass. Do not put credentials in arguments or captured command output; environment values are not serialized. SIGINT/SIGTERM retain partial execution and attempt cleanup; uncatchable termination can leave only persisted start evidence. A helper PASS describes execution only, not coverage, independent review or supervisor acceptance.

## Usage reporting

`python spec-source-suite/helpers/usage_report.py sessions.json --root WORKSPACE --output usage.json`

Version 1 manifest: `root` has `session_id`, log `path`, selected `turn_ids`, `role`; `descendants` are explicit entries with those fields plus `parent_session_id`. Keep this complete session tree with the run. Only selected turns/sessions count. Supported JSONL includes actual Codex response usage/call events and documented normalized fixture events (see helper docstring). Responses deduplicate by session/response and tools by session/call ID. Cached input is a subset of input, reasoning a subset of output; total tokens count input plus output once. Unknown counters are unavailable, never fabricated zeros. Report per-role totals, execution batches, observable nested operations and externally evidenced verification subprocess counts separately. Root session overhead is distinct when the root is an outer benchmark driver; for replay metrics choose the replay supervisor as root and list the driver in a separate report.

Optional `verification_subprocesses` entries identify `session_id`, `turn_id`, `call_id`, `count` and `evidence_path`; retain matching execution evidence instead of inferring subprocess counts from tool names. Logs are read without modification. Elapsed time is a wall-clock span, not sum of concurrent agent durations. Compare equivalent scopes and disclose model/settings, environment/cache differences and missing fields. Baseline context sizes are UTF-8 bytes, not tokenizer estimates.
