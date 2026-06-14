#!/usr/bin/env python3
"""
Verify BDP-001P docs and state markers after update_bdp_001p_docs_and_state.py.
"""

from __future__ import annotations

import json
from pathlib import Path


REQUIRED_MARKERS = {
    "docs/BUCHANAN_SCHEMA_CONTROL.md": "## BDP-001P Reviewed Concept Mention Link Patch",
    "docs/BUCHANAN_INGESTION_WORKFLOW.md": "## BDP-001P Reviewed Concept Mention Link",
    "docs/BUCHANAN_CONCEPT_ONTOLOGY.md": "## BDP-001P Buchanan Concept Mention Boundary",
    "docs/BUCHANAN_SEMANTIC_WORKBENCH.md": "## BDP-001P Workbench Evidence Posture",
    "docs/BUCHANAN_SOURCE_INTAKE_REGISTRY.md": "## BDP-001P Concept Mention Link Record",
    "docs/BUCHANAN_CITATION_AND_RIGHTS.md": "## BDP-001P Concept Mention Rights Boundary",
    "docs/BUCHANAN_THREAD_HANDOVER.md": "## BDP-001P Handover Update",
}


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
    record = state.get("bdp_001p_buchanan_concept_mention_only")
    if not isinstance(record, dict):
        raise SystemExit("[FAIL] state missing bdp_001p_buchanan_concept_mention_only record")

    invariant = record.get("verified_invariant", {})
    expected = {
        "sources_count": 2,
        "source_candidates_count": 3,
        "passage_candidates_count": 1,
        "passages_count": 2,
        "citations_count": 2,
        "concept_mentions_count": 2,
        "concept_relations_count": 0,
        "interpretations_count": 0,
        "bdp_001p_migration_count": 1,
        "buchanan_article_concept_mention_count": 1,
    }

    for key, expected_value in expected.items():
        actual = invariant.get(key)
        if actual != expected_value:
            raise SystemExit(f"[FAIL] state invariant {key}: expected {expected_value!r}, got {actual!r}")
        print(f"[OK] state invariant {key} = {actual!r}")

    boundary = record.get("boundary", {})
    blocked = [
        "new_source",
        "new_passage",
        "new_citation",
        "concept_relation",
        "interpretation",
        "generated_buchanan_claim",
        "frontend_work",
    ]
    for key in blocked:
        if boundary.get(key) is not False:
            raise SystemExit(f"[FAIL] boundary {key} is not false")
        print(f"[OK] boundary {key} = false")

    print("\nBDP-001P docs and state verification passed.")


if __name__ == "__main__":
    main()
