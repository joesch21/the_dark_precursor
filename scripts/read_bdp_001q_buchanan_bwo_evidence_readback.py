#!/usr/bin/env python3
"""
BDP-001Q readback.

Prepares a rights-aware, read-only Buchanan Body without Organs evidence card
from the existing concept -> concept_mentions -> passages -> citations -> sources
chain. The script intentionally does not display restricted passage text and does
not create interpretation, relation, synthesis, or Buchanan-claim authority.
"""

from __future__ import annotations

import os
import subprocess
import sys


DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")


def run_psql(sql: str) -> str:
    result = subprocess.run(
        [
            "psql",
            "-v",
            "ON_ERROR_STOP=1",
            "-X",
            "-q",
            "-t",
            "-A",
            "-d",
            DB_NAME,
            "-c",
            sql,
        ],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        raise SystemExit(result.returncode)
    return result.stdout.strip()


def main() -> None:
    sql = r"""
WITH target AS (
    SELECT
        c.id AS concept_id,
        c.name AS concept_name,
        c.status AS concept_status,
        cm.id AS concept_mention_id,
        cm.mention_type,
        cm.reviewed_status AS concept_mention_reviewed_status,
        cm.confidence,
        p.id AS passage_id,
        p.page_or_timestamp,
        p.chapter_or_section,
        length(p.text) AS stored_text_char_count,
        s.id AS source_id,
        s.title AS source_title,
        s.author AS source_author,
        s.type AS source_type,
        s.year AS source_year,
        s.status AS source_status,
        s.rights_status AS source_rights_status,
        s.reliability_level AS source_reliability_level,
        ci.id AS citation_id,
        ci.locator AS citation_locator,
        ci.citation_format,
        ci.rights_status AS citation_rights_status,
        ci.display_rule AS citation_display_rule,
        ci.url_or_reference AS citation_url_or_reference
    FROM concepts c
    JOIN concept_mentions cm ON cm.concept_id = c.id
    JOIN passages p ON p.id = cm.passage_id
    JOIN sources s ON s.id = p.source_id
    JOIN citations ci ON ci.passage_id = p.id AND ci.source_id = s.id
    WHERE c.name = 'Body without Organs'
      AND s.author = 'Ian Buchanan'
      AND s.title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
),
relation_counts AS (
    SELECT COUNT(*) AS relation_count
    FROM concept_relations cr
    JOIN target t ON t.passage_id = cr.evidence_passage_id
),
interpretation_counts AS (
    SELECT COUNT(*) AS interpretation_count
    FROM interpretations i
    JOIN target t ON t.passage_id = i.evidence_passage_id
),
migration_counts AS (
    SELECT
        COUNT(*) FILTER (
            WHERE id = '015_insert_bdp_001o_buchanan_passage_and_citation_only'
               OR phase = 'BDP-001O'
        ) AS bdp_001o_migration_count,
        COUNT(*) FILTER (
            WHERE id = '016_link_bdp_001p_buchanan_passage_to_bwo_concept_mention_only'
               OR phase = 'BDP-001P'
        ) AS bdp_001p_migration_count,
        COUNT(*) FILTER (
            WHERE phase = 'BDP-001Q'
        ) AS bdp_001q_migration_count
    FROM schema_migrations
)
SELECT jsonb_pretty(
    jsonb_build_object(
        'phase', 'BDP-001Q',
        'status', CASE WHEN COUNT(*) = 1 THEN 'readback_ready' ELSE 'unexpected_target_count' END,
        'readback_type', 'buchanan_body_without_organs_evidence_card',
        'target_count', COUNT(*),
        'concept', jsonb_build_object(
            'name', MAX(concept_name),
            'status', MAX(concept_status),
            'concept_id', MAX(concept_id::text)
        ),
        'buchanan_source', jsonb_build_object(
            'author', MAX(source_author),
            'title', MAX(source_title),
            'type', MAX(source_type),
            'year', MAX(source_year),
            'status', MAX(source_status),
            'rights_status', MAX(source_rights_status),
            'reliability_level', MAX(source_reliability_level),
            'source_id', MAX(source_id::text)
        ),
        'evidence_chain', jsonb_build_object(
            'passage_id', MAX(passage_id::text),
            'passage_status', 'citation_backed',
            'passage_text_display', 'omitted_by_rights_policy',
            'stored_text_char_count', MAX(stored_text_char_count),
            'page_or_timestamp', MAX(page_or_timestamp),
            'chapter_or_section', MAX(chapter_or_section),
            'citation_id', MAX(citation_id::text),
            'citation_locator', MAX(citation_locator),
            'citation_format', MAX(citation_format),
            'citation_rights_status', MAX(citation_rights_status),
            'citation_display_rule', MAX(citation_display_rule),
            'citation_url_or_reference', MAX(citation_url_or_reference),
            'concept_mention_id', MAX(concept_mention_id::text),
            'concept_mention_status', MAX(concept_mention_reviewed_status),
            'mention_type', MAX(mention_type),
            'confidence', MAX(confidence)
        ),
        'authority_boundary', jsonb_build_object(
            'allowed_description', 'A citation-backed Buchanan passage is linked to Body without Organs through a reviewed concept mention.',
            'buchanan_interpretation_status', 'blocked',
            'buchanan_claim_status', 'blocked',
            'concept_relation_status', CASE WHEN MAX(relation_counts.relation_count) = 0 THEN 'blocked_absent' ELSE 'unexpected_relation_present' END,
            'interpretation_count_for_target_passage', MAX(interpretation_counts.interpretation_count),
            'concept_relation_count_for_target_passage', MAX(relation_counts.relation_count),
            'blocked_claims', jsonb_build_array(
                'Buchanan argues that the Body without Organs means X.',
                'Buchanan''s interpretation of the Body without Organs is X.',
                'The concept relation is X.'
            )
        ),
        'read_only_boundary', jsonb_build_object(
            'database_mutation', false,
            'sql_migration', false,
            'new_source', false,
            'new_passage', false,
            'new_citation', false,
            'new_concept_mention', false,
            'new_concept_relation', false,
            'new_interpretation', false,
            'generated_buchanan_claim', false,
            'frontend_work', false
        ),
        'migration_posture', jsonb_build_object(
            'bdp_001o_migration_count', MAX(migration_counts.bdp_001o_migration_count),
            'bdp_001p_migration_count', MAX(migration_counts.bdp_001p_migration_count),
            'bdp_001q_migration_count', MAX(migration_counts.bdp_001q_migration_count)
        )
    )
)
FROM target
CROSS JOIN relation_counts
CROSS JOIN interpretation_counts
CROSS JOIN migration_counts;
"""
    output = run_psql(sql)
    if not output:
        raise SystemExit("BDP-001Q readback failed: no output returned.")
    print(output)


if __name__ == "__main__":
    main()
