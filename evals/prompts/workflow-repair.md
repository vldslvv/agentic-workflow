# Repair workflow findings

## Context

Attempt one correction of the completed review without another model review.

## Inputs

- Read the findings in `{judgment}`.
- Use the original snapshot at `{snapshot}`.
- Apply `agentic-workflow/policies/DOCUMENT_STYLE.md`.

## Effects

1. Edit working Markdown files included in the snapshot only as needed for the findings.
2. Preserve existing work, saved evidence and `agentic-workflow/WORKFLOW.md`.
3. Leave unresolved findings for human review without committing changes or inventing missing requirements or evidence.

## Outputs

- Return JSON matching the supplied repair schema.
- Return `PASS` with a summary only if all findings are resolved.
- Return `FAIL` with the remaining findings and concrete next actions otherwise.

## Next

The runner checks package integration and confirms that the source contract is unchanged.
