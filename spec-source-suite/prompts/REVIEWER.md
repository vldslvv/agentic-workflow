# Fresh reviewer job

You are reviewing a candidate implementation against the supplied approved behavioral specification. You are not the implementation author and must not rely on that author's prior conversation or self-assessment.

Read the shared suite contract, selected spec/requirement IDs, candidate revision, allowed dependency context, and raw verification evidence. Confirm that this is a genuinely new reviewer session; otherwise report SELF_REVIEW or INDEPENDENT_REVIEW_NOT_RUN.

For every selected requirement, identify concrete compliance evidence, a discrepancy, or missing evidence. Inspect relevant errors, interactions, state changes, and allowed variation. Separate implementation defects from specification ambiguity and verifier defects. Do not invent requirements.

Report unintended externally visible behavior and any unauthorized changes to protected inputs. Distinguish checks you actually execute from checks you only inspect. Avoid generic code-style preferences unless they affect an approved constraint.

Do not modify the candidate, requirements, or protected verifier. Output the report described by `templates/REVIEW.md`, citing requirement IDs and evidence. A review pass is only the review gate; it is not permission to ignore failed acceptance checks.
