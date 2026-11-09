"""Review current specification bundles against templates and policies without edits."""

from pathlib import Path

from . import document_review
from . import runtime
from . import spec_inputs


def main():
    parser = document_review.argument_parser(__doc__)
    parser.add_argument("--bundle", help="Bundle directory under specs/ (default: all bundles)")
    args = parser.parse_args()
    root = Path.cwd().resolve()
    results = document_review.prepare_run(root, "specs")
    result = {"status": "RUNNER_ERROR", "review": {"status": "NOT_RUN"},
              "execution": {"status": "NOT_RUN"}}
    try:
        inputs = spec_inputs.capture(root, results / "inputs", args.bundle)
        prompt = document_review.load_prompt("specs-review.md", scope=", ".join(inputs["bundles"]))
        result = document_review.evaluate(root, results, prompt, inputs, args)
        result["bundles"] = inputs["bundles"]
    except runtime.Interrupted as exc:
        result.update(status="INTERRUPTED", signal=exc.signum)
    except (OSError, ValueError, runtime.RunnerError) as exc:
        result.update(status="RUNNER_ERROR", error=str(exc))
    return document_review.finish(results, result, "Specification")

