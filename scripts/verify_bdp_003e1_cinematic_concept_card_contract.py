#!/usr/bin/env python3
"""
BDP-003E.1 — Cinematic concept card persistence contract verifier.

Contract-only verifier. It confirms that BDP-003E.1 defines the persistence
and adapter-boundary contract without adding frontend, backend, SQL, database,
or evidence-spine mutation authority.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "BDP_003E_CINEMATIC_CONCEPT_CARD_PERSISTENCE_CONTRACT.md"
STATE = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
FRONTEND = ROOT / "frontend" / "dark_precursor.py"
BDP_003D_VERIFIER = ROOT / "scripts" / "verify_bdp_003d_cinematic_video_front_page.py"

required_files = [DOC, STATE, HANDOVER, FRONTEND, BDP_003D_VERIFIER]
missing = [str(path.relative_to(ROOT)) for path in required_files if not path.exists()]
if missing:
    raise SystemExit(f"[FAIL] Missing required files: {missing}")

doc = DOC.read_text(encoding="utf-8")
doc_lower = doc.lower()
state_text = STATE.read_text(encoding="utf-8")
handover = HANDOVER.read_text(encoding="utf-8")
handover_lower = handover.lower()
state: dict[str, Any] = json.loads(state_text)


def contains_all(text: str, terms: list[str]) -> bool:
    return all(term in text for term in terms)


def walk_values(obj: Any):
    if isinstance(obj, dict):
        for value in obj.values():
            yield from walk_values(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk_values(item)
    else:
        yield obj


state_values = list(walk_values(state))
state_strings = "\n".join(str(v) for v in state_values)
state_strings_lower = state_strings.lower()

phase_record = state.get("bdp_003e1_cinematic_concept_card_persistence_contract", {})

checks = {
    "doc_title": "BDP-003E" in doc and "Cinematic Concept Card Persistence Contract" in doc,
    "doc_contract_only": "contract-only" in doc_lower or "contract only" in doc_lower,
    "doc_no_database_mutation": "database_mutation" in doc and "false" in doc_lower,
    "doc_no_sql_migration": "sql_migration" in doc and "false" in doc_lower,
    "doc_no_evidence_spine_change": "evidence_spine_change" in doc and "false" in doc_lower,
    "doc_no_frontend_or_backend_implementation": (
        "no frontend" in doc_lower or "frontend change" in doc_lower
    ) and (
        "no backend" in doc_lower or "backend change" in doc_lower
    ),
    "doc_generated_material_not_evidence": "not evidence" in doc_lower,
    "doc_human_review_required": "human review" in doc_lower,
    "doc_adapter_boundary": "adapter boundary" in doc_lower or "image/video generation adapter" in doc_lower,
    "doc_concept_card_fields": contains_all(
        doc_lower,
        ["concept", "mode", "prompt", "response", "authority", "created_at"],
    ),
    "state_phase_recorded": isinstance(phase_record, dict) and phase_record.get("phase") == "BDP-003E.1",
    "state_contract_status": "contract" in str(phase_record).lower(),
    "state_no_database_mutation": phase_record.get("database_mutation") is False,
    "state_no_sql_migration": phase_record.get("sql_migration") is False,
    "state_no_evidence_spine_change": phase_record.get("evidence_spine_change") is False,
    "state_next_step_bdp_003e2": "BDP-003E.2" in state.get("next_recommended_step", "") or "BDP-003E.2" in state_strings,
    "handover_phase_recorded": "BDP-003E.1" in handover,
    "handover_contract_only": "contract-only" in handover_lower or "contract only" in handover_lower,
    "existing_bdp_003d_verifier_preserved": BDP_003D_VERIFIER.exists(),
}

failed = [name for name, ok in checks.items() if not ok]

if failed:
    print("=== BDP-003E.1 verifier failures ===")
    for name in failed:
        print(f"[FAIL] {name}")
    raise SystemExit(1)

print("[OK] BDP-003E.1 cinematic concept card persistence contract verified")
