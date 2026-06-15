#!/usr/bin/env python3
"""
BDP-003E.4 — Concept card persistence readiness decision verifier.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BDP_003E4_CONCEPT_CARD_PERSISTENCE_READINESS_DECISION.md"
E3_DOC = ROOT / "docs" / "BDP_003E3_CINEMATIC_CONCEPT_CARD_SAMPLE_REVIEW.md"
STATE = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
APP = ROOT / "frontend" / "dark_precursor.py"

required = [DOC, E3_DOC, STATE, HANDOVER, APP]
missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
if missing:
    raise SystemExit(f"[FAIL] Missing required files: {missing}")

doc = DOC.read_text(encoding="utf-8")
e3_doc = E3_DOC.read_text(encoding="utf-8")
state = json.loads(STATE.read_text(encoding="utf-8"))
handover = HANDOVER.read_text(encoding="utf-8")
app = APP.read_text(encoding="utf-8")
record = state.get("bdp_003e4_concept_card_persistence_readiness_decision", {})

next_step = "BDP-003E.5 — Define local reviewed concept card archive schema candidate only, without implementation."
e4_step = "BDP-003E.4 — Decide concept card persistence readiness from reviewed samples only."

forbidden_app_runtime = [
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
    "doc_status": "**Status:** Implemented / verified" in doc,
    "doc_decision_gate": "decision gate" in doc.lower(),
    "doc_not_ready_database": "database_persistence_ready = false" in doc,
    "doc_not_ready_adapter": "adapter_implementation_ready = false" in doc,
    "doc_not_ready_evidence": "evidence_promotion_ready = false" in doc,
    "doc_schema_candidate_only": "local_archive_schema_candidate_ready = true" in doc,
    "doc_no_persistence_impl": "does not build a persistence layer" in doc,
    "doc_generated_not_evidence": "Generated cinematic concept cards are provisional synthesis drafts, not evidence" in doc,
    "doc_next_step": next_step in doc,
    "e3_followup": "BDP-003E.4 Decision Follow-up" in e3_doc and next_step in e3_doc,
    "state_recorded": bool(record),
    "state_last_phase": "bdp_003e4_concept_card_persistence_readiness_decision" in state,
    "state_global_next": state.get("bdp_003e4_concept_card_persistence_readiness_decision", {}).get("next_recommended_step") == next_step,
    "state_e3_next_local": state.get("bdp_003e3_cinematic_concept_card_sample_review", {}).get("next_recommended_step") == e4_step,
    "state_no_db": record.get("database_mutation") is False and record.get("database_persistence_ready") is False,
    "state_no_backend": record.get("backend_service") is False,
    "state_no_adapter": record.get("adapter_endpoint") is False and record.get("adapter_invocation") is False and record.get("adapter_implementation_ready") is False,
    "state_no_evidence": record.get("evidence_spine_change") is False and record.get("evidence_promotion_ready") is False,
    "state_schema_candidate_ready": record.get("local_archive_schema_candidate_ready") is True,
    "state_decision": record.get("decision") == "not_ready_for_persistence_or_adapter; ready_for_schema_candidate_only",
    "state_next": record.get("next_recommended_step") == next_step,
    "handover_recorded": "BDP-003E.4" in handover and next_step in handover,
    "app_no_new_runtime_patterns": not any(pattern in app for pattern in forbidden_app_runtime),
}

failed = [name for name, ok in checks.items() if not ok]
if failed:
    print("=== BDP-003E.4 verifier failures ===")
    for name in failed:
        print(f"[FAIL] {name}")
    raise SystemExit(1)

print("[OK] BDP-003E.4 concept card persistence readiness decision verified")
