#!/usr/bin/env python3
"""
BDP-002C — Richer Semantic Readback Surface Generator

Read-only generator for the Body without Organs semantic evidence card.

Default mode uses psql through Python subprocess only.
Offline preview mode is available for repository review in environments without psql;
it is explicitly labelled in the generated audit boundary and must not be treated
as a live database verification.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from typing import Any, Dict, List

DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")

CONTROLLED_AUTHORITY_LABELS = {
    "concept_record",
    "metadata",
    "citation_backed",
    "citation_backed_passage",
    "primary_text_backed",
    "reviewed_concept_mention",
    "source_bound_description",
    "record_description",
    "rights_display_boundary",
    "buchanan_pending",
    "blocked_until_reviewed_relation_evidence",
    "blocked_until_governed_interpretation_phase",
    "blocked_until_interpretive_authority_exists",
    "needs_review",
    "provisional_synthesis",
    "system_synthesis",
    "user_interpretation",
    "experimental_modelling",
    "secondary_scholarship",
}

REQUIRED_SECTION_IDS = [
    "concept_identity",
    "evidence_depth_tier",
    "canonical_source_metadata",
    "citation_backed_passage_record",
    "reviewed_concept_mention_record",
    "rights_display_boundary",
    "current_database_invariant",
    "source_bound_evidence_posture",
    "buchanan_specific_explanation_boundary",
    "relation_layer_status",
    "interpretation_layer_status",
    "related_concept_candidates",
    "psycho_linguistic_placeholder_observations",
    "verification_and_audit_boundary",
    "next_recommended_operator_action",
]

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
    "buchanan_article_passage_count": 1,
    "buchanan_article_citation_count": 1,
    "buchanan_article_concept_mention_count": 1,
}

NEW_SECONDARY_SOURCE_CANDIDATES = [
    {
        "title": "Deleuze and Space",
        "author_or_editor": "Ian Buchanan and Gregg Lambert, eds.",
        "year": 2005,
        "source_type": "edited_collection",
        "pdf_document_id": "VtUTk",
        "candidate_status": "candidate_pending_governed_database_intake",
        "rights_status": "restricted",
        "display_rule": "reference_only",
        "evidence_tier": "Tier 2 — Supporting Scholarship",
        "intended_concept_links": ["assemblage", "Body without Organs", "smooth space", "striated space"],
        "readback_scope": "metadata_only_no_pdf_excerpt_reviewed_in_bdp_002c",
    },
    {
        "title": "Assemblage Theory and Method",
        "author_or_editor": "Ian Buchanan",
        "year": 2021,
        "source_type": "book",
        "pdf_document_id": "XJVks",
        "candidate_status": "candidate_pending_governed_database_intake",
        "rights_status": "restricted",
        "display_rule": "reference_only",
        "evidence_tier": "Tier 2 — Supporting Scholarship",
        "intended_concept_links": ["assemblage", "method", "Body without Organs", "desire"],
        "readback_scope": "metadata_only_no_pdf_excerpt_reviewed_in_bdp_002c",
    },
    {
        "title": "Deleuze and Guattari's Anti-Oedipus: A Reader's Guide",
        "author_or_editor": "Ian Buchanan",
        "year": 2008,
        "source_type": "book",
        "pdf_document_id": "Tl9xR",
        "candidate_status": "candidate_pending_governed_database_intake",
        "rights_status": "restricted",
        "display_rule": "reference_only",
        "evidence_tier": "Tier 2 — Supporting Scholarship",
        "intended_concept_links": ["desire", "schizoanalysis", "Body without Organs", "Anti-Oedipus"],
        "readback_scope": "metadata_only_no_pdf_excerpt_reviewed_in_bdp_002c",
    },
]

SQL_QUERIES = {
    "current_invariant": """
        SELECT
            (SELECT COUNT(*) FROM sources),
            (SELECT COUNT(*) FROM source_candidates),
            (SELECT COUNT(*) FROM passage_candidates),
            (SELECT COUNT(*) FROM passages),
            (SELECT COUNT(*) FROM citations),
            (SELECT COUNT(*) FROM concept_mentions),
            (SELECT COUNT(*) FROM concept_relations),
            (SELECT COUNT(*) FROM interpretations),
            (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001P'),
            (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-002C'),
            (SELECT COUNT(*) FROM passages p JOIN sources s ON s.id = p.source_id WHERE s.author = 'Ian Buchanan' AND s.title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'),
            (SELECT COUNT(*) FROM citations c JOIN sources s ON s.id = c.source_id WHERE s.author = 'Ian Buchanan' AND s.title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'),
            (SELECT COUNT(*) FROM concept_mentions cm JOIN passages p ON p.id = cm.passage_id JOIN sources s ON s.id = p.source_id JOIN concepts co ON co.id = cm.concept_id WHERE s.author = 'Ian Buchanan' AND s.title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?' AND co.name = 'Body without Organs' AND cm.reviewed_status = 'accepted');
    """,
    "canonical_buchanan_source_metadata": """
        SELECT
            title,
            author,
            COALESCE(type, ''),
            COALESCE(year::text, ''),
            COALESCE(publisher, ''),
            COALESCE(url_or_reference, ''),
            COALESCE(rights_status, ''),
            COALESCE(status, '')
        FROM sources
        WHERE author = 'Ian Buchanan'
          AND title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
        LIMIT 1;
    """,
}

FORBIDDEN_SQL_KEYWORDS = {
    "INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP", "TRUNCATE",
    "MERGE", "UPSERT", "GRANT", "REVOKE", "COPY", "CALL", "DO",
}


def _normalise_sql(sql: str) -> str:
    return " ".join(sql.strip().split())


def assert_select_only_sql(sql: str) -> None:
    compact = _normalise_sql(sql)
    upper_tokens = {token.strip(";,()") for token in compact.upper().split()}
    if not compact.upper().startswith("SELECT"):
        raise ValueError(f"Non-SELECT SQL blocked: {compact[:120]}")
    forbidden = sorted(FORBIDDEN_SQL_KEYWORDS.intersection(upper_tokens))
    if forbidden:
        raise ValueError(f"Mutation keyword(s) blocked in SQL: {', '.join(forbidden)}")


def run_psql_query(query: str) -> str:
    """Execute a SELECT-only query via psql subprocess."""
    assert_select_only_sql(query)
    cmd = ["psql", "-d", DB_NAME, "-t", "-A", "-F", "|", "-c", query]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "psql readback failed")
    return result.stdout.strip()


def get_current_invariant(offline_preview: bool = False) -> Dict[str, int]:
    if offline_preview:
        return dict(EXPECTED_INVARIANT)

    raw = run_psql_query(SQL_QUERIES["current_invariant"])
    values = [int(value or 0) for value in raw.split("|")]
    keys = list(EXPECTED_INVARIANT.keys())
    return dict(zip(keys, values))


def get_canonical_buchanan_source_metadata(offline_preview: bool = False) -> Dict[str, Any]:
    if offline_preview:
        return {
            "title": "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?",
            "author": "Ian Buchanan",
            "type": "article",
            "year": "1997",
            "publisher": "SAGE Publications",
            "url_or_reference": "https://doi.org/10.1177/1357034X97003003004",
            "rights_status": "restricted",
            "status": "canonical",
        }

    raw = run_psql_query(SQL_QUERIES["canonical_buchanan_source_metadata"])
    values = raw.split("|") if raw else ["", "", "", "", "", "", "", ""]
    return {
        "title": values[0],
        "author": values[1],
        "type": values[2],
        "year": values[3],
        "publisher": values[4],
        "url_or_reference": values[5],
        "rights_status": values[6],
        "status": values[7],
    }


def field(field_id: str, label: str, value: Any, authority_label: str) -> Dict[str, Any]:
    return {
        "field_id": field_id,
        "label": label,
        "value": value,
        "authority_label": authority_label,
    }


def observation(observation_id: str, observation_type: str, observation_text: str) -> Dict[str, Any]:
    return {
        "observation_id": observation_id,
        "observation_type": observation_type,
        "observation_text": observation_text,
        "authority_label": "experimental_modelling",
        "linked_passage_locator": "printed article page 76 / PDF page 4",
        "requires_human_review": True,
        "current_ceiling": "Level 2 Embedding Deviation",
        "objective_score_claimed": False,
    }


def section(section_id: str, title: str, authority_label: str, fields: List[Dict[str, Any]] | None = None, observations: List[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "section_id": section_id,
        "title": title,
        "authority_label": authority_label,
    }
    if fields is not None:
        payload["fields"] = fields
    if observations is not None:
        payload["observations"] = observations
    return payload


def generate_bdp_002c_card(offline_preview: bool = False) -> Dict[str, Any]:
    invariant = get_current_invariant(offline_preview=offline_preview)
    source_metadata = get_canonical_buchanan_source_metadata(offline_preview=offline_preview)

    secondary_candidate_fields = [
        field(
            f"secondary_source_candidate_{index}",
            candidate["title"],
            candidate,
            "secondary_scholarship",
        )
        for index, candidate in enumerate(NEW_SECONDARY_SOURCE_CANDIDATES, start=1)
    ]

    sections = [
        section(
            "concept_identity",
            "Concept Identity",
            "concept_record",
            [
                field("concept_name", "Preferred concept name", "Body without Organs", "concept_record"),
                field("concept_alias", "Common abbreviation", "BwO", "concept_record"),
                field("anchor_status", "Concept role", "Tier 1 anchor concept", "concept_record"),
            ],
        ),
        section(
            "evidence_depth_tier",
            "Evidence Depth Tier",
            "record_description",
            [
                field("tier", "Evidence tier", "Tier 1 — Anchor Concept", "record_description"),
                field("authority_rule", "Authority rule", "High-authority claims remain blocked until reviewed evidence exists.", "record_description"),
            ],
        ),
        section(
            "canonical_source_metadata",
            "Canonical Source Metadata",
            "metadata",
            [
                field("buchanan_article_metadata", "Canonical Buchanan article metadata", source_metadata, "metadata"),
                field("secondary_source_candidate_count", "New secondary source candidates prepared for state registry", len(NEW_SECONDARY_SOURCE_CANDIDATES), "secondary_scholarship"),
                *secondary_candidate_fields,
            ],
        ),
        section(
            "citation_backed_passage_record",
            "Citation-Backed Passage Record",
            "citation_backed_passage",
            [
                field("passage_status", "Buchanan passage status", "one restricted citation-backed Buchanan passage exists", "citation_backed_passage"),
                field("passage_locator", "Governed locator", "printed article page 76 / PDF page 4", "citation_backed_passage"),
                field("passage_text_display", "Passage text display", "omitted_by_rights_policy", "rights_display_boundary"),
            ],
        ),
        section(
            "reviewed_concept_mention_record",
            "Reviewed Concept Mention Record",
            "reviewed_concept_mention",
            [
                field("mention_status", "Concept mention status", "reviewed direct concept mention links the Buchanan passage to Body without Organs", "reviewed_concept_mention"),
                field("mention_boundary", "Concept mention boundary", "concept mention is not concept relation, interpretation, or Buchanan-specific claim", "reviewed_concept_mention"),
            ],
        ),
        section(
            "rights_display_boundary",
            "Rights Display Boundary",
            "rights_display_boundary",
            [
                field("rights_status", "Rights status", "restricted", "rights_display_boundary"),
                field("display_rule", "Display rule", "reference_only", "rights_display_boundary"),
                field("passage_text_display", "Passage text display", "omitted_by_rights_policy", "rights_display_boundary"),
                field("long_quotation_displayed", "Long quotation displayed", False, "rights_display_boundary"),
                field("article_reproduction_authorized", "Article reproduction authorized", False, "rights_display_boundary"),
                field("secondary_pdf_display_boundary", "New PDF display boundary", "metadata-only candidate descriptions; no PDF excerpts reviewed or displayed in BDP-002C", "rights_display_boundary"),
            ],
        ),
        section(
            "current_database_invariant",
            "Current Database Invariant",
            "metadata",
            [field("invariant", "Readback invariant", invariant, "metadata")],
        ),
        section(
            "source_bound_evidence_posture",
            "Source-Bound Evidence Posture",
            "source_bound_description",
            [
                field("allowed_description", "Allowed source-bound description", "The database records a restricted citation-backed Buchanan passage linked to Body without Organs through a reviewed direct concept mention.", "source_bound_description"),
                field("secondary_scholarship_posture", "Secondary scholarship posture", "Three new Buchanan works are prepared as metadata-only state source candidates for later governed intake.", "secondary_scholarship"),
                field("blocked_upgrade", "Blocked upgrade", "No author-position claim, theoretical consequence, relation, or interpretation is generated by this card.", "blocked_until_interpretive_authority_exists"),
            ],
        ),
        section(
            "buchanan_specific_explanation_boundary",
            "Buchanan-Specific Explanation Boundary",
            "buchanan_pending",
            [
                field("buchanan_specific_explanation_status", "Buchanan-specific explanation status", "buchanan_pending", "buchanan_pending"),
                field("buchanan_specific_interpretation_status", "Buchanan-specific interpretation status", "blocked_until_governed_interpretation_phase", "blocked_until_governed_interpretation_phase"),
                field("buchanan_specific_claim_status", "Buchanan-specific claim status", "blocked_until_interpretive_authority_exists", "blocked_until_interpretive_authority_exists"),
            ],
        ),
        section(
            "relation_layer_status",
            "Relation Layer Status",
            "blocked_until_reviewed_relation_evidence",
            [
                field("concept_relation_count", "Concept relation count", invariant.get("concept_relations_count"), "metadata"),
                field("relation_status", "Relation status", "blocked_until_reviewed_relation_evidence", "blocked_until_reviewed_relation_evidence"),
            ],
        ),
        section(
            "interpretation_layer_status",
            "Interpretation Layer Status",
            "blocked_until_governed_interpretation_phase",
            [
                field("interpretation_count", "Interpretation count", invariant.get("interpretations_count"), "metadata"),
                field("interpretation_status", "Interpretation status", "blocked_until_governed_interpretation_phase", "blocked_until_governed_interpretation_phase"),
            ],
        ),
        section(
            "related_concept_candidates",
            "Related Concept Candidates",
            "record_description",
            [
                field("related_concepts", "Related concept candidates", ["organism", "desire", "assemblage", "strata", "deterritorialisation", "smooth space", "striated space", "schizoanalysis"], "record_description"),
                field("candidate_boundary", "Candidate boundary", "related concept listing does not create concept relations", "record_description"),
            ],
        ),
        section(
            "psycho_linguistic_placeholder_observations",
            "Psycho-Linguistic Placeholder Observations",
            "experimental_modelling",
            observations=[
                observation("metaphor_density_placeholder", "metaphor_density_placeholder", "Placeholder only; no objective score asserted."),
                observation("abstraction_gradient_placeholder", "abstraction_gradient_placeholder", "Placeholder only; no objective score asserted."),
                observation("rhetorical_destabilisation_placeholder", "rhetorical_destabilisation_placeholder", "Placeholder only; no objective score asserted."),
                observation("semantic_drift_placeholder", "semantic_drift_placeholder", "Placeholder only; no objective score asserted."),
            ],
        ),
        section(
            "verification_and_audit_boundary",
            "Verification and Audit Boundary",
            "record_description",
            [
                field("readback_mode", "Readback mode", "offline_preview" if offline_preview else "psql_subprocess_live_readback", "record_description"),
                field("sql_migration", "SQL migration added", False, "record_description"),
                field("database_mutation", "Database mutation performed", False, "record_description"),
                field("psycopg_dependency", "psycopg dependency", False, "record_description"),
                field("psycopg2_dependency", "psycopg2 dependency", False, "record_description"),
                field("sql_boundary", "SQL boundary", "SELECT-only psql subprocess readback", "record_description"),
            ],
        ),
        section(
            "next_recommended_operator_action",
            "Next Recommended Operator Action",
            "record_description",
            [
                field("primary_next_action", "Primary next action", "BDP-001R — Prepare first source-bound Buchanan Body without Organs description candidate, without interpretation.", "record_description"),
                field("secondary_next_action", "Secondary source-candidate action", "Review whether the three new PDFs should be inserted into source_candidates through a later governed database intake phase.", "secondary_scholarship"),
                field("governance_note", "Governance note", "BDP-002C itself remains read-only and does not insert the new PDFs into the database.", "record_description"),
            ],
        ),
    ]

    return {
        "card_id": "bdp_002c_richer_bwo_semantic_readback",
        "bdp_phase": "BDP-002C",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "offline_preview": offline_preview,
        "controlled_authority_labels": sorted(CONTROLLED_AUTHORITY_LABELS),
        "sections": sections,
    }


def to_markdown(card: Dict[str, Any]) -> str:
    lines = ["# BDP-002C Richer Semantic Readback Card — Body without Organs", ""]
    lines.append(f"- `bdp_phase`: `{card['bdp_phase']}`")
    lines.append(f"- `offline_preview`: `{str(card['offline_preview']).lower()}`")
    lines.append("")
    for sec in card["sections"]:
        lines.append(f"## {sec['section_id']} — {sec['title']}")
        lines.append(f"- `authority_label`: `{sec['authority_label']}`")
        for item in sec.get("fields", []):
            value = item["value"]
            if isinstance(value, (dict, list)):
                value_text = json.dumps(value, ensure_ascii=False, sort_keys=True)
            else:
                value_text = str(value)
            lines.append(f"- `{item['field_id']}` / `{item['authority_label']}`: {value_text}")
        for item in sec.get("observations", []):
            lines.append(f"- `{item['observation_id']}` / `{item['authority_label']}`: {item['observation_text']}")
            lines.append(f"  - locator: `{item['linked_passage_locator']}`")
            lines.append(f"  - requires_human_review: `{str(item['requires_human_review']).lower()}`")
            lines.append(f"  - current_ceiling: `{item['current_ceiling']}`")
            lines.append(f"  - objective_score_claimed: `{str(item['objective_score_claimed']).lower()}`")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the BDP-002C richer semantic readback card.")
    parser.add_argument("--offline-preview", action="store_true", help="Generate a labelled offline preview without psql.")
    parser.add_argument("--format", choices=["json", "markdown", "both"], default="both")
    args = parser.parse_args()

    card = generate_bdp_002c_card(offline_preview=args.offline_preview)
    if args.format in {"json", "both"}:
        print(json.dumps(card, indent=2, ensure_ascii=False, sort_keys=True))
    if args.format == "both":
        print("\n=== MARKDOWN ===\n")
    if args.format in {"markdown", "both"}:
        print(to_markdown(card))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
