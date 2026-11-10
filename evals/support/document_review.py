"""Shared model transport, review judgments, and saved document-review evidence."""

import argparse
import json
import shutil
import signal
import sys
import tempfile
from pathlib import Path
from textwrap import indent
from typing import Literal, cast

from . import runtime
from .models import DocumentResult, Execution, Inputs, Judgment, Review, ReviewSettings

ASSETS = Path(__file__).resolve().parents[1]


def prepare_run(root: Path, name: str) -> Path:
    """Allocate evidence before input preparation so preparation errors are saved."""
    reports = root / ".agentic-workflow/evals" / name
    reports.mkdir(parents=True, exist_ok=True)
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, runtime.interrupt)
    results = Path(tempfile.mkdtemp(prefix="review-", dir=reports))
    print(f"{name.capitalize()} eval evidence: {results}", flush=True)
    return results


def load_prompt(name: str, **values: object) -> str:
    return (ASSETS / "prompts" / name).read_text().format(**values)


def invoke_model(
    root: Path,
    results: Path,
    cwd: Path,
    prompt: str,
    schema: str,
    output: str,
    args: ReviewSettings,
    sandbox: str,
) -> Execution:
    """Save the exact prompt/schema, pass prompt as one argv item, and run once."""
    results.mkdir(parents=True, exist_ok=True)
    (results / "prompt.txt").write_text(prompt)
    shutil.copyfile(ASSETS / "schemas" / schema, results / "schema.json")
    command = [
        "codex",
        "exec",
        "--json",
        "--color",
        "never",
        "--sandbox",
        sandbox,
        "--skip-git-repo-check",
        "--disable",
        "multi_agent",
        "--disable",
        "memories",
        "-c",
        'approval_policy="never"',
        "-c",
        "project_doc_max_bytes=0",
        "-c",
        "memories.use_memories=false",
        "-c",
        "memories.generate_memories=false",
        "--output-schema",
        str(results / "schema.json"),
        "--output-last-message",
        str(results / output),
        "--model",
        args.model,
        "-c",
        f"model_reasoning_effort={json.dumps(args.reasoning)}",
        prompt,
    ]
    runtime.write_json(
        results / "run.json",
        {
            "source_root": str(root),
            "cwd": str(cwd),
            "command": command,
            "requested_settings": {"model": args.model, "reasoning": args.reasoning},
            "observed_settings": None,
            "timeout_seconds": args.timeout,
            "prompt_file": "prompt.txt",
            "schema_file": "schema.json",
            "output_file": output,
        },
    )
    print(f"Launching {sandbox} model invocation in {cwd}; evidence: {results}", flush=True)
    return runtime.execute(
        command, cwd, args.timeout, results / "events.jsonl", results / "agent.stderr"
    )


def read_judgment(path: Path) -> Judgment:
    judgment = json.loads(path.read_text())
    if (
        not isinstance(judgment, dict)
        or not isinstance(judgment.get("scope"), str)
        or not judgment["scope"].strip()
        or not isinstance(judgment.get("excluded_inputs"), list)
        or not all(isinstance(item, str) for item in judgment["excluded_inputs"])
        or not isinstance(judgment.get("checks"), list)
        or not judgment["checks"]
    ):
        raise ValueError("Judge response must include scope, excluded_inputs and nonempty checks")
    for row in judgment["checks"]:
        if (
            not isinstance(row, dict)
            or any(
                not isinstance(row.get(key), str) or not row[key].strip()
                for key in ("contract", "status", "evidence")
            )
            or row["status"] not in ("PASS", "FAIL")
        ):
            raise ValueError(
                "Invalid judge check: expected contract, PASS/FAIL status and evidence"
            )
    return cast(Judgment, judgment)


def render(result: DocumentResult, title: str) -> str:
    review = result["review"]
    lines = [
        f"# {title} eval: {result['status']}",
        "",
        f"Reviewer execution: {result['execution']['status']}",
        "",
        f"Original review: {review['status']}",
        "",
    ]
    if "scope" in review:
        lines += [review["scope"], "", "Excluded or unreadable inputs:", ""]
        lines.extend(f"- {item}" for item in review["excluded_inputs"] or ["None reported."])
        lines += ["", "Findings:", ""]
        for row in review["checks"]:
            contract = row["contract"].replace("\n", "\n  ")
            lines += [f"- [{row['status']}] {contract}", indent(row["evidence"], "  "), ""]
    if "repair" in result:
        repair = result["repair"]
        lines += ["", f"Repair: {repair['status']}", ""]
        if "response" in repair:
            lines += [repair["response"]["summary"], ""]
        if "checks" in repair:
            lines += [
                f"Package checks: {repair['checks']['status']}",
                "",
                f"Source contract unchanged: {repair['source_contract_unchanged']}",
                "",
            ]
        lines.extend(repair[key] for key in ("reason", "note", "error") if key in repair)
    lines.extend(result[key] for key in ("note", "error") if key in result)
    lines += [
        "",
        "One LLM judge pass. Advisory document agreement, not proof of agent behavior.",
        "",
    ]
    return "\n".join(lines)


def grade(results: Path, execution: Execution, inputs: Inputs) -> DocumentResult:
    """Keep process execution separate from the raw response and its grade."""
    result: DocumentResult = {
        "status": execution["status"],
        "execution": execution,
        "review": {"status": "NOT_RUN"},
    }
    if execution["status"] != "PASS":
        if execution["status"] == "FAIL":
            result["status"] = "JUDGE_ERROR"
        if "signal" in execution:
            result["signal"] = execution["signal"]
        return result
    try:
        judgment = read_judgment(results / "judgment.json")
    except (OSError, ValueError) as exc:
        return {**result, "status": "RUNNER_ERROR", "error": str(exc)}
    checks = judgment["checks"] + inputs.get("checks", [])
    status: Literal["PASS", "FAIL"] = (
        "FAIL" if any(row["status"] == "FAIL" for row in checks) else "PASS"
    )
    review: Review = {
        **judgment,
        "checks": checks,
        "status": status,
        "excluded_inputs": judgment["excluded_inputs"] + inputs.get("excluded_inputs", []),
    }
    return {**result, "status": status, "review": review}


def save(results: Path, result: DocumentResult, title: str) -> None:
    runtime.write_json(results / "result.json", result)
    report = render(result, title)
    (results / "report.md").write_text(report)
    if "error" in result:
        print(f"{result['status']}: {result['error']}", file=sys.stderr)
    print(report, end="", flush=True)
    print(f"Evidence: {results}", flush=True)


def exit_code(result: DocumentResult) -> int:
    if result["status"] == "INTERRUPTED":
        return 128 + result["signal"]
    return {"PASS": 0, "FAIL": 1, "TIMEOUT": 124}.get(result["status"], 2)


def argument_parser(description: str | None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--timeout",
        type=runtime.positive_seconds,
        default=1800,
        help="Seconds per model invocation or check (default: 1800)",
    )
    parser.add_argument("--model", default="gpt-6-astra")
    parser.add_argument("--reasoning", default="medium")
    return parser
