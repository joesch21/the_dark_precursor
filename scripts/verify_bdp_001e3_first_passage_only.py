#!/usr/bin/env python3
import json
import os
import subprocess
import sys

DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")
TITLE = "A Thousand Plateaus: Capitalism and Schizophrenia"
LOCATOR = "p. 150"
SECTION = "Plateau 6: How Do You Make Yourself a Body without Organs?"


def fail(message):
    print(f"BDP-001E.3 verification failed: {message}", file=sys.stderr)
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
            WHERE id = '006_insert_bdp_001e3_first_cited_passage_only'
              AND phase = 'BDP-001E.3'
        ),
        'source_count', (
            SELECT COUNT(*)
            FROM sources
            WHERE title = 'A Thousand Plateaus: Capitalism and Schizophrenia'
              AND status = 'canonical'
        ),
        'passage', (
            SELECT jsonb_build_object(
                'id', p.id,
                'source_title', s.title,
                'page_or_timestamp', p.page_or_timestamp,
                'chapter_or_section', p.chapter_or_section,
                'citation', p.citation,
                'word_count', array_length(regexp_split_to_array(trim(p.text), '\s+'), 1)
            )
            FROM passages p
            JOIN sources s ON s.id = p.source_id
            WHERE s.title = 'A Thousand Plateaus: Capitalism and Schizophrenia'
              AND p.page_or_timestamp = 'p. 150'
              AND p.chapter_or_section = 'Plateau 6: How Do You Make Yourself a Body without Organs?'
            LIMIT 1
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
        'bdp_001e4_count', (
            SELECT COUNT(*)
            FROM schema_migrations
            WHERE phase = 'BDP-001E.4'
        ),
        'sources_total', (SELECT COUNT(*) FROM sources),
        'passages_total', (SELECT COUNT(*) FROM passages),
        'citations_total', (SELECT COUNT(*) FROM citations),
        'interpretations_total', (SELECT COUNT(*) FROM interpretations)
    )::text;
    """

    payload = json.loads(run_psql(query))

    if payload["migration_count"] != 1:
        fail("BDP-001E.3 migration ledger missing or duplicated")

    if payload["source_count"] != 1:
        fail("expected exactly one canonical A Thousand Plateaus source")

    passage = payload.get("passage") or {}
    if not passage:
        fail("first passage missing")

    if passage.get("page_or_timestamp") != LOCATOR:
        fail("passage locator mismatch")

    if passage.get("chapter_or_section") != SECTION:
        fail("passage section mismatch")

    if not passage.get("citation"):
        fail("passage citation text missing")

    if passage.get("word_count", 999) > 25:
        fail("passage exceeds short quotation boundary")

    candidate = payload.get("candidate") or {}
    metadata = candidate.get("metadata") or {}

    if metadata.get("passage_inserted") is not True:
        fail("candidate metadata does not record passage insertion")

    later_e4_applied = payload.get("bdp_001e4_count") == 1
    if later_e4_applied:
        if metadata.get("citation_inserted") is not True:
            fail("metadata should record citation-table insertion after BDP-001E.4")
    elif metadata.get("citation_inserted") is not False:
        fail("metadata incorrectly indicates citation-table insertion before BDP-001E.4")

    if metadata.get("interpretation_created") is not False:
        fail("metadata incorrectly indicates interpretation creation")

    if payload["sources_total"] != 1:
        fail("unexpected total source count")

    if payload["passages_total"] != 1:
        fail("unexpected passage count")

    expected_citations = 1 if payload.get("bdp_001e4_count") == 1 else 0
    if payload["citations_total"] != expected_citations:
        fail(f"unexpected citation count after phase chain: {payload['citations_total']}")

    if payload["interpretations_total"] != 0:
        fail("interpretations were inserted")

    print("[OK] BDP-001E.3 migration ledger recorded")
    print("[OK] first short cited passage inserted")
    print("[OK] passage is linked to canonical source")
    if payload.get("bdp_001e4_count") == 1:
        print("[OK] later BDP-001E.4 citation insertion tolerated")
    else:
        print("[OK] citation-table remains empty")
    print("[OK] no interpretations inserted")
    print()
    print("BDP-001E.3 first cited passage-only verification passed.")


if __name__ == "__main__":
    main()
