# Checks and acceptance

Read when preparing checks, reviewing work or deciding whether it passes. Use [Bundle](BUNDLE.md) to resolve requirements and [Guidelines](GUIDELINES.md) for engineering rules.

## Prepare checks

Apply before coding and when updating acceptance criteria.

- Write acceptance criteria from the original requirements.
- Cover normal use, boundary cases, failures and interactions.
- State public API contracts in acceptance.
- Include inputs, outputs, errors and observable side effects in each contract.
- Link contracts to source requirements.
- Provide expected test scenarios for each contract.
- State setup, action and expected outcome for each scenario.
- Choose unit or integration tests for each scenario.
- Use both test layers where they cover distinct risks.
- Keep internal design choices in the plan unless the requirements specify them.
- Treat a missing requirement as a defect, even if all listed checks pass.
- Correct incomplete acceptance criteria against the original requirements.
- Preserve approved history during acceptance corrections.
- Rerun checks affected by acceptance corrections.
- Repeat required independent review after acceptance corrections.
- Choose checks that fit the change and test observable behaviour.
- Include relevant regression tests.
- Run required manual checks.
- Run required checks against real dependencies.
- Reuse useful tests.
- Cover test gaps through public interfaces.
- Explain mock use in check evidence.
- State why mocks fit, what they replace and what remains untested.
- Assess internal tests and mocks by the failures they can detect.
- Consider isolation, cost and realism.
- Require meaningful assertions about the code under test.
- Reject production hooks added only for tests.

## Assess results

Apply when reporting checks or accepting work.

- Use `PASS` only when required checks pass, requirements are adequately covered and no findings remain that require action.
- Check coverage separately from test success.
- Use `FAIL` when the work breaks a requirement or an applicable rule.
- Use `BLOCKED` when required tools or capabilities are unavailable, or requirements remain unresolved.
- Mark skipped checks `NOT_RUN`, or `BLOCKED` when their absence prevents acceptance.
- Use `INDEPENDENT_REVIEW_NOT_RUN` when a required fresh review has not run.
- Block acceptance when required fresh review has not run.
- Report substitute checks and coverage gaps without lowering the requirements.
- Save evidence using the [result template](../templates/result.md).
- For manual judgments, name the rule and the item inspected.
- Report cleanup errors separately from the failure being checked.

## Independent checks

Apply to independent review and validation.

- Start with a fresh context and no inherited conversation.
- Use original requirements and guidelines to decide what to check before reading acceptance criteria or code.
- Use only requirements, applicable acceptance criteria, the work being checked, factual check results, contracts, justified guideline exceptions and prior findings.
- Allow focused mock justifications as review inputs.
- Assess mock justifications independently.
- Exclude plans, conversations, project memory, other design explanations and the author's claims of correctness.
- Exclude copies of these from other files too.
- Keep the work being checked unchanged, including relevant dependencies, configuration and check inputs.
- Record its location and revision when available.
- Use existing version information.
- Do not require a new commit or lock.
- Report candidate changes during checking.
- Rerun affected independent checks in a fresh context.
- Run relevant checks yourself.
- Reproduce reported problems where feasible.
- Follow the stated setup, cleanup, pass criteria, sampling rules and thresholds.

## Keep results current

Apply while running checks and when stopping work.

- Batch reads and commands that do not depend on each other.
- Print only useful output.
- Repeat successful checks only after relevant changes, failures, new concerns or when an independent check is required.
- Reassess affected results when requirements, guidelines, dependencies or implementation change.
- Save unfinished work and blockers when cancelled or stopped by a limit.
