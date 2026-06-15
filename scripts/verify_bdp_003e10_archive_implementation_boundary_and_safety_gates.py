#!/usr/bin/env python3
"""Verify BDP-003E.10 archive implementation boundary and safety gates."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
DOC_PATH = ROOT / "docs/BDP_003E10_ARCHIVE_IMPLEMENTATION_BOUNDARY_AND_SAFETY_GATES.md"
EXPECTED_NEXT_STEP = "BDP-003E.11 — Implement local reviewed concept card archive writer behind safety gates, if approved."
RECORD_KEY = "bdp_003e10_archive_implementation_boundary_and_safety_gates"


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def require_file(path: Path) -> str:
    if not path.exists():
        fail(f"missing required file: {path}")
    return path.read_text()


def require_phrase(text: str, phrase: str, label: str) -> None:
    if phrase not in text:
        fail(f"{label} missing required phrase: {phrase}")


def require_false(record: dict, key: str) -> None:
    if record.get(key) is not False:
        fail(f"{RECORD_KEY}.{key} must be false")


def main() -> None:
    state = json.loads(require_file(STATE_PATH))
    record = state.get(RECORD_KEY)
    if not isinstance(record, dict):
        fail(f"missing state record: {RECORD_KEY}")

    if record.get("phase") != "BDP-003E.10":
        fail(f"{RECORD_KEY}.phase must be BDP-003E.10")
    if record.get("status") != "complete":
        fail(f"{RECORD_KEY}.status must be complete")
    if record.get("next_step") != EXPECTED_NEXT_STEP:
        fail(f"{RECORD_KEY}.next_step must be the expected E11 next step")

    for key in [
        "implementation_approved",
        "persistence_approved",
        "writer_implemented",
        "archive_folder_created",
        "local_files_written",
        "frontend_archive_controls_approved",
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

    gates = record.get("safety_gates")
    if not isinstance(gates, list) or len(gates) < 6:
        fail(f"{RECORD_KEY}.safety_gates must list explicit safety gates")

    doc = require_file(DOC_PATH)
    for phrase in [
        "BDP-003E.10",
        "implementation boundary and safety gates before writing code",
        "Implementation is not approved",
        "No writer implementation",
        "No archive folders",
        "No local files written",
        "No frontend archive controls",
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
        require_phrase(doc, phrase, "BDP-003E.10 doc")

    handover = require_file(HANDOVER_PATH)
    require_phrase(handover, "BDP-003E.10", "handover")
    require_phrase(handover, EXPECTED_NEXT_STEP, "handover")

    print("[OK] BDP-003E.10 archive implementation boundary and safety gates verified")


if __name__ == "__main__":
    main()
