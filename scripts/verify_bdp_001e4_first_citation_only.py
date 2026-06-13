#!/usr/bin/env python3
import json
import os
import subprocess
import sys

DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")


def fail(message):
    print(f"BDP-001E.4 verification failed: {message}", file=sys.stderr)
    sys.exit(1)


def run_psql(query):
    result = subprocess.run(
        ["psql", "-X", "-A", "-t", "-d", DB_NAME, "-c", query],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        fail(f"psql query failed\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return result.stdout.strip()


def main():
    query = r"""
    SELECT jsonb_build_object(
        'migration_count', (
            SELECT COUNT(*)
            FROM schema_migrations
            WHERE id = '007_add_bdp_001e4_first_passage_citation_only'
              AND phase = 'BDP-001E.4'
        ),
        'citation_count', (
            SELECT COUNT(*)
            FROM citations c
            JOIN sources s ON s.id = c.source_id
            JOIN passages p ON p.id = c.passage_id
            WHERE s.title = 'A Thousand Plateaus: Capitalism and Schizophrenia'
              AND p.page_or_timestamp = 'p. 150'
              AND c.interpretation_id IS NULL
              AND c.citation_format = 'short_note'
              AND c.rights_status = 'fair_use_reference_only'
              AND c.display_rule = 'short_quote_plus_citation_only'
        ),
        'candidate', (
            SELECT jsonb_build_object(
                'title', title,
                'status', status,
                'metadata', metadata
            )
            FROM source_candidates
            WHERE title = 'A Thousand Plateaus: Capitalism and Schizophrenia'
            LIMIT 1
        ),
        'sources_total', (SELECT COUNT(*) FROM sources),
        'passages_total', (SELECT COUNT(*) FROM passages),
        'citations_total', (SELECT COUNT(*) FROM citations),
        'interpretations_total', (SELECT COUNT(*) FROM interpretations)
    )::text;
    """

    payload = json.loads(run_psql(query))

    if payload["migration_count"] != 1:
        fail("BDP-001E.4 migration ledger missing or duplicated")

    if payload["citation_count"] != 1:
        fail("expected exactly one citation linked to first passage")

    candidate = payload.get("candidate") or {}
    metadata = candidate.get("metadata") or {}

    if metadata.get("citation_inserted") is not True:
        fail("candidate metadata does not record citation insertion")

    if metadata.get("interpretation_created") is not False:
        fail("metadata incorrectly indicates interpretation creation")

    if payload["sources_total"] != 1:
        fail("unexpected source count")

    if payload["passages_total"] != 1:
        fail("unexpected passage count")

    if payload["citations_total"] != 1:
        fail("unexpected citation count")

    if payload["interpretations_total"] != 0:
        fail("interpretations were inserted")

    print("[OK] BDP-001E.4 migration ledger recorded")
    print("[OK] first citation record inserted")
    print("[OK] citation is linked to canonical source and first passage")
    print("[OK] citation remains interpretation-free")
    print("[OK] no interpretations inserted")
    print()
    print("BDP-001E.4 first citation-only verification passed.")


if __name__ == "__main__":
    main()
