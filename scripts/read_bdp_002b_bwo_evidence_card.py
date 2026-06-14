#!/usr/bin/env python3
"""BDP-002B — operator-facing evidence card for Body without Organs.

This script is read-only. It uses psql through subprocess, follows the
Buchanan platform readback convention, and deliberately omits restricted
passage text from output.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any

DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")

SQL_COUNTS = r"""
SELECT json_build_object(
  'sources_count', (SELECT count(*) FROM sources),
  'source_candidates_count', (SELECT count(*) FROM source_candidates),
  'passage_candidates_count', (SELECT count(*) FROM passage_candidates),
  'passages_count', (SELECT count(*) FROM passages),
  'citations_count', (SELECT count(*) FROM citations),
  'concept_mentions_count', (SELECT count(*) FROM concept_mentions),
  'concept_relations_count', (SELECT count(*) FROM concept_relations),
  'interpretations_count', (SELECT count(*) FROM interpretations),
  'BDP-001P migration_count', (
    SELECT count(*) FROM schema_migrations WHERE phase = 'BDP-001P'
  ),
  'BDP-001Q migration_count', (
    SELECT count(*) FROM schema_migrations WHERE phase = 'BDP-001Q'
  ),
  'BDP-002B migration_count', (
    SELECT count(*) FROM schema_migrations WHERE phase = 'BDP-002B'
  )
);
"""

SQL_BUCHANAN_EVIDENCE = r"""
SELECT json_build_object(
  'concept', json_build_object(
    'id', c.id,
    'name', c.name,
    'status', c.status,
    'authority_label', 'concept_record'
  ),
  'source', json_build_object(
    'id', s.id,
    'title', s.title,
    'author', s.author,
    'type', s.type,
    'year', s.year,
    'publisher', s.publisher,
    'url_or_reference', s.url_or_reference,
    'rights_status', s.rights_status,
    'reliability_level', s.reliability_level,
    'status', s.status,
    'display_rule', COALESCE(s.metadata->>'display_rule', 'reference_only'),
    'authority_label', 'metadata'
  ),
  'citation', json_build_object(
    'id', ct.id,
    'locator', ct.locator,
    'page_or_timestamp', ct.page_or_timestamp,
    'chapter_or_section', ct.chapter_or_section,
    'rights_status', ct.rights_status,
    'display_rule', ct.display_rule,
    'citation_format', ct.citation_format,
    'url_or_reference', ct.url_or_reference,
    'authority_label', 'citation_backed'
  ),
  'passage', json_build_object(
    'id', p.id,
    'source_id', p.source_id,
    'page_or_timestamp', p.page_or_timestamp,
    'chapter_or_section', p.chapter_or_section,
    'rights_status', COALESCE(ct.rights_status, s.rights_status),
    'display_rule', COALESCE(ct.display_rule, s.metadata->>'display_rule', 'reference_only'),
    'passage_text_display', 'omitted_by_rights_policy',
    'authority_label', 'citation_backed_passage'
  ),
  'concept_mention', json_build_object(
    'id', cm.id,
    'mention_type', cm.mention_type,
    'reviewed_status', cm.reviewed_status,
    'confidence', cm.confidence,
    'authority_label', 'reviewed_concept_mention'
  )
)
FROM concept_mentions cm
JOIN concepts c ON c.id = cm.concept_id
JOIN passages p ON p.id = cm.passage_id
JOIN sources s ON s.id = p.source_id
LEFT JOIN citations ct ON ct.passage_id = p.id AND ct.source_id = s.id
WHERE c.name = 'Body without Organs'
  AND s.author ILIKE '%Buchanan%'
  AND s.title ILIKE '%The Problem of the Body%'
