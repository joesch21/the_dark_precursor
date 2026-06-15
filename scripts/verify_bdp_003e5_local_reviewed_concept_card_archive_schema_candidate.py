#!/usr/bin/env python3
"""
BDP-003E.5 — Local reviewed concept card archive schema candidate verifier.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BDP_003E5_LOCAL_REVIEWED_CONCEPT_CARD_ARCHIVE_SCHEMA_CANDIDATE.md"
DOC_E4 = ROOT / "docs" / "BDP_003E4_CONCEPT_CARD_PERSISTENCE_READINESS_DECISION.md"
STATE = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
APP = ROOT / "frontend" / "dark_precursor.py"

required = [DOC, DOC_E4, STATE, HANDOVER, APP]
missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
if missing:
    raise SystemExit(f"[FAIL] Missing required files: {missing}")

doc = DOC.read_text(encoding="utf-8")
doc_e4 = DOC_E4.read_text(encoding="utf-8")
state = json.loads(STATE.read_text(encoding="utf-8"))
handover = HANDOVER.read_text(encoding="utf-8")
app = APP.read_text(encoding="utf-8")
record = state.get("bdp_003e5_local_reviewed_concept_card_archive_schema_candidate", {})

checks = {
    "doc_title": "BDP-003E.5 — Local Reviewed Concept Card Archive Schema Candidate" in doc,
    "doc_status": "**Status:** Implemented / verified" in doc,
    "schema_candidate_only": "schema_candidate_only = true" in doc,
    "no_frontend_impl": "No frontend implementation is added in BDP-003E.5" in doc,
    "no_backend_impl": "No backend implementation is added in BDP-003E.5" in doc,
    "no_runtime_impl": "No database migration, database table, file writer" in doc,
    "generated_not_evidence": "Generated material is not evidence" in doc,
    "record_schema_version": "bdp_003e5_local_reviewed_concept_card_archive_candidate_v1" in doc,
    "archive_record_id": "archive_record_id" in doc,
    "source_card_id": "source_card_id" in doc,
    "review_decision": "review_decision" in doc,
    "authority_label": "local_reviewed_archive_candidate_not_evidence" in doc,
    "evidence_promotion_false": '"evidence_promotion_allowed": false' in doc,
    "blocked_actions": "blocked_actions" in doc and "automatic_evidence_promotion" in doc,
    "e4_note": "BDP-003E.5 Schema Candidate Note" in doc_e4,
    "state_recorded": "bdp_003e5_local_reviewed_concept_card_archive_schema_candidate" in state,
    "state_schema_candidate_only": record.get("schema_candidate_only") is True,
    "state_frontend_false": record.get("frontend_change") is False,
    "state_backend_false": record.get("backend_service") is False,
    "state_db_false": record.get("database_mutation") is False,
    "state_sql_false": record.get("sql_migration") is False,
    "state_file_writer_false": record.get("file_writer") is False,
    "state_archive_impl_false": record.get("local_archive_implementation") is False,
    "state_adapter_false": record.get("adapter_invocation") is False,
    "state_evidence_false": record.get("evidence_spine_change") is False,
    "state_next_e6": "BDP-003E.6" in state.get("next_recommended_step", "") and "BDP-003E.6" in record.get("next_recommended_step", ""),
    "handover_recorded": "BDP-003E.5" in handover and "schema candidate only" in handover.lower(),
    "no_app_archive_writer": "archive_record_id" not in app and "local_reviewed_archive_candidate_not_evidence" not in app,
}

failed = [name for name, ok in checks.items() if not ok]
if failed:
    print("=== BDP-003E.5 verifier failures ===")
    for name in failed:
        print(f"[FAIL] {name}")
    raise SystemExit(1)

print("[OK] BDP-003E.5 local reviewed concept card archive schema candidate verified")
