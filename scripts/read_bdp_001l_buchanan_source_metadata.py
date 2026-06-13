#!/usr/bin/env python3
"""BDP-001L readback. This script does not mutate the database."""
from __future__ import annotations

import os
import subprocess

DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")
DOI = "10.1177/1357034X97003003004"


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
  SELECT to_jsonb(s) AS row_json
    FROM sources s
   WHERE s.author = 'Ian Buchanan'
     AND (
          COALESCE(s.metadata->>'doi', '') = '{DOI}'
       OR COALESCE(s.url_or_reference, '') = 'https://doi.org/{DOI}'
       OR s.title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
     )
   LIMIT 1
),
target_candidate AS (
  SELECT to_jsonb(sc) AS row_json
    FROM source_candidates sc
   WHERE sc.author = 'Ian Buchanan'
     AND (
          COALESCE(sc.metadata::text, '') ILIKE '%{DOI}%'
       OR COALESCE(sc.url, '') ILIKE '%{DOI}%'
       OR sc.title ILIKE '%Problem of the Body%'
     )
   ORDER BY sc.created_at DESC NULLS LAST
   LIMIT 1
),
counts AS (
  SELECT jsonb_build_object(
    'sources_count', (SELECT COUNT(*) FROM sources),
    'source_candidates_count', (SELECT COUNT(*) FROM source_candidates),
    'passages_count', (SELECT COUNT(*) FROM passages),
    'citations_count', (SELECT COUNT(*) FROM citations),
    'concept_mentions_count', (SELECT COUNT(*) FROM concept_mentions),
    'concept_relations_count', (SELECT COUNT(*) FROM concept_relations),
    'interpretations_count', (SELECT COUNT(*) FROM interpretations),
    'bdp_001l_migration_count', (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001L')
  ) AS row_json
)
SELECT jsonb_pretty(jsonb_build_object(
  'phase', 'BDP-001L',
  'boundary', jsonb_build_object(
    'metadata_only', true,
    'no_passage_insertion', true,
    'no_citation_insertion', true,
    'no_concept_mention_insertion', true,
    'no_concept_relation_insertion', true,
    'no_interpretation_insertion', true,
    'no_buchanan_claim', true
  ),
  'counts', (SELECT row_json FROM counts),
  'canonical_buchanan_source', COALESCE((SELECT row_json FROM target_source), '{{}}'::jsonb),
  'review_history_candidate', COALESCE((SELECT row_json FROM target_candidate), '{{}}'::jsonb)
));
"""
    print(psql(query))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
