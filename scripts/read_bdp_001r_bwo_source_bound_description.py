#!/usr/bin/env python3
"""
BDP-001R — Source-bound description generator for Body without Organs.

This script is read-only. It uses the Buchanan repository psql subprocess
pattern and generates a labelled source-bound description of governed records.
It does not create sources, passages, citations, concept mentions, concept
relations, interpretations, or Buchanan-specific claims.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List

DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")

CONTROLLED_AUTHORITY_LABELS = {
    "source_bound_description",
    "record_description",
    "secondary_scholarship",
    "buchanan_pending",
    "blocked_until_governed_interpretation_phase",
    "blocked_until_reviewed_relation_evidence",
    "blocked_until_interpretive_authority_exists",
    "rights_display_boundary",
    "metadata",
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
    "BDP-001P migration_count": 1,
    "BDP-002C migration_count": 0,
    "BDP-001R migration_count": 0,
    "buchanan_article_passage_count": 1,
    "buchanan_article_citation_count": 1,
    "buchanan_article_concept_mention_count": 1,
}

BUCHANAN_ARTICLE_TITLE = "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?"

SECONDARY_SCHOLARSHIP_CANDIDATES = [
    {
        "title": "Deleuze and Space",
        "author_or_editor": "Ian Buchanan and Gregg Lambert, eds.",
        "year": 2005,
        "source_type": "edited_collection",
        "pdf_document_id": "VtUTk",
        "candidate_status": "metadata_only_state_candidate_for_later_governed_intake",
        "rights_status": "restricted",
        "display_rule": "reference_only",
        "authority_label": "secondary_scholarship",
        "intended_concept_links": ["assemblage", "Body without Organs", "smooth space", "striated space"],
    },
    {
        "title": "Assemblage Theory and Method",
        "author_or_editor": "Ian Buchanan",
        "year": 2021,
        "source_type": "book",
        "pdf_document_id": "XJVks",
        "candidate_status": "metadata_only_state_candidate_for_later_governed_intake",
        "rights_status": "restricted",
        "display_rule": "reference_only",
        "authority_label": "secondary_scholarship",
        "intended_concept_links": ["assemblage", "method", "Body without Organs", "desire"],
    },
    {
        "title": "Deleuze and Guattari's Anti-Oedipus: A Reader's Guide",
        "author_or_editor": "Ian Buchanan",
        "year": 2008,
        "source_type": "book",
        "pdf_document_id": "Tl9xR",
        "candidate_status": "metadata_only_state_candidate_for_later_governed_intake",
        "rights_status": "restricted",
        "display_rule": "reference_only",
        "authority_label": "secondary_scholarship",
        "intended_concept_links": ["desire", "schizoanalysis", "Body without Organs", "Anti-Oedipus"],
    },
]

SQL_QUERIES = {
    "current_invariant": r"""
