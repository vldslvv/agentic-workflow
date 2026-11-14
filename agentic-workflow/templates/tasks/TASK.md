# <Component — capability or change>

Specify a component’s responsibilities, behavior, constraints and acceptance.

## References:

- [BUNDLE]: Defines specification files, task selection and path resolution. agentic-workflow/policies/BUNDLE.md
- [SUPERVISOR]: Coordinates implementation, recovery and acceptance. agentic-workflow/roles/SUPERVISOR.md

## Context

Apply [BUNDLE] (“Task specifications”).

- **Responsibility:** <The component's purpose.>
- **Boundary:** <Included work and explicit exclusions.>
- **Sources:** <Relevant project requirements and existing components.>

## Contracts

- **Provides:** <Implemented interfaces or shared contract links.>
- **Consumes:** <Used interfaces or shared contract links.>

## Behavior

<Required capabilities and observable rules, grouped by feature or interaction.>

- **Inputs:** <Requests, user actions, events, configuration or resources.>
- **Effects:** <Persistent changes, external calls or notifications, or None.>
- **Outputs:** <Responses, rendered views, emitted events or other visible results.>
- **State and lifecycle:** <Owned state, transitions, initialization, cleanup and recovery.>
- **Failures:** <Observable behavior and remaining state after failures.>
- **Invariants:** <Conditions preserved across operations and transitions.>

## Constraints

<Required implementation choices and quality limits, or links to shared constraints.>

## Acceptance

| Scenario | Observable pass condition |
|---|---|
| <Normal use, boundary, transition or failure> | <Required outcome and effects, or a shared scenario link> |

## Implementation suggestions — optional

<Advisory structure, algorithms, libraries or reuse opportunities.>

## Workflow requirements — optional

<Requested `Workflow: plan-review` or `Workflow: direct` and required approvals/reviews under [SUPERVISOR] (“Task mode”).>
