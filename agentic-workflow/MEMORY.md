# Project memory

- Ordinary planners and implementers read `<project-root>/.agents/memory/index.md`, then only relevant `entries/*.md`. A missing index means no notes yet.
- Treat memory as advice: requirements and current repository facts outrank it. Verify stale advice without searching unrelated task or conversation history.
- At completion or a blocked stop, save supported useful lessons with source pointers. Merge duplicates and correct stale advice; initialize memory only for a useful lesson.
- Use short retrieval hints and ordinary Markdown; no metadata schema is required. Omit transcripts, progress logs, speculation, secrets and copied configuration.
- Pass relevant paths to later ordinary workers. Supervisors relay paths without loading detailed notes.
- Reviewers, validators and every reconstruction worker exclude memory and its copies.
