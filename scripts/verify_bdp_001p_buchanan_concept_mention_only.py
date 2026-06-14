#!/usr/bin/env python3
"""
BDP-001P verifier.

Verifies that the governed slice inserted exactly one reviewed Body without
Organs concept mention for the already inserted Buchanan article passage, while
preserving all other canonical counts and keeping relations/interpretations at 0.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any


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


def load_json(sql: str) -> dict[str, Any]:
    output = run_psql(sql)
    if not output:
        raise SystemExit("Expected JSON output from psql, received empty output.")
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Could not parse JSON from psql output:\n{output}") from exc


def require_equal(payload: dict[str, Any], key: str, expected: Any) -> None:
    actual = payload.get(key)
    if actual != expected:
        raise SystemExit(f"[FAIL] {key}: expected {expected!r}, got {actual!r}")
    print(f"[OK] {key} = {actual!r}")


def main() -> None:
    counts = load_json(
        r"""
SELECT jsonb_build_object(
    'sources_count', (SELECT COUNT(*) FROM sources),
    'source_candidates_count', (SELECT COUNT(*) FROM source_candidates),
    'passage_candidates_count', (SELECT COUNT(*) FROM passage_candidates),
    'passages_count', (SELECT COUNT(*) FROM passages),
    'citations_count', (SELECT COUNT(*) FROM citations),
    'concept_mentions_count', (SELECT COUNT(*) FROM concept_mentions),
    'concept_relations_count', (SELECT COUNT(*) FROM concept_relations),
    'interpretations_count', (SELECT COUNT(*) FROM interpretations),
    'bdp_001o_migration_count', (
        SELECT COUNT(*)
        FROM schema_migrations
        WHERE id = '015_insert_bdp_001o_buchanan_passage_and_citation_only'
           OR phase = 'BDP-001O'
    ),
    'bdp_001p_migration_count', (
        SELECT COUNT(*)
        FROM schema_migrations
        WHERE id = '016_link_bdp_001p_buchanan_passage_to_bwo_concept_mention_only'
           OR phase = 'BDP-001P'
    )
);
"""
    )

    expected_counts = {
        "sources_count": 2,
        "source_candidates_count": 3,
        "passage_candidates_count": 1,
        "passages_count": 2,
        "citations_count": 2,
        "concept_mentions_count": 2,
        "concept_relations_count": 0,
        "interpretations_count": 0,
        "bdp_001o_migration_count": 1,
        "bdp_001p_migration_count": 1,
    }

    print("=== BDP-001P invariant counts ===")
    for key, expected in expected_counts.items():
        require_equal(counts, key, expected)

    target = load_json(
        r"""
WITH buchanan_source AS (
    SELECT id
    FROM sources
    WHERE author = 'Ian Buchanan'
      AND title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
      AND status = 'canonical'
),
buchanan_passage AS (
    SELECT p.id
    FROM passages p
    JOIN buchanan_source s ON s.id = p.source_id
),
target_mention AS (
    SELECT
        cm.id,
        cm.mention_type,
        cm.reviewed_status,
        cm.confidence,
        p.id AS passage_id,
        c.name AS concept_name
    FROM concept_mentions cm
    JOIN concepts c ON c.id = cm.concept_id
    JOIN passages p ON p.id = cm.passage_id
    JOIN buchanan_passage bp ON bp.id = p.id
    WHERE c.name = 'Body without Organs'
),
buchanan_citation AS (
    SELECT ci.id
    FROM citations ci
    JOIN buchanan_source s ON s.id = ci.source_id
    JOIN buchanan_passage bp ON bp.id = ci.passage_id
),
buchanan_relation AS (
    SELECT cr.id
    FROM concept_relations cr
    JOIN buchanan_passage bp ON bp.id = cr.evidence_passage_id
),
buchanan_interpretation AS (
    SELECT i.id
    FROM interpretations i
    JOIN buchanan_passage bp ON bp.id = i.evidence_passage_id
)
SELECT jsonb_build_object(
    'buchanan_article_source_count', (SELECT COUNT(*) FROM buchanan_source),
    'buchanan_article_passage_count', (SELECT COUNT(*) FROM buchanan_passage),
    'buchanan_article_citation_count', (SELECT COUNT(*) FROM buchanan_citation),
    'buchanan_article_concept_mention_count', (SELECT COUNT(*) FROM target_mention),
    'buchanan_article_accepted_direct_concept_mention_count', (
        SELECT COUNT(*)
        FROM target_mention
        WHERE mention_type = 'direct'
          AND reviewed_status = 'accepted'
          AND confidence >= 1.0
    ),
    'buchanan_article_concept_relation_count', (SELECT COUNT(*) FROM buchanan_relation),
    'buchanan_article_interpretation_count', (SELECT COUNT(*) FROM buchanan_interpretation)
);
"""
    )

    expected_target = {
        "buchanan_article_source_count": 1,
        "buchanan_article_passage_count": 1,
        "buchanan_article_citation_count": 1,
        "buchanan_article_concept_mention_count": 1,
        "buchanan_article_accepted_direct_concept_mention_count": 1,
        "buchanan_article_concept_relation_count": 0,
        "buchanan_article_interpretation_count": 0,
    }

    print("\n=== BDP-001P Buchanan article target chain ===")
    for key, expected in expected_target.items():
        require_equal(target, key, expected)

    print("\nBDP-001P concept mention only verification passed.")


if __name__ == "__main__":
    main()
