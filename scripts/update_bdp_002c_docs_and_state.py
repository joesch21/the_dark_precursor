#!/usr/bin/env python3
"""
BDP-002C — Docs and State Update

Repository-file update only. No database connection. No SQL. No source, passage,
citation, concept mention, relation, interpretation, or Buchanan claim is created.

This script records the three new PDFs as state-level source-candidate intake
records only. A later governed database-intake phase is required before they can
be inserted into the source_candidates table.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

STATE_PATH = Path("ai_boot/BUCHANAN_SYSTEM_STATE.json")

NEW_SOURCE_CANDIDATES = [
    {
        "title": "Deleuze and Space",
        "author_or_editor": "Ian Buchanan and Gregg Lambert, eds.",
        "year": 2005,
        "type": "edited_collection",
        "status": "state_recorded_source_candidate_pending_database_intake",
        "rights_status": "restricted",
        "display_rule": "reference_only",
        "reliability_level": "high",
        "evidence_depth_tier": "Tier 2 — Supporting Scholarship",
        "intended_concept_links": ["assemblage", "Body without Organs", "smooth space", "striated space"],
        "pdf_document_id": "VtUTk",
        "database_source_candidate_inserted": False,
        "canonical_source_adopted": False,
        "passage_extracted": False,
        "citation_inserted": False,
        "concept_mention_inserted": False,
        "interpretation_inserted": False,
        "buchanan_claim_authorized": False,
    },
    {
        "title": "Assemblage Theory and Method",
        "author_or_editor": "Ian Buchanan",
        "year": 2021,
        "type": "book",
        "status": "state_recorded_source_candidate_pending_database_intake",
        "rights_status": "restricted",
        "display_rule": "reference_only",
        "reliability_level": "high",
        "evidence_depth_tier": "Tier 2 — Supporting Scholarship",
        "intended_concept_links": ["assemblage", "method", "Body without Organs", "desire"],
        "pdf_document_id": "XJVks",
        "database_source_candidate_inserted": False,
        "canonical_source_adopted": False,
        "passage_extracted": False,
        "citation_inserted": False,
        "concept_mention_inserted": False,
        "interpretation_inserted": False,
        "buchanan_claim_authorized": False,
    },
    {
        "title": "Deleuze and Guattari's Anti-Oedipus: A Reader's Guide",
        "author_or_editor": "Ian Buchanan",
        "year": 2008,
        "type": "book",
        "status": "state_recorded_source_candidate_pending_database_intake",
        "rights_status": "restricted",
        "display_rule": "reference_only",
        "reliability_level": "high",
        "evidence_depth_tier": "Tier 2 — Supporting Scholarship",
        "intended_concept_links": ["desire", "schizoanalysis", "Body without Organs", "Anti-Oedipus"],
        "pdf_document_id": "Tl9xR",
        "database_source_candidate_inserted": False,
        "canonical_source_adopted": False,
        "passage_extracted": False,
        "citation_inserted": False,
        "concept_mention_inserted": False,
        "interpretation_inserted": False,
        "buchanan_claim_authorized": False,
    },
]


def load_state(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing required state file: {path}")
    return json.loads(path.read_text())


def main() -> int:
    state = load_state(STATE_PATH)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    state["bdp_002c_richer_semantic_readback_surface"] = {
        "phase": "BDP-002C",
        "status": "prepared",
        "updated_at": now,
        "sql_migration": False,
        "database_mutation": False,
        "psql_subprocess_only": True,
        "psycopg_dependency": False,
        "psycopg2_dependency": False,
        "frontend_renderer": False,
        "card_contract": "15_section_richer_semantic_readback_surface",
        "concept": "Body without Organs",
        "buchanan_specific_explanation_status": "buchanan_pending",
        "buchanan_specific_interpretation_status": "blocked_until_governed_interpretation_phase",
        "buchanan_specific_claim_status": "blocked_until_interpretive_authority_exists",
        "rights_boundary": {
            "passage_text_display": "omitted_by_rights_policy",
            "long_quotation_displayed": False,
            "article_reproduction_authorized": False,
            "new_pdf_display_rule": "reference_only_metadata_only_until_later_review",
        },
        "psycho_linguistic_boundary": {
            "authority_label": "experimental_modelling",
            "current_ceiling": "Level 2 Embedding Deviation",
            "requires_human_review": True,
            "objective_score_claimed": False,
        },
        "source_candidates_state_registry": NEW_SOURCE_CANDIDATES,
        "source_candidates_database_boundary": {
            "database_source_candidates_inserted_by_bdp_002c": False,
            "later_governed_database_intake_required": True,
            "expected_live_database_source_candidates_count_remains": 3,
        },
        "next_recommended_operator_action": "BDP-001R — Prepare first source-bound Buchanan Body without Organs description candidate, without interpretation.",
    }

    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"[OK] updated {STATE_PATH} for BDP-002C state registry only")
    print("[OK] no database mutation performed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
