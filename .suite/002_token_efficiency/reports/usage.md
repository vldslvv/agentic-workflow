# Selected implementation usage

Null means unavailable. Known subtotals exclude missing measurements. Scope and omissions are in usage.json.

| Metric | Total | Known subtotal | Measured records | Missing records |
|---|---:|---:|---:|---:|
| input_tokens | unavailable | 3028195 | 31 | 0 |
| cached_input_tokens | unavailable | 2953600 | 31 | 0 |
| cache_write_input_tokens | unavailable | 0 | 31 | 0 |
| uncached_input_tokens | unavailable | 74595 | 31 | 0 |
| output_tokens | unavailable | 14670 | 31 | 0 |
| reasoning_output_tokens | unavailable | 6949 | 31 | 0 |
| total_tokens | unavailable | 3042865 | 31 | 0 |

## By task

| Group | Total tokens | Known subtotal | Missing records | Tools |
| --- | --- | --- | --- | --- |
| orchestration | unavailable | 2452634 | 0 | 13 |
| remove_allocation_lock | 590231 | 590231 | 0 | 16 |

Attribution omissions: 0 events; 0 diagnostics.

## By agent_run

| Group | Total tokens | Known subtotal | Missing records | Tools |
| --- | --- | --- | --- | --- |
| codex:01a1b471-b34e-7971-bf0e-9c1b0f2b8d7f | unavailable | 2452634 | 0 | 13 |
| codex:01a1b49e-cc95-76d3-9c53-70f2758ab14a | 337858 | 337858 | 0 | 9 |
| codex:01a1b4a0-92fe-7201-b952-4cc618a28460 | 252373 | 252373 | 0 | 7 |

Attribution omissions: 0 events; 0 diagnostics.

## By role

| Group | Total tokens | Known subtotal | Missing records | Tools |
| --- | --- | --- | --- | --- |
| implementer | 337858 | 337858 | 0 | 9 |
| reviewer | 252373 | 252373 | 0 | 7 |
| supervisor | unavailable | 2452634 | 0 | 13 |

Attribution omissions: 0 events; 0 diagnostics.

## By model

| Group | Total tokens | Known subtotal | Missing records |
| --- | --- | --- | --- |
| gpt-6-astra | unavailable | 2452634 | 0 |
| gpt-6.1-sol | 590231 | 590231 | 0 |

Attribution omissions: 0 events; 4 diagnostics.

## By effort

| Group | Total tokens | Known subtotal | Missing records |
| --- | --- | --- | --- |
| high | 590231 | 590231 | 0 |
| xhigh | unavailable | 2452634 | 0 |

Attribution omissions: 0 events; 4 diagnostics.

## By model_effort

| Group | Total tokens | Known subtotal | Missing records |
| --- | --- | --- | --- |
| gpt-6-astra, xhigh | unavailable | 2452634 | 0 |
| gpt-6.1-sol, high | 590231 | 590231 | 0 |

Attribution omissions: 0 events; 4 diagnostics.

## By task_model_effort

| Group | Total tokens | Known subtotal | Missing records |
| --- | --- | --- | --- |
| orchestration, gpt-6-astra, xhigh | unavailable | 2452634 | 0 |
| remove_allocation_lock, gpt-6.1-sol, high | 590231 | 590231 | 0 |

Attribution omissions: 0 events; 4 diagnostics.

## By tool

| Group | Observed calls | Outcomes | Observed seconds | Untimed |
| --- | --- | --- | --- | --- |
| exec | 22 | {'returned': 21, 'unknown': 1} | 5.4690001010894775 | 1 |
| send_message | 1 | {'returned': 1} | 0.032000064849853516 | 0 |
| spawn_agent | 2 | {'returned': 2} | 0.15000009536743164 | 0 |
| wait_agent | 4 | {'returned': 4} | 115.74599981307983 | 0 |

Attribution omissions: 0 events; 4 diagnostics.

## By task_tool

| Group | Observed calls | Outcomes | Observed seconds | Untimed |
| --- | --- | --- | --- | --- |
| orchestration, exec | 7 | {'returned': 6, 'unknown': 1} | 1.011000156402588 | 1 |
| orchestration, spawn_agent | 2 | {'returned': 2} | 0.15000009536743164 | 0 |
| orchestration, wait_agent | 4 | {'returned': 4} | 115.74599981307983 | 0 |
| remove_allocation_lock, exec | 15 | {'returned': 15} | 4.45799994468689 | 0 |
| remove_allocation_lock, send_message | 1 | {'returned': 1} | 0.032000064849853516 | 0 |

Attribution omissions: 0 events; 4 diagnostics.

## Native lineage

- codex:01a1b462-d404-77e0-8de7-41a76c78d1e9 → codex:01a1b471-b34e-7971-bf0e-9c1b0f2b8d7f (fork)
- codex:01a1b471-b34e-7971-bf0e-9c1b0f2b8d7f → codex:01a1b49e-cc95-76d3-9c53-70f2758ab14a (spawn)
- codex:01a1b471-b34e-7971-bf0e-9c1b0f2b8d7f → codex:01a1b4a0-92fe-7201-b952-4cc618a28460 (spawn)

## Coverage diagnostics

- aggregate_snapshot_excluded: 3
- unfinished_turn: 1
