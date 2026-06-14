#!/usr/bin/env python3
"""Read BDP-001O Buchanan passage and citation state.

This script uses the project-standard psql subprocess pattern.
It does not mutate the database.
"""

from __future__ import annotations

import json
import os
import subprocess
from textwrap import indent

DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")

SQL = r"""
WITH buchanan_source AS (
    SELECT id, title, author, year, url_or_reference, rights_status, status
    FROM sources
    WHERE author = 'Ian Buchanan'
      AND title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
      AND status = 'canonical'
), buchanan_passage AS (
    SELECT p.id,
           p.source_id,
           p.text,
           p.page_or_timestamp,
           p.chapter_or_section,
           p.citation
    FROM passages p
    JOIN buchanan_source s ON s.id = p.source_id
), buchanan_citation AS (
    SELECT c.id,
           c.source_id,
           c.passage_id,
           c.citation_text,
           c.locator,
           c.rights_status,
           c.display_rule,
           c.metadata
    FROM citations c
    JOIN buchanan_passage p ON p.id = c.passage_id
), candidate AS (
    SELECT pc.id,
           pc.candidate_label,
           pc.candidate_text_status,
           pc.page_or_timestamp,
           pc.chapter_or_section,
           pc.locator_status,
           pc.review_status,
           pc.citation_ready,
           pc.concept_mention_ready,
           pc.interpretation_ready,
           pc.buchanan_claim_ready,
           pc.inserted_as_passage,
           pc.metadata
    FROM passage_candidates pc
    JOIN buchanan_source s ON s.id = pc.source_id
)
SELECT jsonb_pretty(jsonb_build_object(
    'phase', 'BDP-001O',
    'buchanan_source', (SELECT to_jsonb(s) FROM buchanan_source s LIMIT 1),
    'candidate', (SELECT to_jsonb(c) FROM candidate c LIMIT 1),
    'passage', (SELECT to_jsonb(p) FROM buchanan_passage p LIMIT 1),
    'citation', (SELECT to_jsonb(c) FROM buchanan_citation c LIMIT 1),
    'counts', jsonb_build_object(
        'buchanan_passage_count', (SELECT count(*) FROM buchanan_passage),
        'buchanan_citation_count', (SELECT count(*) FROM buchanan_citation),
        'concept_mentions_count', (SELECT count(*) FROM concept_mentions),
        'concept_relations_count', (SELECT count(*) FROM concept_relations),
        'interpretations_count', (SELECT count(*) FROM interpretations),
        'bdp_001o_migration_count', (
            SELECT count(*)
            FROM schema_migrations
            WHERE id = 'bdp_001o_insert_buchanan_passage_and_citation_only'
               OR phase = 'BDP-001O'
        )
    ),
    'boundary', jsonb_build_object(
        'concept_mention_inserted_this_phase', false,
        'concept_relation_inserted_this_phase', false,
        'interpretation_inserted_this_phase', false,
        'buchanan_claim_inserted_this_phase', false
    )
));
"""


def run_psql(sql: str) -> str:
    result = subprocess.run(
        ["psql", "-X", "-A", "-t", "-d", DB_NAME, "-c", sql],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def main() -> None:
    payload = run_psql(SQL)
    print(payload)


if __name__ == "__main__":
    main()
