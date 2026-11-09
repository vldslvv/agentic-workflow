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
3. Leave unresolved findings for human review without committing changes.

## Outputs

- Return JSON matching the supplied repair schema.
- Return `FIXED` with a summary only if all findings are resolved.
- Return `UNCLEAR` with a summary of what remains otherwise.

## Next

The runner checks package integration and confirms that the source contract is unchanged.
