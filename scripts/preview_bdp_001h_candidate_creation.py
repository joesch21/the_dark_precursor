#!/usr/bin/env python3
import json
import os

preview = {
    "schema": "buchanan.source_candidate_creation_preview.v1",
    "phase": "BDP-001H",
    "mode": "read_only_preview",
    "writes_database": False,
    "candidate_preview": {
        "title": os.environ.get("BDP_001H_PREVIEW_TITLE", "Operator-supplied Buchanan source title"),
        "author": os.environ.get("BDP_001H_PREVIEW_AUTHOR", "Ian Buchanan"),
        "source_type": os.environ.get("BDP_001H_PREVIEW_SOURCE_TYPE", "book_or_article_or_transcript"),
        "url_or_reference": os.environ.get("BDP_001H_PREVIEW_REFERENCE", "operator must supply bibliographic reference or URL"),
        "discovered_by": "operator_preview",
        "rights_status_recommendation": "fair_use_reference_only_or_user_provided",
        "reliability_level_recommendation": "requires_review",
        "bibliographic_note": "Preview only. Bibliographic details must be checked before candidate creation.",
        "operator_review_requirement": "required_before_candidate_insert",
        "canonical_adoption_boundary": "candidate_preview_is_not_candidate; candidate_is_not_canonical_source",
        "intended_concept_link": "Body without Organs",
    },
    "hard_boundaries": {
        "creates_source_candidate": False,
        "creates_canonical_source": False,
        "creates_passage": False,
        "creates_citation": False,
        "creates_concept_mention": False,
        "creates_concept_relation": False,
        "creates_interpretation": False,
        "creates_buchanan_claim": False,
    },
    "next_step": "BDP-001I — Select first Buchanan source candidate for Body without Organs.",
}

print(json.dumps(preview, indent=2, ensure_ascii=False))
