# Implementation task acceptance

This follow-up task selects the registered [TODO-CLI v0.1 specification](../002-todo-cli/acceptance.md), requirements TODO-R001 through TODO-R012, without copying or changing them. The [target](../../../specs/targets/linux-python-uv.yaml) constrains execution. There are no prerequisite subsystems or retained assets.

Mandatory checks are C01–C12 in `.suite/runs/003-implement-todo-cli/checks/acceptance.py`. Each check maps to the same-numbered TODO requirement; shared assertions also establish error/output/byte-preservation rules across scenarios. Checks operate on the actual console script, create disposable fixtures, record process results and file bytes, and remove fixtures afterward. The entire check must succeed. C12 must additionally pass on the assembled app. No manual app criterion applies. Independent review must establish coverage, inspect atomic replacement, execute the frozen checks, and verify protected input and candidate identities.

The user instruction selecting `specs` for implementation is the authority recorded in `approval.json`. Original specification bytes remain unchanged, including their historical draft/readiness annotations; this later approval record and frozen execution registration describe the current run.
