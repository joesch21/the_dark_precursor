#!/usr/bin/env python3
"""
BDP-001P readback.

Reads the reviewed concept mention linking the inserted Buchanan passage to
Body without Organs without displaying the restricted passage text.
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
        cm.id AS concept_mention_id,
        c.name AS concept_name,
        cm.mention_type,
        cm.reviewed_status,
        cm.confidence,
        p.id AS passage_id,
        p.page_or_timestamp,
        p.chapter_or_section,
        length(p.text) AS stored_text_char_count,
        s.title AS source_title,
        s.author AS source_author,
        s.rights_status AS source_rights_status,
        ci.locator AS citation_locator,
        ci.rights_status AS citation_rights_status,
        ci.display_rule AS citation_display_rule
    FROM concept_mentions cm
    JOIN concepts c ON c.id = cm.concept_id
    JOIN passages p ON p.id = cm.passage_id
    JOIN sources s ON s.id = p.source_id
    LEFT JOIN citations ci ON ci.passage_id = p.id AND ci.source_id = s.id
    WHERE c.name = 'Body without Organs'
      AND s.author = 'Ian Buchanan'
      AND s.title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
)
SELECT jsonb_pretty(
    jsonb_build_object(
        'phase', 'BDP-001P',
        'status', CASE WHEN COUNT(*) = 1 THEN 'linked' ELSE 'unexpected_target_count' END,
        'target_count', COUNT(*),
        'concept', MAX(concept_name),
        'concept_mention_id', MAX(concept_mention_id::text),
        'mention_type', MAX(mention_type),
        'reviewed_status', MAX(reviewed_status),
        'confidence', MAX(confidence),
        'source_author', MAX(source_author),
        'source_title', MAX(source_title),
        'passage_id', MAX(passage_id::text),
        'page_or_timestamp', MAX(page_or_timestamp),
        'chapter_or_section', MAX(chapter_or_section),
        'stored_text_char_count', MAX(stored_text_char_count),
        'passage_text_display', 'omitted_by_rights_policy',
        'citation_locator', MAX(citation_locator),
        'citation_rights_status', MAX(citation_rights_status),
        'citation_display_rule', MAX(citation_display_rule),
        'authority_boundary', jsonb_build_array(
            'concept mention only',
            'no concept relation',
            'no interpretation',
            'no Buchanan claim',
            'restricted passage text not displayed'
        )
    )
)
FROM target;
"""
    output = run_psql(sql)
    if not output:
        raise SystemExit("BDP-001P readback failed: no output returned.")
    print(output)


if __name__ == "__main__":
    main()
