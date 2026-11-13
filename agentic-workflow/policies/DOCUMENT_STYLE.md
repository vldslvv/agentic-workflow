# Document style

Apply when writing or editing project documents, including workflow documentation.
Source code, code comments and docstrings are outside this policy's scope.

## Guidelines

- Open with a self-contained purpose statement without document references.
- Describe workflows in this order: Context → Inputs → Effects → Outputs → Next.
- Omit Next when unnecessary.
- Define reusable handoff types in `contracts/` with purpose, fields, presence conditions and meanings.
- Declare each handoff with one input type and one output type in a Contracts section.
- Reference data contracts from consuming procedures while keeping effects and decisions in those procedures.
- Use artifact paths rather than copied contents in contract fields.
- Format guideline sections with a short heading, an applicability sentence and flat imperative bullets.
- Write one short, single-sentence rule per list item.
- Keep related details together when the rule remains short.
- Use bullets for rules and numbered lists only for action sequences.
- Separate procedural sections from guideline sections.
- Cite each shared policy rule by its authoritative document name except in policies and the self-contained workflow contract.

## Reference format

- Put `References:` after the opening purpose and before other sections when references exist.
- List each document once as `- [DOC]: One-sentence description. path`, using a project-root-relative path or an external URL.
- Use unique uppercase `[DOC]` markers in prose, retaining section names and read conditions at the point of use.
