#!/usr/bin/env python3
"""Rebuild usage and trace reports once for an existing implementation.

implementation is the allocated implementation directory. The tracing provider
is detected from saved native evidence, independently of the current agent shell.
Missing, invalid or mixed-provider evidence fails before writes. Only the detected
provider is refreshed; internal routing always uses an explicit provider.

Creates/uses implementation/.records.lock; refreshes saved native turns and
proven dispatch descendants under implementation/native/<session-id>/<turn-
id>.jsonl (Codex) or .json (OpenCode). Creates/overwrites implementation/reports/usage.json, usage.md,
events.json and timeline.json; starts no viewer or continuous capture.

Prints JSON with implementation_id (directory name), reports (report directory
path), tracing_provider and coverage (diagnostic-code counts). Exit 0 means reports were written,
not complete telemetry. Inspect coverage and usage.json diagnostics; null means
unavailable, known_subtotal excludes missing measurements. Exit 2 means invalid
input or an operation error (stderr).

Rerun after more evidence is saved, or use trace_view.py for live capture.

Example: python3 agentic-workflow/helpers/usage_report.py .agentic-workflow/records/001_example
"""

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

from tracing.registry import detect_saved, select
from tracing.shared.enrichment import enrich
from tracing.shared.files import locked, safe_destination, write_atomic
from tracing.shared.reporting import build_report, markdown, timeline
from tracing.shared.types import Diagnostic, Event, EventReport, Report


def import_evidence(root: Path, provider: str) -> tuple[list[Event], list[Diagnostic]]:
    root = Path(root).resolve()
    return enrich(root, select(provider).collect(root))


@dataclass(frozen=True)
class ReportBundle:
    usage: Report
    content: EventReport
    files: dict[str, bytes]
    timeline_available: bool


def refresh(implementation_dir: Path, provider: str) -> ReportBundle:
    selected = select(provider)
    root = Path(implementation_dir).resolve()
    with locked(root / ".records.lock"):
        events, diagnostics = enrich(root, selected.collect(root))
        report = build_report(events, diagnostics)
        report["implementation_id"] = root.name
        report["tracing_provider"] = provider
        trace = timeline(events)
        trace["metadata"]["tracing_provider"] = provider
        content_report: EventReport = dict(
            version=1,
            tracing_provider=provider,
            implementation_id=root.name,
            events=events,
            timing_omissions=trace["metadata"]["timing_omissions"],
        )
        outputs = {
            name: (json.dumps(value, indent=2) + "\n").encode()
            for name, value in [
                ("usage.json", report),
                ("timeline.json", trace),
                ("events.json", content_report),
            ]
        }
        outputs["usage.md"] = markdown(report).encode()
        # Validate the whole output set before writing, including symlink/hardlink
        # aliases. Native inputs live outside this output boundary.
        for name in outputs:
            safe_destination(root, root / "reports" / name)
        for name, data in outputs.items():
            write_atomic(root / "reports" / name, data)
    return ReportBundle(
        report, content_report, outputs, any(e["ph"] != "M" for e in trace["traceEvents"])
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("implementation", type=Path, help="existing implementation directory")
    args = parser.parse_args()
    try:
        provider = detect_saved(args.implementation)
        report = refresh(args.implementation, provider).usage
        print(
            json.dumps(
                {
                    "tracing_provider": provider,
                    "implementation_id": report["implementation_id"],
                    "reports": str(args.implementation / "reports"),
                    "coverage": report["summary"]["coverage"],
                }
            )
        )
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"usage-report: {exc}\n")


if __name__ == "__main__":
    main()
