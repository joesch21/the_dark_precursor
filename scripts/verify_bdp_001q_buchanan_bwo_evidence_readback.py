#!/usr/bin/env python3
"""
BDP-001Q verifier.

Verifies the read-only Buchanan Body without Organs evidence readback after
BDP-001P. This phase must not add SQL migration, database rows, concept
relations, interpretations, generated Buchanan claims, or frontend work.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")
READBACK_SCRIPT = Path("scripts/read_bdp_001q_buchanan_bwo_evidence_readback.py")


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


def require_true(name: str, condition: bool) -> None:
    if not condition:
        raise SystemExit(f"[FAIL] {name}")
    print(f"[OK] {name}")


def verify_readback_script_boundary() -> None:
    if not READBACK_SCRIPT.exists():
        raise SystemExit(f"[FAIL] missing readback script: {READBACK_SCRIPT}")

    text = READBACK_SCRIPT.read_text()

    # Inspect likely executed SQL content only enough to block obvious mutation.
    # This intentionally does not scan operator-facing prose in docs.
    mutating_patterns = [
        r"\bINSERT\b",
        r"\bUPDATE\b",
        r"\bDELETE\b",
        r"\bCREATE\b",
        r"\bALTER\b",
        r"\bDROP\b",
        r"\bTRUNCATE\b",
        r"\bBEGIN\b",
        r"\bCOMMIT\b",
    ]
    sql_fragments = re.findall(r"sql\s*=\s*r\"\"\"(.*?)\"\"\"", text, flags=re.DOTALL)
    if len(sql_fragments) != 1:
        raise SystemExit("[FAIL] expected exactly one readback SQL fragment")

    executed_sql = sql_fragments[0]
    for pattern in mutating_patterns:
        if re.search(pattern, executed_sql, flags=re.IGNORECASE):
            raise SystemExit(f"[FAIL] readback SQL contains mutating keyword: {pattern}")

    if "p.text AS" in executed_sql or "MAX(p.text" in executed_sql:
        raise SystemExit("[FAIL] readback SQL appears to expose restricted passage text")

    require_true("readback SQL is SELECT-only", True)
    require_true("readback omits restricted passage text", "length(p.text)" in executed_sql and "passage_text_display" in executed_sql)


def main() -> None:
    verify_readback_script_boundary()

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
    ),
    'bdp_001q_migration_count', (
        SELECT COUNT(*)
        FROM schema_migrations
        WHERE phase = 'BDP-001Q'
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
        "bdp_001q_migration_count": 0,
    }

    print("=== BDP-001Q invariant counts ===")
    for key, expected in expected_counts.items():
        require_equal(counts, key, expected)

    target = load_json(
        r"""
WITH target AS (
    SELECT
        c.name AS concept_name,
        c.status AS concept_status,
        cm.mention_type,
        cm.reviewed_status,
        cm.confidence,
        p.id AS passage_id,
        length(p.text) AS stored_text_char_count,
        p.page_or_timestamp,
        p.chapter_or_section,
        s.title AS source_title,
        s.author AS source_author,
        s.status AS source_status,
        s.rights_status AS source_rights_status,
        s.reliability_level AS source_reliability_level,
        ci.locator AS citation_locator,
        ci.rights_status AS citation_rights_status,
        ci.display_rule AS citation_display_rule
    FROM concepts c
    JOIN concept_mentions cm ON cm.concept_id = c.id
    JOIN passages p ON p.id = cm.passage_id
    JOIN sources s ON s.id = p.source_id
    JOIN citations ci ON ci.passage_id = p.id AND ci.source_id = s.id
    WHERE c.name = 'Body without Organs'
      AND s.author = 'Ian Buchanan'
      AND s.title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
),
relations AS (
    SELECT COUNT(*) AS relation_count
    FROM concept_relations cr
    JOIN target t ON t.passage_id = cr.evidence_passage_id
),
interpretations_for_target AS (
    SELECT COUNT(*) AS interpretation_count
    FROM interpretations i
    JOIN target t ON t.passage_id = i.evidence_passage_id
)
SELECT jsonb_build_object(
    'target_count', (SELECT COUNT(*) FROM target),
    'concept_name', (SELECT MAX(concept_name) FROM target),
    'concept_status', (SELECT MAX(concept_status) FROM target),
    'source_author', (SELECT MAX(source_author) FROM target),
    'source_title', (SELECT MAX(source_title) FROM target),
    'source_status', (SELECT MAX(source_status) FROM target),
    'source_rights_status', (SELECT MAX(source_rights_status) FROM target),
    'source_reliability_level', (SELECT MAX(source_reliability_level) FROM target),
    'citation_rights_status', (SELECT MAX(citation_rights_status) FROM target),
    'citation_display_rule', (SELECT MAX(citation_display_rule) FROM target),
    'citation_locator', (SELECT MAX(citation_locator) FROM target),
    'page_or_timestamp', (SELECT MAX(page_or_timestamp) FROM target),
    'chapter_or_section', (SELECT MAX(chapter_or_section) FROM target),
    'mention_type', (SELECT MAX(mention_type) FROM target),
    'reviewed_status', (SELECT MAX(reviewed_status) FROM target),
    'confidence', (SELECT MAX(confidence) FROM target),
    'stored_text_char_count', (SELECT MAX(stored_text_char_count) FROM target),
    'concept_relation_count_for_target_passage', (SELECT relation_count FROM relations),
    'interpretation_count_for_target_passage', (SELECT interpretation_count FROM interpretations_for_target)
);
"""
    )

    expected_target = {
        "target_count": 1,
        "concept_name": "Body without Organs",
        "source_author": "Ian Buchanan",
        "source_title": "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?",
        "source_status": "canonical",
        "source_rights_status": "restricted",
        "source_reliability_level": "high",
        "citation_rights_status": "restricted",
        "citation_display_rule": "reference_only",
        "mention_type": "direct",
        "reviewed_status": "accepted",
        "concept_relation_count_for_target_passage": 0,
        "interpretation_count_for_target_passage": 0,
    }

    print("\n=== BDP-001Q Buchanan Body without Organs evidence target ===")
    for key, expected in expected_target.items():
        require_equal(target, key, expected)

    require_true("confidence is evidence-readback strong", float(target.get("confidence", 0)) >= 1.0)
    require_true("restricted passage remains short", 0 < int(target.get("stored_text_char_count", 0)) <= 280)
    require_true("locator is retained", bool(target.get("citation_locator")) and bool(target.get("page_or_timestamp")))
    require_true("section is retained", bool(target.get("chapter_or_section")))

    print("\nBDP-001Q Buchanan Body without Organs evidence readback verification passed.")


if __name__ == "__main__":
    main()
