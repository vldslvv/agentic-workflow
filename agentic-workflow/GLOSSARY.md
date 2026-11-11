# Role vocabulary

These terms name existing workflow roles, inputs and outputs.
Role instructions and policies retain procedures, permissions and storage rules.

## Language

**Supervisor**: Coordinator of task execution, recovery and acceptance.

**Planner**: Author of project documents and maintainer of workflow instructions.

**Implementer**: Owner of an assigned task's Implementation, checks and corrections.

**Reviewer**: Independent assessor of Acceptance and Implementation against task requirements.

**Validator**: Independent assessor of the assembled application and author of repair Task specifications for implementation failures.

**Instructions**: Applicable role instructions, workflow policies and project guidance.

**Assignment**: Authorized objective, selected scope, task mode, target location, record location and ownership constraints.

**Project specification**: Project-wide requirements and constraints in `project.md`.

**Task specification**: Requirements for one task in `tasks/*.md`, including repair tasks.

**Task order**: Task dependencies in `task_order.md`.

**Application Contract** (or **Contract** in specification bundles): An interface specification provided or consumed by a task.

**Workflow data contract**: A reusable handoff type in `contracts/`, independent of roles.

**WorkResult**: The concise return contract referencing a saved Result.

**Verification**: Shared checks and assembled-application scenarios in `verification.md`.

**Implementation**: Application source, tests, configuration, dependencies and assets at the assigned target.

**Plan**: The task’s proposed implementation approach in `plan.md`.

**Acceptance**: The requirement-to-check mapping and pass criteria in `acceptance.md`.

**Evidence**: Recorded check execution, observations and inspection findings.

**Result**: A role’s status, completed scope, evidence references, findings, limits and unfinished work.

**Memory**: Saved project lessons and their index.

**Execution state**: Supervisor’s record of task status, ownership, acceptance and continuation information.
