#!/usr/bin/env python3
"""Review current workflow documents; optionally attempt one repair with --repair."""

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


from evals.support import document_review, runtime, workflow_review
from evals.support.models import DocumentResult, ReviewSettings


def run(root: Path, args: ReviewSettings) -> DocumentResult:
    results = document_review.prepare_run(root, "workflow")
    result: DocumentResult = {
        "status": "RUNNER_ERROR",
        "review": {"status": "NOT_RUN"},
        "execution": {"status": "NOT_RUN"},
    }
    try:
        workflow_review.capture_inputs(root, results / "inputs")
        prompt = document_review.load_prompt("workflow-review.md")
        execution = document_review.invoke_model(
            root,
            results,
            results / "inputs",
            prompt,
            "review.json",
            "judgment.json",
            args,
            "read-only",
        )
        result = document_review.grade(results, execution, {})
        if args.repair:
            review = result["review"]
            result["repair"] = {
                "status": "NOT_RUN",
                "attempted": False,
                "reason": "Repair requires a failed review.",
            }
            if review["status"] == "FAIL":
                original_contract = (results / "inputs/agentic-workflow/WORKFLOW.md").read_bytes()
                attempt = workflow_review.repair(root, results, args)
                if "response" in attempt:
                    attempt = workflow_review.check_repair(
                        root, results, args, attempt, original_contract
                    )
                result["repair"] = attempt
                result["status"] = attempt["status"]
                if "signal" in attempt:
                    result["signal"] = attempt["signal"]
                if attempt["status"] == "PASS":
                    result["note"] = (
                        "Editor reported resolution and mechanical checks passed. No independent re-review occurred."
                    )
                else:
                    result["partial_edits_may_remain"] = attempt["attempted"]
                    result["note"] = (
                        "Repair did not complete successfully; partial edits may remain."
                    )
    except runtime.Interrupted as exc:
        result.update({"status": "INTERRUPTED", "signal": exc.signum})
    except (OSError, ValueError, runtime.RunnerError) as exc:
        result.update({"status": "RUNNER_ERROR", "error": str(exc)})
    document_review.save(results, result, "Workflow")
    return result


def main() -> int:
    parser = document_review.argument_parser(__doc__)
    parser.add_argument(
        "--repair",
        action="store_true",
        help="Attempt one edit after a failed review",
    )
    args = parser.parse_args()
    return document_review.exit_code(run(Path.cwd().resolve(), ReviewSettings(**vars(args))))


if __name__ == "__main__":
    raise SystemExit(main())
