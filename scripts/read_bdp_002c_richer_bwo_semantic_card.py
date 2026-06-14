#!/usr/bin/env python3
"""BDP-002C richer Body without Organs semantic readback card.

Read-only boundary:
- uses psql through Python subprocess only
- imports no psycopg / psycopg2
- passes SELECT-only SQL to psql
- writes only local JSON/Markdown readback artifacts
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PHASE = "BDP-002C"
ANCHOR_CONCEPT_NAME = "Body without Organs"
BUCHANAN_ARTICLE_TITLE_MATCH = "The Problem of the Body in Deleuze and Guattari"
DEFAULT_DB_NAME = "buchanan_platform_dev"
DEFAULT_OUT_DIR = Path("build/bdp_002c_richer_semantic_readback")
EXPECTED_BUCHANAN_LOCATOR = "printed article page 76 / PDF page 4"
CURRENT_MODELLING_CEILING = "Level 2 Embedding Deviation"

ALLOWED_AUTHORITY_LABELS = {
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
    "bdp_002c_migration_count": 0,
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

SQL_QUERIES = {
    "invariant_counts": """
        SELECT
          (SELECT COUNT(*)::int FROM sources) AS sources_count,
          (SELECT COUNT(*)::int FROM source_candidates) AS source_candidates_count,
          (SELECT COUNT(*)::int FROM passage_candidates) AS passage_candidates_count,
          (SELECT COUNT(*)::int FROM passages) AS passages_count,
          (SELECT COUNT(*)::int FROM citations) AS citations_count,
          (SELECT COUNT(*)::int FROM concept_mentions) AS concept_mentions_count,
          (SELECT COUNT(*)::int FROM concept_relations) AS concept_relations_count,
          (SELECT COUNT(*)::int FROM interpretations) AS interpretations_count,
          (SELECT COUNT(*)::int FROM schema_migrations WHERE phase = 'BDP-001P') AS bdp_001p_migration_count,
          (SELECT COUNT(*)::int FROM schema_migrations WHERE phase = 'BDP-002C') AS bdp_002c_migration_count
    """,
    "concept_record": """
        SELECT
          id::text AS concept_id,
          name,
          aliases,
          short_description,
          status
        FROM concepts
        WHERE name = 'Body without Organs'
        LIMIT 1
    """,
    "buchanan_source_metadata": """
        SELECT
          s.id::text AS source_id,
          s.title,
          s.author,
          s.type,
          s.year,
          s.publisher,
          s.url_or_reference,
          s.rights_status,
          s.reliability_level,
          s.status,
          COALESCE(s.metadata, '{}'::jsonb) AS metadata
        FROM sources s
        WHERE lower(s.author) LIKE '%buchanan%'
          AND lower(s.title) LIKE '%problem of the body in deleuze%'
        ORDER BY s.created_at ASC
        LIMIT 1
    """,
    "buchanan_passage_candidate": """
        SELECT
          pc.id::text AS passage_candidate_id,
          pc.candidate_label,
          pc.candidate_status,
          pc.candidate_scope,
          pc.candidate_text_status,
          pc.page_or_timestamp,
          pc.chapter_or_section,
          pc.locator_status,
          pc.rights_status,
          pc.display_rule,
          pc.review_status,
          pc.inserted_as_passage,
          pc.citation_ready,
          pc.concept_mention_ready,
          pc.interpretation_ready,
          pc.buchanan_claim_ready,
          COALESCE(pc.metadata, '{}'::jsonb) AS metadata
        FROM passage_candidates pc
        JOIN sources s ON s.id = pc.source_id
        JOIN concepts c ON c.id = pc.concept_id
        WHERE c.name = 'Body without Organs'
          AND lower(s.author) LIKE '%buchanan%'
          AND lower(s.title) LIKE '%problem of the body in deleuze%'
        ORDER BY pc.created_at ASC
        LIMIT 1
    """,
    "buchanan_evidence_chain": """
        SELECT
          cm.id::text AS concept_mention_id,
          cm.mention_type,
          cm.reviewed_status,
          cm.confidence,
          p.id::text AS passage_id,
          p.page_or_timestamp AS passage_page_or_timestamp,
          p.chapter_or_section AS passage_chapter_or_section,
          ctn.id::text AS citation_id,
          ctn.locator AS citation_locator,
          ctn.page_or_timestamp AS citation_page_or_timestamp,
          ctn.chapter_or_section AS citation_chapter_or_section,
          ctn.rights_status AS citation_rights_status,
          ctn.display_rule AS citation_display_rule,
          s.id::text AS source_id,
          s.title AS source_title,
          s.author AS source_author,
          s.year AS source_year,
          s.url_or_reference AS source_reference
        FROM concept_mentions cm
        JOIN concepts c ON c.id = cm.concept_id
        JOIN passages p ON p.id = cm.passage_id
        JOIN sources s ON s.id = p.source_id
        LEFT JOIN citations ctn ON ctn.passage_id = p.id
        WHERE c.name = 'Body without Organs'
          AND lower(s.author) LIKE '%buchanan%'
          AND lower(s.title) LIKE '%problem of the body in deleuze%'
        ORDER BY cm.created_at ASC
    """,
    "related_concept_candidates": """
        SELECT
          id::text AS concept_id,
          name,
          status
        FROM concepts
        WHERE name IN ('organism', 'desire', 'assemblage', 'strata')
        ORDER BY name ASC
    """,
    "supplemental_buchanan_counts": """
        SELECT
          (
            SELECT COUNT(*)::int
            FROM passages p
            JOIN sources s ON s.id = p.source_id
            WHERE lower(s.author) LIKE '%buchanan%'
              AND lower(s.title) LIKE '%problem of the body in deleuze%'
          ) AS buchanan_article_passage_count,
          (
            SELECT COUNT(*)::int
            FROM citations ctn
            JOIN sources s ON s.id = ctn.source_id
            WHERE lower(s.author) LIKE '%buchanan%'
              AND lower(s.title) LIKE '%problem of the body in deleuze%'
          ) AS buchanan_article_citation_count,
          (
            SELECT COUNT(*)::int
            FROM concept_mentions cm
            JOIN passages p ON p.id = cm.passage_id
            JOIN sources s ON s.id = p.source_id
            JOIN concepts c ON c.id = cm.concept_id
            WHERE c.name = 'Body without Organs'
              AND lower(s.author) LIKE '%buchanan%'
              AND lower(s.title) LIKE '%problem of the body in deleuze%'
          ) AS buchanan_article_concept_mention_count
    """,
}


def _normalise_sql(sql: str) -> str:
    return "\n".join(line.rstrip() for line in sql.strip().splitlines())


def _psql_json_rows(db_name: str, sql: str) -> list[dict[str, Any]]:
    wrapped_sql = (
        "SELECT COALESCE(jsonb_agg(to_jsonb(q)), '[]'::jsonb)::text "
        f"FROM ({_normalise_sql(sql)}) q;"
    )
    completed = subprocess.run(
        ["psql", "-X", "-q", "-d", db_name, "-v", "ON_ERROR_STOP=1", "-t", "-A", "-c", wrapped_sql],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "psql readback failed\n"
            f"database: {db_name}\n"
            f"stderr:\n{completed.stderr.strip()}\n"
        )
    raw = completed.stdout.strip()
    if not raw:
        return []
    parsed = json.loads(raw)
    if not isinstance(parsed, list):
        raise RuntimeError(f"Expected JSON array from psql, got {type(parsed).__name__}")
    return parsed


def _fetch_one(db_name: str, sql_key: str) -> dict[str, Any]:
    rows = _psql_json_rows(db_name, SQL_QUERIES[sql_key])
    return rows[0] if rows else {}


def _fetch_all(db_name: str, sql_key: str) -> list[dict[str, Any]]:
    return _psql_json_rows(db_name, SQL_QUERIES[sql_key])


def collect_database_state(db_name: str) -> dict[str, Any]:
    invariant = _fetch_one(db_name, "invariant_counts")
    supplemental = _fetch_one(db_name, "supplemental_buchanan_counts")
    return {**invariant, **supplemental}


def labelled_field(
    field_id: str,
    label: str,
    value: Any,
    authority_label: str,
    evidence_locator: str | None = None,
) -> dict[str, Any]:
    if authority_label not in ALLOWED_AUTHORITY_LABELS:
        raise ValueError(f"Unsupported authority label for {field_id}: {authority_label}")
    field: dict[str, Any] = {
        "field_id": field_id,
        "label": label,
        "value": value,
        "authority_label": authority_label,
    }
    if evidence_locator:
        field["evidence_locator"] = evidence_locator
    return field


def section(
    section_id: str,
    title: str,
    authority_label: str,
    fields: list[dict[str, Any]] | None = None,
    observations: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if authority_label not in ALLOWED_AUTHORITY_LABELS:
        raise ValueError(f"Unsupported section authority label for {section_id}: {authority_label}")
    payload: dict[str, Any] = {
        "section_id": section_id,
        "title": title,
        "authority_label": authority_label,
    }
    if fields is not None:
        payload["fields"] = fields
    if observations is not None:
        payload["observations"] = observations
    return payload


def observation(
    observation_id: str,
    observation_type: str,
    observation_text: str,
    linked_passage_locator: str,
) -> dict[str, Any]:
    return {
        "observation_id": observation_id,
        "observation_type": observation_type,
        "observation_text": observation_text,
        "authority_label": "experimental_modelling",
        "linked_passage_locator": linked_passage_locator,
        "requires_human_review": True,
        "current_ceiling": CURRENT_MODELLING_CEILING,
        "objective_score_claimed": False,
    }


def _first_non_empty(*values: Any, fallback: str = "not_recorded") -> Any:
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return fallback


def _evidence_locator(candidate: dict[str, Any], evidence_chain: list[dict[str, Any]]) -> str:
    evidence = evidence_chain[0] if evidence_chain else {}
    return str(
        _first_non_empty(
            evidence.get("citation_locator"),
            evidence.get("citation_page_or_timestamp"),
            evidence.get("passage_page_or_timestamp"),
            candidate.get("page_or_timestamp"),
            fallback=EXPECTED_BUCHANAN_LOCATOR,
        )
    )


def build_card(db_name: str) -> dict[str, Any]:
    counts = collect_database_state(db_name)
    concept = _fetch_one(db_name, "concept_record")
    source = _fetch_one(db_name, "buchanan_source_metadata")
    candidate = _fetch_one(db_name, "buchanan_passage_candidate")
    evidence_chain = _fetch_all(db_name, "buchanan_evidence_chain")
    related = _fetch_all(db_name, "related_concept_candidates")
    locator = _evidence_locator(candidate, evidence_chain)
    evidence = evidence_chain[0] if evidence_chain else {}

    related_fields = [
        labelled_field(
            f"related_concept_{idx}",
            row.get("name", "unknown"),
            {"concept_id": row.get("concept_id"), "status": row.get("status")},
            "concept_record",
        )
        for idx, row in enumerate(related, start=1)
    ]
    if not related_fields:
        related_fields = [
            labelled_field(
                "related_concepts_status",
                "Related concept candidates",
                "No related concept candidate records were returned by the readback query.",
                "record_description",
            )
        ]

    invariant_fields = [
        labelled_field(key, key, counts.get(key), "record_description")
        for key in [
            "sources_count",
            "source_candidates_count",
            "passage_candidates_count",
            "passages_count",
            "citations_count",
            "concept_mentions_count",
            "concept_relations_count",
            "interpretations_count",
            "bdp_001p_migration_count",
            "bdp_002c_migration_count",
            "buchanan_article_passage_count",
            "buchanan_article_citation_count",
            "buchanan_article_concept_mention_count",
        ]
    ]

    sections = [
        section(
            "concept_identity",
            "Concept identity",
            "concept_record",
            [
                labelled_field("concept_name", "Concept name", concept.get("name", ANCHOR_CONCEPT_NAME), "concept_record"),
                labelled_field("concept_id", "Concept ID", concept.get("concept_id", "not_recorded"), "concept_record"),
                labelled_field("concept_status", "Concept status", concept.get("status", "not_recorded"), "concept_record"),
                labelled_field("aliases", "Aliases", concept.get("aliases", []), "concept_record"),
            ],
        ),
        section(
            "evidence_depth_tier",
            "Evidence depth tier",
            "record_description",
            [
                labelled_field("tier", "Tier", "Tier 1 — Anchor Concept", "record_description"),
                labelled_field(
                    "authority_rule",
                    "Authority rule",
                    "High-authority claims remain blocked until citation-backed interpretation evidence exists.",
                    "record_description",
                ),
            ],
        ),
        section(
            "canonical_source_metadata",
            "Canonical Buchanan source metadata",
            "metadata",
            [
                labelled_field("source_id", "Source ID", source.get("source_id", "not_recorded"), "metadata"),
                labelled_field("title", "Title", source.get("title", "not_recorded"), "metadata"),
                labelled_field("author", "Author", source.get("author", "not_recorded"), "metadata"),
                labelled_field("year", "Year", source.get("year", "not_recorded"), "metadata"),
                labelled_field("source_type", "Source type", source.get("type", "not_recorded"), "metadata"),
                labelled_field("rights_status", "Rights status", source.get("rights_status", "not_recorded"), "rights_display_boundary"),
                labelled_field("reliability_level", "Reliability level", source.get("reliability_level", "not_recorded"), "metadata"),
                labelled_field("status", "Canonical status", source.get("status", "not_recorded"), "metadata"),
            ],
        ),
        section(
            "citation_backed_passage_record",
            "Citation-backed Buchanan passage record",
            "citation_backed_passage",
            [
                labelled_field("passage_id", "Passage ID", evidence.get("passage_id", "not_recorded"), "citation_backed_passage", locator),
                labelled_field("citation_id", "Citation ID", evidence.get("citation_id", "not_recorded"), "citation_backed", locator),
                labelled_field("citation_locator", "Citation locator", _first_non_empty(evidence.get("citation_locator"), locator), "citation_backed", locator),
                labelled_field("page_or_timestamp", "Page or timestamp", _first_non_empty(evidence.get("citation_page_or_timestamp"), evidence.get("passage_page_or_timestamp"), locator), "citation_backed", locator),
                labelled_field("passage_text_display", "Passage text display", "omitted_by_rights_policy", "rights_display_boundary", locator),
            ],
        ),
        section(
            "reviewed_concept_mention_record",
            "Reviewed concept mention record",
            "reviewed_concept_mention",
            [
                labelled_field("concept_mention_id", "Concept mention ID", evidence.get("concept_mention_id", "not_recorded"), "reviewed_concept_mention", locator),
                labelled_field("mention_type", "Mention type", evidence.get("mention_type", "not_recorded"), "reviewed_concept_mention", locator),
                labelled_field("reviewed_status", "Reviewed status", evidence.get("reviewed_status", "not_recorded"), "reviewed_concept_mention", locator),
                labelled_field("confidence", "Recorded confidence", evidence.get("confidence", "not_recorded"), "reviewed_concept_mention", locator),
            ],
        ),
        section(
            "rights_display_boundary",
            "Rights display boundary",
            "rights_display_boundary",
            [
                labelled_field("rights_status", "Rights status", _first_non_empty(evidence.get("citation_rights_status"), source.get("rights_status")), "rights_display_boundary", locator),
                labelled_field("display_rule", "Display rule", _first_non_empty(evidence.get("citation_display_rule"), "reference_only"), "rights_display_boundary", locator),
                labelled_field("passage_text_display", "Passage text display", "omitted_by_rights_policy", "rights_display_boundary", locator),
                labelled_field("long_quotation_displayed", "Long quotation displayed", False, "rights_display_boundary", locator),
                labelled_field("article_reproduction_authorized", "Article reproduction authorized", False, "rights_display_boundary", locator),
            ],
        ),
        section(
            "current_database_invariant",
            "Current database invariant",
            "record_description",
            invariant_fields,
        ),
        section(
            "source_bound_evidence_posture",
            "Source-bound evidence posture",
            "source_bound_description",
            [
                labelled_field(
                    "allowed_description",
                    "Allowed description",
                    "The database records a restricted citation-backed Buchanan passage linked to Body without Organs through a reviewed direct concept mention.",
                    "source_bound_description",
                    locator,
                ),
                labelled_field(
                    "description_scope",
                    "Description scope",
                    "This describes governed records and evidence posture only; it does not attribute a position, argument, intention, conceptual meaning, or theoretical consequence to the author.",
                    "record_description",
                    locator,
                ),
            ],
        ),
        section(
            "buchanan_specific_explanation_boundary",
            "Buchanan-specific explanation boundary",
            "buchanan_pending",
            [
                labelled_field("buchanan_specific_explanation_status", "Buchanan-specific explanation status", "buchanan_pending", "buchanan_pending", locator),
                labelled_field("buchanan_specific_interpretation_status", "Buchanan-specific interpretation status", "blocked_until_governed_interpretation_phase", "blocked_until_governed_interpretation_phase", locator),
                labelled_field("buchanan_specific_claim_status", "Buchanan-specific claim status", "blocked_until_interpretive_authority_exists", "blocked_until_interpretive_authority_exists", locator),
            ],
        ),
        section(
            "relation_layer_status",
            "Relation layer status",
            "blocked_until_reviewed_relation_evidence",
            [
                labelled_field("concept_relations_count", "Concept relations count", counts.get("concept_relations_count"), "record_description"),
                labelled_field("relation_status", "Relation status", "blocked_until_reviewed_relation_evidence", "blocked_until_reviewed_relation_evidence", locator),
            ],
        ),
        section(
            "interpretation_layer_status",
            "Interpretation layer status",
            "blocked_until_governed_interpretation_phase",
            [
                labelled_field("interpretations_count", "Interpretations count", counts.get("interpretations_count"), "record_description"),
                labelled_field("interpretation_status", "Interpretation status", "blocked_until_governed_interpretation_phase", "blocked_until_governed_interpretation_phase", locator),
                labelled_field("claim_status", "Claim status", "blocked_until_interpretive_authority_exists", "blocked_until_interpretive_authority_exists", locator),
            ],
        ),
        section(
            "related_concept_candidates",
            "Related concept candidates",
            "concept_record",
            related_fields,
        ),
        section(
            "psycho_linguistic_placeholder_observations",
            "Psycho-linguistic placeholder observations",
            "experimental_modelling",
            observations=[
                observation(
                    "metaphor_density_placeholder",
                    "metaphor_density_placeholder",
                    "Placeholder only. No objective metaphor-density score is asserted by this card.",
                    locator,
                ),
                observation(
                    "abstraction_gradient_placeholder",
                    "abstraction_gradient_placeholder",
                    "Placeholder only. No abstraction-gradient result is promoted to concept authority.",
                    locator,
                ),
                observation(
                    "rhetorical_destabilisation_placeholder",
                    "rhetorical_destabilisation_placeholder",
                    "Placeholder only. No Buchanan-specific interpretation is generated from rhetorical movement modelling.",
                    locator,
                ),
                observation(
                    "semantic_drift_placeholder",
                    "semantic_drift_placeholder",
                    "Placeholder only. Semantic drift remains a later reviewed modelling surface.",
                    locator,
                ),
            ],
        ),
        section(
            "verification_and_audit_boundary",
            "Verification and audit boundary",
            "record_description",
            [
                labelled_field("read_only_status", "Read-only status", True, "record_description"),
                labelled_field("psql_subprocess_only", "psql subprocess only", True, "record_description"),
                labelled_field("psycopg_dependency", "psycopg dependency", False, "record_description"),
                labelled_field("psycopg2_dependency", "psycopg2 dependency", False, "record_description"),
                labelled_field("sql_migration", "SQL migration", False, "record_description"),
                labelled_field("database_mutation", "Database mutation", False, "record_description"),
            ],
        ),
        section(
            "next_recommended_operator_action",
            "Next recommended operator action",
            "record_description",
            [
                labelled_field("primary_next_action", "Primary next action", "BDP-001R — Prepare first source-bound Buchanan Body without Organs description candidate, without interpretation.", "record_description"),
                labelled_field("governance_note", "Governance note", "Prepare a source-bound description candidate only; do not create a concept relation, interpretation, theoretical consequence, or author-position claim.", "record_description"),
            ],
        ),
    ]

    return {
        "phase": PHASE,
        "title": "Richer Semantic Readback Surface",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "authority_label": "record_description",
        "anchor_concept": ANCHOR_CONCEPT_NAME,
        "read_only": True,
        "schema_change": False,
        "database_mutation": False,
        "psql_subprocess_only": True,
        "authority_label_contract": {
            "authority_label": "record_description",
            "allowed_labels": sorted(ALLOWED_AUTHORITY_LABELS),
        },
        "required_section_ids": REQUIRED_SECTION_IDS,
        "sections": sections,
    }


def render_markdown(card: dict[str, Any]) -> str:
    lines = [
        f"# {card['phase']} — {card['title']}",
        "",
        f"Generated at: `{card['generated_at']}`",
        "",
        f"Anchor concept: `{card['anchor_concept']}`",
        "",
        "Read-only status: `true`",
        "",
        "Passage text display: `omitted_by_rights_policy`",
        "",
        "Long quotation displayed: `false`",
        "",
        "Article reproduction authorized: `false`",
        "",
        "## Authority Label Contract",
        "",
    ]
    for label in card["authority_label_contract"]["allowed_labels"]:
        lines.append(f"- `{label}`")
    lines.append("")

    for index, sec in enumerate(card["sections"], start=1):
        lines.extend([
            f"## {index:02d}. {sec['title']}",
            "",
            f"Section ID: `{sec['section_id']}`",
            "",
            f"Authority label: `{sec['authority_label']}`",
            "",
        ])
        for field in sec.get("fields", []):
            evidence = f"; evidence locator: `{field['evidence_locator']}`" if field.get("evidence_locator") else ""
            lines.append(
                f"- **{field['label']}**: `{field['value']}` "
                f"[authority_label=`{field['authority_label']}`{evidence}]"
            )
        for obs in sec.get("observations", []):
            lines.append(
                f"- **{obs['observation_type']}**: {obs['observation_text']} "
                f"[authority_label=`{obs['authority_label']}`; "
                f"linked_passage_locator=`{obs['linked_passage_locator']}`; "
                f"requires_human_review=`{str(obs['requires_human_review']).lower()}`; "
                f"current_ceiling=`{obs['current_ceiling']}`; "
                f"objective_score_claimed=`{str(obs['objective_score_claimed']).lower()}`]"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(card: dict[str, Any], out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "bdp_002c_richer_bwo_semantic_card.json"
    md_path = out_dir / "bdp_002c_richer_bwo_semantic_card.md"
    json_path.write_text(json.dumps(card, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(card), encoding="utf-8")
    return json_path, md_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate BDP-002C richer semantic readback card.")
    parser.add_argument("--db-name", default=os.environ.get("BUCHANAN_DB_NAME", DEFAULT_DB_NAME))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--json-only", action="store_true", help="Print card JSON to stdout without writing files.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    card = build_card(args.db_name)
    if args.json_only:
        print(json.dumps(card, indent=2, sort_keys=True))
        return 0
    json_path, md_path = write_outputs(card, Path(args.out_dir))
    print(f"[OK] wrote {json_path}")
    print(f"[OK] wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
