# Model routing

Read on role entry and before launching workers.

## Routing source

- Context: choose the routing policy when starting a role and before launching workers.
- Inputs: assigned workspace and optional `<project-root>/.agentic-workflow/MODELS.md`.
- Effects:
  1. Find the project root from the assigned workspace.
  2. Use the project file if it exists; otherwise use this file. The project file replaces the whole policy and all tables. Do not merge in defaults.
  3. Correct missing or invalid routes in the project file instead of falling back to this file.
- Outputs: the chosen policy path. Pass it in handoffs and reread it before launching more workers. The eval launcher follows the same rule for the Supervisor's default route.

To customize routing, copy this file to the project path and edit it there.

## Select settings

- Context: read the chosen policy and its tables, including edits made before launching another worker.
- Inputs: role, task conditions, profiles and role routes.
- Effects:
  1. Check that routes are valid and refer to defined profiles. Correct errors before choosing a route.
  2. Select the first matching route below.
  3. Request its settings through controls the host supports.
- Outputs: record the profile and reason in the role's result. Record requested and observed settings separately; leave unknown observations unavailable.

## Routing guidelines

Apply when requesting or changing worker settings.

- Use host defaults when a setting is unsupported and report the fallback. Do not guess a replacement.
- Keep missing infrastructure, credentials and unresolved requirements as blockers.
- Change an existing worker's settings only through supported controls. Preserve its context and the rules for fresh reviews.
- Keep current settings when the session has no controls to change them. In that case, use top-level routing only as guidance when launching a session.
- Report known differences between requested and actual settings.
- Keep model names and supported reasoning values in this policy. Use model identifiers exactly as supplied, including provider prefixes.
- Use `default` to keep the host setting.
- Update model names and values when the provider changes them. Keep authentication and connections in the host configuration.
- Do not add a dispatcher, adapters or a Markdown parser to apply these tables.

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
