# Removal audit

User authority: remove role-context, check-execution and memory-validation helpers and their corresponding tests.

| Retired owner / tests | Former contract / callers | Reason no replacement proof is needed |
|---|---|---|
| helpers/role_context.py / tests/test_role_context.py | Role read manifests, hashes, section byte counts, forbidden paths and memory write declarations; called by documented workflow CLI and its tests | This validation interface is explicitly retired. Context exclusions remain instructions in shared rules, Implement, Reviewer and Regeneration; these are not represented as enforced access control. |
| helpers/check_execution.py / tests/test_check_execution.py | Frozen check manifests, mappings, process cleanup/interruption and immutable evidence; called by documented workflow CLI and its tests | The suite no longer provides a check executor. Workers run project checks directly; shared rules and Reviewer retain evidence, failure distinctions and cleanup guidance. |
| helpers/project_memory.py / tests/test_project_memory.py | Prescribed note metadata/index validation and containment; called by documented workflow CLI and its tests | Prescribed memory validation is explicitly retired. Ordinary Markdown index/notes remain, with no automated format claim. |

Owners originated in the Helpers and Project memory commits (4289645 and 130171f). Repository reference search found documentation callers, owner tests and historical research references, with no app runtime import or CI configuration requiring these helpers. The first test run before removal passed all 25 tests; removal is requested scope, not a response to failing tests. Retained usage helper/tests are unchanged and own telemetry compatibility. Removed production code: 562 lines; removed tests: 473 lines.

The test-audit skill's referenced openclaw proof-policy file is absent in the installed skill tree. Its unrelated JavaScript CI commands do not apply to this Python/docs repository. Verification uses retained unittest coverage, link/inventory checks, diff checks and review.
