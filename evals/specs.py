#!/usr/bin/env python3
"""Review current specification bundles against templates and policies without edits."""

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


from evals.support import document_review, runtime, spec_inputs
from evals.support.models import DocumentResult, ReviewSettings


def run(root: Path, args: ReviewSettings) -> DocumentResult:
    results = document_review.prepare_run(root, "specs")
    result: DocumentResult = {
        "status": "RUNNER_ERROR",
        "review": {"status": "NOT_RUN"},
        "execution": {"status": "NOT_RUN"},
    }
    try:
        inputs = spec_inputs.capture(root, results / "inputs", args.bundle)
        prompt = document_review.load_prompt("specs-review.md", scope=", ".join(inputs["bundles"]))
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
        result = document_review.grade(results, execution, inputs)
        result["bundles"] = inputs["bundles"]
    except runtime.Interrupted as exc:
        result.update({"status": "INTERRUPTED", "signal": exc.signum})
    except (OSError, ValueError, runtime.RunnerError) as exc:
        result.update({"status": "RUNNER_ERROR", "error": str(exc)})
    document_review.save(results, result, "Specification")
    return result


def main() -> int:
    parser = document_review.argument_parser(__doc__)
    parser.add_argument("--bundle", help="Bundle directory under specs/ (default: all bundles)")
    args = parser.parse_args()
    return document_review.exit_code(run(Path.cwd().resolve(), ReviewSettings(**vars(args))))


if __name__ == "__main__":
    raise SystemExit(main())
