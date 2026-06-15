#!/usr/bin/env python3
"""
BDP-003E.2 — Read-only cinematic concept card export draft verifier.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "frontend" / "dark_precursor.py"
CSS = ROOT / "frontend" / "styles" / "dark_precursor.css"
DOC = ROOT / "docs" / "BDP_003E2_CINEMATIC_CONCEPT_CARD_EXPORT_DRAFT.md"
DOC_E1 = ROOT / "docs" / "BDP_003E_CINEMATIC_CONCEPT_CARD_PERSISTENCE_CONTRACT.md"
STATE = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER = ROOT / "BUCHANAN_THREAD_HANDOVER.md"

required = [APP, CSS, DOC, DOC_E1, STATE, HANDOVER]
missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
if missing:
    raise SystemExit(f"[FAIL] Missing required files: {missing}")

app = APP.read_text(encoding="utf-8")
css = CSS.read_text(encoding="utf-8")
doc = DOC.read_text(encoding="utf-8")
doc_e1 = DOC_E1.read_text(encoding="utf-8")
state_text = STATE.read_text(encoding="utf-8")
handover = HANDOVER.read_text(encoding="utf-8")
state = json.loads(state_text)

forbidden_runtime_patterns = [
    "psycopg",
    "sqlite3",
    "CREATE TABLE",
    "INSERT INTO",
    "ALTER TABLE",
    "requests.post(",
    "requests.get(",
    "subprocess.",
    "FastAPI(",
    "Flask(",
]

checks = {
    "schema_constant": "bdp_003e2_cinematic_concept_card_export_draft_v1" in app,
    "authority_label": "provisional_cinematic_synthesis_not_evidence" in app,
    "download_only_label": "download_only_no_database_mutation" in app,
    "build_function": "def build_cinematic_concept_card_export" in app,
    "markdown_formatter": "def format_concept_card_markdown" in app,
    "render_export_dock": "def render_cinematic_concept_card_export_dock" in app,
    "markdown_download": "Download concept card draft (.md)" in app and "text/markdown" in app,
    "json_download": "Download concept card data (.json)" in app and "application/json" in app,
    "download_button_only": "st.download_button" in app,
    "generated_not_evidence_field": '"generated_material_is_evidence": False' in app,
    "database_false_field": '"database_mutation": False' in app,
    "adapter_false_field": '"adapter_invocation": False' in app,
    "promotion_false_field": '"promotion_allowed": False' in app,
    "blocked_actions": "blocked_actions" in app and "automatic_evidence_promotion" in app,
    "session_only_source": "last_dark_precursor_response" in app,
    "css_marker": "BDP-003E.2" in css,
    "doc_status": "**Status:** Implemented / verified" in doc,
    "doc_download_only": "local Markdown / JSON download" in doc,
    "doc_no_database": "This is not database persistence" in doc,
    "doc_generated_not_evidence": "Generated cinematic concept cards are not evidence" in doc,
    "doc_no_server_persist": "Persist files on the server" in doc,
    "e1_note": "BDP-003E.2 Implementation Note" in doc_e1,
    "state_recorded": "bdp_003e2_cinematic_concept_card_export_draft" in state,
    "state_no_db": state.get("bdp_003e2_cinematic_concept_card_export_draft", {}).get("database_mutation") is False,
    "state_no_backend": state.get("bdp_003e2_cinematic_concept_card_export_draft", {}).get("backend_service") is False,
    "state_no_adapter": state.get("bdp_003e2_cinematic_concept_card_export_draft", {}).get("adapter_invocation") is False,
    "state_next_e3": "BDP-003E.3" in state.get("next_recommended_step", ""),
    "handover_recorded": "BDP-003E.2" in handover and "read-only cinematic concept card export draft" in handover.lower(),
    "no_forbidden_runtime_patterns": not any(pattern in app for pattern in forbidden_runtime_patterns),
}

failed = [name for name, ok in checks.items() if not ok]
if failed:
    print("=== BDP-003E.2 verifier failures ===")
    for name in failed:
        print(f"[FAIL] {name}")
    raise SystemExit(1)

print("[OK] BDP-003E.2 read-only cinematic concept card export draft verified")
