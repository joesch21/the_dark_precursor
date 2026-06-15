#!/usr/bin/env python3
"""Verify BDP-003E.13 UI integration contract for archive controls.

This verifier is intentionally phase-local: it checks the E13 record and its
own next step, while later phases may advance the global project state.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
DOC_PATH = ROOT / "docs" / "BDP_003E13_UI_INTEGRATION_CONTRACT_FOR_ARCHIVE_CONTROLS.md"

STATE_KEY = "bdp_003e13_ui_integration_contract_for_archive_controls"
EXPECTED_NEXT_STEP = (
    "BDP-003E.14 — Decide UI archive control frontend wiring readiness, "
    "without wiring frontend."
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


def main() -> None:
    state = json.loads(STATE_PATH.read_text())
    record = state.get(STATE_KEY)
    if not isinstance(record, dict):
        fail(f"missing state record: {STATE_KEY}")

    if record.get("phase") != "BDP-003E.13":
        fail(f"{STATE_KEY}.phase must be BDP-003E.13")
    if record.get("status") != "complete":
        fail(f"{STATE_KEY}.status must be complete")
    if record.get("next_step") != EXPECTED_NEXT_STEP:
        fail(f"{STATE_KEY}.next_step must remain E14 readiness decision")

    for key in [
        "frontend_wiring_approved",
        "frontend_wired",
        "frontend_archive_controls_added",
        "archive_buttons_added",
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
        if key in record and record.get(key) is not False:
            fail(f"{STATE_KEY}.{key} must be false")

    doc = require_file(DOC_PATH)
    for phrase in [
        "BDP-003E.13",
        "UI integration contract",
        "frontend wiring is not approved",
        "No frontend wiring",
        "No frontend archive controls",
        EXPECTED_NEXT_STEP,
    ]:
        require_phrase(doc, phrase, "BDP-003E.13 doc")

    handover = require_file(HANDOVER_PATH)
    require_phrase(handover, "BDP-003E.13", "handover")
    require_phrase(handover, EXPECTED_NEXT_STEP, "handover")

    print("[OK] BDP-003E.13 UI integration contract for archive controls verified")


if __name__ == "__main__":
    main()
