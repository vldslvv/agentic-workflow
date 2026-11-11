# WorkResult

Return a concise account of work with a reference to its saved record.

## Fields

| Field | Presence | Meaning |
|---|---|---|
| summary | Required | Brief description of work completed. |
| status | Required | PASS, FAIL, BLOCKED or NOT_RUN for the reported work. |
| result | Required | Saved Result path containing detailed findings, produced artifact paths, evidence and limits. |
| decision | When applicable | Acceptance/correction decision, blocker or readiness for independent review. |
| self_review | When performed | Brief self-review report and reference to details in the Result. |

Self-review is optional and separate from independent review; it does not satisfy an independent review gate.
