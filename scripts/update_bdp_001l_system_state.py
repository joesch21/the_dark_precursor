#!/usr/bin/env python3
"""Conservatively update ai_boot/BUCHANAN_SYSTEM_STATE.json for BDP-001L."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

STATE_PATH = Path("ai_boot/BUCHANAN_SYSTEM_STATE.json")

PHASE_RECORD: dict[str, Any] = {
    "phase": "BDP-001L",
    "status": "complete",
    "title": "Adopt reviewed Buchanan source metadata into canonical sources only",
    "controlled_slice": "source_metadata_adoption_only",
    "canonical_source_adopted": {
        "title": "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?",
        "author": "Ian Buchanan",
        "type": "article",
        "publication_year": 1997,
        "journal": "Body & Society",
        "volume": "3",
        "issue": "3",
        "pages": "73-91",
        "doi": "10.1177/1357034X97003003004",
        "url_or_reference": "https://doi.org/10.1177/1357034X97003003004",
        "publisher": "SAGE Publications",
        "rights_status": "restricted",
        "reliability_level": "high",
        "status": "canonical",
    },
    "adopted_from_phases": ["BDP-001J", "BDP-001K"],
    "candidate_history": {
        "preserved_in_source_candidates": True,
        "status": "approved",
        "history_status": "approved_adopted_metadata_history",
    },
    "pdf_availability_metadata": {
        "pdf_access_status": "user_provided_pdf_available",
        "source_text_available_for_review": True,
        "display_rule": "reference_only",
    },
    "verified_invariant": {
        "sources_count": 2,
        "source_candidates_count": 3,
        "passages_count": 1,
        "citations_count": 1,
        "concept_mentions_count": 1,
        "concept_relations_count": 0,
        "interpretations_count": 0,
        "BDP-001L migration_count": 1,
    },
    "boundaries": {
        "passage_insertion": False,
        "citation_insertion": False,
        "concept_mention_insertion": False,
        "concept_relation_insertion": False,
        "interpretation_insertion": False,
        "generated_buchanan_claim": False,
        "long_pdf_quotation": False,
    },
    "next_step": "BDP-001M — Prepare first Buchanan passage candidate from the adopted article, without inserting citation or interpretation yet.",
}


def main() -> int:
    if not STATE_PATH.exists():
        raise FileNotFoundError(f"Missing state file: {STATE_PATH}")

    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if not isinstance(state, dict):
        raise TypeError(f"{STATE_PATH} must contain a JSON object")

    state["last_completed_phase"] = "BDP-001L"
    state["current_phase"] = "BDP-001L"
    state["next_phase"] = "BDP-001M"
    state["bdp_001l_metadata_only_source_adoption"] = PHASE_RECORD

    if isinstance(state.get("phase_records"), dict):
        state["phase_records"]["BDP-001L"] = PHASE_RECORD

    if isinstance(state.get("phases"), dict):
        state["phases"]["BDP-001L"] = PHASE_RECORD

    if isinstance(state.get("phase_history"), list):
        state["phase_history"] = [
            item for item in state["phase_history"]
            if not (isinstance(item, dict) and item.get("phase") == "BDP-001L")
        ]
        state["phase_history"].append(PHASE_RECORD)

    if isinstance(state.get("database_scope"), dict):
        state["database_scope"]["current_verified_invariant"] = PHASE_RECORD["verified_invariant"]
        state["database_scope"]["sources_count"] = 2
        state["database_scope"]["source_candidates_count"] = 3
        state["database_scope"]["passages_count"] = 1
        state["database_scope"]["citations_count"] = 1
        state["database_scope"]["concept_mentions_count"] = 1
        state["database_scope"]["concept_relations_count"] = 0
        state["database_scope"]["interpretations_count"] = 0

    if isinstance(state.get("database"), dict):
        state["database"]["current_verified_invariant"] = PHASE_RECORD["verified_invariant"]

    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {STATE_PATH} for BDP-001L.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
