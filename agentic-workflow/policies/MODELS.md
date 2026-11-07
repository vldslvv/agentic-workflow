# Model routing

Read on role entry and before launching workers.

## Routing source

- Context: apply this routing policy on role entry and before launching workers.
- Inputs: assigned workspace and optional `<project-root>/.agentic-workflow/MODELS.md`.
- Effects: resolve the project root from the assigned workspace. Use the project file when present; otherwise use this file. The project file replaces the complete routing policy, profiles and role routes without merging defaults. Copy this file there to start a customization. Correct missing or malformed override routes without silently falling back.
- Outputs: chosen routing path, passed in handoffs and reread before subsequent dispatches. The eval launcher uses the same precedence for the Supervisor default route.

## Select settings

- Context: read the chosen routing source and its tables; reread edits for subsequent dispatches.
- Inputs: role, work conditions, profiles and role routes.
- Effects: resolve profiles and role routes; correct undefined profiles or malformed entries before routing. Select the first applicable route below and request settings through supported host controls.
- Outputs: profile, reason, requested settings and observed settings recorded separately in the role's result. Keep unknown observations unavailable.

## Routing guidelines

Apply when requesting or changing worker settings.

- Use host defaults with a reported fallback for unsupported settings; never guess equivalent replacements. Keep infrastructure, credentials and unresolved requirements as blockers.
- Change retained-worker settings only through supported controls, preserving contexts and fresh-review rules. Keep existing settings in sessions without controls; treat top-level routing as launch guidance in that case. Disclose known mismatches.
- Keep concrete models and native reasoning values in this policy. Treat model identifiers as opaque, including provider-qualified names; use `default` to leave the host setting.
- Update model names/values for provider changes; keep authentication and connectivity in host configuration. Add no dispatcher, adapters or Markdown parser through these tables.

## Route selection

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

## Role routes

| Role | Default | Demanding work |
|---|---|---|
| Supervisor | coordination | standard |
| Planner | standard | careful |
| Implementer | standard | careful |
| Reviewer | careful | escalation |
| Validator | careful | escalation |
