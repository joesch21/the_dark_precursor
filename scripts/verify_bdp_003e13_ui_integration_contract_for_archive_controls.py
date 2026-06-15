#!/usr/bin/env python3
"""Verify BDP-003E.13 UI integration contract boundary.

This verifier is intentionally contract-only. It confirms that the UI integration
contract exists, the state/handover records preserve the no-wiring boundary, and
no frontend archive control implementation is approved by this phase.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
DOC_PATH = ROOT / "docs" / "BDP_003E13_UI_INTEGRATION_CONTRACT_FOR_ARCHIVE_CONTROLS.md"
E12_DOC_PATH = ROOT / "docs" / "BDP_003E12_ARCHIVE_WRITER_OUTPUT_SAMPLE_REVIEW.md"
FRONTEND_PATH = ROOT / "frontend" / "dark_precursor.py"

STATE_KEY = "bdp_003e13_ui_integration_contract_for_archive_controls"
EXPECTED_NEXT_STEP = "BDP-003E.14 — Decide UI archive control frontend wiring readiness, without wiring frontend."


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


def require_true(record: dict, key: str) -> None:
    if record.get(key) is not True:
        fail(f"{STATE_KEY}.{key} must be true")


def main() -> None:
    state = json.loads(require_file(STATE_PATH))
    record = state.get(STATE_KEY)
    if not isinstance(record, dict):
        fail(f"missing state record: {STATE_KEY}")

    if record.get("phase") != "BDP-003E.13":
        fail(f"{STATE_KEY}.phase must be BDP-003E.13")
    if record.get("status") != "complete":
        fail(f"{STATE_KEY}.status must be complete")
    if record.get("controlled_slice") != "ui_integration_contract_only":
        fail(f"{STATE_KEY}.controlled_slice must be ui_integration_contract_only")
    if record.get("next_step") != EXPECTED_NEXT_STEP:
        fail(f"{STATE_KEY}.next_step mismatch")

    require_true(record, "ui_integration_contract_defined")

    for key in [
        "frontend_wiring_approved",
        "frontend_controls_implemented",
        "archive_button_implemented",
        "backend_services_approved",
        "adapter_endpoints_approved",
        "database_tables_approved",
        "sql_migrations_approved",
        "evidence_promotion_approved",
        "citations_created",
        "concept_relations_created",
        "interpretations_created",
        "buchanan_claims_created",
    ]:
        require_false(record, key)

    doc = require_file(DOC_PATH)
    for phrase in [
        "BDP-003E.13",
        "UI integration contract only",
        "Implementation is not approved",
        "No frontend wiring",
        "No archive control implementation",
        "No backend services",
        "No adapter endpoints",
        "No database tables",
        "No SQL migrations",
        "No evidence promotion",
        "No citations",
        "No concept relations",
        "No interpretations",
        "No Buchanan-specific claims",
        EXPECTED_NEXT_STEP,
    ]:
        require_phrase(doc, phrase, "BDP-003E.13 doc")

    e12_doc = require_file(E12_DOC_PATH)
    require_phrase(e12_doc, "BDP-003E.13 Follow-up UI Contract Note", "BDP-003E.12 doc")
    require_phrase(e12_doc, "UI integration remains blocked", "BDP-003E.12 doc")

    handover = require_file(HANDOVER_PATH)
    require_phrase(handover, "BDP-003E.13", "handover")
    require_phrase(handover, EXPECTED_NEXT_STEP, "handover")
    require_phrase(handover, "No frontend wiring", "handover")

    frontend = require_file(FRONTEND_PATH)
    forbidden_frontend_phrases = [
        "BDP-003E.13 — UI Integration Contract",
        "Archive reviewed local concept card",
        "Local archive only — not evidence",
    ]
    for phrase in forbidden_frontend_phrases:
        if phrase in frontend:
            fail(f"frontend appears to contain E13 UI archive control phrase: {phrase}")

    print("[OK] BDP-003E.13 UI integration contract for archive controls verified")


if __name__ == "__main__":
    main()
