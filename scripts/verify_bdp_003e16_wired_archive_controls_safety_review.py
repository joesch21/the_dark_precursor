#!/usr/bin/env python3
"""Verify BDP-003E.16 wired archive controls safety gate review."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
FRONTEND_PATH = ROOT / "frontend" / "dark_precursor.py"
HELPER_PATH = ROOT / "scripts" / "ui_reviewed_concept_card_archive_controls.py"
DOC_PATH = ROOT / "docs" / "BDP_003E16_WIRED_ARCHIVE_CONTROLS_SAFETY_REVIEW.md"

STATE_KEY = "bdp_003e16_wired_archive_controls_safety_gate_review"
EXPECTED_NEXT_STEP = (
    "BDP-003E.17 — Decide broader archive workflow readiness before expanding "
    "beyond local reviewed UI archive controls."
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


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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

    expected_pairs = {
        "phase": "BDP-003E.16",
        "status": "complete",
        "controlled_slice": "wired_archive_controls_safety_review_only",
        "review_type": "post_frontend_wiring_safety_gate_review",
        "next_step": EXPECTED_NEXT_STEP,
    }
    for key, expected in expected_pairs.items():
        if record.get(key) != expected:
            fail(f"{STATE_KEY}.{key} expected {expected!r}, got {record.get(key)!r}")

    for key in [
        "frontend_ux_ui_changed_by_bdp_003e15",
        "wired_controls_reviewed",
        "local_reviewed_payload_gate_confirmed",
        "explicit_archive_path_gate_confirmed",
        "operator_confirmation_gate_confirmed",
        "local_writer_only_confirmed",
        "broader_archive_workflow_blocked",
    ]:
        require_true(record, key)

    for key in [
        "frontend_ux_ui_changed_by_bdp_003e16",
        "frontend_modified_by_bdp_003e16",
        "new_frontend_controls_added_by_bdp_003e16",
        "broader_archive_workflow_approved",
        "backend_services_added",
        "adapter_endpoints_added",
        "database_tables_added",
        "sql_migrations_added",
        "evidence_promotion_added",
        "citations_created",
        "concept_relations_created",
        "interpretations_created",
        "buchanan_claims_created",
    ]:
        require_false(record, key)

    frontend = require_file(FRONTEND_PATH)
    recorded_frontend_sha = record.get("frontend_dark_precursor_sha256_at_review")
    if not isinstance(recorded_frontend_sha, str) or len(recorded_frontend_sha) != 64:
        fail("frontend/dark_precursor.py E16 review hash must remain recorded as a sha256 string")

    # Phase-local rule:
    # BDP-003E.16 verified the frontend hash at the time of the safety review.
    # Later approved frontend phases may change frontend/dark_precursor.py, so E16 must not
    # compare its historic review hash against the current frontend after later phases.

    for phrase in [
        "BDP-003E.15 Local reviewed concept card archive controls wiring",
        "render_bdp_003e15_archive_controls",
        "ui_reviewed_concept_card_archive_controls",
    ]:
        require_phrase(frontend, phrase, "frontend")

    helper = require_file(HELPER_PATH)
    for phrase in [
        "Local reviewed concept card archive",
        "Explicit local archive folder path",
        "I confirm this card is locally reviewed",
        "write_reviewed_concept_card_archive",
        "evidence_promotion_approved",
        "citations_created",
        "concept_relations_created",
        "interpretations_created",
        "buchanan_claims_created",
    ]:
        require_phrase(helper, phrase, "UI archive helper")

    for phrase in [
        "CREATE TABLE",
        "INSERT INTO citations",
        "INSERT INTO concept_relations",
        "INSERT INTO interpretations",
        "psycopg",
    ]:
        if phrase in frontend or phrase in helper:
            fail(f"banned persistence/evidence phrase found in UI wiring: {phrase}")

    doc = require_file(DOC_PATH)
    for phrase in [
        "BDP-003E.16",
        "safety review only",
        "Frontend UX/UI was changed by BDP-003E.15",
        "BDP-003E.16 does not make additional frontend UX/UI changes",
        "No new frontend UX/UI change",
        "No broader archive workflow",
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
        require_phrase(doc, phrase, "BDP-003E.16 doc")

    handover = require_file(HANDOVER_PATH)
    require_phrase(handover, "BDP-003E.16", "handover")
    require_phrase(handover, EXPECTED_NEXT_STEP, "handover")

    print("[OK] BDP-003E.16 wired archive controls safety gate review verified")


if __name__ == "__main__":
    main()