SELECT json_build_object(
  'sources_count', (SELECT COUNT(*) FROM sources),
  'source_candidates_count', (SELECT COUNT(*) FROM source_candidates),
  'passage_candidates_count', (SELECT COUNT(*) FROM passage_candidates),
  'passages_count', (SELECT COUNT(*) FROM passages),
  'citations_count', (SELECT COUNT(*) FROM citations),
  'concept_mentions_count', (SELECT COUNT(*) FROM concept_mentions),
  'concept_relations_count', (SELECT COUNT(*) FROM concept_relations),
  'interpretations_count', (SELECT COUNT(*) FROM interpretations),
  'BDP-001P migration_count', (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001P'),
  'BDP-002C migration_count', (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-002C'),
  'BDP-001R migration_count', (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001R'),
  'buchanan_article_passage_count', (
    SELECT COUNT(*)
    FROM passages p
    JOIN sources s ON s.id = p.source_id
    WHERE s.author = 'Ian Buchanan'
      AND s.title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
  ),
  'buchanan_article_citation_count', (
    SELECT COUNT(*)
    FROM citations c
    JOIN sources s ON s.id = c.source_id
    WHERE s.author = 'Ian Buchanan'
      AND s.title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
  ),
  'buchanan_article_concept_mention_count', (
    SELECT COUNT(*)
    FROM concept_mentions cm
    JOIN passages p ON p.id = cm.passage_id
    JOIN sources s ON s.id = p.source_id
    JOIN concepts co ON co.id = cm.concept_id
    WHERE s.author = 'Ian Buchanan'
      AND s.title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
      AND co.name = 'Body without Organs'
      AND cm.reviewed_status = 'accepted'
  )
)::text;
""",
    "canonical_buchanan_source_metadata": r"""
SELECT COALESCE(json_build_object(
  'title', title,
  'author', author,
  'type', type,
  'year', year,
  'publisher', publisher,
  'url_or_reference', url_or_reference,
  'rights_status', rights_status,
  'status', status
)::text, '{}')
FROM sources
WHERE author = 'Ian Buchanan'
  AND title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
LIMIT 1;
""",
}

REQUIRED_SECTIONS = [
    "evidence_chain_summary",
    "buchanan_1997_article_posture",
    "secondary_scholarship_posture",
    "blocked_layers_status",
    "rights_display_status",
    "current_evidence_posture_statement",
    "next_recommended_governed_action",
    "authority_label_summary",
]


def run_psql_query(query: str) -> str:
    """Execute a SELECT-only query using psql subprocess."""
    cmd = ["psql", "-d", DB_NAME, "-t", "-A", "-c", query]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "psql query failed")
    return result.stdout.strip()


def read_json_query(name: str) -> Dict[str, Any]:
    raw = run_psql_query(SQL_QUERIES[name])
    if not raw:
        return {}
    return json.loads(raw)


def field(field_id: str, label: str, value: Any, authority_label: str) -> Dict[str, Any]:
    return {
        "field_id": field_id,
        "label": label,
        "value": value,
        "authority_label": authority_label,
    }


def section(section_id: str, title: str, authority_label: str, fields: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "section_id": section_id,
        "title": title,
        "authority_label": authority_label,
        "fields": list(fields),
    }


def build_description_card(offline: bool = False) -> Dict[str, Any]:
    if offline:
        invariant = dict(EXPECTED_INVARIANT)
        metadata = {
            "title": BUCHANAN_ARTICLE_TITLE,
            "author": "Ian Buchanan",
            "type": "article",
            "year": "1997",
            "publisher": "SAGE Publications",
            "url_or_reference": "https://doi.org/10.1177/1357034X97003003004",
            "rights_status": "restricted",
            "status": "canonical",
        }
    else:
        invariant = read_json_query("current_invariant")
        metadata = read_json_query("canonical_buchanan_source_metadata")

    card = {
        "bdp_phase": "BDP-001R",
        "title": "Source-Bound Description Candidate — Body without Organs",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "description_mode": True,
        "offline_preview": offline,
        "invariant_at_generation": invariant,
        "sections": [
            section(
                "evidence_chain_summary",
                "Evidence Chain Summary",
                "source_bound_description",
                [
                    field(
                        "governed_chain",
                        "Governed record chain",
                        "canonical Buchanan metadata → restricted citation-backed passage → citation record → reviewed direct concept mention → readback description",
                        "source_bound_description",
                    ),
                    field(
                        "passage_locator",
                        "Passage locator",
                        "printed article page 76 / PDF page 4",
                        "metadata",
                    ),
                    field(
                        "current_counts",
                        "Current invariant counts",
                        invariant,
                        "metadata",
                    ),
                ],
            ),
            section(
                "buchanan_1997_article_posture",
                "Buchanan 1997 Article Posture",
                "source_bound_description",
                [
                    field(
                        "canonical_metadata",
                        "Canonical source metadata",
                        metadata,
                        "metadata",
                    ),
                    field(
                        "article_record_posture",
                        "Article record posture",
                        "Canonical metadata exists for the 1997 Buchanan article; one restricted passage record and one citation record are available for readback.",
                        "source_bound_description",
                    ),
                    field(
                        "concept_mention_posture",
                        "Concept mention posture",
                        "A reviewed direct concept mention links the restricted passage record to the Body without Organs concept record.",
                        "source_bound_description",
                    ),
                    field(
                        "buchanan_specific_explanation_status",
                        "Buchanan-specific explanation status",
                        "buchanan_pending",
                        "buchanan_pending",
                    ),
                ],
            ),
            section(
                "secondary_scholarship_posture",
                "Secondary Scholarship Posture",
                "secondary_scholarship",
                [
                    field(
                        "secondary_candidate_scope",
                        "Secondary scholarship scope",
                        "The three additional Buchanan works remain metadata-only intake targets for later governed source-candidate handling.",
                        "secondary_scholarship",
                    ),
                    field(
                        "secondary_candidates",
                        "Secondary scholarship candidates",
                        SECONDARY_SCHOLARSHIP_CANDIDATES,
                        "secondary_scholarship",
                    ),
                    field(
                        "secondary_boundary",
                        "Secondary scholarship boundary",
                        "No PDF excerpt is reviewed, displayed, promoted, or used for direct source evidence in BDP-001R.",
                        "secondary_scholarship",
                    ),
                ],
            ),
            section(
                "blocked_layers_status",
                "Blocked Layers Status",
                "record_description",
                [
                    field(
                        "relation_layer_status",
                        "Relation layer status",
                        "blocked_until_reviewed_relation_evidence",
                        "blocked_until_reviewed_relation_evidence",
                    ),
                    field(
                        "interpretation_layer_status",
                        "Interpretation layer status",
                        "blocked_until_governed_interpretation_phase",
                        "blocked_until_governed_interpretation_phase",
                    ),
                    field(
                        "buchanan_specific_claim_status",
                        "Buchanan-specific claim status",
                        "blocked_until_interpretive_authority_exists",
                        "blocked_until_interpretive_authority_exists",
                    ),
                    field(
                        "blocked_boundary",
                        "Blocked boundary",
                        "No relation, interpretation, theoretical consequence, or author-position claim is generated by this description.",
                        "record_description",
                    ),
                ],
            ),
            section(
                "rights_display_status",
                "Rights & Display Status",
                "rights_display_boundary",
                [
                    field("rights_status", "Rights status", "restricted", "rights_display_boundary"),
                    field("display_rule", "Display rule", "reference_only", "rights_display_boundary"),
                    field("passage_text_display", "Passage text display", "omitted_by_rights_policy", "rights_display_boundary"),
                    field("long_quotation_displayed", "Long quotation displayed", False, "rights_display_boundary"),
                    field("article_reproduction_authorized", "Article reproduction authorized", False, "rights_display_boundary"),
                    field(
                        "secondary_pdf_display_boundary",
                        "Secondary PDF display boundary",
                        "Metadata-only descriptions; no excerpts from VtUTk, XJVks, or Tl9xR are displayed.",
                        "rights_display_boundary",
                    ),
                ],
            ),
            section(
                "current_evidence_posture_statement",
                "Current Evidence Posture Statement",
                "source_bound_description",
                [
                    field(
                        "source_bound_statement",
                        "Source-bound statement",
                        "The database records a restricted citation-backed Buchanan passage from the 1997 article and a reviewed direct concept mention linking that passage record to Body without Organs.",
                        "source_bound_description",
                    ),
                    field(
                        "description_not_claim",
                        "Description boundary",
                        "This statement describes governed records only and does not assign a position, argument, intention, conceptual meaning, or theoretical consequence to any author.",
                        "record_description",
                    ),
                ],
            ),
            section(
                "next_recommended_governed_action",
                "Next Recommended Governed Action",
                "record_description",
                [
                    field(
                        "primary_next_action",
                        "Primary next action",
                        "BDP-001S — Decide the next governed path: secondary-scholarship source-candidate database intake or reviewed relation-evidence preparation.",
                        "record_description",
                    ),
                    field(
                        "continuity_note",
                        "Continuity note",
                        "Keep BDP-001R as a description candidate unless a later phase explicitly promotes it into another readback surface.",
                        "record_description",
                    ),
                ],
            ),
            section(
                "authority_label_summary",
                "Authority Label Summary",
                "metadata",
                [
                    field(
                        "labels_used",
                        "Labels used",
                        sorted(CONTROLLED_AUTHORITY_LABELS),
                        "metadata",
                    ),
                    field(
                        "label_rule",
                        "Label rule",
                        "Every section and field in this document carries a controlled authority label.",
                        "metadata",
                    ),
                ],
            ),
        ],
    }
    return card


def card_to_markdown(card: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append(f"# {card['title']}")
    lines.append("")
    lines.append(f"- `bdp_phase`: `{card['bdp_phase']}`")
    lines.append(f"- `description_mode`: `{str(card['description_mode']).lower()}`")
    lines.append(f"- `offline_preview`: `{str(card['offline_preview']).lower()}`")
    lines.append("")
    for sec in card["sections"]:
        lines.append(f"## {sec['title']}")
        lines.append(f"- `section_id`: `{sec['section_id']}`")
        lines.append(f"- `authority_label`: `{sec['authority_label']}`")
        for item in sec["fields"]:
            value = item["value"]
            if isinstance(value, (dict, list)):
                value_text = json.dumps(value, ensure_ascii=False, sort_keys=True)
            else:
                value_text = str(value)
            lines.append(f"- `{item['field_id']}` / `{item['authority_label']}`: {value_text}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate BDP-001R source-bound description")
    parser.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    parser.add_argument("--markdown", action="store_true", help="print Markdown (default)")
    parser.add_argument("--offline-preview", action="store_true", help="generate preview without psql")
    args = parser.parse_args()

    card = build_description_card(offline=args.offline_preview)
    if args.json:
        print(json.dumps(card, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(card_to_markdown(card))


if __name__ == "__main__":
    main()
