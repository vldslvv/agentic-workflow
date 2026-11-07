# Selected implementation usage

Null means unavailable. Known subtotals exclude missing measurements. Scope and omissions are in usage.json.

| Metric | Total | Known subtotal | Measured records | Missing records |
|---|---:|---:|---:|---:|
| input_tokens | 1446241 | 1446241 | 55 | 0 |
| cached_input_tokens | 1317120 | 1317120 | 55 | 0 |
| cache_write_input_tokens | 0 | 0 | 55 | 0 |
| uncached_input_tokens | 129121 | 129121 | 55 | 0 |
| output_tokens | 16025 | 16025 | 55 | 0 |
| reasoning_output_tokens | 1341 | 1341 | 55 | 0 |
| total_tokens | 1462266 | 1462266 | 55 | 0 |

## By task

| Group | Total tokens | Known subtotal | Missing records | Tools |
| --- | --- | --- | --- | --- |
| 01_business_logic | 339752 | 339752 | 0 | 11 |
| 02_cli | 245422 | 245422 | 0 | 8 |
| orchestration | 707887 | 707887 | 0 | 25 |
| validation | 169205 | 169205 | 0 | 5 |

Attribution omissions: 0 events; 0 diagnostics.

## By agent_run

| Group | Total tokens | Known subtotal | Missing records | Tools |
| --- | --- | --- | --- | --- |
| codex:01a1b6af-9ace-7061-a1a6-f738938c484d | 707887 | 707887 | 0 | 25 |
| codex:01a1b6b0-48ef-79b2-886d-4ab5d3cc5647 | 339752 | 339752 | 0 | 11 |
| codex:01a1b6b2-7178-7460-8422-fb76cc2c892b | 245422 | 245422 | 0 | 8 |
| codex:01a1b6b4-69b8-7e42-8fca-ec16791537d2 | 169205 | 169205 | 0 | 5 |

Attribution omissions: 0 events; 0 diagnostics.

## By role

| Group | Total tokens | Known subtotal | Missing records | Tools |
| --- | --- | --- | --- | --- |
| implementer | 585174 | 585174 | 0 | 19 |
| supervisor | 707887 | 707887 | 0 | 25 |
| validator | 169205 | 169205 | 0 | 5 |

Attribution omissions: 0 events; 0 diagnostics.

## By model

| Group | Total tokens | Known subtotal | Missing records |
| --- | --- | --- | --- |
| gpt-6.1-sol | 1462266 | 1462266 | 0 |

Attribution omissions: 0 events; 4 diagnostics.

## By effort

| Group | Total tokens | Known subtotal | Missing records |
| --- | --- | --- | --- |
| high | 877092 | 877092 | 0 |
| medium | 585174 | 585174 | 0 |

Attribution omissions: 0 events; 4 diagnostics.

## By model_effort

| Group | Total tokens | Known subtotal | Missing records |
| --- | --- | --- | --- |
| gpt-6.1-sol, high | 877092 | 877092 | 0 |
| gpt-6.1-sol, medium | 585174 | 585174 | 0 |

Attribution omissions: 0 events; 4 diagnostics.

## By task_model_effort

| Group | Total tokens | Known subtotal | Missing records |
| --- | --- | --- | --- |
| 01_business_logic, gpt-6.1-sol, medium | 339752 | 339752 | 0 |
| 02_cli, gpt-6.1-sol, medium | 245422 | 245422 | 0 |
| orchestration, gpt-6.1-sol, high | 707887 | 707887 | 0 |
| validation, gpt-6.1-sol, high | 169205 | 169205 | 0 |

Attribution omissions: 0 events; 4 diagnostics.

## By tool

| Group | Observed calls | Outcomes | Observed seconds | Untimed |
| --- | --- | --- | --- | --- |
| exec | 32 | {'returned': 32} | 9.875999212265015 | 0 |
| send_message | 4 | {'returned': 4} | 0.12400007247924805 | 0 |
| spawn_agent | 3 | {'returned': 3} | 0.056999921798706055 | 0 |
| wait_agent | 10 | {'returned': 10} | 278.1010003089905 | 0 |

Attribution omissions: 0 events; 4 diagnostics.

## By task_tool

| Group | Observed calls | Outcomes | Observed seconds | Untimed |
| --- | --- | --- | --- | --- |
| 01_business_logic, exec | 10 | {'returned': 10} | 3.240999221801758 | 0 |
| 01_business_logic, send_message | 1 | {'returned': 1} | 0.005000114440917969 | 0 |
| 02_cli, exec | 7 | {'returned': 7} | 2.444999933242798 | 0 |
| 02_cli, send_message | 1 | {'returned': 1} | 0.006000041961669922 | 0 |
| orchestration, exec | 10 | {'returned': 10} | 2.6469998359680176 | 0 |
| orchestration, send_message | 2 | {'returned': 2} | 0.11299991607666016 | 0 |
| orchestration, spawn_agent | 3 | {'returned': 3} | 0.056999921798706055 | 0 |
| orchestration, wait_agent | 10 | {'returned': 10} | 278.1010003089905 | 0 |
| validation, exec | 5 | {'returned': 5} | 1.5430002212524414 | 0 |

Attribution omissions: 0 events; 4 diagnostics.

## Native lineage

- codex:01a1b6af-9ace-7061-a1a6-f738938c484d → codex:01a1b6b0-48ef-79b2-886d-4ab5d3cc5647 (spawn)
- codex:01a1b6af-9ace-7061-a1a6-f738938c484d → codex:01a1b6b2-7178-7460-8422-fb76cc2c892b (spawn)
- codex:01a1b6af-9ace-7061-a1a6-f738938c484d → codex:01a1b6b4-69b8-7e42-8fca-ec16791537d2 (spawn)

## Coverage diagnostics

- aggregate_snapshot_excluded: 4
