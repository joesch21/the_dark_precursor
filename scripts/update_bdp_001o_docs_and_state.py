#!/usr/bin/env python3
"""Update Buchanan system state for BDP-001O.

This script intentionally touches only ai_boot/BUCHANAN_SYSTEM_STATE.json.
Docs are updated by the patch itself.
"""

from __future__ import annotations

import json
from pathlib import Path

STATE_PATH = Path("ai_boot/BUCHANAN_SYSTEM_STATE.json")

BDP_001O_RECORD = {
    "phase": "BDP-001O",
    "title": "Insert reviewed Buchanan passage and citation only",
    "status": "completed",
    "sql_migration": True,
    "database_mutation": True,
    "canonical_passage_inserted": True,
    "citation_inserted": True,
    "concept_mention_inserted": False,
    "concept_relation_inserted": False,
    "interpretation_inserted": False,
    "buchanan_claim_inserted": False,
    "expected_invariant": {
        "sources_count": 2,
        "source_candidates_count": 3,
        "passage_candidates_count": 1,
        "passages_count": 2,
        "citations_count": 2,
        "concept_mentions_count": 1,
        "concept_relations_count": 0,
        "interpretations_count": 0,
        "BDP-001O_migration_count": 1,
    },
    "next_step": "BDP-001P — Link the inserted Buchanan passage to Body without Organs through a reviewed concept mention only.",
}


def main() -> None:
    if not STATE_PATH.exists():
        raise SystemExit(f"Missing required state file: {STATE_PATH}")

    state = json.loads(STATE_PATH.read_text())
    state["current_phase"] = "BDP-001O"
    state["last_completed_phase"] = "BDP-001O"
    state.setdefault("phase_records", {})["BDP-001O"] = BDP_001O_RECORD
    state.setdefault("database_invariant", {}).update(BDP_001O_RECORD["expected_invariant"])

    history = state.setdefault("phase_history", [])
    if isinstance(history, list) and not any(
        isinstance(item, dict) and item.get("phase") == "BDP-001O" for item in history
    ):
        history.append(BDP_001O_RECORD)

    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    print(f"updated {STATE_PATH} for BDP-001O")


if __name__ == "__main__":
    main()
