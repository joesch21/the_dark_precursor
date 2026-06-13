#!/usr/bin/env python3
"""Update BUCHANAN_SYSTEM_STATE.json for BDP-002A without touching the database."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

PHASE = "BDP-002A"
ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "ai_boot" / "BUCHANAN_SYSTEM_STATE.json"
EXPECTED_COUNTS = {
    "sources_count": 2,
    "source_candidates_count": 3,
    "passage_candidates_count": 1,
    "passages_count": 1,
    "citations_count": 1,
    "concept_mentions_count": 1,
    "concept_relations_count": 0,
    "interpretations_count": 0,
    "BDP-001L_migration_count": 1,
    "BDP-001M_migration_count": 1,
    "BDP-002A_migration_count": 0,
}


def load_state() -> Dict[str, Any]:
    if not STATE_PATH.exists():
        raise FileNotFoundError(f"Missing required state file: {STATE_PATH}")
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def append_phase_history(state: Dict[str, Any], record: Dict[str, Any]) -> None:
    history = state.get("phase_history")
    if isinstance(history, list):
        if not any(isinstance(item, dict) and item.get("phase") == PHASE for item in history):
            history.append(record)
        return
    if isinstance(history, dict):
        history[PHASE] = record
        return
    state["phase_history"] = {PHASE: record}


def main() -> int:
    state = load_state()
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    record: Dict[str, Any] = {
        "phase": PHASE,
        "status": "prepared_read_only_semantic_workbench",
        "concept": "Body without Organs",
        "database_mutation": False,
        "schema_migration": False,
        "authority_boundary": {
            "plain_explanation": "provisional_synthesis",
            "technical_explanation": "provisional_synthesis",
            "buchanan_explanation": "buchanan_pending",
        },
        "buchanan_specific_explanation_status": "blocked_until_buchanan_passage_citation",
        "verified_invariant": EXPECTED_COUNTS,
        "updated_at": stamp,
    }

    state["current_phase"] = PHASE
    state["last_updated_phase"] = PHASE
    state["bdp_002a_semantic_workbench"] = record
    state["current_verified_invariant"] = EXPECTED_COUNTS
    append_phase_history(state, record)

    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Updated {STATE_PATH} for {PHASE}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
