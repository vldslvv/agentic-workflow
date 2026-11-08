#!/usr/bin/env python3
"""Review workflow documents once and automatically attempt one repair when needed."""

import json
from pathlib import Path
import shutil
import sys

import document_review
import runtime


PROMPT = """Review whether the other project Markdown files follow
agentic-workflow/WORKFLOW.md, the source of truth. Check for inconsistencies,
overlapping or conflicting requirements, and missing or redundant instructions.
Use agentic-workflow/guides/WORKFLOW_REVIEW.md for one read-only review pass.
Return the findings as JSON matching the supplied schema.
"""

REPAIR_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["FIXED", "UNCLEAR"]},
        "summary": {"type": "string"},
    },
    "required": ["status", "summary"],
    "additionalProperties": False,
}


def get_prompt(review):
    """Preserve current candidate files without copying project execution history."""
    root, destination = review.root, review.results / "inputs"
    shutil.copytree(root / "agentic-workflow", destination / "agentic-workflow",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for relative in ("AGENTS.md", ".agentic-workflow/config/MODELS.md"):
        source = root / relative
        if source.is_file():
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    for source in (root / ".agents/skills").glob("agentic-workflow-*"):
        shutil.copytree(source, destination / ".agents/skills" / source.name)

    return PROMPT


def needs_repair(result):
    if any(row["status"] == "UNCLEAR" for row in result.get("checks", [])):
        result.update(status="UNCLEAR", note="Review contains uncertainty; no repairs attempted.")
        return False
    return result.get("review_status") == "FAIL"


def do_repair(review):
    root, results = review.root, review.results
    timeout, settings, result = review.timeout, review.settings, review.result
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
    runtime.write_json(evidence / "schema.json", REPAIR_SCHEMA)
    (evidence / "prompt.txt").write_text(prompt)
    command = document_review.agent_command(settings, "workspace-write", evidence / "schema.json",
                            evidence / "output.json", prompt)
    attempt = {"requested_settings": settings, "observed_settings": None}
    result["repair"] = attempt
    runtime.write_json(evidence / "run.json", {
        **attempt, "source_root": str(root), "candidate_root": str(candidate),
        "timeout_seconds": timeout, "command": command,
    })
    print(f"Launching one Planner repair ({settings['model']}, {settings['reasoning']}); "
          "editing working files directly", flush=True)
    attempt["attempted"] = True
    agent = runtime.execute(command, root, timeout, evidence / "events.jsonl", evidence / "agent.stderr")
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
    checks = runtime.execute(
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


def main():
    parser = document_review.argument_parser(__doc__)
    parser.epilog = ("Repairs edit working Markdown files directly; partial edits may remain. "
                     "FIXED means mechanical checks passed without independent re-review.")
    with document_review.session("workflow", parser.parse_args(), repair=True) as review:
        prompt = get_prompt(review)
        document_review.evaluate(review, prompt)
        if needs_repair(review.result):
            do_repair(review)
    return document_review.exit_code(review.result)


if __name__ == "__main__":
    sys.exit(main())
