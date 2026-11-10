"""Provider diagnostic codes and their normalized accounting effects."""

from tracing.shared.types import Diagnostic

MISSING = {"missing_usage", "unidentified_usage", "invalid_json_line"}
INCOMPLETE = {
    "native_source_unavailable",
    "no_native_evidence",
    "native_storage_unavailable",
    "native_turn_unavailable",
    "unfinished_turn",
    "source_unavailable",
    "native_identity_unresolved",
    "ambiguous_native_identity",
    "selected_turn_absent",
    "unverified_native_version",
    "native_identity_mismatch",
    "ambiguous_dispatch_turn",
    "missing_native_identity",
}


def classify(diagnostics: list[Diagnostic]) -> list[Diagnostic]:
    for diagnostic in diagnostics:
        diagnostic["tracing_provider"] = "codex"
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
