#!/usr/bin/env python3
import json
import os
import subprocess
import sys


DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")

REQUIRED_TITLES = {
    "Anti-Oedipus: Capitalism and Schizophrenia",
    "A Thousand Plateaus: Capitalism and Schizophrenia",
    "Ian Buchanan Body without Organs source candidate",
}

REQUIRED_METADATA_KEYS = {
    "phase",
    "candidate_status",
    "bibliographic_edition_or_version_note",
    "rights_status_recommendation",
    "reliability_level_recommendation",
    "adoption_readiness",
    "operator_review_requirement",
    "canonical_adoption",
    "passages_authorized",
    "interpretations_authorized",
    "review_notes",
}


def fail(message):
    print(f"BDP-001D verification failed: {message}", file=sys.stderr)
    sys.exit(1)


def run_psql(query):
    command = [
        "psql",
        "-X",
        "-A",
        "-t",
        "-d",
        DB_NAME,
        "-c",
        query,
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        fail(
            "psql verification query failed.\n"
            f"Command: {' '.join(command)}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    return result.stdout.strip()


def main():
    query = r"""
    SELECT jsonb_build_object(
        'metadata_column_type', (
            SELECT udt_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = 'source_candidates'
              AND column_name = 'metadata'
        ),
        'migration_count', (
            SELECT COUNT(*)
            FROM schema_migrations
            WHERE id = '003_enrich_bdp_001d_source_candidates'
              AND phase = 'BDP-001D'
        ),
        'candidates', COALESCE((
            SELECT jsonb_agg(
                jsonb_build_object(
                    'title', title,
                    'author', author,
                    'type', type,
                    'status', status,
                    'review_notes', review_notes,
                    'metadata', metadata
                )
                ORDER BY title
            )
            FROM source_candidates
            WHERE title IN (
                'Anti-Oedipus: Capitalism and Schizophrenia',
                'A Thousand Plateaus: Capitalism and Schizophrenia',
                'Ian Buchanan Body without Organs source candidate'
            )
        ), '[]'::jsonb),
        'sources_count', (SELECT COUNT(*) FROM sources),
        'bdp_001e2_count', (
            SELECT COUNT(*)
            FROM schema_migrations
            WHERE phase = 'BDP-001E.2'
        ),
        'bdp_001e3_count', (
            SELECT COUNT(*)
            FROM schema_migrations
            WHERE phase = 'BDP-001E.3'
        ),
        'passages_count', (SELECT COUNT(*) FROM passages),
        'interpretations_count', (SELECT COUNT(*) FROM interpretations)
    )::text;
    """

    payload_raw = run_psql(query)

    try:
        payload = json.loads(payload_raw)
    except json.JSONDecodeError as exc:
        fail(f"could not parse psql JSON output: {exc}\nRaw output:\n{payload_raw}")

    if payload.get("metadata_column_type") != "jsonb":
        fail("source_candidates.metadata is missing or is not JSONB")

    if payload.get("migration_count") != 1:
        fail("BDP-001D migration ledger entry missing or duplicated")

    candidates = payload.get("candidates", [])
    found_titles = {candidate.get("title") for candidate in candidates}

    if found_titles != REQUIRED_TITLES:
        fail(f"candidate title mismatch. Found: {sorted(found_titles)}")

    for candidate in candidates:
        title = candidate.get("title")

        for field in ("author", "type", "status", "review_notes"):
            if not candidate.get(field):
                fail(f"{title} missing required field: {field}")

        later_e2_applied = payload.get("bdp_001e2_count") == 1
        if title == "A Thousand Plateaus: Capitalism and Schizophrenia" and later_e2_applied:
            if candidate.get("status") not in {"candidate", "approved"}:
                fail(f"{title} has unexpected post-selection status: {candidate.get('status')}")
        elif candidate.get("status") != "candidate":
            fail(f"{title} is not still marked candidate")

        metadata = candidate.get("metadata") or {}
        missing_keys = REQUIRED_METADATA_KEYS - set(metadata.keys())
        if missing_keys:
            fail(f"{title} missing metadata keys: {sorted(missing_keys)}")

        if metadata.get("phase") != "BDP-001D":
            fail(f"{title} metadata phase is not BDP-001D")

        if metadata.get("candidate_status") != "candidate":
            fail(f"{title} metadata candidate_status is not candidate")

        if metadata.get("canonical_adoption") is not False:
            fail(f"{title} incorrectly indicates canonical adoption")

        if metadata.get("passages_authorized") is not False:
            fail(f"{title} incorrectly authorizes passages")

        if metadata.get("interpretations_authorized") is not False:
            fail(f"{title} incorrectly authorizes interpretations")

    if payload.get("sources_count") != 0 and payload.get("bdp_001e2_count") != 1:
        fail("canonical sources were inserted before an approved later adoption phase")

    expected_passages = 1 if payload.get("bdp_001e3_count") == 1 else 0
    if payload.get("passages_count") != expected_passages:
        fail(f"unexpected passage count after phase chain: {payload.get('passages_count')}")

    if payload.get("interpretations_count") != 0:
        fail("interpretations were inserted")

    print("[OK] BDP-001D metadata column exists")
    print("[OK] BDP-001D migration ledger recorded")
    print("[OK] required source candidates exist")
    print("[OK] source candidates have enriched review metadata")
    print("[OK] source candidates remain non-canonical")
    if payload.get("bdp_001e3_count") == 1:
        print("[OK] later BDP-001E.3 passage insertion tolerated")
    else:
        if payload.get("bdp_001e3_count") == 1:
            print("[OK] later BDP-001E.3 passage insertion tolerated")
    else:
        print("[OK] no passages were inserted")
    print("[OK] no interpretations were inserted")
    print()
    print("BDP-001D source candidate review verification passed.")


if __name__ == "__main__":
    main()
