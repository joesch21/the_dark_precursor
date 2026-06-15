#!/usr/bin/env python3
"""Verify BDP-003E.11 local reviewed concept card archive writer."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
DOC_PATH = ROOT / "docs/BDP_003E11_LOCAL_REVIEWED_CONCEPT_CARD_ARCHIVE_WRITER_IMPLEMENTATION.md"
WRITER_PATH = ROOT / "scripts/local_reviewed_concept_card_archive_writer.py"
EXPECTED_NEXT_STEP = "BDP-003E.12 — Review local reviewed concept card archive writer output against sample payloads before UI integration."
RECORD_KEY = "bdp_003e11_local_reviewed_concept_card_archive_writer"


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


def require_true(record: dict, key: str) -> None:
    if record.get(key) is not True:
        fail(f"{RECORD_KEY}.{key} must be true")


def load_writer_module():
    spec = importlib.util.spec_from_file_location("local_reviewed_concept_card_archive_writer", WRITER_PATH)
    if spec is None or spec.loader is None:
        fail("could not load writer module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample_payload() -> dict:
    return {
        "schema_version": "bdp-003e5-local-reviewed-concept-card-archive-v1",
        "archive_record_id": "bdp_003e11_sample_body_without_organs",
        "review_status": "locally_reviewed",
        "reviewed_at": "2026-06-15T19:30:00+00:00",
        "reviewed_by": "operator",
        "concept": {"concept_id": "body_without_organs", "label": "Body without Organs"},
        "card": {
            "title": "Body without Organs",
            "summary": "Reviewed cinematic concept card sample for writer verification only.",
            "cinematic_prompt": "A dark cinematic abstraction of stratification and becoming.",
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


def assert_raises_archive_error(writer, payload: dict, archive_root: Path) -> None:
    try:
        writer.write_reviewed_concept_card_archive(payload, archive_root)
    except writer.ArchiveWriterError:
        return
    fail("expected ArchiveWriterError for invalid payload")


def verify_writer_behavior() -> None:
    writer = load_writer_module()
    payload = sample_payload()

    with tempfile.TemporaryDirectory(prefix="bdp_003e11_writer_") as temp_dir:
        archive_root = Path(temp_dir) / "archive"
        result = writer.write_reviewed_concept_card_archive(payload, archive_root)
        if result.get("created") is not True:
            fail("first write must create the archive file")
        target = Path(result.get("path", ""))
        if not target.exists():
            fail("archive file was not written inside temporary directory")
        if archive_root not in target.parents:
            fail("archive file was not written under explicit archive root")

        record = json.loads(target.read_text())
        if record.get("archive_writer_phase") != "BDP-003E.11":
            fail("archive record must preserve BDP-003E.11 writer phase")
        if record.get("integration_boundaries", {}).get("evidence_promotion") is not False:
            fail("archive record must not promote evidence")

        second = writer.write_reviewed_concept_card_archive(payload, archive_root)
        if second.get("created") is not False or second.get("idempotent") is not True:
            fail("second identical write must be idempotent")
        if second.get("sha256") != result.get("sha256"):
            fail("idempotent write must preserve sha256")

        unreviewed = sample_payload()
        unreviewed["review_status"] = "generated_draft"
        assert_raises_archive_error(writer, unreviewed, archive_root)

        promoted = sample_payload()
        promoted["governance"]["evidence_promotion_approved"] = True
        assert_raises_archive_error(writer, promoted, archive_root)

        traversal = sample_payload()
        traversal["archive_record_id"] = "../escape"
        assert_raises_archive_error(writer, traversal, archive_root)

        conflict = sample_payload()
        target.write_text("{}\n")
        assert_raises_archive_error(writer, conflict, archive_root)


def main() -> None:
    state = json.loads(require_file(STATE_PATH))
    record = state.get(RECORD_KEY)
    if not isinstance(record, dict):
        fail(f"missing state record: {RECORD_KEY}")

    if record.get("phase") != "BDP-003E.11":
        fail(f"{RECORD_KEY}.phase must be BDP-003E.11")
    if record.get("status") != "complete":
        fail(f"{RECORD_KEY}.status must be complete")
    if record.get("next_step") != EXPECTED_NEXT_STEP:
        fail(f"{RECORD_KEY}.next_step must be the expected E12 next step")

    for key in ["implementation_approved", "persistence_approved", "writer_implemented", "local_file_writer_implemented"]:
        require_true(record, key)

    for key in [
        "archive_folder_created",
        "repo_archive_records_written",
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

    doc = require_file(DOC_PATH)
    for phrase in [
        "BDP-003E.11",
        "local reviewed concept card archive writer",
        "behind safety gates",
        "Implementation approved only for the local writer",
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
        require_phrase(doc, phrase, "BDP-003E.11 doc")

    writer_text = require_file(WRITER_PATH)
    for forbidden in ["streamlit", "FastAPI", "psycopg", "psycopg2", "CREATE TABLE", "INSERT INTO"]:
        if forbidden in writer_text:
            fail(f"writer must not contain forbidden integration token: {forbidden}")

    handover = require_file(HANDOVER_PATH)
    require_phrase(handover, "BDP-003E.11", "handover")
    require_phrase(handover, EXPECTED_NEXT_STEP, "handover")

    verify_writer_behavior()
    print("[OK] BDP-003E.11 local reviewed concept card archive writer verified")


if __name__ == "__main__":
    main()
