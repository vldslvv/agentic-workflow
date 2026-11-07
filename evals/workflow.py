#!/usr/bin/env python3
"""One LLM judgment of workflow documents against the fixed workflow contract."""

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


def run(root, timeout):
    reports = root / ".evals/workflow"
    reports.mkdir(parents=True, exist_ok=True)
    results = Path(tempfile.mkdtemp(prefix="review-", dir=reports))
    print(f"Workflow review evidence: {results}", flush=True)
    result = {"status": "RUNNER_ERROR", "max_passes": 1}
    code = 2
    try:
        candidate = results / "inputs"
        copy_inputs(root, candidate)
        override = Path(".agentic-workflow/MODELS.md")
        routing = override if (candidate / override).exists() else Path("agentic-workflow/policies/MODELS.md")
        settings = todolist.role_settings(candidate / routing, "Reviewer")
        todolist.write_json(results / "schema.json", SCHEMA)
        (results / "prompt.txt").write_text(PROMPT)
        command = ["codex", "exec", "--json", "--color", "never", "--sandbox", "read-only",
                   "--skip-git-repo-check", "--disable", "multi_agent", "--disable", "memories",
                   "-c", 'approval_policy="never"', "-c", "project_doc_max_bytes=0",
                   "-c", "memories.use_memories=false", "-c", "memories.generate_memories=false",
                   "--output-schema", str(results / "schema.json"),
                   "--output-last-message", str(results / "judgment.json")]
        if settings["model"] != "default":
            command += ["--model", settings["model"]]
        if settings["reasoning"] != "default":
            command += ["-c", f'model_reasoning_effort={json.dumps(settings["reasoning"])}']
        command.append(PROMPT)
        result.update(routing_source=str(routing), routing_reason="Reviewer default for document review",
                      requested_settings=settings, observed_settings=None)
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
            report = render(judgment)
            (results / "report.md").write_text(report)
            print(report)
            code = 0 if result["status"] == "PASS" else 1
        else:
            result["status"] = "JUDGE_ERROR" if agent["status"] == "FAIL" else agent["status"]
            if agent["status"] == "TIMEOUT":
                code = 124
            elif agent["status"] == "INTERRUPTED":
                code = 128 + agent["signal"]
    except todolist.Interrupted as exc:
        result.update(status="INTERRUPTED", signal=exc.signum)
        code = 128 + exc.signum
    except (OSError, ValueError, todolist.RunnerError) as exc:
        result.update(status="RUNNER_ERROR", error=str(exc))
        print(f"RUNNER_ERROR: {exc}", file=sys.stderr)
    todolist.write_json(results / "result.json", result)
    print(f"Workflow review: {result['status']}; evidence: {results}", flush=True)
    return code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=todolist.positive_seconds, default=1800)
    args = parser.parse_args()
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, todolist.interrupt)
    return run(Path.cwd().resolve(), args.timeout)


if __name__ == "__main__":
    sys.exit(main())
