#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


STATE_KEY = "bdp_003e8_archive_writer_contract_boundary_review"
EXPECTED_NEXT_STEP = "BDP-003E.9 — Decide local reviewed concept card archive writer implementation readiness, without implementation."

STATE_PATH = Path("BUCHANAN_SYSTEM_STATE.json")
DOC_PATH = Path("docs/BDP_003E8_ARCHIVE_WRITER_CONTRACT_BOUNDARY_REVIEW.md")
E7_DOC_PATH = Path("docs/BDP_003E7_LOCAL_REVIEWED_CONCEPT_CARD_ARCHIVE_WRITER_CONTRACT.md")
HANDOVER_PATH = Path("BUCHANAN_THREAD_HANDOVER.md")


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
        fail(f"state record expected {key}=false")


def ensure_no_banned_implementation_paths() -> None:
    banned_paths = [
        Path("frontend/local_reviewed_concept_card_archive.py"),
        Path("backend/services/local_reviewed_concept_card_archive.py"),
        Path("backend/routes/local_reviewed_concept_card_archive.py"),
        Path("scripts/write_local_reviewed_concept_card_archive.py"),
        Path("data/local_reviewed_concept_card_archive"),
        Path("data/reviewed_concept_card_archive"),
        Path("archive/local_reviewed_concept_card_archive"),
    ]
    existing = [str(path) for path in banned_paths if path.exists()]
    if existing:
        fail(f"unexpected implementation path(s) present: {existing}")

    for sql_path in list(Path(".").glob("**/*.sql")):
        lowered = str(sql_path).lower()
        if "003e8" in lowered or "reviewed_concept_card_archive_writer" in lowered:
            fail(f"unexpected SQL implementation artifact present: {sql_path}")


def main() -> None:
    state = json.loads(require_file(STATE_PATH))
    record = state.get(STATE_KEY)
    if not isinstance(record, dict):
        fail(f"missing state record: {STATE_KEY}")

    if record.get("status") != "complete":
        fail("BDP-003E.8 state status must be complete")
    if record.get("controlled_slice") != "review_only_writer_contract_boundary":
        fail("BDP-003E.8 controlled_slice mismatch")
    if record.get("next_step") != EXPECTED_NEXT_STEP:
        fail("BDP-003E.8 next_step mismatch")
    if record.get("review_output") != str(DOC_PATH):
        fail("BDP-003E.8 review_output mismatch")
    if record.get("verifier") != "scripts/verify_bdp_003e8_archive_writer_contract_boundary_review.py":
        fail("BDP-003E.8 verifier path mismatch")

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
        "Archive Writer Contract Boundary Review",
        "review phase only",
        "Implementation is not approved",
        "No persistence implementation",
        "No writer implementation",
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
        "suitable as a future implementation boundary",
        EXPECTED_NEXT_STEP,
    ]:
        require_phrase(doc, phrase, "BDP-003E.8 doc")

    e7_doc = require_file(E7_DOC_PATH)
    require_phrase(e7_doc, "BDP-003E.8 Follow-up Boundary Review Note", "BDP-003E.7 doc")
    require_phrase(e7_doc, "Implementation is not approved", "BDP-003E.7 doc follow-up")

    handover = require_file(HANDOVER_PATH)
    require_phrase(handover, "BDP-003E.8 — Local Reviewed Concept Card Archive Writer Contract Boundary Review", "handover")
    require_phrase(handover, "Implementation is not approved", "handover")
    require_phrase(handover, EXPECTED_NEXT_STEP, "handover")

    ensure_no_banned_implementation_paths()

    print("[OK] BDP-003E.8 archive writer contract boundary review verified")


if __name__ == "__main__":
    main()
