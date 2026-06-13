#!/usr/bin/env python3
"""BDP-001M readback. This script does not mutate the database."""
from __future__ import annotations

import os
import subprocess

DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")
DOI = "10.1177/1357034X97003003004"
TITLE = "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?"
LABEL = "BDP-001M first Buchanan passage candidate for Body without Organs"


def psql(sql: str) -> str:
    result = subprocess.run(
        ["psql", "-d", DB_NAME, "-X", "-q", "-t", "-A", "-v", "ON_ERROR_STOP=1", "-c", sql],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> int:
    query = f"""
WITH target_source AS (
  SELECT s.*
    FROM sources s
   WHERE s.author = 'Ian Buchanan'
     AND s.title = '{TITLE}'
     AND COALESCE(s.metadata->>'doi', '') = '{DOI}'
     AND s.status = 'canonical'
   LIMIT 1
),
target_candidate AS (
  SELECT pc.*,
         c.name AS concept_name,
         s.title AS source_title,
         s.author AS source_author,
         s.metadata->>'doi' AS source_doi
    FROM passage_candidates pc
    JOIN sources s ON s.id = pc.source_id
    LEFT JOIN concepts c ON c.id = pc.concept_id
   WHERE s.author = 'Ian Buchanan'
     AND s.title = '{TITLE}'
     AND pc.candidate_label = '{LABEL}'
   LIMIT 1
),
counts AS (
  SELECT jsonb_build_object(
    'sources_count', (SELECT COUNT(*) FROM sources),
    'source_candidates_count', (SELECT COUNT(*) FROM source_candidates),
    'passage_candidates_count', (SELECT COUNT(*) FROM passage_candidates),
    'passages_count', (SELECT COUNT(*) FROM passages),
    'citations_count', (SELECT COUNT(*) FROM citations),
    'concept_mentions_count', (SELECT COUNT(*) FROM concept_mentions),
    'concept_relations_count', (SELECT COUNT(*) FROM concept_relations),
    'interpretations_count', (SELECT COUNT(*) FROM interpretations),
    'bdp_001m_migration_count', (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001M')
  ) AS row_json
),
blocked_counts AS (
  SELECT jsonb_build_object(
    'buchanan_article_passages_count', (
      SELECT COUNT(*) FROM passages p WHERE p.source_id = (SELECT id FROM target_source)
    ),
    'buchanan_article_citations_count', (
      SELECT COUNT(*) FROM citations ct WHERE ct.source_id = (SELECT id FROM target_source)
    ),
    'buchanan_article_interpretations_count', (
      SELECT COUNT(*)
        FROM interpretations i
        JOIN passages p ON p.id = i.evidence_passage_id
       WHERE p.source_id = (SELECT id FROM target_source)
    )
  ) AS row_json
)
SELECT jsonb_pretty(jsonb_build_object(
  'phase', 'BDP-001M',
  'counts', (SELECT row_json FROM counts),
  'boundary', jsonb_build_object(
    'passage_candidate_prepared', true,
    'canonical_passage_inserted', false,
    'citation_inserted', false,
    'concept_mention_inserted', false,
    'concept_relation_inserted', false,
    'interpretation_inserted', false,
    'buchanan_claim_created', false,
    'long_quotation_stored', false
  ),
  'blocked_counts_for_buchanan_article', (SELECT row_json FROM blocked_counts),
  'canonical_buchanan_source', COALESCE((SELECT to_jsonb(target_source) FROM target_source), '{{}}'::jsonb),
  'passage_candidate', COALESCE((SELECT to_jsonb(target_candidate) FROM target_candidate), '{{}}'::jsonb)
));
"""
    print(psql(query))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
