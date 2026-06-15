#!/usr/bin/env python3
# Verifier for BDP-003E.7.
#
# Proves that BDP-003E.7 defines a writer contract only and does not
# implement persistence, a writer, an archive folder, frontend controls,
# backend services, database tables, evidence promotion, or Buchanan claims.

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_PATH = ROOT / "docs" / "BDP_003E7_LOCAL_REVIEWED_CONCEPT_CARD_ARCHIVE_WRITER_CONTRACT.md"
E6_DOC_PATH = ROOT / "docs" / "BDP_003E6_ARCHIVE_SCHEMA_SAMPLE_REVIEW.md"
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"

PHASE_KEY = "bdp_003e7_local_reviewed_concept_card_archive_writer_contract"
NEXT_STEP = "BDP-003E.8 — Review local reviewed concept card archive writer contract against archive boundaries before implementation."


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require_contains(label: str, text: str, needles: list[str]) -> None:
    lower = text.lower()
    for needle in needles:
        if needle.lower() not in lower:
            fail(f"{label} missing required phrase: {needle}")


def require_not_contains(label: str, text: str, needles: list[str]) -> None:
    lower = text.lower()
    for needle in needles:
        if needle.lower() in lower:
            fail(f"{label} contains forbidden implementation claim: {needle}")


def main() -> None:
    doc = read(DOC_PATH)
    e6_doc = read(E6_DOC_PATH)
    handover = read(HANDOVER_PATH)

    try:
        state = json.loads(read(STATE_PATH))
    except json.JSONDecodeError as exc:
        fail(f"BUCHANAN_SYSTEM_STATE.json is invalid JSON: {exc}")

    require_contains(
        "BDP-003E.7 doc",
        doc,
        [
            "BDP-003E.7",
            "Writer Contract",
            "Contract only",
            "Implementation is not approved",
            "BDP-003E.5 local reviewed archive schema candidate",
            "BDP-003E.6 archive schema sample review",
            "Writer Contract Scope",
            "Contract Inputs",
            "Required Refusals",
            "Contract Output Shape",
            "local reviewed sample material only",
            NEXT_STEP,
        ],
    )

    require_contains(
        "BDP-003E.7 governance boundary",
        doc,
        [
            "does not",
            "implement a writer",
            "create archive folders",
            "write local files",
            "add frontend archive buttons",
            "add backend services",
            "add adapter endpoints",
            "add database tables",
            "add SQL migrations",
            "persist generated concept cards",
            "promote generated concept cards into evidence",
            "create citations",
            "create concept relations",
            "create interpretations",
            "create Buchanan-specific claims",
        ],
    )

    require_not_contains(
        "BDP-003E.7 doc",
        doc,
        [
            "implementation is approved",
            "persistence is approved",
            "writer implemented",
            "archive writer implemented",
            "frontend archive button implemented",
            "backend service implemented",
            "database migration added",
            "sql migration added",
            "archive folder created",
            "local file writer added",
        ],
    )

    require_contains(
        "BDP-003E.6 follow-up note",
        e6_doc,
        [
            "BDP-003E.7 Follow-up Contract Note",
            "writer contract only",
            "Implementation is not approved",
            NEXT_STEP,
        ],
    )

    require_contains(
        "handover",
        handover,
        [
            "BDP-003E.7",
            "writer contract",
            "contract-only",
            "implementation remains blocked",
            NEXT_STEP,
        ],
    )

    record = state.get(PHASE_KEY)
    if not isinstance(record, dict):
        fail(f"state missing {PHASE_KEY} record")

    expected_false_keys = [
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
    ]

    for key in expected_false_keys:
        if record.get(key) is not False:
            fail(f"state record must keep {key}=False")

    require_contains(
        "state record",
        json.dumps(record, ensure_ascii=False),
        [
            "BDP-003E.7",
            "contract_only_writer_boundary",
            "writer contract only",
            "Implementation is not approved",
            "BDP-003E.5",
            "BDP-003E.6",
            NEXT_STEP,
        ],
    )

    global_dump = json.dumps(state, ensure_ascii=False)
    if NEXT_STEP not in global_dump:
        fail("state does not record BDP-003E.8 as the next safe step")

    print("[OK] BDP-003E.7 local reviewed concept card archive writer contract verified")


if __name__ == "__main__":
    main()
