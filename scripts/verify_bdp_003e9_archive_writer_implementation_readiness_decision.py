#!/usr/bin/env python3
"""Verify BDP-003E.9 archive writer implementation readiness decision."""
from __future__ import annotations

import json
from pathlib import Path

STATE_PATH = Path("BUCHANAN_SYSTEM_STATE.json")
HANDOVER_PATH = Path("BUCHANAN_THREAD_HANDOVER.md")
E8_DOC_PATH = Path("docs/BDP_003E8_ARCHIVE_WRITER_CONTRACT_BOUNDARY_REVIEW.md")
DOC_PATH = Path("docs/BDP_003E9_ARCHIVE_WRITER_IMPLEMENTATION_READINESS_DECISION.md")
EXPECTED_NEXT_STEP = "BDP-003E.10 — Define local reviewed concept card archive implementation boundary and safety gates before writing code."


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
    if record.get(key) is not False:
        fail(f"state record {key} must be false")


def require_true(record: dict, key: str) -> None:
    if record.get(key) is not True:
        fail(f"state record {key} must be true")


def main() -> None:
    state = json.loads(require_file(STATE_PATH))
    record = state.get("bdp_003e9_archive_writer_implementation_readiness_decision")
    if not isinstance(record, dict):
        fail("missing bdp_003e9_archive_writer_implementation_readiness_decision state record")

    if record.get("phase") != "BDP-003E.9":
        fail("BDP-003E.9 state record has wrong phase")
    if record.get("status") != "complete":
        fail("BDP-003E.9 state record must be complete")
    if record.get("controlled_slice") != "readiness_decision_only":
        fail("BDP-003E.9 controlled slice must be readiness_decision_only")
    if record.get("next_step") != EXPECTED_NEXT_STEP:
        fail("BDP-003E.9 state record has wrong next step")

    require_true(record, "implementation_readiness_decided")
    require_true(record, "ready_for_future_implementation_boundary")

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
        "database_migration_approved",
        "evidence_promotion_approved",
        "citations_created",
        "concept_relations_created",
        "interpretations_created",
        "buchanan_claims_created",
    ]:
        require_false(record, key)

    doc = require_file(DOC_PATH)
    for phrase in [
        "BDP-003E.9",
        "implementation readiness decision",
        "readiness-decision only",
        "ready for a future implementation-boundary phase",
        "Implementation is not approved",
        "No writer implementation",
        "No persistence implementation",
        "No frontend archive controls",
        "No backend services",
        "No adapter endpoints",
        "No database tables",
        "No SQL migrations",
        "No archive folders",
        "No local files written",
        "No evidence promotion",
        "No citations",
        "No concept relations",
        "No interpretations",
        "No Buchanan-specific claims",
        EXPECTED_NEXT_STEP,
    ]:
        require_phrase(doc, phrase, "BDP-003E.9 doc")

    handover = require_file(HANDOVER_PATH)
    require_phrase(handover, "BDP-003E.9", "handover")
    require_phrase(handover, EXPECTED_NEXT_STEP, "handover")

    e8_doc = require_file(E8_DOC_PATH)
    require_phrase(e8_doc, "BDP-003E.9 Follow-up Readiness Decision Note", "BDP-003E.8 doc")
    require_phrase(e8_doc, EXPECTED_NEXT_STEP, "BDP-003E.8 doc")

    print("[OK] BDP-003E.9 archive writer implementation readiness decision verified")


if __name__ == "__main__":
    main()
