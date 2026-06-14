#!/usr/bin/env python3
"""
Verify BDP-001Q docs and state markers after update_bdp_001q_docs_and_state.py.
"""

from __future__ import annotations

import json
from pathlib import Path


REQUIRED_MARKERS = {
    "docs/BUCHANAN_SCHEMA_CONTROL.md": "## BDP-001Q Evidence Readback Boundary",
    "docs/BUCHANAN_INGESTION_WORKFLOW.md": "## BDP-001Q Evidence Readback Step",
    "docs/BUCHANAN_CONCEPT_ONTOLOGY.md": "## BDP-001Q Body without Organs Evidence Readback Boundary",
    "docs/BUCHANAN_SEMANTIC_WORKBENCH.md": "## BDP-001Q Buchanan Evidence Card Readback",
    "docs/BUCHANAN_SOURCE_INTAKE_REGISTRY.md": "## BDP-001Q Evidence Readback Record",
    "docs/BUCHANAN_CITATION_AND_RIGHTS.md": "## BDP-001Q Evidence Readback Rights Boundary",
    "docs/BUCHANAN_THREAD_HANDOVER.md": "## BDP-001Q Handover Update",
}


EXPECTED_INVARIANT = {
    "sources_count": 2,
    "source_candidates_count": 3,
    "passage_candidates_count": 1,
    "passages_count": 2,
    "citations_count": 2,
    "concept_mentions_count": 2,
    "concept_relations_count": 0,
    "interpretations_count": 0,
    "bdp_001p_migration_count": 1,
    "bdp_001q_migration_count": 0,
    "buchanan_article_passage_count": 1,
    "buchanan_article_citation_count": 1,
    "buchanan_article_concept_mention_count": 1,
}


BOUNDARY_FALSE_KEYS = [
    "new_source",
    "new_source_candidate",
    "new_passage_candidate",
    "new_passage",
    "new_citation",
    "new_concept_mention",
    "concept_relation",
    "interpretation",
    "generated_buchanan_claim",
    "frontend_work",
]


AUTHORITY_FALSE_KEYS = [
    "buchanan_interpretation",
    "buchanan_claim",
    "generated_synthesis",
    "concept_relation",
]


def main() -> None:
    for filename, marker in REQUIRED_MARKERS.items():
        path = Path(filename)
        if not path.exists():
            raise SystemExit(f"[FAIL] missing required document: {filename}")
        text = path.read_text()
        if marker not in text:
            raise SystemExit(f"[FAIL] {filename} missing marker: {marker}")
        print(f"[OK] {filename} contains {marker}")

    state_path = Path("ai_boot/BUCHANAN_SYSTEM_STATE.json")
    if not state_path.exists():
        raise SystemExit(f"[FAIL] missing required state file: {state_path}")

    state = json.loads(state_path.read_text())
    record = state.get("bdp_001q_buchanan_bwo_evidence_readback")
    if not isinstance(record, dict):
        raise SystemExit("[FAIL] state missing bdp_001q_buchanan_bwo_evidence_readback record")

    if record.get("database_mutation") is not False:
        raise SystemExit("[FAIL] BDP-001Q state database_mutation is not false")
    print("[OK] state database_mutation = false")

    if record.get("sql_migration") is not False:
        raise SystemExit("[FAIL] BDP-001Q state sql_migration is not false")
    print("[OK] state sql_migration = false")

    invariant = record.get("verified_invariant", {})
    for key, expected_value in EXPECTED_INVARIANT.items():
        actual = invariant.get(key)
        if actual != expected_value:
            raise SystemExit(f"[FAIL] state invariant {key}: expected {expected_value!r}, got {actual!r}")
        print(f"[OK] state invariant {key} = {actual!r}")

    inserted_rows = record.get("inserted_rows", {})
    for key, actual in inserted_rows.items():
        if actual != 0:
            raise SystemExit(f"[FAIL] inserted_rows {key}: expected 0, got {actual!r}")
        print(f"[OK] inserted_rows {key} = 0")

    boundary = record.get("boundary", {})
    for key in BOUNDARY_FALSE_KEYS:
        if boundary.get(key) is not False:
            raise SystemExit(f"[FAIL] boundary {key} is not false")
        print(f"[OK] boundary {key} = false")

    authority = record.get("authority_boundary", {})
    if authority.get("source_bound_description_allowed") is not True:
        raise SystemExit("[FAIL] source_bound_description_allowed is not true")
    print("[OK] source_bound_description_allowed = true")

    for key in AUTHORITY_FALSE_KEYS:
        if authority.get(key) is not False:
            raise SystemExit(f"[FAIL] authority boundary {key} is not false")
        print(f"[OK] authority boundary {key} = false")

    target = record.get("readback_target", {})
    expected_target = {
        "concept": "Body without Organs",
        "source_author": "Ian Buchanan",
        "source_title": "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?",
        "passage_text_display": "omitted_by_rights_policy",
        "rights_status": "restricted",
    }
    for key, expected_value in expected_target.items():
        actual = target.get(key)
        if actual != expected_value:
            raise SystemExit(f"[FAIL] readback target {key}: expected {expected_value!r}, got {actual!r}")
        print(f"[OK] readback target {key} = {actual!r}")

    print("\nBDP-001Q docs and state verification passed.")


if __name__ == "__main__":
    main()
