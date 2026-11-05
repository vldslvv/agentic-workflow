# Frozen-check execution instructions

These instructions are used by the reviewer or a controlled execution service; they do not require another agent. The planner prepares checks before implementation under the [shared contract](../docs/SUITE_CONTRACT.md) §4.

Identify the selected requirements, frozen check/fixture/adapter digests, candidate identity, environment, and observed boundary. Execute the prescribed checks and retain commands, exit codes, actual outputs, and side effects. Map outcomes to requirement IDs. Run cleanup as specified, without changing the candidate or acceptance inputs.

For authorized manual criteria record the authority, inspected artifact, and decision. A missing executable check, unavailable service, skipped execution, or timeout remains BLOCKED/NOT_RUN with the infrastructure reason; an agent opinion cannot replace execution. Apply predeclared sampling and thresholds for nondeterministic checks.

Verify the candidate and baseline remain unchanged. Preserve any failure and report suspected verifier defects immediately to the supervisor. Expectations cannot be edited during a run. Return results and raw evidence for the actual attempt, keeping the initial outcome separate from repairs.
