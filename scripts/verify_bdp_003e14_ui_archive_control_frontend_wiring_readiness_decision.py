#!/usr/bin/env python3
"""Verify BDP-003E.14 UI archive control frontend wiring readiness decision.

This verifier confirms that BDP-003E.14 remains a readiness-decision phase only.
It must not require or imply frontend wiring.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
DOC_PATH = ROOT / "docs" / "BDP_003E14_UI_ARCHIVE_CONTROL_FRONTEND_WIRING_READINESS_DECISION.md"

STATE_KEY = "bdp_003e14_ui_archive_control_frontend_wiring_readiness_decision"
EXPECTED_NEXT_STEP = (
    "BDP-003E.15 — Wire local reviewed concept card archive controls into "
    "The Dark Precursor UI behind safety gates."
)


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def require_file(path: Path) -> str:
    if not path.exists():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text()


def require_phrase(text: str, phrase: str, label: str) -> None:
    if phrase not in text:
        fail(f"{label} missing required phrase: {phrase}")


def require_false(record: dict, key: str) -> None:
    if record.get(key) is not False:
        fail(f"{STATE_KEY}.{key} must be false")


def main() -> None:
    if not STATE_PATH.exists():
        fail("BUCHANAN_SYSTEM_STATE.json missing")

    state = json.loads(STATE_PATH.read_text())
    record = state.get(STATE_KEY)
    if not isinstance(record, dict):
        fail(f"missing state record: {STATE_KEY}")

    expected_pairs = {
        "phase": "BDP-003E.14",
        "status": "complete",
        "controlled_slice": "frontend_wiring_readiness_decision_only",
        "decision_type": "ui_archive_control_frontend_wiring_readiness_decision_only",
        "next_step": EXPECTED_NEXT_STEP,
    }
    for key, expected in expected_pairs.items():
        if record.get(key) != expected:
            fail(f"{STATE_KEY}.{key} expected {expected!r}, got {record.get(key)!r}")

    for key in [
        "frontend_wiring_approved",
        "frontend_wired",
        "frontend_archive_controls_added",
        "archive_buttons_added",
        "streamlit_writer_call_added",
        "backend_services_approved",
        "adapter_endpoints_approved",
        "database_tables_approved",
        "sql_migrations_approved",
        "archive_folders_created_by_default",
        "evidence_promotion_approved",
        "citations_created",
        "concept_relations_created",
        "interpretations_created",
        "buchanan_claims_created",
    ]:
        require_false(record, key)

    if record.get("ready_for_future_frontend_wiring") is not True:
        fail(f"{STATE_KEY}.ready_for_future_frontend_wiring must be true")

    doc = require_file(DOC_PATH)
    for phrase in [
        "BDP-003E.14",
        "UI archive control frontend wiring readiness decision",
        "readiness decision only",
        "frontend wiring is not approved",
        "No frontend wiring",
        "No frontend archive controls",
        "No archive buttons",
        "No Streamlit writer call",
        "No backend services",
        "No adapter endpoints",
        "No database tables",
        "No SQL migrations",
        "No archive folders created by default",
        "No evidence promotion",
        "No citations",
        "No concept relations",
        "No interpretations",
        "No Buchanan-specific claims",
        EXPECTED_NEXT_STEP,
    ]:
        require_phrase(doc, phrase, "BDP-003E.14 doc")

    handover = require_file(HANDOVER_PATH)
    require_phrase(handover, "BDP-003E.14", "handover")
    require_phrase(handover, EXPECTED_NEXT_STEP, "handover")

    print("[OK] BDP-003E.14 UI archive control frontend wiring readiness decision verified")


if __name__ == "__main__":
    main()
