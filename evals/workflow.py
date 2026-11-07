#!/usr/bin/env python3
"""Review workflow documents once and automatically attempt one repair when needed."""

import argparse
import json
from pathlib import Path
import shutil
import signal
import sys
import tempfile

import todolist


PROMPT = """Review whether the other project Markdown files follow
agentic-workflow/WORKFLOW.md, the source of truth. Check for inconsistencies,
overlapping or conflicting requirements, and missing or redundant instructions.
Use agentic-workflow/guides/WORKFLOW_REVIEW.md for one read-only review pass.
Return the findings as JSON matching the supplied schema.
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "scope": {"type": "string"},
        "excluded_inputs": {"type": "array", "items": {"type": "string"}},
        "checks": {
            "type": "array", "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "contract": {"type": "string"},
                    "status": {"type": "string", "enum": ["PASS", "FAIL", "UNCLEAR"]},
                    "evidence": {"type": "string"},
                },
                "required": ["contract", "status", "evidence"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["scope", "excluded_inputs", "checks"],
    "additionalProperties": False,
}

REPAIR_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["FIXED", "UNCLEAR"]},
        "summary": {"type": "string"},
    },
    "required": ["status", "summary"],
    "additionalProperties": False,
}


def agent_command(settings, sandbox, schema, output, prompt):
    command = ["codex", "exec", "--json", "--color", "never", "--sandbox", sandbox,
               "--skip-git-repo-check", "--disable", "multi_agent", "--disable", "memories",
               "-c", 'approval_policy="never"', "-c", "project_doc_max_bytes=0",
               "-c", "memories.use_memories=false", "-c", "memories.generate_memories=false",
               "--output-schema", str(schema), "--output-last-message", str(output),
               "--model", settings["model"],
               "-c", f'model_reasoning_effort={json.dumps(settings["reasoning"])}']
    return command + [prompt]


def copy_inputs(root, destination):
    """Preserve current candidate files without copying project execution history."""
    shutil.copytree(root / "agentic-workflow", destination / "agentic-workflow",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for relative in ("AGENTS.md", ".agentic-workflow/MODELS.md"):
        source = root / relative
        if source.is_file():
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    for source in (root / ".agents/skills").glob("agentic-workflow-*"):
        shutil.copytree(source, destination / ".agents/skills" / source.name)


def read_judgment(path):
    judgment = json.loads(path.read_text())
    if (not isinstance(judgment, dict)
            or not isinstance(judgment.get("scope"), str) or not judgment["scope"].strip()
            or not isinstance(judgment.get("excluded_inputs"), list)
            or not all(isinstance(item, str) for item in judgment["excluded_inputs"])
            or not isinstance(judgment.get("checks"), list) or not judgment["checks"]):
        raise ValueError("Judge response must include scope, excluded_inputs and nonempty checks")
    for row in judgment["checks"]:
        if (not isinstance(row, dict)
                or any(not isinstance(row.get(key), str) or not row[key].strip()
                       for key in ("contract", "status", "evidence"))
                or row["status"] not in ("PASS", "FAIL", "UNCLEAR")):
            raise ValueError("Invalid judge check: expected contract, status and evidence")
    statuses = {row["status"] for row in judgment["checks"]}
    judgment["status"] = next(status for status in ("FAIL", "UNCLEAR", "PASS") if status in statuses)
    return judgment


def render(judgment):
    def cell(value):
        return value.replace("|", "\\|").replace("\n", "<br>")

    lines = [f"# Workflow review: {judgment['status']}", "", judgment["scope"], "",
             "Excluded or unreadable inputs:", ""]
    lines.extend(f"- {item}" for item in judgment["excluded_inputs"] or ["None reported."])
    lines += ["", "| Step/contract | Status | Evidence or finding |", "|---|---|---|"]
    lines.extend("| " + " | ".join(cell(row[key]) for key in ("contract", "status", "evidence")) + " |"
                 for row in judgment["checks"])
    lines += ["", "One LLM judge pass. Advisory document agreement, not proof of agent behavior.", ""]
    return "\n".join(lines)


def repair(root, results, timeout, settings, result):
    evidence = results / "repair"
    evidence.mkdir()
    candidate = results / "inputs"
    contract = Path("agentic-workflow/WORKFLOW.md")
    original_contract = (candidate / contract).read_bytes()
    prompt = f"""Correct the workflow review findings in {results / 'judgment.json'}.
