#!/usr/bin/env python3
import os
import subprocess
import sys

DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")

SQL = r"""
SELECT jsonb_pretty(jsonb_build_object(
    'phase', 'BDP-001N',
    'passage_candidate', jsonb_build_object(
        'id', pc.id,
        'candidate_label', pc.candidate_label,
        'candidate_status', pc.candidate_status,
        'candidate_scope', pc.candidate_scope,
        'candidate_text', pc.candidate_text,
        'candidate_text_status', pc.candidate_text_status,
        'page_or_timestamp', pc.page_or_timestamp,
        'chapter_or_section', pc.chapter_or_section,
        'locator_status', pc.locator_status,
        'rights_status', pc.rights_status,
        'display_rule', pc.display_rule,
        'review_status', pc.review_status,
        'extraction_status', pc.extraction_status,
        'inserted_as_passage', pc.inserted_as_passage,
        'citation_ready', pc.citation_ready,
        'concept_mention_ready', pc.concept_mention_ready,
        'interpretation_ready', pc.interpretation_ready,
        'buchanan_claim_ready', pc.buchanan_claim_ready,
        'reviewed_at', pc.reviewed_at,
        'source_title', s.title,
        'source_author', s.author,
        'target_concept', c.name,
        'metadata', pc.metadata
    )
))
FROM passage_candidates pc
JOIN sources s ON s.id = pc.source_id
LEFT JOIN concepts c ON c.id = pc.concept_id
WHERE s.author = 'Ian Buchanan'
  AND s.title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
  AND c.name = 'Body without Organs'
ORDER BY pc.created_at, pc.id;
"""

def run_psql(sql: str) -> str:
    result = subprocess.run(
        ["psql", "-X", "-v", "ON_ERROR_STOP=1", "-d", DB_NAME, "-t", "-A", "-c", sql],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    return result.stdout.strip()

def main() -> None:
    print(run_psql(SQL))

if __name__ == "__main__":
    main()
