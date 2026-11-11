# ReviewInput

Supply requirements and a stable candidate for independent task review.

## References:

- [CHECKS]: Restricts independent inputs and defines checking rules. agentic-workflow/policies/CHECKS.md

## Fields

| Field | Presence | Meaning |
|---|---|---|
| assignment | Required | Review objective, assigned scope and result location. |
| requirements | Required | Project and assigned Task specification paths, with applicable application Contracts and Verification paths. |
| task_order | When relevant | Task dependency table path. |
| candidate | Required | Implementation location and revision when available. |
| acceptance | Required | Acceptance path. |
| evidence | When available | Permitted factual Evidence and Result paths, including prior findings. |
| writers_paused | Required | Supervisor confirmation that all affected writers are paused. |

Filter all fields under [CHECKS] (“Independent checks”).
