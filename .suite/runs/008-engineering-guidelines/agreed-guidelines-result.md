# Agreed guidelines incorporated

Authority: the user's follow-up request to re-read project files and incorporate the nine concise guidelines established in this conversation. This supersedes the initial decision to preserve the old wording for discussion; earlier results remain historical.

G5 PASS: `guidelines.md` now contains the agreed nine bullets verbatim, with an engineering-guidelines heading. The functional core, justified stateful objects, cohesive composition, compatible pipeline contracts, public behavior tests, isolated real infrastructure and explained departures are explicit.

G6 PASS: re-read the current root instructions, shared rules, all five role routines, project template, and both existing project briefs. Root routing still requires guideline reading before code work; shared rules require every role to read applicable guidelines and carry their resolved paths into handoffs. Planner, reviewer and validator requirements remain intact. Existing project briefs inherit repository guidelines without duplicated text. No suite files or app inputs changed in this follow-up.

Validation from the repository root: `python spec-source-suite/helpers/check_package.py --base 4aa4b7a7ed9d2ac96a750f26497f823b8a61d629` passed with 38 links checked; see `agreed-guidelines-package-check.json`. `git diff --check` passed. From `spec-source-suite/`, `sha256sum -c SHA256SUMS` passed for all 19 entries. Suite metadata/checksums remain unchanged because the updated guideline source is outside the package. No runtime tests were repeated for this prose-only edit.

Current package metrics: 20 files, 10 directories, 4,953 instruction words; shared-plus-role words are Supervisor 2,648, Planner 2,343, Implementer 2,154, Reviewer 2,105 and Validator 2,266. This follow-up adds no package files or instruction words; changes relative to HEAD precede this follow-up. The guidelines retain one source of truth and introduce no additional procedure files.

Scope and limits: document-only completion. Existing application conformance was not reassessed; future code work must apply the revised source under the existing changed-source rules. No application execution, independent review or generation-readiness claim. Session/turn counters unavailable.
