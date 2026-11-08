"""Command, judgment and evidence for a single read-only document review."""

import argparse
from contextlib import contextmanager
from dataclasses import dataclass, field
import json
from pathlib import Path
import signal
import sys
import tempfile

import runtime


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


def agent_command(settings, sandbox, schema, output, prompt):
    command = ["codex", "exec", "--json", "--color", "never", "--sandbox", sandbox,
               "--skip-git-repo-check", "--disable", "multi_agent", "--disable", "memories",
               "-c", 'approval_policy="never"', "-c", "project_doc_max_bytes=0",
               "-c", "memories.use_memories=false", "-c", "memories.generate_memories=false",
               "--output-schema", str(schema), "--output-last-message", str(output),
               "--model", settings["model"],
               "-c", f'model_reasoning_effort={json.dumps(settings["reasoning"])}']
    return command + [prompt]


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
    return judgment


def render(judgment, title="Workflow"):
    def cell(value):
        return value.replace("|", "\\|").replace("\n", "<br>")

    lines = [f"# {title} review: {judgment['status']}", "", judgment["scope"], "",
             "Excluded or unreadable inputs:", ""]
    lines.extend(f"- {item}" for item in judgment["excluded_inputs"] or ["None reported."])
    lines += ["", "| Step/contract | Status | Evidence or finding |", "|---|---|---|"]
    lines.extend("| " + " | ".join(cell(row[key]) for key in ("contract", "status", "evidence")) + " |"
                 for row in judgment["checks"])
    lines += ["", "One LLM judge pass. Advisory document agreement, not proof of agent behavior.", ""]
    return "\n".join(lines)


@dataclass
class Review:
    root: Path
    results: Path
    title: str
    timeout: float
    settings: dict
    result: dict
    inputs: dict = field(default_factory=dict)


@contextmanager
def session(name, args, repair=False):
    """Own evidence, error handling and final reporting around an eval workflow."""
    root = Path.cwd().resolve()
    reports = root / ".agentic-workflow/evals" / name
    reports.mkdir(parents=True, exist_ok=True)
    results = Path(tempfile.mkdtemp(prefix="review-", dir=reports))
    title = "Specification" if name == "specs" else "Workflow"
    settings = {"model": args.model, "reasoning": args.reasoning}
    result = {"status": "RUNNER_ERROR", "max_passes": 1,
              "requested_settings": settings, "observed_settings": None}
    if repair:
        result["max_repair_attempts"] = 1
    print(f"{title} review evidence: {results}", flush=True)
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, runtime.interrupt)
    review = Review(root, results, title, args.timeout, settings, result)
    try:
        yield review
    except runtime.Interrupted as exc:
        result.update(status="INTERRUPTED", signal=exc.signum)
    except (OSError, ValueError, runtime.RunnerError) as exc:
        result.update(status="RUNNER_ERROR", error=str(exc))
        print(f"RUNNER_ERROR: {exc}", file=sys.stderr)
    if result.get("repair", {}).get("attempted") and result["status"] != "FIXED":
        result["partial_edits_may_remain"] = True
        print("Repair did not complete successfully; partial edits may remain. No changes were rolled back.", flush=True)
    runtime.write_json(results / "result.json", result)
    if "note" in result:
        print(result["note"], flush=True)
    print(f"{title} review: {result['status']}; evidence: {results}", flush=True)


def evaluate(review, prompt):
    root, results = review.root, review.results
    timeout, settings, result = review.timeout, review.settings, review.result
    if "bundles" in review.inputs:
        result["bundles"] = review.inputs["bundles"]
    candidate = results / "inputs"
    runtime.write_json(results / "schema.json", SCHEMA)
    (results / "prompt.txt").write_text(prompt)
    command = agent_command(settings, "read-only", results / "schema.json", results / "judgment.json", prompt)
    runtime.write_json(results / "run.json", {
        **result, "source_root": str(root), "candidate_root": str(candidate),
        "timeout_seconds": timeout, "command": command,
    })
    print(f"Launching one Reviewer pass ({settings['model']}, {settings['reasoning']})", flush=True)
    agent = runtime.execute(command, candidate, timeout, results / "events.jsonl", results / "agent.stderr")
    result["agent"] = agent
    if agent["status"] != "PASS":
        result.update(status="JUDGE_ERROR" if agent["status"] == "FAIL" else agent["status"],
                      signal=agent.get("signal"))
        return
    judgment = read_judgment(results / "judgment.json")
    judgment["excluded_inputs"].extend(review.inputs.get("excluded_inputs", []))
    judgment["checks"].extend(review.inputs.get("checks", []))
    judgment["status"] = aggregate_status(judgment["checks"])
    result.update(judgment)
    result["review_status"] = judgment["status"]
    report = render(judgment, review.title)
    (results / "report.md").write_text(report)
    print(report)


def aggregate_status(checks):
    statuses = {row["status"] for row in checks}
    return next(status for status in ("FAIL", "UNCLEAR", "PASS") if status in statuses)


def exit_code(result):
    if result["status"] == "INTERRUPTED":
        return 128 + result["signal"]
    return {"PASS": 0, "FIXED": 0, "FAIL": 1, "UNCLEAR": 1, "TIMEOUT": 124}.get(result["status"], 2)


def argument_parser(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--timeout", type=runtime.positive_seconds, default=1800,
                        help="Seconds per model invocation or check (default: 1800)")
    parser.add_argument("--model", default="gpt-6-astra")
    parser.add_argument("--reasoning", default="medium")
    return parser
