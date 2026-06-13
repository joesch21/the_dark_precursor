#!/usr/bin/env python3
import json
import os
import subprocess
import sys


DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")

SOURCE_TITLE = "A Thousand Plateaus: Capitalism and Schizophrenia"
PASSAGE_LOCATOR = "p. 150"
PASSAGE_SECTION = "Plateau 6: How Do You Make Yourself a Body without Organs?"


def fail(message):
    print(f"BDP-001E verification failed: {message}", file=sys.stderr)
    sys.exit(1)


def run_psql(query):
    result = subprocess.run(
        ["psql", "-X", "-A", "-t", "-d", DB_NAME, "-c", query],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        fail(
            "psql verification query failed.\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    return result.stdout.strip()


def main():
    query = r"""
    SELECT jsonb_build_object(
        'migration_count', (
            SELECT COUNT(*)
            FROM schema_migrations
            WHERE id = '004_adopt_bdp_001e_first_source_and_passage'
              AND phase = 'BDP-001E'
        ),
        'source', (
            SELECT jsonb_build_object(
                'id', id,
                'title', title,
                'author', author,
                'type', type,
                'year', year,
                'publisher', publisher,
                'rights_status', rights_status,
                'reliability_level', reliability_level,
                'status', status
            )
            FROM sources
            WHERE title = 'A Thousand Plateaus: Capitalism and Schizophrenia'
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
        'passage', (
            SELECT jsonb_build_object(
                'id', id,
                'source_id', source_id,
                'page_or_timestamp', page_or_timestamp,
                'chapter_or_section', chapter_or_section,
                'citation', citation,
                'text_word_count', array_length(regexp_split_to_array(trim(text), '\s+'), 1)
            )
            FROM passages
            WHERE page_or_timestamp = 'p. 150'
              AND chapter_or_section = 'Plateau 6: How Do You Make Yourself a Body without Organs?'
            LIMIT 1
        ),
        'citation_count', (
            SELECT COUNT(*)
            FROM citations c
            JOIN passages p ON p.id = c.passage_id
            JOIN sources s ON s.id = c.source_id
            WHERE s.title = 'A Thousand Plateaus: Capitalism and Schizophrenia'
              AND p.page_or_timestamp = 'p. 150'
              AND c.interpretation_id IS NULL
              AND c.rights_status = 'fair_use_reference_only'
        ),
        'sources_count', (SELECT COUNT(*) FROM sources),
        'passages_count', (SELECT COUNT(*) FROM passages),
        'interpretations_count', (SELECT COUNT(*) FROM interpretations)
    )::text;
    """

    raw = run_psql(query)

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"could not parse JSON: {exc}\nRaw output:\n{raw}")

    if payload.get("migration_count") != 1:
        fail("BDP-001E migration ledger missing or duplicated")

    source = payload.get("source")
    if not source:
        fail("canonical source missing")

    if source.get("title") != SOURCE_TITLE:
        fail("canonical source title mismatch")

    if source.get("status") != "canonical":
        fail("source was not adopted with canonical status")

    if source.get("rights_status") != "fair_use_reference_only":
        fail("source rights status is not fair_use_reference_only")

    if source.get("reliability_level") != "primary_text":
        fail("source reliability level is not primary_text")

    candidate = payload.get("candidate")
    if not candidate:
        fail("source candidate missing")

    if candidate.get("status") != "approved":
        fail("source candidate was not marked approved")

    metadata = candidate.get("metadata") or {}
    if metadata.get("adopted_to_canonical_source") is not True:
        fail("candidate metadata does not record canonical adoption decision")

    if metadata.get("candidate_record_is_canonical") is not False:
        fail("candidate metadata incorrectly treats candidate record as canonical")

    passage = payload.get("passage")
    if not passage:
        fail("first cited passage missing")

    if passage.get("page_or_timestamp") != PASSAGE_LOCATOR:
        fail("passage locator mismatch")

    if passage.get("chapter_or_section") != PASSAGE_SECTION:
        fail("passage section mismatch")

    if not passage.get("citation"):
        fail("passage citation missing")

    if passage.get("text_word_count", 999) > 25:
        fail("passage exceeds short quotation boundary")

    if payload.get("citation_count") != 1:
        fail("citation record missing, duplicated, or incorrectly linked")

    if payload.get("sources_count") != 1:
        fail("unexpected canonical source count")

    if payload.get("passages_count") != 1:
        fail("unexpected passage count")

    if payload.get("interpretations_count") != 0:
        fail("interpretations were inserted")

    print("[OK] BDP-001E migration ledger recorded")
    print("[OK] first canonical source adopted")
    print("[OK] source candidate records adoption without becoming canonical itself")
    print("[OK] first cited passage inserted")
    print("[OK] citation record linked to source and passage")
    print("[OK] short quotation boundary preserved")
    print("[OK] no interpretations were inserted")
    print()
    print("BDP-001E first source adoption and cited passage verification passed.")


if __name__ == "__main__":
    main()
