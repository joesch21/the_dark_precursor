#!/usr/bin/env python3
import json
import os
import subprocess
import sys


DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")
SELECTED_TITLE = "A Thousand Plateaus: Capitalism and Schizophrenia"


def fail(message):
    print(f"BDP-001E.1 verification failed: {message}", file=sys.stderr)
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
            WHERE id = '004_select_bdp_001e1_first_adoption_candidate'
              AND phase = 'BDP-001E.1'
        ),
        'selected_count', (
            SELECT COUNT(*)
            FROM source_candidates
            WHERE metadata->>'first_adoption_candidate_selected' = 'true'
              AND metadata->>'selection_lock' = 'true'
              AND metadata->>'selection_lock_phase' = 'BDP-001E.1'
        ),
        'selected_candidate', (
            SELECT jsonb_build_object(
                'title', title,
                'status', status,
                'metadata', metadata
            )
            FROM source_candidates
            WHERE metadata->>'first_adoption_candidate_selected' = 'true'
              AND metadata->>'selection_lock' = 'true'
              AND metadata->>'selection_lock_phase' = 'BDP-001E.1'
            LIMIT 1
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
        fail("BDP-001E.1 migration ledger missing or duplicated")

    if payload.get("selected_count") != 1:
        fail("expected exactly one locked first-adoption candidate")

    selected = payload.get("selected_candidate") or {}
    metadata = selected.get("metadata") or {}

    if selected.get("title") != SELECTED_TITLE:
        fail(f"wrong candidate selected: {selected.get('title')}")

    if selected.get("status") != "candidate":
        fail("selected candidate must remain status=candidate")

    if metadata.get("adoption_selection_status") != "selected_for_canonical_adoption_review":
        fail("selection status metadata missing or incorrect")

    if metadata.get("source_adoption_created") is not False:
        fail("metadata incorrectly indicates source adoption")

    if metadata.get("passage_inserted") is not False:
        fail("metadata incorrectly indicates passage insertion")

    if metadata.get("citation_inserted") is not False:
        fail("metadata incorrectly indicates citation insertion")

    if metadata.get("interpretation_created") is not False:
        fail("metadata incorrectly indicates interpretation creation")

    if payload.get("sources_count") != 0:
        fail("canonical source was created during selection-only phase")

    if payload.get("passages_count") != 0:
        fail("passage was inserted during selection-only phase")

    if payload.get("interpretations_count") != 0:
        fail("interpretation was inserted during selection-only phase")

    print("[OK] BDP-001E.1 migration ledger recorded")
    print("[OK] exactly one first adoption candidate selected")
    print("[OK] selected candidate remains candidate-only")
    print("[OK] no canonical source was created")
    print("[OK] no passage was inserted")
    print("[OK] no interpretation was inserted")
    print()
    print("BDP-001E.1 first adoption candidate selection verification passed.")


if __name__ == "__main__":
    main()
