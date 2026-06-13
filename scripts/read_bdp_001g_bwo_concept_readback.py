#!/usr/bin/env python3
"""BDP-001G read-only Body without Organs concept readback.

Reads the verified evidence chain:
concepts -> concept_mentions -> passages -> citations -> sources.

Boundary:
- SELECT only.
- No database mutation.
- No interpretations.
- No generated synthesis.
- No concept relations.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any


DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")


def psql_json(sql: str) -> list[dict[str, Any]]:
    result = subprocess.run(
        [
            "psql",
            "-d",
            DB_NAME,
            "-v",
            "ON_ERROR_STOP=1",
            "-P",
            "pager=off",
            "-t",
            "-A",
            "-c",
            sql,
        ],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)

    raw = result.stdout.strip()
    if not raw:
        return []

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print("[FAIL] Could not parse readback JSON from psql.", file=sys.stderr)
        print(raw, file=sys.stderr)
        raise SystemExit(1) from exc

    if not isinstance(data, list):
        print("[FAIL] Expected a JSON array from readback query.", file=sys.stderr)
        raise SystemExit(1)

    return data


READBACK_SQL = r"""
WITH readback AS (
  SELECT
    c.name AS concept_name,
    c.status AS concept_status,

    cm.mention_type,
    cm.reviewed_status,
    cm.confidence,

    p.page_or_timestamp,
    p.chapter_or_section,
    p.citation AS passage_citation,
    LEFT(REGEXP_REPLACE(COALESCE(p.text, ''), '\s+', ' ', 'g'), 280) AS passage_preview,
    CHAR_LENGTH(COALESCE(p.text, '')) AS passage_text_length,

    cit.citation_text,
    cit.citation_format,
    cit.locator,
    cit.page_or_timestamp AS citation_page_or_timestamp,
    cit.chapter_or_section AS citation_chapter_or_section,
    cit.rights_status AS citation_rights_status,
    cit.display_rule,
    cit.interpretation_id::text AS citation_interpretation_id,

    s.title AS source_title,
    s.author,
    s.year,
    s.publisher,
    s.url_or_reference,
    s.rights_status AS source_rights_status,
    s.reliability_level,
    s.status AS source_status
  FROM concepts c
  JOIN concept_mentions cm
    ON cm.concept_id = c.id
  JOIN passages p
    ON p.id = cm.passage_id
  JOIN sources s
    ON s.id = p.source_id
  LEFT JOIN citations cit
    ON cit.passage_id = p.id
   AND cit.source_id = s.id
  WHERE c.name = 'Body without Organs'
  ORDER BY p.created_at ASC
)
SELECT COALESCE(json_agg(row_to_json(readback)), '[]'::json)::text
FROM readback;
"""


def main() -> None:
    rows = psql_json(READBACK_SQL)

    print("=== BDP-001G — Body without Organs citation-backed concept readback ===")
    print(f"database={DB_NAME}")
    print(f"readback_rows={len(rows)}")
    print()

    if not rows:
        print("[FAIL] No Body without Organs concept readback rows found.")
        raise SystemExit(1)

    for index, row in enumerate(rows, start=1):
        print(f"--- evidence card {index} ---")
        print(f"Concept: {row.get('concept_name')}")
        print(f"Concept status: {row.get('concept_status')}")
        print(f"Mention: {row.get('mention_type')} / {row.get('reviewed_status')}")
        print(f"Confidence: {row.get('confidence')}")
        print()
        print(f"Source: {row.get('source_title')}")
        print(f"Author: {row.get('author')}")
        print(f"Year: {row.get('year')}")
        print(f"Publisher: {row.get('publisher')}")
        print(f"Source status: {row.get('source_status')}")
        print(f"Source rights: {row.get('source_rights_status')}")
        print(f"Reliability: {row.get('reliability_level')}")
        print()
        print(f"Passage locator: {row.get('page_or_timestamp')}")
        print(f"Section: {row.get('chapter_or_section')}")
        print(f"Passage citation: {row.get('passage_citation')}")
        print(f"Passage preview: {row.get('passage_preview')}")
        print(f"Passage stored length: {row.get('passage_text_length')} chars")
        print()
        print(f"Citation text: {row.get('citation_text')}")
        print(f"Citation format: {row.get('citation_format')}")
        print(f"Citation locator: {row.get('locator')}")
        print(f"Citation rights: {row.get('citation_rights_status')}")
        print(f"Display rule: {row.get('display_rule')}")
        print(f"Interpretation link: {row.get('citation_interpretation_id')}")
        print()
        print("Authority boundary: Deleuze and Guattari primary text evidence only.")
        print("Interpretation boundary: no Buchanan interpretation, no system synthesis, no concept relation.")
        print()

    print("BDP-001G readback complete.")


if __name__ == "__main__":
    main()
