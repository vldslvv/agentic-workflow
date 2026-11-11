# TaskInput

Supply one task assignment for implementation, continuation or correction.

## Fields

| Field | Presence | Meaning |
|---|---|---|
| assignment | Required | Objective, scope, direct or plan-review mode, record location and file ownership. |
| specifications | Required | Project and assigned Task specification paths, with applicable application Contracts and Verification paths. |
| workspace | Required | Implementation location. |
| memory | Ordinary work only | Permitted index and relevant note paths; omit when absent or excluded. |
| continuation | When continuing | Prior Result and existing Plan and Acceptance paths, with continuation phase and unfinished work. |
| correction | When correcting | Assigned findings and source Result path; explicit Supervisor release to edit after independent checking. |
