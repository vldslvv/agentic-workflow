# Shared suite contract

Version: 0.3-draft. Normative for every role. This procedure requires no scheduler. Role steps live in [Define](DEFINE.md), [Implement](IMPLEMENT.md), [Generate](GENERATE.md), and the [reviewer prompt](../prompts/REVIEWER.md); read only your role plus triggered branches.

## 1. Authority and readiness

The app's approved [Markdown bundle](MARKDOWN_BUNDLES.md) and normative references define behavior; derived acceptance maps source clauses to stable requirement IDs. Plans cannot override either. Keep app inputs, candidates, and evidence outside the suite. No intent yields NO_PROJECT; unavailable mandatory inputs yield BLOCKED.

A request to implement an identified bundle authorizes its baseline, derived plan/acceptance, check preparation, and implementation. Record this authority and digests; do not claim separate user review of derived text or request routine approval. Choose simple defaults for unspecified details. Material conflicts or changes to explicit requirements require a decision. Approved sources and handoffs are immutable except under explicit authority, including §4's delegated additive-verifier policy. The planner follows [planning records](PLANNING.md) for persistence and document approval.

Before implementation require source-linked approved acceptance, complete plan, baseline/authority identities, target, retained inputs, authorized paths, frozen checks, and current accepted dependency evidence. Integrity checks hash protected files without rereading their contents into context. Unauthorized writes invalidate the attempt; preserve the incident and resolve through the supervisor before restarting.

## 2. Roles and context

The **supervisor also owns planning**: prepare each ready task through Define in the supervisor's existing context, then dispatch a fresh implementer and independent review. Retain source requirements, acceptance decisions, interfaces and accepted dependency contracts across tasks. Planner is a responsibility, not a required separate agent. If planning is explicitly delegated, the supervisor reads and validates the complete plan/acceptance before dispatch. Keep the implementer's context through repairs; if replaced, resume from durable records and current findings.

Handoffs list exact read paths/sections, identities, owned paths, excluded inputs, dependencies, and evidence destinations. Read unchanged material once per session. Additional relevant inspection is allowed and recorded. Mandatory source access and execution remain required. The [helper interface](HELPERS.md) validates manifests; it does not dispatch workers.

For selecting, retaining or maintaining curated notes, follow [project memory](PROJECT_MEMORY.md). Independent reviewers and regeneration contexts exclude those notes; ordinary handoffs retain selected copies and declare live memory maintenance separately from candidate/protected paths.

The implementer MUST spawn a fresh reviewer without inherited conversation (`fork_turns="none"` where supported). Reviewer inputs exclude plans and planner/implementer conversations, including historical narratives and persuasive summaries. Supply acceptance, normative sources, candidate/check identities, dependency evidence and raw results. Missing fresh-context capability is INDEPENDENT_REVIEW_NOT_RUN and blocks acceptance. A fresh context does not guarantee independent reasoning.

Return compact [receipts](../templates/RECEIPT.json): status, requirement IDs, candidate/check identities, evidence paths and actionable findings. The supervisor checks readiness and acceptance from evidence, opening raw logs for failures or disputed evidence. Use completion/blocker messages and supported waits instead of repeated status inquiries/report rereads. Maintain required user progress updates.

## 3. Graph, ownership and execution

The supervisor validates unique task IDs, source order plus explicit prerequisites, mappings, unknown references and cycles using the bundle standard. A task is ready only when all prerequisites are accepted at current identities. FAIL, BLOCKED, NOT_RUN, stubs and unreviewed candidates never unlock consumers. Scope controls cannot bypass prerequisites; an empty selection is NO_WORK, not acceptance. Run serially unless contract-first parallel work is explicitly authorized with approved contracts and coordinated ownership; real-dependency integration remains mandatory.

