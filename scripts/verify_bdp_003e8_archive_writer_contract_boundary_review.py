#!/usr/bin/env python3
"""Verify BDP-003E.8 archive writer contract boundary review."""
from __future__ import annotations

import json
from pathlib import Path

STATE_PATH = Path("BUCHANAN_SYSTEM_STATE.json")
HANDOVER_PATH = Path("BUCHANAN_THREAD_HANDOVER.md")
DOC_PATH = Path("docs/BDP_003E8_ARCHIVE_WRITER_CONTRACT_BOUNDARY_REVIEW.md")
EXPECTED_NEXT_STEP = "BDP-003E.9 — Decide local reviewed concept card archive writer implementation readiness, without implementation."


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def require_file(path: Path) -> str:
    if not path.exists():
        fail(f"missing required file: {path}")
    return path.read_text(encoding="utf-8")


def require_phrase(text: str, phrase: str, label: str) -> None:
    if phrase not in text:
        fail(f"{label} missing required phrase: {phrase}")


def require_false(record: dict, key: str) -> None:
    if key in record and record.get(key) is not False:
        fail(f"state record {key} must be false")


def main() -> None:
    state = json.loads(require_file(STATE_PATH))
    record = state.get("bdp_003e8_archive_writer_contract_boundary_review")
    if not isinstance(record, dict):
        fail("missing bdp_003e8_archive_writer_contract_boundary_review state record")

    if record.get("phase") != "BDP-003E.8":
        fail("BDP-003E.8 state record has wrong phase")
    if record.get("status") != "complete":
        fail("BDP-003E.8 state record must be complete")
    if record.get("next_step") != EXPECTED_NEXT_STEP:
        fail("BDP-003E.8 state record must preserve phase-local next step")

    for key in [
        "implementation_approved",
        "persistence_approved",
        "writer_implemented",
        "archive_folder_created",
        "local_files_written",
        "frontend_archive_controls_approved",
        "backend_services_approved",
        "adapter_endpoints_approved",
        "database_migration_approved",
        "database_tables_approved",
        "evidence_promotion_approved",
        "citations_created",
        "concept_relations_created",
        "interpretations_created",
        "buchanan_claims_created",
    ]:
        require_false(record, key)

    doc = require_file(DOC_PATH)
    for phrase in [
        "BDP-003E.8",
        "Implementation is not approved",
        "archive writer contract boundary review",
        EXPECTED_NEXT_STEP,
    ]:
        require_phrase(doc, phrase, "BDP-003E.8 doc")

    handover = require_file(HANDOVER_PATH)
    require_phrase(handover, "BDP-003E.8", "handover")
    require_phrase(handover, EXPECTED_NEXT_STEP, "handover")

    print("[OK] BDP-003E.8 archive writer contract boundary review verified")


if __name__ == "__main__":
    main()
