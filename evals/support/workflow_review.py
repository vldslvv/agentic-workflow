"""Workflow snapshots and a single optional editor attempt with mechanical checks."""

import json
import shutil
import sys
from pathlib import Path
from typing import cast

from . import document_review, runtime
from .models import Repair, RepairResponse, ReviewSettings


def capture_inputs(root: Path, destination: Path) -> None:
    """Preserve current candidate files without project execution history."""
    shutil.copytree(
        root / "agentic-workflow",
        destination / "agentic-workflow",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    for relative in ("AGENTS.md", ".agentic-workflow/config/MODELS.md"):
        source = root / relative
        if source.is_file():
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    for source in (root / ".agents/skills").glob("agentic-workflow-*"):
        shutil.copytree(source, destination / ".agents/skills" / source.name)


def repair(root: Path, results: Path, args: ReviewSettings) -> Repair:
    """Return the editor outcome separately from the original review judgment."""
    evidence = results / "repair"
    prompt = document_review.load_prompt(
        "workflow-repair.md", judgment=results / "judgment.json", snapshot=results / "inputs"
    )
    attempt: Repair = {"status": "RUNNER_ERROR", "attempted": False}
    try:
        attempt["attempted"] = True
        execution = document_review.invoke_model(
            root, evidence, root, prompt, "repair.json", "output.json", args, "workspace-write"
        )
        attempt["execution"] = execution
        if execution["status"] != "PASS":
            attempt["status"] = (
                "REPAIR_ERROR" if execution["status"] == "FAIL" else execution["status"]
            )
            if "signal" in execution:
                attempt["signal"] = execution["signal"]
            return attempt
        response = json.loads((evidence / "output.json").read_text())
        if (
            not isinstance(response, dict)
            or response.get("status") not in ("PASS", "FAIL")
            or not isinstance(response.get("summary"), str)
            or not response["summary"].strip()
        ):
            raise ValueError("Editor response must include PASS or FAIL and a nonempty summary")
        response = cast(RepairResponse, response)
        attempt["response"] = response
    except runtime.Interrupted as exc:
        attempt.update({"status": "INTERRUPTED", "signal": exc.signum})
    except (OSError, ValueError, runtime.RunnerError) as exc:
        attempt.update({"status": "RUNNER_ERROR", "error": str(exc)})
    return attempt


def check_repair(
    root: Path, results: Path, args: ReviewSettings, attempt: Repair, original_contract: bytes
) -> Repair:
    """Check a valid editor response without replacing the original review."""
    evidence = results / "repair"
    contract = Path("agentic-workflow/WORKFLOW.md")
    try:
        checks = runtime.execute(
            [
                sys.executable,
                "-B",
                "agentic-workflow/helpers/check_package.py",
                "--integration-root",
                ".",
            ],
            root,
            args.timeout,
            evidence / "checks.stdout",
            evidence / "checks.stderr",
        )
        attempt["checks"] = checks
        unchanged = (root / contract).is_file() and (
            root / contract
        ).read_bytes() == original_contract
        attempt["source_contract_unchanged"] = unchanged
        attempt["status"] = (
            checks["status"] if checks["status"] != "PASS" else attempt["response"]["status"]
        )
        if "signal" in checks:
            attempt["signal"] = checks["signal"]
        if not unchanged:
            attempt["note"] = "WORKFLOW.md changed from the original snapshot."
            if checks["status"] == "PASS":
                attempt["status"] = "FAIL"
    except runtime.Interrupted as exc:
        attempt.update({"status": "INTERRUPTED", "signal": exc.signum})
    except (OSError, ValueError, runtime.RunnerError) as exc:
        attempt.update({"status": "RUNNER_ERROR", "error": str(exc)})
    return attempt
