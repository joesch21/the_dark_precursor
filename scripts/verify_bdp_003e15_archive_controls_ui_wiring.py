#!/usr/bin/env python3
"""Verify BDP-003E.15 archive controls UI wiring."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
FRONTEND_PATH = ROOT / "frontend" / "dark_precursor.py"
DOC_PATH = ROOT / "docs" / "BDP_003E15_ARCHIVE_CONTROLS_UI_WIRING.md"
HELPER_PATH = ROOT / "scripts" / "ui_reviewed_concept_card_archive_controls.py"

STATE_KEY = "bdp_003e15_archive_controls_ui_wiring"
EXPECTED_NEXT_STEP = (
    "BDP-003E.16 — Review wired archive controls in The Dark Precursor UI "
    "against safety gates before broader archive workflow."
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


def require_true(record: dict, key: str) -> None:
    if record.get(key) is not True:
        fail(f"{STATE_KEY}.{key} must be true")


def main() -> None:
    state = json.loads(require_file(STATE_PATH))
    record = state.get(STATE_KEY)
    if not isinstance(record, dict):
        fail(f"missing state record: {STATE_KEY}")

    expected_pairs = {
        "phase": "BDP-003E.15",
        "status": "complete",
        "controlled_slice": "guarded_frontend_wiring_only",
        "implementation_type": "frontend_archive_controls_behind_safety_gates",
        "next_step": EXPECTED_NEXT_STEP,
    }
    for key, expected in expected_pairs.items():
        if record.get(key) != expected:
            fail(f"{STATE_KEY}.{key} expected {expected!r}, got {record.get(key)!r}")

    for key in [
        "frontend_wired",
        "frontend_archive_controls_added",
        "archive_buttons_added",
        "streamlit_writer_call_added",
        "requires_explicit_archive_path",
        "requires_operator_confirmation",
        "uses_local_writer_only",
    ]:
        require_true(record, key)

    for key in [
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

    doc = require_file(DOC_PATH)
    for phrase in [
        "BDP-003E.15",
        "guarded frontend wiring only",
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
        require_phrase(doc, phrase, "BDP-003E.15 doc")

    helper = require_file(HELPER_PATH)
    for phrase in [
        "render_bdp_003e15_archive_controls",
        "find_reviewed_archive_payload",
        "write_reviewed_concept_card_archive",
        "Explicit local archive folder path",
        "Archive locally reviewed card",
        "evidence_promotion_approved",
        "citations_created",
        "concept_relations_created",
        "interpretations_created",
        "buchanan_claims_created",
    ]:
        require_phrase(helper, phrase, "UI helper")

    frontend = require_file(FRONTEND_PATH)
    for phrase in [
        "BDP-003E.15 Local reviewed concept card archive controls wiring",
        "render_bdp_003e15_archive_controls",
        "ui_reviewed_concept_card_archive_controls",
    ]:
        require_phrase(frontend, phrase, "frontend")

    banned_frontend_phrases = [
        "psycopg",
        "CREATE TABLE",
        "INSERT INTO concept_relations",
        "INSERT INTO citations",
        "INSERT INTO interpretations",
    ]
    for phrase in banned_frontend_phrases:
        if phrase in frontend:
            fail(f"frontend contains banned phrase for E15 wiring: {phrase}")

    spec = importlib.util.spec_from_file_location("ui_reviewed_concept_card_archive_controls", HELPER_PATH)
    if spec is None or spec.loader is None:
        fail("could not load UI helper module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    sample_payload = {
        "schema_version": module.INPUT_SCHEMA_VERSION,
        "archive_record_id": "bwo-reviewed-sample",
        "review_status": "locally_reviewed",
        "reviewed_at": "2026-06-16T00:00:00+00:00",
        "reviewed_by": "operator",
        "concept": {"concept_id": "body-without-organs", "label": "Body without Organs"},
        "card": {
            "title": "Reviewed cinematic card",
            "summary": "A reviewed sample card.",
            "cinematic_prompt": "A cinematic prompt.",
        },
        "governance": {
            "evidence_promotion_approved": False,
            "citations_created": False,
            "concept_relations_created": False,
            "interpretations_created": False,
            "buchanan_claims_created": False,
        },
        "source_trace": {
            "export_phase": "BDP-003E.3",
            "schema_phase": "BDP-003E.5",
            "sample_review_phase": "BDP-003E.6",
            "writer_contract_phase": "BDP-003E.7",
            "implementation_boundary_phase": "BDP-003E.10",
        },
    }
    found = module.find_reviewed_archive_payload({"nested": {"payload": sample_payload}})
    if not found or found.get("archive_record_id") != "bwo-reviewed-sample":
        fail("UI helper did not find reviewed payload in nested session state")

    handover = require_file(HANDOVER_PATH)
    require_phrase(handover, "BDP-003E.15", "handover")
    require_phrase(handover, EXPECTED_NEXT_STEP, "handover")

    print("[OK] BDP-003E.15 archive controls UI wiring verified")


if __name__ == "__main__":
    main()
