"""Provider diagnostic codes and their normalized accounting effects."""

from tracing.shared.types import Diagnostic

MISSING = {"missing_usage", "unidentified_usage", "invalid_json_line"}
INCOMPLETE = {
    "no_native_evidence",
    "message_only_usage",
    "opencode_turn_unavailable",
    "opencode_dispatch_unresolved",
    "unfinished_turn",
    "source_unavailable",
    "selected_turn_absent",
    "unverified_native_version",
    "opencode_export_unavailable",
    "unmeasured_message",
    "ambiguous_dispatch_turn",
    "opencode_parent_mismatch",
    "opencode_continuation_unresolved",
    "missing_native_identity",
}


def classify(diagnostics: list[Diagnostic]) -> list[Diagnostic]:
    for diagnostic in diagnostics:
        diagnostic["tracing_provider"] = "opencode"
        diagnostic["coverage_effect"] = (
            "missing_measurement"
            if diagnostic["code"] in MISSING
            else "incomplete"
            if diagnostic["code"] in INCOMPLETE
            else "informational"
        )
    return diagnostics


def gap(code: str, session: str | None = None, turn: str | None = None) -> Diagnostic:
    return dict(code=code, session_id=session, turn_id=turn)
