#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


STATE_KEY = "bdp_003e7_local_reviewed_concept_card_archive_writer_contract"
EXPECTED_NEXT_STEP = "BDP-003E.8 — Review local reviewed concept card archive writer contract against archive boundaries before implementation."

STATE_PATH = Path("BUCHANAN_SYSTEM_STATE.json")
DOC_PATH = Path("docs/BDP_003E7_LOCAL_REVIEWED_CONCEPT_CARD_ARCHIVE_WRITER_CONTRACT.md")
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


def main() -> None:
    state = json.loads(require_file(STATE_PATH))
    record = state.get(STATE_KEY)
    if not isinstance(record, dict):
        fail(f"missing state record: {STATE_KEY}")

    if record.get("status") != "complete":
        fail("BDP-003E.7 state status must be complete")
    if record.get("controlled_slice") != "contract_only_writer_boundary":
        fail("BDP-003E.7 controlled_slice mismatch")
    if record.get("next_step") != EXPECTED_NEXT_STEP:
        fail("BDP-003E.7 phase-local next_step mismatch")

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
        "buchanan_claims_created",
    ]:
        require_false(record, key)

    doc = require_file(DOC_PATH)
    for phrase in [
        "BDP-003E.7",
        "Implementation is not approved",
        "writer contract only",
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
    ]:
        require_phrase(doc, phrase, "BDP-003E.7 doc")

    handover = require_file(HANDOVER_PATH)
    require_phrase(handover, "BDP-003E.7", "handover")
    require_phrase(handover, EXPECTED_NEXT_STEP, "handover")

    print("[OK] BDP-003E.7 local reviewed concept card archive writer contract verified")


if __name__ == "__main__":
    main()
