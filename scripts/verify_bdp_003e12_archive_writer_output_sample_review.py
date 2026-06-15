#!/usr/bin/env python3
"""Verify BDP-003E.12 local reviewed archive writer output sample review."""
from __future__ import annotations

import importlib.util
import json
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
DOC_PATH = ROOT / "docs/BDP_003E12_ARCHIVE_WRITER_OUTPUT_SAMPLE_REVIEW.md"
E11_DOC_PATH = ROOT / "docs/BDP_003E11_LOCAL_REVIEWED_CONCEPT_CARD_ARCHIVE_WRITER_IMPLEMENTATION.md"
WRITER_PATH = ROOT / "scripts/local_reviewed_concept_card_archive_writer.py"
RECORD_KEY = "bdp_003e12_archive_writer_output_sample_review"
EXPECTED_NEXT_STEP = "BDP-003E.13 — Define UI integration contract for local reviewed concept card archive controls before wiring frontend."


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def require_file(path: Path) -> str:
    if not path.exists():
        fail(f"missing required file: {path}")
    return path.read_text()


def require_phrase(text: str, phrase: str, label: str) -> None:
    if phrase not in text:
        fail(f"{label} missing required phrase: {phrase}")


def require_false(record: dict[str, Any], key: str) -> None:
    if record.get(key) is not False:
        fail(f"{RECORD_KEY}.{key} must be false")


def require_true(record: dict[str, Any], key: str) -> None:
    if record.get(key) is not True:
        fail(f"{RECORD_KEY}.{key} must be true")


