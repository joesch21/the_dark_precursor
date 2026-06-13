#!/usr/bin/env python3
import json
import os
import subprocess
import sys

DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")
TITLE = "A Thousand Plateaus: Capitalism and Schizophrenia"


def fail(message):
    print(f"BDP-001E.2 verification failed: {message}", file=sys.stderr)
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
            WHERE id = '005_adopt_bdp_001e2_selected_candidate_source_only'
              AND phase = 'BDP-001E.2'
        ),
        'source_count', (
            SELECT COUNT(*)
            FROM sources
            WHERE title = 'A Thousand Plateaus: Capitalism and Schizophrenia'
              AND status = 'canonical'
              AND reliability_level = 'high'
              AND rights_status = 'fair_use_reference_only'
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
        'bdp_001e3_count', (
            SELECT COUNT(*)
            FROM schema_migrations
            WHERE phase = 'BDP-001E.3'
        ),
        'passages_total', (SELECT COUNT(*) FROM passages),
        'citations_total', (SELECT COUNT(*) FROM citations),
        'interpretations_total', (SELECT COUNT(*) FROM interpretations)
    )::text;
    """

    payload = json.loads(run_psql(query))

    if payload["migration_count"] != 1:
        fail("BDP-001E.2 migration ledger missing or duplicated")

    if payload["source_count"] != 1:
        fail("expected exactly one canonical A Thousand Plateaus source")

    candidate = payload.get("candidate") or {}
    metadata = candidate.get("metadata") or {}

    if candidate.get("status") != "approved":
        fail("source candidate was not marked approved")

    if metadata.get("source_adoption_created") is not True:
        fail("candidate metadata does not record source adoption")

    if metadata.get("candidate_record_is_canonical") is not False:
        fail("candidate metadata incorrectly treats candidate row as canonical")

    later_e3_applied = payload.get("bdp_001e3_count") == 1
    if later_e3_applied:
        if metadata.get("passage_inserted") is not True:
            fail("metadata should record passage insertion after BDP-001E.3")
    elif metadata.get("passage_inserted") is not False:
        fail("metadata incorrectly indicates passage insertion before BDP-001E.3")

    if metadata.get("citation_inserted") is not False:
        fail("metadata incorrectly indicates citation insertion")

    if metadata.get("interpretation_created") is not False:
        fail("metadata incorrectly indicates interpretation creation")

    if payload["sources_total"] != 1:
        fail("unexpected total source count")

    expected_passages = 1 if later_e3_applied else 0
    if payload["passages_total"] != expected_passages:
        fail(f"unexpected passage count after phase chain: {payload['passages_total']}")

    if payload["citations_total"] != 0:
        fail("citations were inserted")

    if payload["interpretations_total"] != 0:
        fail("interpretations were inserted")

    print("[OK] BDP-001E.2 migration ledger recorded")
    print("[OK] selected candidate adopted into canonical sources")
    print("[OK] candidate row remains review history, not canonical source")
    print("[OK] no passages inserted")
    print("[OK] no citations inserted")
    print("[OK] no interpretations inserted")
    print()
    print("BDP-001E.2 source-only adoption verification passed.")


if __name__ == "__main__":
    main()
