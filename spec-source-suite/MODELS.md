# Model configuration

Use the [shared routing procedure](AGENTS.md#model-routing) to select a profile. Edit these tables to change subsequent dispatch requests.

## Profiles

| Profile | Model | Reasoning |
|---|---|---|
| coordination | `gpt-6.1-sol` | `low` |
| standard | `gpt-6.1-sol` | `medium` |
| careful | `gpt-6.1-sol` | `high` |
| small-change | `gpt-6-luna` | `high` |
| escalation | `gpt-6-astra` | `medium` |

Model identifiers are opaque strings, including provider-qualified names. Provider switching changes the model names here and, where necessary, native reasoning values. Reasoning values use the host's native settings; `default` leaves reasoning at the host's setting. Provider authentication and connectivity remain host configuration. This file supplies configuration only; it adds no dispatcher, provider adapters or Markdown parser.

## Fallbacks

Unsupported model or reasoning: use host defaults and report the fallback. Profile names do not imply equivalent models across providers; never guess a replacement. Sessions without setting controls keep their existing settings. Invalid configuration requires correction; missing credentials or infrastructure remain blockers.

## Role routes

| Role | Default | Demanding work |
|---|---|---|
| Supervisor | coordination | standard |
| Planner | standard | careful |
| Implementer | standard | careful |
| Reviewer | careful | escalation |
| Validator | careful | escalation |
