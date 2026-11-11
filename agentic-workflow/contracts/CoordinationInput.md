# CoordinationInput

Supply the scope and records needed to coordinate execution or recovery.

## Fields

| Field | Presence | Meaning |
|---|---|---|
| assignment | Required | Authorized objective, mode, target and record locations, ownership constraints. |
| specifications | Required | Paths to Project specification, selected Task specifications, Task order, applicable application Contracts and Verification. |
| scope | Required | Selected tasks and application workspace; identify existing implementation for reconciliation or recovery. |
| records | When available | Execution state, Results and Evidence paths for the selected execution. |
| memory_index | Ordinary work only | Permitted memory index path; a missing index means no saved notes. |
