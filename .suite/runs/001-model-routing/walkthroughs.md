# Documentation walkthroughs

Authority: [acceptance](../../tasks/001-model-routing/acceptance.md). Inspected artifacts: [model configuration](../../../spec-source-suite/MODELS.md), [shared rules](../../../spec-source-suite/AGENTS.md), [root index](../../../AGENTS.md), and [record index](../../index.md). Each row is a manual evaluation of the written procedure, not a live host/model execution. PASS means the instructions yield the required selection or action.

| Case | Requirement | Input and expected action | Observed document outcome |
|---|---|---|---|
| 1 | R2–R3 | Routine Supervisor → coordination; demanding Supervisor → standard. | PASS: exact routes and profile settings match acceptance. |
| 2 | R2–R3 | Routine Planner → standard; demanding Planner → careful. | PASS: exact routes and profile settings match acceptance. |
| 3 | R2–R3 | Routine Implementer → standard; demanding Implementer → careful. | PASS: exact routes and profile settings match acceptance. |
| 4 | R2–R3 | Routine Reviewer → careful; demanding Reviewer → escalation. | PASS: exact routes and profile settings match acceptance. |
| 5 | R2–R3 | Routine Validator → careful; demanding Validator → escalation. | PASS: exact routes and profile settings match acceptance. |
| 6 | R4 | Two consecutive repairs reproduce the same failure without new diagnostic evidence, even for an otherwise small or demanding implementation → escalation request. | PASS: first-applicable ordering makes escalation win. |
| 7 | R4 | One failed repair, different failures, or new diagnostic evidence on the second repair → no automatic escalation from rule 1. | PASS: all trigger conditions are required; evaluate remaining routes. |
| 8 | R4 | Conflicting requirements or complex component interactions → role demanding route; unresolved requirements still block work. | PASS: rule 2 selects the route; blocker paragraph preserves the blocked state. |
| 9 | R4 | Security, data-loss or compatibility correctness decision in otherwise local work → demanding, even with an established pattern. | PASS: each risk is named; rule 2 precedes small-change. |
| 10 | R4 | Local implementation, explicit expected behavior, established pattern, no interface/dependency changes, no higher exception → small-change. | PASS: rule 3 requires every condition. |
| 11 | R4 | Interface/dependency change, missing expected behavior, or no established pattern → role default unless demanding/escalation applies. Routine review/validation is not local implementation. | PASS: small-change is scoped to implementation and conjunctive; other work reaches rule 4. |
| 12 | R4 | Missing infrastructure or credentials at any profile → blocked dependency, not solved by model escalation. | PASS: blocker paragraph applies independently of route. |
| 13 | R5 | Replace a profile model with `provider-x/family-v2`, retaining its profile key → role mappings unchanged; identifier passed intact. | PASS: names are opaque and may be provider-qualified; no splitting/normalization or provider adapter is prescribed. |
| 14 | R5 | Provider requires a native reasoning value → edit the profile's reasoning cell; `default` → use host reasoning setting. | PASS: both native values and default semantics are explicit; auth/connectivity stay in the host. |
| 15 | R6 | Enter a role or launch a worker after a table edit → read current configuration and select from updated tables. | PASS: both read triggers and rereading edits for subsequent dispatches are explicit. |
| 16 | R6–R8 | Retained implementer needs a new profile and host exposes a change control → request through that control, retain context; fresh reviewer still starts in a new context. | PASS: settings changes preserve contexts and fresh-review requirements; requests and observations remain separate. |
| 17 | R6–R8 | Retained worker has no setting-change control → host defaults, report fallback/known mismatch; no claim that settings changed and no replacement solely to imitate retention. | PASS: only supported controls authorize changes; existing shared Records rule also requires disclosure of actual replacement. |
| 18 | R7–R8 | Host cannot apply requested model or reasoning → continue with host defaults, record requested settings and fallback; unknown observed settings remain unavailable. | PASS: unsupported-setting behavior and result fields are explicit. This is distinct from required infrastructure being absent. |
| 19 | R7–R8 | Existing top-level session cannot change settings → launch guidance, disclose any known mismatch. | PASS: no unsupported live switch is claimed. |
| 20 | R7 | Route references undefined profile or has malformed entry → correct configuration before routing, not silent fallback. | PASS: validation is required before selection; unsupported host settings have a separate fallback. |
| 21 | R8 | Produce ordinary role result → chosen profile, reason, requested model/reasoning, observed settings if available, fallback/mismatch. | PASS: existing common result outline has one added field; telemetry files and schemas remain untouched. |
| 22 | R9–R10 | Add MODELS.md → explicit direct root-index link with role-entry/worker-setting condition in the same change. | PASS: root row contains exact target and read condition. |
| 23 | R10 | Add project document, task record or memory note → use applicable scoped index; create one only if absent and link parent. | PASS: shared rule specifies placement; this task uses one new .suite/index.md linked from root and containing each new Markdown record with purpose. |
| 24 | R10 | Move or rename Markdown file → update its index link to the new relative path in the same change; remove file → update index by removing obsolete link. | PASS: moves, renames and removals are explicitly covered. These are hypothetical walkthroughs; no disposable repo file is claimed as a live exercise. |
| 25 | R10 | Reviewer follows record index → acceptance and permitted evidence only; indexed plan/memory remain excluded. | PASS: indexing does not authorize excluded context; scoped index preserves the role limitation. |

The five role routines contain no concrete model settings. Configuration is the single operative table source; historical plan/acceptance and observed execution records are evidence, not competing configuration. Existing role links to shared guidance suffice without repeating the routing procedure.
