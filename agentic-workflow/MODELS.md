# Model routing

Read on role entry and before launching workers; reread edits for subsequent dispatches. Keep concrete models and native reasoning values here.

## Routing source

Use `<project-root>/.agentic-workflow/MODELS.md` when present; otherwise use this
file. The project file replaces the complete routing policy, profiles and role
routes, without merging defaults. Copy this file there to start a customization.
Missing or malformed routes in an override require correction; do not fall back
silently. Resolve the project root from the assigned workspace, pass the chosen
path in handoffs, and reread it before subsequent dispatches. The eval launcher
uses the same precedence for the Supervisor default route.

## Routing rules

1. Resolve profiles and role routes from the tables. Undefined profiles or malformed entries require correction before routing.
2. Select the first applicable route below.
3. Request settings through supported host controls. Unsupported settings use host defaults with a reported fallback; never guess equivalent replacements. Infrastructure, credentials and unresolved requirements remain blockers.
4. Change retained-worker settings only through supported controls, preserving contexts and fresh-review rules. Sessions without setting controls keep existing settings; top-level routing is launch guidance in that case. Disclose known mismatches.
5. Record profile, reason, requested settings and observed settings separately in the role's result. Unknown observations remain unavailable.

| First matching condition | Route |
|---|---|
| Two consecutive implementation repairs reproduce the same failure without new diagnostic evidence | `escalation` |
| Conflicting requirements, complex interactions, or correctness decisions involving security, data loss or compatibility | Role's demanding route |
| Local implementation, explicit behavior, established pattern, no interface or dependency changes | `small-change` |
| Otherwise | Role default |

## Profiles

| Profile | Model | Reasoning |
|---|---|---|
| coordination | `gpt-6.1-sol` | `low` |
| standard | `gpt-6.1-sol` | `medium` |
| careful | `gpt-6.1-sol` | `high` |
| small-change | `gpt-6-luna` | `high` |
| escalation | `gpt-6-astra` | `medium` |

Model identifiers are opaque, including provider-qualified names. Use native reasoning values; `default` leaves the host setting. Provider changes update these names/values; authentication and connectivity remain host configuration. These tables add no dispatcher, adapters or Markdown parser.

## Role routes

| Role | Default | Demanding work |
|---|---|---|
| Supervisor | coordination | standard |
| Planner | standard | careful |
| Implementer | standard | careful |
| Reviewer | careful | escalation |
| Validator | careful | escalation |
