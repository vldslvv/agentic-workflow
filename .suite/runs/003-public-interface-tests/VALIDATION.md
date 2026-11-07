# Public-interface testing instructions — validation

Authority: the user's supplied plan, “Require public-interface tests for implementation tasks,” and explicit instruction to implement and verify it. Scope is reusable guidance and package metadata; this is documentation-only work, not app generation. Baseline identities and unchanged-record hashes are retained in `baseline.json`; the previous package metadata is preserved in `package-checks-before.json`.

## Scenario review

These are manual instruction walkthroughs, not executed app tests or an independent implementation review. Each row traces the prescribed action through the edited documents.

| Scenario | Instruction path and expected disposition | Result |
|---|---|---|
| New observable behavior lacks coverage | Contract §4 defines exported APIs, HTTP endpoints, CLI commands, UI interactions and documented pipeline inputs/outputs as public boundaries. Define D3 and Planning / Check authorship identify the applicable boundary and add or extend requirement-linked tests before freezing. Acceptance records interface, check and outcome; Implement I2 executes it and Reviewer steps 1–2 assess coverage and execute independently. | PASS |
| Refactor already has adequate tests | Contract §4 permits reuse; Planning explicitly maps existing coverage for refactors. Existing public-interface tests are retained when sufficient, with current-candidate execution under Implement I2. No duplicate test is required merely because code changed. | PASS |
| Real dependency is impractical or destructive | Contract §4 prefers the real dependency, then a meaningful safe substitute that exercises candidate behavior. Acceptance records the substitute's fidelity limits; Reviewer step 1 evaluates them. A mock supplying the asserted behavior does not count. An explicitly required real-dependency integration gate remains mandatory. | PASS |
| Meaningful test remains impractical | Planner/supervisor records obstacle, affected IDs, alternatives, remaining evidence and coverage gap in acceptance/run evidence. Contract §4 delegates this decision without a user approval prompt. No production test-only export or hook is permitted. A skipped check remains NOT_RUN/BLOCKED; reviewer judges evidence sufficiency, and inadequate evidence still blocks acceptance. | PASS |
| Exception is discovered after freezing | Implement I4 preserves the obstacle and routes it to the supervisor. Contract §4 requires a recorded CHANGE authorization and a new frozen acceptance/check revision while preserving original expectations, inventories and results. Affected evidence is invalidated; revised checks execute. Reviewer-visible acceptance/evidence carries the decision without exposing excluded plans or conversations. | PASS |
| Failed behavior or documentation-only scope | An observed specification mismatch remains FAIL and unresolved violations block acceptance under contract §5; an exception cannot waive functional requirements or other acceptance gates. Independent review, applicable manual/integration checks and final assembled-app execution remain required for app work. Documentation-only work is expressly exempt and follows Define's existing document-completion gate. | PASS |

## Consistency and scope review

The shared contract owns the public-interface definition, test quality rules and exception authority. Role documents apply those rules at planning, execution, revision and review; acceptance/review/run templates capture the needed evidence. Additive coverage revisions remain distinct from testing exceptions. Helper schemas, runtime APIs, test frameworks and automated enforcement are unchanged; existing PASS/FAIL/BLOCKED/NOT_RUN dispositions are retained.

Testing exceptions concern feasibility. They do not grant acceptance by themselves, erase earlier failures, satisfy a mandatory real-dependency gate with a substitute, or permit acceptance with zero mandatory checks executed. Reviewer exclusions and fresh-context requirements remain intact. The future-only policy does not rewrite completed records.

## Mechanical validation

`package-validation.json` records local Markdown link/fragment checks, heading changes, JSON parsing, package version consistency, checksum coverage/digests, preserved helper/test and historical record hashes, and `git diff --check`. `checksum-verification.log` retains the separate `sha256sum --check SHA256SUMS` result. `changes.diff` records the reviewed package diff.

Final mechanical result: PASS. Checked 107 local Markdown links, including 20 fragments, across 29 Markdown files; both package JSON files parse and all five current metadata evidence references resolve. No headings were removed; the acceptance template adds `Testing exceptions`. All 42 package checksum entries match and cover the complete package inventory. All eight helper/test files and 172 existing task/run files retain their baseline hashes. `git diff --check` exits 0.

The first link-validation attempt mistakenly treated a fenced Markdown example in the unchanged project-memory guidance as a live link. `package-validation-attempt-0.json` retains that failure. The validator was corrected to exclude fenced examples; no suite content was changed for that false positive.

No helper tests were added, changed or run: this change affects instructions and templates, and verification targets those artifacts. No live app generation, regeneration, or multi-agent execution was attempted. These results demonstrate instruction consistency and package integrity only.
