#!/usr/bin/env python3
# Verifier for BDP-003E.5.
#
# This repaired verifier checks BDP-003E.5 against its own phase record and
# documentation. It intentionally does not depend on the mutable global
# current-next-step field, because later phases are allowed to advance that field.

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_PATH = ROOT / "docs" / "BDP_003E5_LOCAL_REVIEWED_CONCEPT_CARD_ARCHIVE_SCHEMA_CANDIDATE.md"
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"

PHASE_KEY = "bdp_003e5_local_reviewed_concept_card_archive_schema_candidate"
PHASE = "BDP-003E.5"
EXPECTED_NEXT = "BDP-003E.6 — Review local reviewed concept card archive schema candidate against exported samples before implementation."


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


def main() -> None:
    doc = read(DOC_PATH)
    handover = read(HANDOVER_PATH)

    try:
        state = json.loads(read(STATE_PATH))
    except json.JSONDecodeError as exc:
        fail(f"BUCHANAN_SYSTEM_STATE.json is invalid JSON: {exc}")

    require_contains(
        "BDP-003E.5 doc",
        doc,
        [
            "BDP-003E.5",
            "local reviewed",
            "archive schema",
            "schema candidate",
            "implementation",
            "not approved",
        ],
    )

    require_contains(
        "handover",
        handover,
        [
            "BDP-003E.5",
            "local reviewed",
            "archive schema",
        ],
    )

    record = state.get(PHASE_KEY)
    if not isinstance(record, dict):
        fail(f"state missing {PHASE_KEY} record")

    require_contains(
        "state phase record",
        json.dumps(record, ensure_ascii=False),
        [
            PHASE,
            "local",
            "reviewed",
            "archive",
            "schema",
        ],
    )

    # E5's next step must be preserved inside its own phase record. Do not
    # inspect global current_next_step here; BDP-003E.6 and later phases may
    # legitimately advance the global current step.
    phase_next_dump = json.dumps(record, ensure_ascii=False)
    if EXPECTED_NEXT not in phase_next_dump:
        fail("E5 phase record does not preserve its own next-step chain to BDP-003E.6")

    for key in (
        "implementation_approved",
        "persistence_approved",
        "frontend_archive_controls_approved",
        "backend_services_approved",
        "database_migration_approved",
        "local_writer_approved",
    ):
        value = record.get(key)
        if value is not None and value is not False:
            fail(f"E5 phase record must not approve {key}")

    print("[OK] BDP-003E.5 local reviewed archive schema candidate verified")


if __name__ == "__main__":
    main()
