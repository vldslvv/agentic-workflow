# ValidationInput

Supply selected application scope for independent validation or repair publication recovery.

## References:

- [CHECKS]: Restricts independent inputs and defines checking rules. agentic-workflow/policies/CHECKS.md

## Fields

| Field | Presence | Meaning |
|---|---|---|
| assignment | Required | Validation objective, selected application scope and result location. |
| specifications | Required | Project, selected Task specifications, Task order, applicable application Contracts and Verification paths. |
| candidate | Required | Implementation location and revision when available. |
| records | Required | Permitted factual Results and Evidence paths for the selected scope. |
| acceptance | For plan-review tasks | Acceptance paths. |
| writers_paused | Required | Supervisor confirmation that all affected writers are paused. |
| publication | When resuming repair publication | Saved failed validation Result with reserved repair path, dependencies and unfinished publication. |

Filter all fields under [CHECKS] (“Independent checks”).
