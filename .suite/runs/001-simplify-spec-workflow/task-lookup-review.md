# Task-document lookup follow-up review

Result: PASS. Reviewed only the new `Locate existing task documents first` section in root `AGENTS.md` against the user-requested lookup behavior, the repository task layout, and the shared contract's reviewer exclusion rules. This is a separate follow-up review, not a review or re-identification of candidate 0.

No blocking findings.

Reviewed root `AGENTS.md` SHA-256: `bc790175b2b4b713b6c3d7b4bf6e1c77cecffbe8f5b66ceba76431cac0f79fe7`.

- The ordered lookup starts with explicit paths or manifest `task_records` references, then the repository-relative `.agents/tasks/<task-id>/plan.md`, `acceptance.md`, and approval record.
- Missing IDs or files trigger an explicit hidden-directory search. The actual task layout contains all three expected artifacts under `.agents/tasks/simplify-spec-workflow/`.
- Deferred saving or still-missing documents triggers recovery of complete approved originals and approval references from available prior-task history; summaries cannot substitute for originals.
- Asking the user is deferred until available sources are exhausted or conflicting records leave authority unresolved, and must identify checked locations and remaining missing inputs.
- The explicit independent-reviewer exception preserves the shared contract's restricted input boundary: acceptance and approval records are allowed; plans and prior conversation remain excluded. No plan or conversation/transcript content was read during this review.

Checks executed independently:

- `git diff --check` — PASS, exit 0, no output.
- `python .suite/runs/simplify-spec-workflow/validate.py` — PASS, exit 0. All nine reported check groups passed, including 91 local links, 10 YAML/frontmatter documents, 3 skill metadata records, approved-artifact/index integrity, and 29 package inventory entries; 28 source documents checked.

Review scope is the new lookup guidance only. Other changes already present in the working-tree diff were not reassessed.
