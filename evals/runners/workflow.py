"""Review current workflow documents; optionally attempt one repair with --repair."""

import json
from pathlib import Path
import shutil
import sys

from . import document_review
from . import runtime


def capture_inputs(root, destination):
    """Preserve current candidate files without project execution history."""
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


def repair(root, results, args):
    """Return the editor outcome separately from the original review judgment."""
    evidence = results / "repair"
    contract = Path("agentic-workflow/WORKFLOW.md")
    original_contract = (results / "inputs" / contract).read_bytes()
    prompt = document_review.load_prompt("workflow-repair.md", judgment=results / "judgment.json",
                                       snapshot=results / "inputs")
    attempt = {"status": "RUNNER_ERROR", "attempted": False}
    try:
        attempt["attempted"] = True
        execution = document_review.invoke_model(root, evidence, root, prompt,
                    "repair.json", "output.json", args, "workspace-write")
        attempt["execution"] = execution
        if execution["status"] != "PASS":
            attempt["status"] = "REPAIR_ERROR" if execution["status"] == "FAIL" else execution["status"]
            if "signal" in execution:
                attempt["signal"] = execution["signal"]
            return attempt
        response = json.loads((evidence / "output.json").read_text())
        if (not isinstance(response, dict) or response.get("status") not in ("FIXED", "UNCLEAR")
                or not isinstance(response.get("summary"), str) or not response["summary"].strip()):
            raise ValueError("Editor response must include FIXED or UNCLEAR and a nonempty summary")
        attempt["response"] = response
        checks = runtime.execute(
            [sys.executable, "-B", "agentic-workflow/helpers/check_package.py", "--integration-root", "."],
            root, args.timeout, evidence / "checks.stdout", evidence / "checks.stderr")
        attempt["checks"] = checks
        unchanged = (root / contract).is_file() and (root / contract).read_bytes() == original_contract
        attempt["source_contract_unchanged"] = unchanged
        attempt["status"] = checks["status"] if checks["status"] != "PASS" else response["status"]
        if "signal" in checks:
            attempt["signal"] = checks["signal"]
        if not unchanged:
            attempt["note"] = "WORKFLOW.md changed from the original snapshot."
            if checks["status"] == "PASS":
                attempt["status"] = "FAIL"
    except runtime.Interrupted as exc:
        attempt.update(status="INTERRUPTED", signal=exc.signum)
    except (OSError, ValueError, runtime.RunnerError) as exc:
        attempt.update(status="RUNNER_ERROR", error=str(exc))
    return attempt


def main():
    parser = document_review.argument_parser(__doc__)
    parser.add_argument("--repair", action="store_true",
                        help="Attempt one edit after a failed review with no uncertainty")
    args = parser.parse_args()
    root = Path.cwd().resolve()
    results = document_review.prepare_run(root, "workflow")
    result = {"status": "RUNNER_ERROR", "review": {"status": "NOT_RUN"},
              "execution": {"status": "NOT_RUN"}}
    try:
        capture_inputs(root, results / "inputs")
        prompt = document_review.load_prompt("workflow-review.md")
        result = document_review.evaluate(root, results, prompt, {}, args)
        if args.repair:
            review = result["review"]
            uncertain = any(row["status"] == "UNCLEAR" for row in review.get("checks", []))
            result["repair"] = {"status": "NOT_RUN", "attempted": False,
                                "reason": "Repair requires a failed review without uncertainty."}
            if review["status"] == "FAIL" and not uncertain:
                attempt = repair(root, results, args)
                result["repair"] = attempt
                result["status"] = attempt["status"]
                if "signal" in attempt:
                    result["signal"] = attempt["signal"]
                if attempt["status"] == "FIXED":
                    result["note"] = "Editor reported resolution and mechanical checks passed. No independent re-review occurred."
                else:
                    result["partial_edits_may_remain"] = attempt["attempted"]
                    result["note"] = "Repair did not complete successfully; partial edits may remain."
    except runtime.Interrupted as exc:
        result.update(status="INTERRUPTED", signal=exc.signum)
    except (OSError, ValueError, runtime.RunnerError) as exc:
        result.update(status="RUNNER_ERROR", error=str(exc))
    return document_review.finish(results, result, "Workflow")

