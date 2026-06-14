#!/usr/bin/env python3
import json
import os
import subprocess
import sys


DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")
SOURCE_TITLE = "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?"
LOCATOR = "printed article page 76; PDF page 4"
SECTION = "opening section before Spinoza"


def sql_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def psql_scalar(sql: str) -> str:
    result = subprocess.run(
        ["psql", "-X", "-d", DB_NAME, "-t", "-A", "-v", "ON_ERROR_STOP=1", "-c", sql],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        raise SystemExit(result.returncode)
    return result.stdout.strip()


def psql_json(sql: str):
    raw = psql_scalar(sql)
    if not raw:
        raise SystemExit("[FAIL] expected JSON result, got empty response")
    return json.loads(raw)


def expect(name, actual, expected):
    if actual != expected:
        raise SystemExit(f"[FAIL] {name}: expected {expected!r}, got {actual!r}")
    print(f"[OK] {name}: {actual!r}")


counts = psql_json(
    """
    SELECT jsonb_build_object(
        'sources_count', (SELECT count(*) FROM sources),
        'source_candidates_count', (SELECT count(*) FROM source_candidates),
        'passage_candidates_count', (SELECT count(*) FROM passage_candidates),
        'passages_count', (SELECT count(*) FROM passages),
        'citations_count', (SELECT count(*) FROM citations),
        'concept_mentions_count', (SELECT count(*) FROM concept_mentions),
        'concept_relations_count', (SELECT count(*) FROM concept_relations),
        'interpretations_count', (SELECT count(*) FROM interpretations),
        'bdp_001o_migration_count', (
            SELECT count(*) FROM schema_migrations WHERE phase = 'BDP-001O'
        )
    )::text;
    """
)

expected_counts = {
    "sources_count": 2,
    "source_candidates_count": 3,
    "passage_candidates_count": 1,
    "passages_count": 2,
    "citations_count": 2,
    "concept_mentions_count": 1,
    "concept_relations_count": 0,
    "interpretations_count": 0,
    "bdp_001o_migration_count": 1,
}

for key, expected in expected_counts.items():
    expect(key, counts.get(key), expected)

source_title_sql = sql_literal(SOURCE_TITLE)
locator_sql = sql_literal(LOCATOR)
section_sql = sql_literal(SECTION)

row_counts = psql_json(
    f"""
    WITH buchanan_source AS (
        SELECT id
        FROM sources
        WHERE author = 'Ian Buchanan'
          AND title = {source_title_sql}
        LIMIT 1
    ),
    target_passage AS (
        SELECT p.id
        FROM passages p
        JOIN buchanan_source s ON s.id = p.source_id
        WHERE p.page_or_timestamp = {locator_sql}
          AND p.chapter_or_section = {section_sql}
    ),
    target_citation AS (
        SELECT c.id
        FROM citations c
        JOIN target_passage p ON p.id = c.passage_id
        WHERE c.locator = {locator_sql}
          AND c.rights_status = 'restricted'
          AND c.display_rule = 'reference_only'
    )
    SELECT jsonb_build_object(
        'buchanan_source_count', (SELECT count(*) FROM buchanan_source),
        'buchanan_article_passage_count', (SELECT count(*) FROM target_passage),
        'buchanan_article_citation_count', (SELECT count(*) FROM target_citation),
        'buchanan_article_concept_mention_count', (
            SELECT count(*)
            FROM concept_mentions cm
            JOIN target_passage p ON p.id = cm.passage_id
        ),
        'buchanan_article_interpretation_count', (
            SELECT count(*)
            FROM interpretations i
            JOIN target_passage p ON p.id = i.evidence_passage_id
        ),
        'candidate_inserted_count', (
            SELECT count(*)
            FROM passage_candidates pc
            JOIN buchanan_source s ON s.id = pc.source_id
            WHERE pc.page_or_timestamp = {locator_sql}
              AND pc.chapter_or_section = {section_sql}
              AND pc.inserted_as_passage = true
              AND pc.citation_ready = true
              AND pc.concept_mention_ready = false
              AND pc.interpretation_ready = false
              AND pc.buchanan_claim_ready = false
        ),
        'citation_display_detail_count', (
            SELECT count(*)
            FROM citations c
            JOIN target_passage p ON p.id = c.passage_id
            WHERE c.display_rule = 'reference_only'
              AND COALESCE(c.metadata, '{{}}'::jsonb)->>'display_rule_detail' = 'reference_only_short_excerpt'
        )
    )::text;
    """
)

expected_row_counts = {
    "buchanan_source_count": 1,
    "buchanan_article_passage_count": 1,
    "buchanan_article_citation_count": 1,
    "buchanan_article_concept_mention_count": 0,
    "buchanan_article_interpretation_count": 0,
    "candidate_inserted_count": 1,
    "citation_display_detail_count": 1,
}

for key, expected in expected_row_counts.items():
    expect(key, row_counts.get(key), expected)

print("BDP-001O Buchanan passage and citation-only verification passed.")
