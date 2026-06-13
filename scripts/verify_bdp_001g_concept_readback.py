#!/usr/bin/env python3
"""Verify BDP-001G read-only concept readback readiness."""

from __future__ import annotations

import os
import subprocess
import sys


DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")


def run_scalar(sql: str) -> str:
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
            "-F",
            "|",
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

    return result.stdout.strip()


def ok(condition: bool, message: str, detail: str | None = None) -> None:
    if not condition:
        suffix = f": {detail}" if detail else ""
        print(f"[FAIL] {message}{suffix}")
        raise SystemExit(1)
    print(f"[OK] {message}")


def main() -> None:
    counts = run_scalar(
        """
        SELECT
          (SELECT COUNT(*) FROM sources)::text || '|' ||
          (SELECT COUNT(*) FROM passages)::text || '|' ||
          (SELECT COUNT(*) FROM citations)::text || '|' ||
          (SELECT COUNT(*) FROM concept_mentions)::text || '|' ||
          (SELECT COUNT(*) FROM concept_relations)::text || '|' ||
          (SELECT COUNT(*) FROM interpretations)::text || '|' ||
          (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001F')::text;
        """
    )
    ok(
        counts == "1|1|1|1|0|0|1",
        "BDP-001G starts from the verified source/passage/citation/concept-mention invariant",
        f"expected 1|1|1|1|0|0|1, got {counts}",
    )

    readback_count = run_scalar(
        """
        SELECT COUNT(*)
        FROM concepts c
        JOIN concept_mentions cm
          ON cm.concept_id = c.id
        JOIN passages p
          ON p.id = cm.passage_id
        JOIN sources s
          ON s.id = p.source_id
        JOIN citations cit
          ON cit.passage_id = p.id
         AND cit.source_id = s.id
        WHERE c.name = 'Body without Organs'
          AND cm.mention_type = 'direct'
          AND cm.reviewed_status = 'accepted'
          AND s.title = 'A Thousand Plateaus: Capitalism and Schizophrenia'
          AND s.status = 'canonical'
          AND s.rights_status = 'fair_use_reference_only'
          AND s.reliability_level = 'high'
          AND (
            p.page_or_timestamp ILIKE '%150%'
            OR p.citation ILIKE '%150%'
            OR p.chapter_or_section ILIKE '%Body without Organs%'
          )
          AND cit.interpretation_id IS NULL
          AND cit.rights_status = 'fair_use_reference_only'
          AND cit.display_rule = 'reference_only';
        """
    )
    ok(
        readback_count == "1",
        "Body without Organs readback resolves one accepted direct concept mention with citation chain",
        f"expected 1, got {readback_count}",
    )

    non_null_required = run_scalar(
        """
        SELECT COUNT(*)
        FROM concepts c
        JOIN concept_mentions cm
          ON cm.concept_id = c.id
        JOIN passages p
          ON p.id = cm.passage_id
        JOIN sources s
          ON s.id = p.source_id
        JOIN citations cit
          ON cit.passage_id = p.id
         AND cit.source_id = s.id
        WHERE c.name = 'Body without Organs'
          AND COALESCE(p.text, '') <> ''
          AND COALESCE(p.page_or_timestamp, '') <> ''
          AND COALESCE(p.chapter_or_section, '') <> ''
          AND COALESCE(cit.citation_text, '') <> ''
          AND COALESCE(cit.locator, '') <> ''
          AND COALESCE(s.title, '') <> '';
        """
    )
    ok(
        non_null_required == "1",
        "readback fields contain source, passage, locator, and citation text",
        f"expected 1, got {non_null_required}",
    )

    interpretation_links = run_scalar(
        """
        SELECT COUNT(*)
        FROM citations
        WHERE interpretation_id IS NOT NULL;
        """
    )
    ok(
        interpretation_links == "0",
        "citation chain remains interpretation-free",
        f"expected 0, got {interpretation_links}",
    )

    print()
    print("BDP-001G concept readback verification passed.")


if __name__ == "__main__":
    main()
