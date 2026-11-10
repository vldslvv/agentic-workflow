# Checking agent instructions for consistency

The goal is to provide agents with consistent, clear and jointly satisfiable
instructions. This is an author-controlled contribution to successful work;
whether agents follow those instructions is outside this proposal's scope.

Proposal only; no checking tooling is implemented.
[WORKFLOW.md](../agentic-workflow/WORKFLOW.md) remains authoritative and self-contained.

## Key ideas

- Find instructions that require and forbid the same action under overlapping conditions.
- Find missing definitions, unclear scope, unspecified authority and unresolved exceptions.
- Check that required inputs have an authorized producer and required actions have satisfiable prerequisites.
- Check that role instructions agree with the authoritative workflow and with each other at handoffs.
- Check each intended task mode and recovery path for impossible obligations or circular dependencies.
- Review the translation into formal rules; a consistent model can still misrepresent the prose.
- Report checked scenarios, assumptions and limits rather than claiming all ambiguity has been eliminated.

## Recommended first step

Extract a source-linked rule table for implementation, review and acceptance.
Check whether applicable duties can be satisfied together in both task modes,
during writer pauses and after interruptions. Report conflicting clauses and the
conditions that activate them, then revise the instructions.

- [Alloy](https://alloytools.org/spec.html): check role permissions and artifact relationships within stated scopes.
- [TLA+/TLC](https://nightly.tlapl.us/doc/model/overview-page.html): explore whether prescribed sequencing creates deadlocks or makes required outcomes unreachable.

## Lessons from legal contracts

Normalize rules into a reviewed table:

```text
Actor | Must/May/Must not | Action/scope | Trigger
      | Deadline | Exception/priority | Authority | Source
```

Check defined terms, overlapping duties and prohibitions, missing authority,
conflicting exceptions and impossible deadlines. For example, correcting findings
must remain compatible with the prohibition on writing while review is active.
Specify when that duty becomes actionable and who can release the pause.

- [LegalRuleML](https://docs.oasis-open.org/legalruleml/legalruleml-core-spec/v1.0/legalruleml-core-spec-v1.0.html): vocabulary for obligations, permissions, prohibitions and overrides; not a verification engine.
- [Catala](https://book.catala-lang.org/en/5-4-definitions-exceptions.html): explicit exceptions and priorities for overlapping legal rules.
- [Contract Tools](https://contract-tools.helpscoutdocs.com/article/149-checking-for-drafting-errors): inspiration for defined-term and reference linting.
- [Z3](https://z3prover.github.io/papers/programmingz3): check encoded constraints and identify conflicting subsets; returned unsatisfiable cores need not be minimal.

Start with the rule table; choose a solver or temporal model for the conflicts being checked.

## Historical perspective

Instruction consistency is an established requirements-engineering problem;
these overlapping approaches predate LLMs.

| Approach | Outcome and lesson |
|---|---|
| [SCR requirements tables](https://www.jucs.org/jucs_13_5/formal_methods_for_specifying/jucs_13_5_0607_0618_heitmeyer.pdf), 1970s onward | Automated checks detect missing cases, conflicting outcomes and circular definitions before implementation. |
| [Z specifications at IBM](https://research.ibm.com/publications/use-of-software-engineering-including-the-z-notation-in-the-development-of-cics), 1980s | The CICS experience reported potential for fewer defects at little additional development cost. |
| [UML + OCL / USE](https://www.db.informatik.uni-bremen.de/projects/USE-2.3.0/), 1990s onward | Diagrams plus explicit constraints enabled model validation; diagrams alone do not establish consistency. |
| [Workflow nets](https://www.vdaalst.com/publications/p98.pdf), 1990s onward | Soundness analysis detects control-flow defects; a sound process can still express the wrong requirements. |
| [TLA+ at AWS](https://www.amazon.science/publications/how-amazon-web-services-uses-formal-methods), 2015 report | Found subtle design defects; choosing a faithful abstraction remained a learned skill. |
| [NASA FRET](https://ntrs.nasa.gov/citations/20220007510), 2022 report | Structured natural language supports realizability checking and diagnosis of conflicting requirements. |

Distinguish consistency (rules can hold together), realizability (requirements can
be met across allowed environmental inputs) and intent validation (rules express
what the author meant). For this project, SCR-style tables, FRET and workflow
soundness are close precedents. LLMs may reduce formalization effort; reviewing
and maintaining the representation remains necessary.

## State of research

Selected work as of November 2026:

- [ContractCheck](https://link.springer.com/article/10.1007/s10506-025-09456-8) (2025): translates structured legal clauses into SMT constraints to find executable scenarios or conflicts.
- [Autoformalization of Agent Instructions into Policy-as-Code](https://arxiv.org/abs/2606.26649) (2026 workshop): translates prompts and tool descriptions into Cedar policies using an LLM generator–critic loop.
- [COVENANT](https://arxiv.org/abs/2607.25400) (2026 preprint): compiles workflow instructions into graphs and checks proposed steps at runtime; evaluates compliance rather than proving prose unambiguous.
- [Requirement Formalization from Unstructured Specifications](https://arxiv.org/abs/2604.18228) (2026 workshop): extracts and translates verification properties, explicitly addressing alignment with source requirements.
- [From Informal to Formal](https://aclanthology.org/2025.acl-long.1310/) (ACL 2025): evaluates LLM formalization across five languages, including TLA+.

ContractCheck and requirement formalization are the closest matches to this goal:
prose → reviewed rules → consistency checks → instruction revisions.
COVENANT's runtime enforcement is adjacent research, outside the proposed scope.

### Frontier labs and related industrial work

- OpenAI — [IH-Challenge](https://openai.com/index/instruction-hierarchy-challenge/) (March 2026): trains and evaluates instruction precedence under conflicts; measures compliance, not policy consistency.
- OpenAI — [Deliberative alignment](https://openai.com/index/deliberative-alignment/) (December 2024): trains models to reason over written safety specifications without symbolic verification.
- Anthropic + Theorem — [Formal software verification](https://www.anthropic.com/research/formal-verification) (October 2026): generates machine-checked security proofs for production libraries, conditional on specifications and modeling assumptions.
- Microsoft Research — [PDD Kit](https://www.microsoft.com/en-us/research/blog/formally-verifying-agent-written-full-stack-web-apps-with-pdd-kit/) (November 2026): translates reviewed intent into Verus specifications and separates proofs from empirical tests.
- AWS — [Automated Reasoning checks](https://docs.aws.amazon.com/bedrock/latest/userguide/automated-reasoning-checks-concepts.html): deployed tooling that translates policy documents into formal rules, with source-linked fidelity reports for reviewing the translation.

These projects mainly address compliance or implementation correctness, rather
than instruction consistency. Transferable ideas are reviewed formalization,
source-to-rule traceability and explicit assumptions; agent training and runtime
enforcement remain outside this proposal.