Use the original snapshot at {candidate}. Edit working files in this project,
only Markdown files included in that snapshot and only as needed for the findings.
Preserve existing work, all evidence, and agentic-workflow/WORKFLOW.md, the source
of truth. Apply agentic-workflow/policies/DOCUMENT_STYLE.md. Do not commit or run
another LLM review. Return JSON matching the supplied schema: FIXED and a summary
only if all findings are resolved; otherwise UNCLEAR and explain what remains.
"""
    todolist.write_json(evidence / "schema.json", REPAIR_SCHEMA)
    (evidence / "prompt.txt").write_text(prompt)
    command = agent_command(settings, "workspace-write", evidence / "schema.json",
                            evidence / "output.json", prompt)
    attempt = {"requested_settings": settings, "observed_settings": None}
    result["repair"] = attempt
    todolist.write_json(evidence / "run.json", {
        **attempt, "source_root": str(root), "candidate_root": str(candidate),
        "timeout_seconds": timeout, "command": command,
    })
    print(f"Launching one Planner repair ({settings['model']}, {settings['reasoning']}); "
          "editing working files directly", flush=True)
    attempt["attempted"] = True
    agent = todolist.execute(command, root, timeout, evidence / "events.jsonl", evidence / "agent.stderr")
    attempt["agent"] = agent
    if agent["status"] != "PASS":
        result.update(status="REPAIR_ERROR" if agent["status"] == "FAIL" else agent["status"],
                      signal=agent.get("signal"))
        return
    response = json.loads((evidence / "output.json").read_text())
    if (not isinstance(response, dict) or response.get("status") not in ("FIXED", "UNCLEAR")
            or not isinstance(response.get("summary"), str) or not response["summary"].strip()):
        raise ValueError("Editor response must include FIXED or UNCLEAR and a nonempty summary")
    attempt["response"] = response
    print(f"Editor: {response['status']}: {response['summary']}", flush=True)
    checks = todolist.execute(
        [sys.executable, "-B", "agentic-workflow/helpers/check_package.py", "--integration-root", "."],
        root, timeout, evidence / "checks.stdout", evidence / "checks.stderr",
    )
    attempt["checks"] = checks
    unchanged = (root / contract).is_file() and (root / contract).read_bytes() == original_contract
    attempt["source_contract_unchanged"] = unchanged
    if not unchanged:
        result["note"] = "WORKFLOW.md changed from the original snapshot; repair cannot succeed."
    if checks["status"] != "PASS":
        result.update(status=checks["status"], signal=checks.get("signal"))
        result.setdefault("note", "Package or integration checks did not pass; see repair/checks.stdout and checks.stderr.")
    elif not unchanged:
        result["status"] = "FAIL"
    else:
        result["status"] = response["status"]
        if result["status"] == "FIXED":
            result["note"] = ("The editor reported all findings resolved and mechanical checks passed. "
                              "No independent re-review occurred.")


def run(root, timeout, settings):
    reports = root / ".evals/workflow"
    reports.mkdir(parents=True, exist_ok=True)
    results = Path(tempfile.mkdtemp(prefix="review-", dir=reports))
    print(f"Workflow review evidence: {results}", flush=True)
    result = {"status": "RUNNER_ERROR", "max_passes": 1, "max_repair_attempts": 1,
              "requested_settings": settings, "observed_settings": None}
    try:
        candidate = results / "inputs"
        copy_inputs(root, candidate)
        todolist.write_json(results / "schema.json", SCHEMA)
        (results / "prompt.txt").write_text(PROMPT)
        command = agent_command(settings, "read-only", results / "schema.json", results / "judgment.json", PROMPT)
        todolist.write_json(results / "run.json", {
            **result, "source_root": str(root), "candidate_root": str(candidate),
            "timeout_seconds": timeout, "command": command,
        })
        print(f"Launching one Reviewer pass ({settings['model']}, {settings['reasoning']})", flush=True)
        agent = todolist.execute(command, candidate, timeout, results / "events.jsonl", results / "agent.stderr")
        result["agent"] = agent
        if agent["status"] == "PASS":
            judgment = read_judgment(results / "judgment.json")
            result.update(judgment)
            result["review_status"] = judgment["status"]
            report = render(judgment)
            (results / "report.md").write_text(report)
            print(report)
            if any(row["status"] == "UNCLEAR" for row in judgment["checks"]):
                result.update(status="UNCLEAR", note="Review contains uncertainty; no repairs attempted.")
            elif judgment["status"] == "FAIL":
                repair(root, results, timeout, settings, result)
        else:
            result.update(status="JUDGE_ERROR" if agent["status"] == "FAIL" else agent["status"],
                          signal=agent.get("signal"))
    except todolist.Interrupted as exc:
        result.update(status="INTERRUPTED", signal=exc.signum)
    except (OSError, ValueError, todolist.RunnerError) as exc:
        result.update(status="RUNNER_ERROR", error=str(exc))
        print(f"RUNNER_ERROR: {exc}", file=sys.stderr)
    if result.get("repair", {}).get("attempted") and result["status"] != "FIXED":
        result["partial_edits_may_remain"] = True
        print("Repair did not complete successfully; partial edits may remain. No changes were rolled back.", flush=True)
    todolist.write_json(results / "result.json", result)
    if "note" in result:
        print(result["note"], flush=True)
    print(f"Workflow review: {result['status']}; evidence: {results}", flush=True)
    if result["status"] == "INTERRUPTED":
        return 128 + result["signal"]
    return {"PASS": 0, "FIXED": 0, "FAIL": 1, "UNCLEAR": 1, "TIMEOUT": 124}.get(result["status"], 2)


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog=(
        "Repairs edit working Markdown files directly and remain uncommitted. "
        "Partial edits may remain on failure; changes are not rolled back. Avoid concurrent edits. "
        "FIXED means the editor reported resolution and mechanical checks passed; no independent re-review occurred."))
    parser.add_argument("--timeout", type=todolist.positive_seconds, default=1800,
                        help="Seconds per LLM invocation and for mechanical checks (default: 1800)")
    parser.add_argument("--model", default="gpt-6-astra",
                        help="Codex model for both review and repair (default: gpt-6-astra)")
    parser.add_argument("--reasoning", default="medium",
                        help="Reasoning effort for both review and repair (default: medium)")
    args = parser.parse_args()
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, todolist.interrupt)
    return run(Path.cwd().resolve(), args.timeout, {"model": args.model, "reasoning": args.reasoning})


if __name__ == "__main__":
    sys.exit(main())
