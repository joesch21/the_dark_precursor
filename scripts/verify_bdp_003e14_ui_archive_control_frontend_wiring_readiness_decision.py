#!/usr/bin/env python3
"""Verify BDP-003E.14 UI archive control frontend wiring readiness decision.

This verifier is phase-local: it checks E14's readiness decision and its
own next step, while later phases may advance the global state.
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
    state = json.loads(require_file(STATE_PATH))
    record = state.get(STATE_KEY)
    if not isinstance(record, dict):
        fail(f"missing state record: {STATE_KEY}")

    if record.get("phase") != "BDP-003E.14":
        fail(f"{STATE_KEY}.phase must be BDP-003E.14")
    if record.get("status") != "complete":
        fail(f"{STATE_KEY}.status must be complete")
    if record.get("next_step") != EXPECTED_NEXT_STEP:
        fail(f"{STATE_KEY}.next_step must remain E15 wiring phase")

    for key in [
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
        if key in record:
            require_false(record, key)

    doc = require_file(DOC_PATH)
    for phrase in [
        "BDP-003E.14",
        "UI archive control frontend wiring readiness decision",
        "frontend wiring is not approved",
        "No backend services",
        "No adapter endpoints",
        "No database tables",
        "No SQL migrations",
        EXPECTED_NEXT_STEP,
    ]:
        require_phrase(doc, phrase, "BDP-003E.14 doc")

    handover = require_file(HANDOVER_PATH)
    require_phrase(handover, "BDP-003E.14", "handover")
    require_phrase(handover, EXPECTED_NEXT_STEP, "handover")

    print("[OK] BDP-003E.14 UI archive control frontend wiring readiness decision verified")


if __name__ == "__main__":
    main()