def load_writer_module() -> Any:
    if not WRITER_PATH.exists():
        fail(f"missing writer file: {WRITER_PATH}")
    spec = importlib.util.spec_from_file_location("local_reviewed_concept_card_archive_writer", WRITER_PATH)
    if spec is None or spec.loader is None:
        fail("could not load writer module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample_payload(record_id: str, concept_id: str, label: str) -> dict[str, Any]:
    return {
        "schema_version": "bdp-003e5-local-reviewed-concept-card-archive-v1",
        "archive_record_id": record_id,
        "review_status": "locally_reviewed",
        "reviewed_at": "2026-06-16T00:00:00+00:00",
        "reviewed_by": "operator-review",
        "concept": {
            "concept_id": concept_id,
            "label": label,
        },
        "card": {
            "title": f"Cinematic Concept Card — {label}",
            "summary": "Controlled reviewed sample payload used to verify local archive writer output shape.",
            "cinematic_prompt": "A dark cinematic field of conceptual forces, reviewed locally before archival output.",
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


def assert_writer_rejects(writer: Any, payload: dict[str, Any], archive_root: Path) -> None:
    try:
        writer.write_reviewed_concept_card_archive(payload, archive_root)
    except Exception as exc:  # noqa: BLE001 - verifier accepts writer domain errors
        if exc.__class__.__name__ == "ArchiveWriterError" or isinstance(exc, ValueError):
            return
        fail(f"writer raised unexpected exception type: {exc.__class__.__name__}: {exc}")
    fail("writer accepted an invalid sample payload")


def review_writer_output_against_samples() -> None:
    writer = load_writer_module()

    for name in [
        "validate_reviewed_concept_card",
        "build_archive_record",
        "archive_path_for",
        "write_reviewed_concept_card_archive",
    ]:
        if not hasattr(writer, name):
            fail(f"writer missing required function: {name}")

    samples = [
        sample_payload("bwo-reviewed-sample-card", "body_without_organs", "Body without Organs"),
        sample_payload("assemblage-reviewed-sample-card", "assemblage", "Assemblage"),
    ]

    with tempfile.TemporaryDirectory(prefix="bdp_003e12_writer_output_review_") as tmp:
        archive_root = Path(tmp)

        for payload in samples:
            result = writer.write_reviewed_concept_card_archive(payload, archive_root)
            if result.get("created") is not True:
                fail("first sample write must create a file")
            if result.get("idempotent") is not False:
                fail("first sample write must not be marked idempotent")

            output_path = Path(result.get("path", ""))
            if not output_path.exists():
                fail(f"writer did not create output path: {output_path}")
            if output_path.parent != archive_root:
                fail("writer output escaped temporary archive root")
            if output_path.name != f"{payload['archive_record_id']}.json":
                fail("writer output filename does not match safe archive record id")

            record = json.loads(output_path.read_text())
            if record.get("archive_schema_version") != "bdp-003e11-local-reviewed-concept-card-archive-record-v1":
                fail("archive record missing expected output schema version")
            if record.get("archive_writer_phase") != "BDP-003E.11":
                fail("archive record missing expected writer phase")
            if record.get("archive_writer_scope") != "local writer only":
                fail("archive record missing local writer only scope")

            boundaries = record.get("integration_boundaries")
            if not isinstance(boundaries, dict):
                fail("archive record missing integration_boundaries object")
            for key in [
                "frontend_archive_controls",
                "backend_services",
                "adapter_endpoints",
                "database_tables",
                "sql_migrations",
                "evidence_promotion",
                "citations",
                "concept_relations",
                "interpretations",
                "buchanan_specific_claims",
            ]:
                if boundaries.get(key) is not False:
                    fail(f"archive record boundary {key} must be false")

            reviewed = record.get("reviewed_concept_card")
            if reviewed != writer.validate_reviewed_concept_card(payload):
                fail("archive record did not preserve canonical reviewed payload")

            second = writer.write_reviewed_concept_card_archive(payload, archive_root)
            if second.get("created") is not False or second.get("idempotent") is not True:
                fail("repeat sample write must be idempotent")
            if second.get("sha256") != result.get("sha256"):
                fail("idempotent sample write must preserve digest")

        if len(list(archive_root.glob("*.json"))) != len(samples):
            fail("temporary output review wrote an unexpected number of JSON files")

        unreviewed = deepcopy(samples[0])
        unreviewed["review_status"] = "generated_draft"
        assert_writer_rejects(writer, unreviewed, archive_root)

        promoted = deepcopy(samples[0])
        promoted["archive_record_id"] = "bwo-reviewed-sample-card-promoted"
        promoted["governance"]["evidence_promotion_approved"] = True
        assert_writer_rejects(writer, promoted, archive_root)

        traversal = deepcopy(samples[0])
        traversal["archive_record_id"] = "../escape"
        assert_writer_rejects(writer, traversal, archive_root)


def main() -> None:
    state = json.loads(require_file(STATE_PATH))
    record = state.get(RECORD_KEY)
    if not isinstance(record, dict):
        fail(f"missing state record: {RECORD_KEY}")

    if record.get("phase") != "BDP-003E.12":
        fail(f"{RECORD_KEY}.phase must be BDP-003E.12")
    if record.get("status") != "complete":
        fail(f"{RECORD_KEY}.status must be complete")
    if record.get("next_step") != EXPECTED_NEXT_STEP:
        fail(f"{RECORD_KEY}.next_step must be the expected E13 next step")

    for key in [
        "writer_output_reviewed",
        "sample_payloads_reviewed",
        "temporary_directory_review_only",
    ]:
        require_true(record, key)

    for key in [
        "ui_integration_approved",
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
        "repo_archive_records_written",
    ]:
        require_false(record, key)

    doc = require_file(DOC_PATH)
    for phrase in [
        "BDP-003E.12",
        "writer output sample review",
        "UI integration is not approved",
        "temporary directory only",
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
        require_phrase(doc, phrase, "BDP-003E.12 doc")

    e11_doc = require_file(E11_DOC_PATH)
    require_phrase(e11_doc, "BDP-003E.12 Follow-up Output Review Note", "BDP-003E.11 doc")
    require_phrase(e11_doc, EXPECTED_NEXT_STEP, "BDP-003E.11 doc")

    handover = require_file(HANDOVER_PATH)
    require_phrase(handover, "BDP-003E.12", "handover")
    require_phrase(handover, EXPECTED_NEXT_STEP, "handover")

    review_writer_output_against_samples()
    print("[OK] BDP-003E.12 archive writer output sample review verified")


if __name__ == "__main__":
    main()
