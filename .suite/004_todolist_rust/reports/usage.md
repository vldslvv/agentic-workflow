# Selected implementation usage

Null means unavailable. Known subtotals exclude missing measurements. Scope and omissions are in usage.json.

| Metric | Total | Known subtotal | Measured records | Missing records |
|---|---:|---:|---:|---:|
| input_tokens | unavailable | 9931557 | 246 | 0 |
| cached_input_tokens | unavailable | 9474304 | 246 | 0 |
| cache_write_input_tokens | unavailable | 0 | 246 | 0 |
| uncached_input_tokens | unavailable | 457253 | 246 | 0 |
| output_tokens | unavailable | 90727 | 246 | 0 |
| reasoning_output_tokens | unavailable | 14448 | 246 | 0 |
| total_tokens | unavailable | 10022284 | 246 | 0 |

## By task

| Group | Total tokens | Known subtotal | Missing records | Tools |
| --- | --- | --- | --- | --- |
| 01_business_logic | unavailable | 997634 | 0 | 29 |
| 02_cli | unavailable | 990264 | 0 | 27 |
| 03_database | unavailable | 4663759 | 0 | 87 |
| orchestration | unavailable | 2947324 | 0 | 75 |
| validation | unavailable | 423303 | 0 | 10 |

Attribution omissions: 0 events; 1 diagnostics.

## By agent_run

| Group | Total tokens | Known subtotal | Missing records | Tools |
| --- | --- | --- | --- | --- |
| codex:01a1b6ca-228a-7fa2-8853-29a85535715f | unavailable | 2947324 | 0 | 75 |
| codex:01a1b6ca-f8ea-77a0-b9ce-7126434936e5 | unavailable | 684715 | 0 | 19 |
| codex:01a1b6cb-5354-70f1-a89f-76107013f1fc | unavailable | 171343 | 0 | 6 |
| codex:01a1b6cf-0274-7341-aa53-4e117241827b | unavailable | 141576 | 0 | 4 |
| codex:01a1b6d0-ccae-79e0-9a30-e1c6225d19ec | unavailable | 560008 | 0 | 15 |
| codex:01a1b6d1-24b0-76d2-8274-46567cd4793d | unavailable | 195226 | 0 | 6 |
| codex:01a1b6d4-ebe2-7a70-a76e-de129afdbd18 | unavailable | 235030 | 0 | 6 |
| codex:01a1b6d6-ad7f-7aa1-adde-9a279323ce76 | unavailable | 3152606 | 0 | 49 |
| codex:01a1b6d7-58b6-7610-9ff9-12aeab878459 | unavailable | 430769 | 0 | 12 |
| codex:01a1b6e0-0583-7cc1-a8cd-30360c97b55b | unavailable | 350797 | 0 | 9 |
| codex:01a1b6e3-ee8c-7662-8ab2-296efe7854f7 | unavailable | 397537 | 0 | 9 |
| codex:01a1b6e6-50c0-7161-9ae8-265492458674 | unavailable | 332050 | 0 | 8 |
| codex:01a1b6e8-d669-7771-bdd3-50095066308a | unavailable | 423303 | 0 | 10 |

Attribution omissions: 0 events; 1 diagnostics.

## By role

| Group | Total tokens | Known subtotal | Missing records | Tools |
| --- | --- | --- | --- | --- |
| implementer | unavailable | 4397329 | 0 | 83 |
| planner | unavailable | 797338 | 0 | 24 |
| reviewer | unavailable | 1456990 | 0 | 36 |
| supervisor | unavailable | 2947324 | 0 | 75 |
| validator | unavailable | 423303 | 0 | 10 |

Attribution omissions: 0 events; 1 diagnostics.

## By model

| Group | Total tokens | Known subtotal | Missing records |
| --- | --- | --- | --- |
| gpt-6-astra | unavailable | 1503687 | 0 |
| gpt-6.1-sol | unavailable | 8518597 | 0 |

Attribution omissions: 0 events; 17 diagnostics.

## By effort

| Group | Total tokens | Known subtotal | Missing records |
| --- | --- | --- | --- |
| high | unavailable | 6907305 | 0 |
| medium | unavailable | 3114979 | 0 |

Attribution omissions: 0 events; 17 diagnostics.

## By model_effort

| Group | Total tokens | Known subtotal | Missing records |
| --- | --- | --- | --- |
| gpt-6-astra, medium | unavailable | 1503687 | 0 |
| gpt-6.1-sol, high | unavailable | 6907305 | 0 |
| gpt-6.1-sol, medium | unavailable | 1611292 | 0 |

Attribution omissions: 0 events; 17 diagnostics.

## By task_model_effort

| Group | Total tokens | Known subtotal | Missing records |
| --- | --- | --- | --- |
| 01_business_logic, gpt-6.1-sol, high | unavailable | 141576 | 0 |
| 01_business_logic, gpt-6.1-sol, medium | unavailable | 856058 | 0 |
| 02_cli, gpt-6.1-sol, high | unavailable | 235030 | 0 |
| 02_cli, gpt-6.1-sol, medium | unavailable | 755234 | 0 |
| 03_database, gpt-6-astra, medium | unavailable | 1080384 | 0 |
| 03_database, gpt-6.1-sol, high | unavailable | 3583375 | 0 |
| orchestration, gpt-6.1-sol, high | unavailable | 2947324 | 0 |
| validation, gpt-6-astra, medium | unavailable | 423303 | 0 |

