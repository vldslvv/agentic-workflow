# Checks and acceptance

Prepare requirement-based checks and assess whether work passes.

## References:

- [RESULT_TEMPLATE]: Records completion status, evidence, findings and limits. agentic-workflow/templates/result.md

## Prepare acceptance

Apply before coding in plan-review mode and when authoring or correcting Acceptance.

- Derive observable criteria from original requirements, excluding advisory implementation suggestions.
- Cover normal use, boundaries, failures, interactions and specified state or lifecycle guarantees.
- Define or link source-backed contracts covering inputs, outputs, errors and observable side effects.
- Map acceptance outcomes and contract guarantees to concrete scenarios, reusing shared checks.
- Keep internal design choices in the Plan unless required by the specifications.
- Preserve approved history when correcting Acceptance, then rerun affected checks and required independent review.

## Prepare checks

Apply before coding and when updating checks in either mode.

- Use source criteria directly for direct tasks.
- Check observable behaviour and relevant regressions through public interfaces.
- Choose unit or integration checks by detectable failures, using both for distinct risks and asserting meaningful outcomes.
- Run required manual checks and checks against real dependencies.
- Record mock justifications, replacements and remaining gaps in evidence, assessing isolation, cost, realism and detectable failures.
- Reject production hooks added only for tests.

## Assess results

Apply when reporting checks or accepting work.

- Use `PASS` only with passing required checks, adequate requirement coverage and no actionable findings.
- Use `FAIL` for violated requirements or applicable rules, even when listed checks pass.
- Use `BLOCKED` for unresolved requirements or unavailable required capabilities.
- Mark skipped checks `NOT_RUN`, or `BLOCKED` when their absence prevents acceptance.
- Block acceptance with `INDEPENDENT_REVIEW_NOT_RUN` when a required fresh review has not run.
- Record evidence, substitute checks and coverage gaps in [RESULT_TEMPLATE] without lowering requirements.
- Name the rule and inspected item for manual judgments, reporting cleanup errors separately.

## Independent checks

Apply to independent review and validation.

- Start in a fresh context without inherited conversation.
- Choose checks from original requirements and guidelines before reading Acceptance or code.
- Admit only the role's input contract and Instructions, filtering Results and Evidence to facts, prior findings and focused guideline or mock justifications.
- Exclude plans, implementation suggestions, conversations, memory, design explanations and correctness claims, including copies in other files.
- Exclude native logs, `events.json`, `timeline.json` and dashboard evidence; allow usage measurements and metadata in JSON or Markdown.
- Assess supplied justifications independently and run relevant checks yourself, reproducing reported problems where feasible.
- Follow specified setup, cleanup, pass criteria, sampling rules and thresholds.
- Keep the candidate, dependencies, configuration and check inputs unchanged, recording location and existing revision when available.
- Report candidate changes and rerun affected independent checks in a fresh context without requiring a new commit or lock.

## Keep results current

Apply when evidence may be outdated or work stops.

- Reassess affected results after changes to requirements, guidelines, dependencies or implementation.
- Repeat successful checks only for relevant changes, failures, new concerns or required independent checks.
- Save unfinished work and blockers when cancelled or stopped by a limit.
