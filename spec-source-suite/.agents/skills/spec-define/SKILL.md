---
name: spec-define
description: Define, import, review, or revise project specifications that also serve as acceptance documents. Use for explicit specification work; do not invent an application or implement project code.
---

# Define project specifications

Read the repository `AGENTS.md`, [shared contract](../../../docs/SUITE_CONTRACT.md), and [Define workflow](../../../docs/DEFINE.md).

## Inputs

Use the user's project intent, supplied specs, or explicitly authorized existing-system observations. With no project material, prepare the blank templates or explain what input is needed. Do not choose a demonstration application.

## Procedure

1. Establish scope, observation boundary, authority, and preservation target. Distinguish user requirements from proposals and observations.
2. Select acceptance-sized capabilities. Assign stable IDs and canonical dependency declarations; derive a DAG rather than inventing an arbitrary serial order.
3. Write each spec as its acceptance document using [SPEC.md](../../../templates/SPEC.md). Use prose, scenarios, schemas, models, or properties only as needed.
4. Map mandatory requirements to concrete verification rules with [VERIFICATION.md](../../../templates/VERIFICATION.md). Define tolerances and nondeterminism before evaluating outputs.
5. Review ambiguity, contradictions, failure/interaction behavior, references, and required retained inputs. Preserve unresolved normative questions.
6. Obtain approval from the designated authority for exact content, or leave the result proposed. An agent-written approved status is not authority.
7. Register the documents in a project manifest. For changes, produce a change proposal and affected-evidence analysis.

## Outputs

Produce reviewed specs, acceptance mapping, manifest/DAG, approval references or open issues, and readiness status. Do not generate implementation code in this skill. State NO_PROJECT or BLOCKED rather than filling missing requirements yourself.