Default isolation is procedural: planner owns acceptance/frozen inputs, implementer owns candidate/local logs, reviewer owns independent results. Declare shared integration paths. Compare protected digests and inspect out-of-scope diffs before/after implementation, repair and review. Digest checking detects changes; it is not a sandbox. Read [strong isolation](STRONG_ISOLATION.md) only when enforcement is required, and [regeneration](REGENERATION.md) only for reconstruction/target changes.

## 4. Checks and repairs

The planner freezes requirement-linked checks/fixtures/adapters and normative inputs before implementation. Declare task checks, regression sets and final assembled-app scenarios separately. Include setup, inputs, assertions, cleanup, pass rules, evidence, manual authorities and fixed sampling/thresholds where applicable. Missing mandatory checks block readiness. Hidden cases may test only disclosed requirements. Implementers may add local tests, but cannot edit frozen expectations or reviewer results.

Continue confirmed implementation-defect repairs **until accepted**. Stop for cancellation, an applicable user/platform budget limit, unavailable infrastructure, or a specification conflict requiring a decision. Preserve attempt numbers (initial = 0), candidate snapshots/digests, failures and findings across sessions; no reset on resume. Every changed candidate runs affected checks and its declared regression set and receives a **new fresh reviewer**. Reuse unchanged evidence only with a recorded scope/identity justification. Avoid duplicate executions within a role; independent review and final end-to-end execution remain separate mandatory gates.

For a reviewer-discovered coverage gap: reviewer preserves finding plus executable reproduction; planner confirms it tests an existing requirement; supervisor may authorize an **additive verifier revision** under this delegated policy. Retain the original inventory/checks unchanged, freeze the new revision and execute it against the candidate before acceptance. Requirements, weakened expectations or verifier corrections beyond additive coverage need explicit authorization. A baseline revision invalidates affected evidence without erasing prior attempts.

Route ambiguity/conflicts to SPEC_CONFLICT/BLOCKED; suspected verifier defects immediately to the supervisor with preserved failure; significant plan deviations to the supervisor for resolution. Missing services/tools and infrastructure timeouts are INFRA_ERROR/BLOCKED. A timeout asserting a declared behavioral deadline is FAIL. Budget/cancellation stops preserve partial evidence and unexecuted gates. Target incompatibility requires an explicit decision; never silently downgrade behavior.

## 5. Acceptance and durable evidence

Record PASS, FAIL, BLOCKED or NOT_RUN for each mandatory requirement and gate. FAIL is an observed mismatch; BLOCKED an unmet precondition; NOT_RUN no assessment. Distinguish **check execution, coverage assessment, and review outcome**. A command pass, empty coverage or zero executed mandatory checks cannot establish acceptance. Manual judgments name authority and inspected artifact.

The supervisor accepts only with prescribed checks, adequate requirement coverage, independent review, applicable real-dependency integration/manual gates, and intact baseline for the actual candidate. Independent review must report zero unresolved actionable findings. Severity sets repair priority; every actionable finding requires resolution before review PASS or task acceptance. After all selected nodes pass, final checks on the assembled app (including cross-task interactions) are mandatory. Changed accepted nodes invalidate affected downstream/final evidence. Partial scope names its boundary and retained dependencies.

Use one external evidence root and [run report](../templates/RUN_REPORT.md). Retain baseline/approval/spec/check/input identities; dependency/target/suite/prompt revisions; ownership/isolation; environment/cache differences; agent/session/read lists; timestamps/resource limits; every attempt, command, exit, observation, finding, intervention and next action. Keep executable builds in temporary/build directories and preserve source snapshots for uncommitted candidate identities. Logs remain detailed on disk; receipts stay compact.

Resume only when all relevant inputs, dependencies, candidates and evidence exist at recorded identities; changed or missing artifacts invalidate affected gates. Report first-attempt versus eventual results separately, actual isolation, limitations and unmet gates. Procedural fixtures do not demonstrate actual app generation. [Usage reporting](HELPERS.md#usage-reporting) records unavailable counters explicitly and keeps outer-driver overhead separate.