Attribution omissions: 0 events; 17 diagnostics.

## By tool

| Group | Observed calls | Outcomes | Observed seconds | Untimed |
| --- | --- | --- | --- | --- |
| exec | 148 | {'returned': 148} | 124.50999879837036 | 0 |
| followup_task | 3 | {'returned': 3} | 0.13100028038024902 | 0 |
| send_message | 17 | {'returned': 17} | 0.7579996585845947 | 0 |
| spawn_agent | 12 | {'returned': 12} | 0.4159994125366211 | 0 |
| wait_agent | 48 | {'returned': 48} | 2036.764999628067 | 0 |

Attribution omissions: 0 events; 17 diagnostics.

## By task_tool

| Group | Observed calls | Outcomes | Observed seconds | Untimed |
| --- | --- | --- | --- | --- |
| 01_business_logic, exec | 22 | {'returned': 22} | 12.393999576568604 | 0 |
| 01_business_logic, send_message | 4 | {'returned': 4} | 0.16699981689453125 | 0 |
| 01_business_logic, spawn_agent | 1 | {'returned': 1} | 0.042999982833862305 | 0 |
| 01_business_logic, wait_agent | 2 | {'returned': 2} | 52.59099984169006 | 0 |
| 02_cli, exec | 23 | {'returned': 23} | 8.131999731063843 | 0 |
| 02_cli, send_message | 2 | {'returned': 2} | 0.10400009155273438 | 0 |
| 02_cli, spawn_agent | 1 | {'returned': 1} | 0.02499985694885254 | 0 |
| 02_cli, wait_agent | 1 | {'returned': 1} | 50.062999963760376 | 0 |
| 03_database, exec | 70 | {'returned': 70} | 83.45199942588806 | 0 |
| 03_database, send_message | 10 | {'returned': 10} | 0.43599987030029297 | 0 |
| 03_database, spawn_agent | 3 | {'returned': 3} | 0.1379997730255127 | 0 |
| 03_database, wait_agent | 4 | {'returned': 4} | 188.1280002593994 | 0 |
| orchestration, exec | 23 | {'returned': 23} | 8.012999773025513 | 0 |
| orchestration, followup_task | 3 | {'returned': 3} | 0.13100028038024902 | 0 |
| orchestration, send_message | 1 | {'returned': 1} | 0.05099987983703613 | 0 |
| orchestration, spawn_agent | 7 | {'returned': 7} | 0.20999979972839355 | 0 |
| orchestration, wait_agent | 41 | {'returned': 41} | 1745.9829995632172 | 0 |
| validation, exec | 10 | {'returned': 10} | 12.51900029182434 | 0 |

Attribution omissions: 0 events; 17 diagnostics.

## Native lineage

- codex:01a1b6ca-228a-7fa2-8853-29a85535715f → codex:01a1b6ca-f8ea-77a0-b9ce-7126434936e5 (spawn)
- codex:01a1b6ca-228a-7fa2-8853-29a85535715f → codex:01a1b6cb-5354-70f1-a89f-76107013f1fc (spawn)
- codex:01a1b6ca-228a-7fa2-8853-29a85535715f → codex:01a1b6d0-ccae-79e0-9a30-e1c6225d19ec (spawn)
- codex:01a1b6ca-228a-7fa2-8853-29a85535715f → codex:01a1b6d1-24b0-76d2-8274-46567cd4793d (spawn)
- codex:01a1b6ca-228a-7fa2-8853-29a85535715f → codex:01a1b6d6-ad7f-7aa1-adde-9a279323ce76 (spawn)
- codex:01a1b6ca-228a-7fa2-8853-29a85535715f → codex:01a1b6d7-58b6-7610-9ff9-12aeab878459 (spawn)
- codex:01a1b6ca-228a-7fa2-8853-29a85535715f → codex:01a1b6e8-d669-7771-bdd3-50095066308a (spawn)
- codex:01a1b6ca-f8ea-77a0-b9ce-7126434936e5 → codex:01a1b6cf-0274-7341-aa53-4e117241827b (spawn)
- codex:01a1b6d0-ccae-79e0-9a30-e1c6225d19ec → codex:01a1b6d4-ebe2-7a70-a76e-de129afdbd18 (spawn)
- codex:01a1b6d6-ad7f-7aa1-adde-9a279323ce76 → codex:01a1b6e0-0583-7cc1-a8cd-30360c97b55b (spawn)
- codex:01a1b6d6-ad7f-7aa1-adde-9a279323ce76 → codex:01a1b6e3-ee8c-7662-8ab2-296efe7854f7 (spawn)
- codex:01a1b6d6-ad7f-7aa1-adde-9a279323ce76 → codex:01a1b6e6-50c0-7161-9ae8-265492458674 (spawn)

## Coverage diagnostics

- aggregate_snapshot_excluded: 16
- ambiguous_dispatch_turn: 1
