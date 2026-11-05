# External conventions and scope of claims

Checked on 2026-11-05.

The workflow, acceptance requirements, and templates in this package are proposed design decisions for this suite. They are not represented as an industry standard or as empirically proven to guarantee regeneration.

Only the Codex integration conventions below rely on external product documentation.

## Codex skills

Official documentation: `https://developers.openai.com/codex/skills/` (redirects to `https://learn.chatgpt.com/docs/build-skills`).

The documentation describes skills as folders containing `SKILL.md` with name/description metadata. It documents repository-local `.agents/skills/`, explicit `$skill-name` invocation, and optional `agents/openai.yaml` invocation policy. This package uses instruction-only skills and explicitly disables implicit invocation in their optional metadata.

## Repository instructions

Official documentation: `https://developers.openai.com/codex/guides/agents-md/` (redirects to `https://learn.chatgpt.com/docs/agent-configuration/agents-md`).

This documents repository instructions through `AGENTS.md`. The package supplies a root instruction file to be merged deliberately when adopted in an existing repository.

## Integration limitations

No installed Codex runtime, worker launch command, model, or sandbox capability was exercised when preparing these documents. Check the actual installed tool's help and official documentation when implementing an adapter. The suite does not rely on a specific model name or undocumented CLI flag.

Earlier research claims from the conversation are not carried into these files as verified empirical evidence. The documents stand as a proposed, testable engineering design.
