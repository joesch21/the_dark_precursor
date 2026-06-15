#!/usr/bin/env python3
"""Verify BDP-003F.1 teleprompter narrator stage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
FRONTEND_PATH = ROOT / "frontend" / "dark_precursor.py"
CSS_PATH = ROOT / "frontend" / "styles" / "dark_precursor.css"
DOC_PATH = ROOT / "docs" / "BDP_003F1_TELEPROMPTER_NARRATOR_STAGE.md"

STATE_KEY = "bdp_003f1_teleprompter_narrator_stage"
EXPECTED_NEXT_STEP = (
    "BDP-003F.2 — Review teleprompter narrator stage in the running frontend "
    "before further cinematic UX changes."
)


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def require_file(path: Path) -> str:
    if not path.exists():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text()


def require_phrase(text: str, phrase: str, label: str) -> None:
    if phrase not in text:
        fail(f"{label} missing required phrase: {phrase}")


def require_false(record: dict, key: str) -> None:
    if record.get(key) is not False:
        fail(f"{STATE_KEY}.{key} must be false")


def require_true(record: dict, key: str) -> None:
    if record.get(key) is not True:
        fail(f"{STATE_KEY}.{key} must be true")


def main() -> None:
    state = json.loads(require_file(STATE_PATH))
    record = state.get(STATE_KEY)
    if not isinstance(record, dict):
        fail(f"missing state record: {STATE_KEY}")

    expected_pairs = {
        "phase": "BDP-003F.1",
        "status": "complete",
        "controlled_slice": "frontend_cinematic_narrator_ux_only",
        "implementation_type": "teleprompter_narrator_stage",
        "next_step": EXPECTED_NEXT_STEP,
    }
    for key, expected in expected_pairs.items():
        if record.get(key) != expected:
            fail(f"{STATE_KEY}.{key} expected {expected!r}, got {record.get(key)!r}")

    for key in [
        "frontend_ux_changed",
        "teleprompter_stage_added",
        "narrator_scrolls_upward",
        "uses_existing_reveal_path",
        "reduced_motion_guard_preserved",
    ]:
        require_true(record, key)

    for key in [
        "backend_services_added",
        "adapter_endpoints_added",
        "database_tables_added",
        "sql_migrations_added",
        "archive_workflow_expanded",
        "evidence_promotion_added",
        "citations_created",
        "concept_relations_created",
        "interpretations_created",
        "buchanan_claims_created",
    ]:
        require_false(record, key)

    frontend = require_file(FRONTEND_PATH)
    for phrase in [
        "def teleprompter_duration_seconds",
        "BDP-003F.1 — teleprompter narrator stage",
        "dp-teleprompter-stage",
        "dp-teleprompter-track",
        "--dp-teleprompter-duration",
        "THE NARRATOR SPEAKS",
        "markdown_to_stage_html(text)",
    ]:
        require_phrase(frontend, phrase, "frontend")

    css = require_file(CSS_PATH)
    for phrase in [
        "BDP-003F.1 — teleprompter narrator stage",
        ".dp-teleprompter-stage",
        ".dp-teleprompter-track",
        "@keyframes dpTeleprompterScroll",
        "translateY",
        "prefers-reduced-motion",
    ]:
        require_phrase(css, phrase, "CSS")

    for phrase in [
        "CREATE TABLE",
        "INSERT INTO citations",
        "INSERT INTO concept_relations",
        "INSERT INTO interpretations",
        "psycopg",
    ]:
        if phrase in frontend or phrase in css:
            fail(f"banned backend/evidence phrase found in frontend UX slice: {phrase}")

    doc = require_file(DOC_PATH)
    for phrase in [
        "BDP-003F.1",
        "Teleprompter Narrator Stage",
        "frontend cinematic narrator UX only",
        "scrolls upward",
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
        require_phrase(doc, phrase, "BDP-003F.1 doc")

    handover = require_file(HANDOVER_PATH)
    require_phrase(handover, "BDP-003F.1", "handover")
    require_phrase(handover, EXPECTED_NEXT_STEP, "handover")

    print("[OK] BDP-003F.1 teleprompter narrator stage verified")


if __name__ == "__main__":
    main()