ORDER BY p.created_at DESC, cm.created_at DESC
LIMIT 1;
"""


def run_psql_json(sql: str) -> dict[str, Any]:
    command = [
        "psql",
        "-X",
        "-v",
        "ON_ERROR_STOP=1",
        "-d",
        DB_NAME,
        "-At",
        "-c",
        sql,
    ]
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    payload = result.stdout.strip()
    if not payload:
        raise RuntimeError("psql returned no JSON payload")
    return json.loads(payload)


def source_bound_description(evidence: dict[str, Any]) -> dict[str, str]:
    source = evidence["source"]
    citation = evidence["citation"]
    concept = evidence["concept"]
    locator = citation.get("locator") or citation.get("page_or_timestamp") or "recorded locator"
    title = source.get("title") or "the recorded Buchanan source"
    year = source.get("year") or "recorded year"
    concept_name = concept.get("name") or "the recorded concept"

    return {
        "authority_label": "source_bound_description",
        "claim_status": "non_interpretive_record_description",
        "text": (
            "The database records a restricted, citation-backed Buchanan passage "
            f"from {year}, {title}, at {locator}, linked to {concept_name} "
            "through a reviewed direct concept mention."
        ),
    }


def build_card() -> dict[str, Any]:
    counts = run_psql_json(SQL_COUNTS)
    evidence = run_psql_json(SQL_BUCHANAN_EVIDENCE)

    if not evidence:
        raise RuntimeError(
            "No Buchanan Body without Organs evidence chain found. "
            "Expected the BDP-001O passage/citation and BDP-001P concept mention."
        )

    card: dict[str, Any] = {
        "phase": "BDP-002B",
        "card_type": "operator_facing_evidence_card",
        "concept_identity": evidence["concept"],
        "evidence_chain": [
            {
                "layer": "canonical_buchanan_source",
                "status": "available",
                "authority_label": "metadata",
                "record": evidence["source"],
            },
            {
                "layer": "citation_backed_passage",
                "status": "available",
                "authority_label": "citation_backed_passage",
                "record": evidence["passage"],
                "citation": evidence["citation"],
            },
            {
                "layer": "reviewed_concept_mention",
                "status": "available",
                "authority_label": "reviewed_concept_mention",
                "record": evidence["concept_mention"],
            },
        ],
        "source_bound_description": source_bound_description(evidence),
        "blocked_layers": [
            {
                "layer": "concept_relation",
                "status": "blocked",
                "authority_label": "blocked_until_reviewed_relation_evidence",
            },
            {
                "layer": "interpretation",
                "status": "blocked",
                "authority_label": "blocked_until_governed_interpretation_phase",
            },
            {
                "layer": "buchanan_specific_claim",
                "status": "blocked",
                "authority_label": "blocked_until_interpretive_authority_exists",
            },
        ],
        "rights_display_rules": {
            "rights_status": evidence["passage"].get("rights_status") or "restricted",
            "display_rule": evidence["passage"].get("display_rule") or "reference_only",
            "passage_text_display": "omitted_by_rights_policy",
            "long_quotation_displayed": False,
            "article_reproduction_authorized": False,
            "authority_label": "rights_display_boundary",
        },
        "operator_readback": {
            "what_is_available": (
                "A canonical Buchanan source, citation-backed passage record, "
                "citation trail, and reviewed direct concept mention are available."
            ),
            "what_is_not_available": (
                "No concept relation, interpretation, synthesis, or authorial claim layer is available."
            ),
            "authority_label": "record_description",
        },
        "database_invariant": counts,
    }
    return card


def render_markdown(card: dict[str, Any]) -> str:
    concept = card["concept_identity"]
    source_layer = card["evidence_chain"][0]
    passage_layer = card["evidence_chain"][1]
    mention_layer = card["evidence_chain"][2]
    source = source_layer["record"]
    passage = passage_layer["record"]
    citation = passage_layer["citation"]
    mention = mention_layer["record"]
    rights = card["rights_display_rules"]

    lines = [
        "# BDP-002B Evidence Card — Body without Organs",
        "",
        "## Concept identity",
        f"- name: {concept.get('name')}",
        f"- status: {concept.get('status')}",
        f"- authority_label: {concept.get('authority_label')}",
        "",
        "## Current evidence chain",
        "1. canonical_buchanan_source",
        f"   - title: {source.get('title')}",
        f"   - author: {source.get('author')}",
        f"   - year: {source.get('year')}",
        f"   - rights_status: {source.get('rights_status')}",
        f"   - display_rule: {source.get('display_rule')}",
        f"   - authority_label: {source_layer.get('authority_label')}",
        "2. citation_backed_passage",
        f"   - page_or_timestamp: {passage.get('page_or_timestamp')}",
        f"   - chapter_or_section: {passage.get('chapter_or_section')}",
        f"   - locator: {citation.get('locator')}",
        f"   - passage_text_display: {passage.get('passage_text_display')}",
        f"   - authority_label: {passage_layer.get('authority_label')}",
        "3. reviewed_concept_mention",
        f"   - mention_type: {mention.get('mention_type')}",
        f"   - reviewed_status: {mention.get('reviewed_status')}",
        f"   - authority_label: {mention_layer.get('authority_label')}",
        "",
        "## Source-bound description",
        f"- authority_label: {card['source_bound_description']['authority_label']}",
        f"- claim_status: {card['source_bound_description']['claim_status']}",
        f"- text: {card['source_bound_description']['text']}",
        "",
        "## Blocked layers",
    ]

    for blocked in card["blocked_layers"]:
        lines.append(
            f"- {blocked['layer']}: {blocked['status']} "
            f"({blocked['authority_label']})"
        )

    lines.extend(
        [
            "",
            "## Rights/display rules",
            f"- rights_status: {rights['rights_status']}",
            f"- display_rule: {rights['display_rule']}",
            f"- passage_text_display: {rights['passage_text_display']}",
            f"- long_quotation_displayed: {str(rights['long_quotation_displayed']).lower()}",
            f"- article_reproduction_authorized: {str(rights['article_reproduction_authorized']).lower()}",
            f"- authority_label: {rights['authority_label']}",
            "",
            "## Operator readback",
            f"- available: {card['operator_readback']['what_is_available']}",
            f"- blocked: {card['operator_readback']['what_is_not_available']}",
            f"- authority_label: {card['operator_readback']['authority_label']}",
            "",
            "## Database invariant",
        ]
    )

    for key, value in card["database_invariant"].items():
        lines.append(f"- {key}: {value}")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format. Defaults to markdown.",
    )
    args = parser.parse_args()

    card = build_card()
    if args.format == "json":
        print(json.dumps(card, indent=2, sort_keys=True))
    else:
        print(render_markdown(card), end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.stderr or str(exc))
        raise SystemExit(exc.returncode)
