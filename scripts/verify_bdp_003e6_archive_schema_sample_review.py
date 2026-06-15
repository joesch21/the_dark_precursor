#!/usr/bin/env python3
# Verifier for BDP-003E.6.
#
# Proves that BDP-003E.6 is a review-only phase:
# - the archive schema candidate was compared against exported samples,
# - implementation remains blocked,
# - the next step is a writer contract boundary only.

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_PATH = ROOT / "docs" / "BDP_003E6_ARCHIVE_SCHEMA_SAMPLE_REVIEW.md"
E5_DOC_PATH = ROOT / "docs" / "BDP_003E5_LOCAL_REVIEWED_CONCEPT_CARD_ARCHIVE_SCHEMA_CANDIDATE.md"
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"

NEXT_STEP = "BDP-003E.7 — Define local reviewed concept card archive writer contract only, without implementation."


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
    e5_doc = read(E5_DOC_PATH)
    handover = read(HANDOVER_PATH)

    try:
        state = json.loads(read(STATE_PATH))
    except json.JSONDecodeError as exc:
        fail(f"BUCHANAN_SYSTEM_STATE.json is invalid JSON: {exc}")

    require_contains(
        "BDP-003E.6 doc",
        doc,
        [
            "BDP-003E.6",
            "Review only",
            "BDP-003E.3 exported cinematic concept card sample cases",
            "BDP-003E.5 local reviewed concept card archive schema candidate",
            "Sample Comparison Method",
            "suitable for reviewed sample comparison",
            "Implementation is not approved",
            NEXT_STEP,
        ],
    )

    require_contains(
        "BDP-003E.6 doc governance boundary",
        doc,
        [
            "does not",
            "implement persistence",
            "add frontend archive buttons",
            "add backend services",
            "add database tables or SQL migrations",
            "add local file writers",
            "promote generated concept cards into evidence",
            "create citations",
            "create concept relations",
            "create interpretations",
            "create Buchanan-specific claims",
        ],
    )

    require_not_contains(
        "BDP-003E.6 doc",
        doc,
        [
            "implementation is approved",
            "persistence is approved",
            "archive writer implemented",
            "frontend archive button implemented",
            "database migration added",
        ],
    )

    require_contains(
        "BDP-003E.5 follow-up note",
        e5_doc,
        [
            "BDP-003E.6 Follow-up Review Note",
            "suitable for reviewed sample comparison",
            "implementation is still not approved",
            NEXT_STEP,
        ],
    )

    require_contains(
        "handover",
        handover,
        [
            "BDP-003E.6",
            "archive schema sample review",
            "review-only",
            "implementation remains blocked",
            NEXT_STEP,
        ],
    )

    record = state.get("bdp_003e6_archive_schema_sample_review")
    if not isinstance(record, dict):
        fail("state missing bdp_003e6_archive_schema_sample_review record")

    expected_false_keys = [
        "implementation_approved",
        "persistence_approved",
        "frontend_archive_controls_approved",
        "backend_services_approved",
        "database_migration_approved",
        "local_writer_approved",
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
            "BDP-003E.6",
            "review_only_schema_candidate_against_exported_samples",
            "suitable for reviewed sample comparison",
            "BDP-003E.3",
            "BDP-003E.5",
            NEXT_STEP,
        ],
    )

    state_dump = json.dumps(state, ensure_ascii=False)
    if NEXT_STEP not in state_dump:
        fail("state does not record BDP-003E.7 as the next step")

    print("[OK] BDP-003E.6 archive schema sample review verified")


if __name__ == "__main__":
    main()
