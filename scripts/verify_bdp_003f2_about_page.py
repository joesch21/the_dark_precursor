#!/usr/bin/env python3
'''Verify BDP-003F.2 About page for The Dark Precursor.'''

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
FRONTEND_PATH = ROOT / "frontend" / "dark_precursor.py"
CSS_PATH = ROOT / "frontend" / "styles" / "dark_precursor.css"
DOC_PATH = ROOT / "docs" / "BDP_003F2_ABOUT_PAGE.md"

STATE_KEY = "bdp_003f2_about_page"
EXPECTED_NEXT_STEP = (
    "BDP-003F.3 — Review The Dark Precursor About page in the running frontend "
    "before further public-facing explanation changes."
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
        "phase": "BDP-003F.2",
        "status": "complete",
        "controlled_slice": "frontend_explanatory_ux_only",
        "implementation_type": "about_page",
        "next_step": EXPECTED_NEXT_STEP,
    }
    for key, expected in expected_pairs.items():
        if record.get(key) != expected:
            fail(f"{STATE_KEY}.{key} expected {expected!r}, got {record.get(key)!r}")

    for key in [
        "frontend_ux_changed",
        "about_page_added",
        "about_sidebar_control_added",
        "public_explanation_added",
        "governance_boundary_visible",
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
        "BDP-003F.2 — About page",
        "def render_about_page",
        "About The Dark Precursor",
        "dark_precursor_view",
        "Return to concept stage",
        "It separates atmosphere from authority",
        "does not claim to think like Ian Buchanan",
        "generated synthesis",
        "evidence authority",
    ]:
        require_phrase(frontend, phrase, "frontend")

    css = require_file(CSS_PATH)
    for phrase in [
        "BDP-003F.2 — About page",
        ".dp-about-shell",
        ".dp-about-panel",
        ".dp-about-title",
        ".dp-about-pullquote",
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
            fail(f"banned backend/evidence phrase found in About page slice: {phrase}")

    doc = require_file(DOC_PATH)
    for phrase in [
        "BDP-003F.2",
        "About Page",
        "frontend explanatory UX only",
        "does not claim to think like Ian Buchanan",
        "generated synthesis",
        "evidence authority",
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
        require_phrase(doc, phrase, "BDP-003F.2 doc")

    handover = require_file(HANDOVER_PATH)
    require_phrase(handover, "BDP-003F.2", "handover")
    require_phrase(handover, EXPECTED_NEXT_STEP, "handover")

    print("[OK] BDP-003F.2 About page verified")


if __name__ == "__main__":
    main()
