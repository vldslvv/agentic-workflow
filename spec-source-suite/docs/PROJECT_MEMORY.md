# Shared project memory

Curated notes are advice for later tasks, subordinate to current instructions, specifications and repository facts. This workflow needs no supervisor: the agent completing a task maintains the selected project's notes. Existing app planning/review responsibilities remain unchanged.

## Store and format

Use `<project-root>/.agents/memory/index.md` and `entries/<short-descriptive-name>.md`, outside the reusable suite and tracked in Git. Resolve the selected project root from its execution inventory or declared scope; keep projects that share a repository separately scoped. A missing memory directory means there are no notes yet. Initialize it only when saving the first useful lesson.

The index has one link and retrieval hint per entry:

```markdown
# Project memory

- [Short title](entries/short-name.md) — Read when <situation>.
```

Entries use lowercase hyphenated filenames and this format:

```markdown
# Short title

- Kind: navigation
- Use when: <Situation where this helps>
- Source: <Relevant file, decision, or evidence>
- Last checked: YYYY-MM-DD

<What was learned and how to use it. Keep it short.>
```

Allowed kinds: `navigation`, `command`, `pitfall`, `decision`. Save non-obvious navigation, command prerequisites, verified pitfalls and pointers to authoritative decisions. Exclude transcripts, task progress, speculation, secrets and copies of routine configuration. Source paths are project-relative unless explicitly qualified; they are provenance, not instructions to retrieve history. Dates record the last actual source check, with no automatic expiry.

## Starting and retaining inputs

1. The planner (including an agent planning its own task) reads only the selected project's index, then entries relevant to the current task. Fresh work may consult these curated notes without searching past tasks or following provenance into unrelated records. Check current authorized sources when advice could be stale or conflicts with facts.
2. Before freezing handoffs, copy the index used for selection and each used entry into the task's `memory-inputs/` directory alongside its existing records. Retain the original bytes as ordinary files, never symlinks or hard links. Record original project-relative paths and full-file digests. Only selected entries need copies; the retained index records selection context and is not a standalone memory library.
3. Give ordinary implementers the selected copies through existing role-manifest `reads`, with `category: project-memory` and their retained-file digests. Include the selecting planner's copies in its recorded inputs as well. Frozen input identities refer to these copies, so later live-note maintenance cannot invalidate the task. Use retained copies on resume; a deliberate change to selected advice requires a new handoff revision.

## Completing and maintaining

In ordinary contexts, at completion, including failure or a blocked stop, the completing agent considers supported reusable lessons. Add useful lessons, merge duplicates, and correct or remove outdated advice based on current evidence. Failed checks may support a narrow observed pitfall; an unverified diagnosis does not. Update the index with additions/removals and `Last checked` when checking a note. No useful lesson or correction means no write; do not initialize an empty library or backfill historical tasks.

Declare live note maintenance in `memory_write_paths` separately from candidate `owned_paths` and protected inputs. Scope this declaration to the selected project's `.agents/memory/`; keep it disjoint from candidate paths, retained copies, frozen inputs and forbidden paths. Memory edits are maintenance, not app candidate changes. Validate the resulting memory with the [memory helper](HELPERS.md#project-memory) and retain its result with task evidence. It checks structure, not whether the advice is true. Preserve previous task copies unchanged.

## Excluded contexts

Independent reviewers and every regeneration context receive neither live project memory nor retained copies and skip memory selection and maintenance. Reviewer manifests reject recognized memory paths and `project-memory` categories. Explicitly list live roots, retained `memory-inputs/` directories and any renamed copies in `forbidden_paths`; regeneration manifests must declare these exclusions for every worker role. Keep memory out of exports, prompts, metadata and inherited conversations. An agent that has read excluded memory cannot become a clean regeneration worker by omitting it from a later manifest; start a fresh allowed-input context.

The [role-context helper](HELPERS.md#role-context) checks declared paths, including symlink aliases, for all roles. These checks are procedural validation, not filesystem isolation or detection of unlabeled copied prose. Apply the existing regeneration isolation policy when stronger controls are required.
