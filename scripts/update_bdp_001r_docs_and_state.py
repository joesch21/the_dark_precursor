#!/usr/bin/env python3
"""Update BUCHANAN_SYSTEM_STATE.json for BDP-001R file/state registration only."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

STATE_PATH = Path("ai_boot/BUCHANAN_SYSTEM_STATE.json")


def main() -> None:
    if not STATE_PATH.exists():
        raise SystemExit(f"missing state file: {STATE_PATH}")

    state = json.loads(STATE_PATH.read_text())
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    state["bdp_001r_source_bound_description_candidate"] = {
        "phase": "BDP-001R",
        "title": "Prepare first source-bound Buchanan Body without Organs description candidate, without interpretation",
        "status": "complete",
        "updated_at": now,
        "controlled_slice": "source_bound_description_candidate_readback_only",
        "sql_migration": False,
        "database_mutation": False,
        "canonical_source_inserted": False,
        "source_candidate_inserted": False,
        "passage_inserted": False,
        "citation_inserted": False,
        "concept_mention_inserted": False,
        "concept_relation_inserted": False,
        "interpretation_inserted": False,
        "generated_buchanan_claim_created": False,
        "description_mode_only": True,
        "description_authority_label": "source_bound_description",
        "generated_description_document": "docs/BDP_001R_BWO_SOURCE_BOUND_DESCRIPTION.md",
        "doctrine_document": "docs/BDP_001R_Source_Bound_Description.md",
        "readback_script": "scripts/read_bdp_001r_bwo_source_bound_description.py",
        "verifier_script": "scripts/verify_bdp_001r_source_bound_description.py",
        "buchanan_specific_explanation_status": "buchanan_pending",
        "buchanan_specific_interpretation_status": "blocked_until_governed_interpretation_phase",
        "buchanan_specific_claim_status": "blocked_until_interpretive_authority_exists",
        "relation_layer_status": "blocked_until_reviewed_relation_evidence",
        "rights_display_boundary": {
            "rights_status": "restricted",
            "display_rule": "reference_only",
            "passage_text_display": "omitted_by_rights_policy",
            "long_quotation_displayed": False,
            "article_reproduction_authorized": False,
        },
        "secondary_scholarship_posture": {
            "authority_label": "secondary_scholarship",
            "scope": "metadata_only_state_candidates_for_later_governed_intake",
            "pdf_document_ids": ["VtUTk", "XJVks", "Tl9xR"],
            "excerpt_reviewed_in_bdp_001r": False,
            "database_candidate_insertion_in_bdp_001r": False,
        },
        "expected_invariant": {
            "sources_count": 2,
            "source_candidates_count": 3,
            "passage_candidates_count": 1,
            "passages_count": 2,
            "citations_count": 2,
            "concept_mentions_count": 2,
            "concept_relations_count": 0,
            "interpretations_count": 0,
            "BDP-001P migration_count": 1,
            "BDP-002C migration_count": 0,
            "BDP-001R migration_count": 0,
            "buchanan_article_passage_count": 1,
            "buchanan_article_citation_count": 1,
            "buchanan_article_concept_mention_count": 1,
        },
        "next_recommended_operator_action": "BDP-001S — Decide the next governed path: secondary-scholarship source-candidate database intake or reviewed relation-evidence preparation.",
    }

    state["next_recommended_step"] = "BDP-001S — Decide the next governed path: secondary-scholarship source-candidate database intake or reviewed relation-evidence preparation."

    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    print("[OK] updated ai_boot/BUCHANAN_SYSTEM_STATE.json for BDP-001R state registration only")
    print("[OK] no database mutation performed")


if __name__ == "__main__":
    main()
