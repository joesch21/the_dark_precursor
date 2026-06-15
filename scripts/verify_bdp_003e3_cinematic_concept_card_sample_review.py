#!/usr/bin/env python3
"""
BDP-003E.3 — Cinematic concept card sample review verifier.

This verifier checks that BDP-003E.3 remains a review-only governance gate.
It must not add database persistence, adapter invocation, backend services, or
evidence-spine promotion.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

APP = ROOT / "frontend" / "dark_precursor.py"
CSS = ROOT / "frontend" / "styles" / "dark_precursor.css"
DOC = ROOT / "docs" / "BDP_003E3_CINEMATIC_CONCEPT_CARD_SAMPLE_REVIEW.md"
DOC_E2 = ROOT / "docs" / "BDP_003E2_CINEMATIC_CONCEPT_CARD_EXPORT_DRAFT.md"
STATE = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER = ROOT / "BUCHANAN_THREAD_HANDOVER.md"

required = [APP, CSS, DOC, DOC_E2, STATE, HANDOVER]
missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
if missing:
    raise SystemExit(f"[FAIL] Missing required files: {missing}")

app = APP.read_text(encoding="utf-8")
css = CSS.read_text(encoding="utf-8")
doc = DOC.read_text(encoding="utf-8")
doc_e2 = DOC_E2.read_text(encoding="utf-8")
state = json.loads(STATE.read_text(encoding="utf-8"))
handover = HANDOVER.read_text(encoding="utf-8")

record = state.get("bdp_003e3_cinematic_concept_card_sample_review", {})

runtime_forbidden = [
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
    "doc_exists": DOC.exists(),
    "doc_status": "**Status:** Implemented / verified" in doc,
    "review_only": "Review-only governance gate" in doc,
    "required_sample_cases": "E3-S1" in doc and "E3-S2" in doc and "E3-S3" in doc,
    "minimum_fields_listed": "schema_version" in doc and "response_markdown" in doc and "blocked_actions" in doc,
    "generated_not_evidence": "Generated cinematic concept cards remain not evidence" in doc,
    "no_persistence_approval": "It does not approve:" in doc and "Database persistence" in doc,
    "not_ready_for_persistence": "not yet ready" in doc and "persistence or adapter connection" in doc,
    "next_e4_doc": "BDP-003E.4 — Decide concept card persistence readiness from reviewed samples only." in doc,
    "e2_review_note": "BDP-003E.3 Review Note" in doc_e2,
    "app_export_still_present": "def build_cinematic_concept_card_export" in app,
    "app_downloads_still_present": "Download concept card draft (.md)" in app and "Download concept card data (.json)" in app,
    "state_recorded": bool(record),
    "state_status_complete": record.get("status") == "complete",
    "state_review_only": record.get("authority") == "review_only_no_runtime_change",
    "state_no_database": record.get("database_mutation") is False,
    "state_no_backend": record.get("backend_service") is False,
    "state_no_adapter": record.get("adapter_invocation") is False,
    "state_no_persistence": record.get("persistence_approved") is False,
    "state_no_evidence": record.get("evidence_spine_change") is False,
    "state_next_e4": "BDP-003E.4" in state.get("next_recommended_step", ""),
    "handover_recorded": "BDP-003E.3" in handover and "sample review" in handover.lower(),
    "no_runtime_forbidden": not any(pattern in app for pattern in runtime_forbidden),
}

failed = [name for name, ok in checks.items() if not ok]
if failed:
    print("=== BDP-003E.3 verifier failures ===")
    for name in failed:
        print(f"[FAIL] {name}")
    raise SystemExit(1)

print("[OK] BDP-003E.3 cinematic concept card sample review verified")
