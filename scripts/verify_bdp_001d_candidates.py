#!/usr/bin/env python3
"""Verify BDP-001D source candidate enrichment.

This verifier proves the BDP-001D boundary:
- expected source candidates exist
- candidates have structured review metadata
- candidates remain non-canonical
- no canonical sources exist
- no passages exist
- no interpretations exist

Connection strategy matches the existing local governance scripts:
- default: sudo -u postgres psql -d $BUCHANAN_DB_NAME
- if BUCHANAN_DB_USER is set: psql -U $BUCHANAN_DB_USER -d $BUCHANAN_DB_NAME
- if BUCHANAN_USE_DIRECT_PSQL=1: psql -d $BUCHANAN_DB_NAME
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any

EXPECTED_TITLES = [
    "Anti-Oedipus: Capitalism and Schizophrenia",
    "A Thousand Plateaus: Capitalism and Schizophrenia",
    "Ian Buchanan Body without Organs source candidate",
]

REQUIRED_METADATA_KEYS = [
    "candidate_status",
    "review_notes",
    "bibliographic_edition_or_version_note",
    "rights_status_recommendation",
    "reliability_level_recommendation",
    "adoption_readiness",
    "operator_review_requirement",
    "canonical_adoption_boundary",
    "bdp_phase",
]


def psql_command() -> list[str]:
    db_name = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")
    db_user = os.environ.get("BUCHANAN_DB_USER")

    if os.environ.get("BUCHANAN_USE_DIRECT_PSQL") == "1":
        return ["psql", "-X", "-A", "-t", "-d", db_name]

    if db_user:
        return ["psql", "-X", "-A", "-t", "-U", db_user, "-d", db_name]

    return ["sudo", "-u", "postgres", "psql", "-X", "-A", "-t", "-d", db_name]


def run_sql(sql: str) -> str:
    cmd = psql_command() + ["-c", sql]
    result = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            "psql verification query failed.\n"
            f"Command: {' '.join(cmd)}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )
    return result.stdout.strip()


def load_snapshot() -> dict[str, Any]:
    titles_sql = ", ".join("'" + title.replace("'", "''") + "'" for title in EXPECTED_TITLES)
    sql = f"""
    SELECT jsonb_build_object(
        'required_tables_count', (
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name IN (
                'schema_migrations',
                'source_candidates',
                'sources',
                'passages',
                'interpretations'
              )
        ),
        'metadata_column_type', (
            SELECT udt_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = 'source_candidates'
              AND column_name = 'metadata'
        ),
        'migration_count', (
            SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001D'
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
            WHERE title IN ({titles_sql})
        ), '[]'::jsonb),
        'sources_count', (SELECT COUNT(*) FROM sources),
        'passages_count', (SELECT COUNT(*) FROM passages),
        'interpretations_count', (SELECT COUNT(*) FROM interpretations)
    )::text;
    """
    raw = run_sql(sql)
    if not raw:
        raise AssertionError("verification query returned no data")
    return json.loads(raw)


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    snapshot = load_snapshot()

    assert_true(
        snapshot.get("required_tables_count") == 5,
        f"Expected 5 required tables, found {snapshot.get('required_tables_count')}",
    )
    assert_true(
        snapshot.get("metadata_column_type") == "jsonb",
        f"source_candidates.metadata must be jsonb, found {snapshot.get('metadata_column_type')!r}",
    )
    assert_true(
        snapshot.get("migration_count") == 1,
        f"Expected exactly one BDP-001D schema_migrations row, found {snapshot.get('migration_count')}",
    )

    candidates = snapshot.get("candidates", [])
    assert_true(
        len(candidates) == 3,
        f"Expected 3 BDP-001D source candidates, found {len(candidates)}",
    )

    found_titles = {candidate.get("title") for candidate in candidates}
    assert_true(
        set(EXPECTED_TITLES) == found_titles,
        f"Candidate title mismatch. Expected {EXPECTED_TITLES}, found {sorted(found_titles)}",
    )

    for candidate in candidates:
        title = candidate.get("title")
        metadata = candidate.get("metadata") or {}

        assert_true(candidate.get("status") == "candidate", f"{title} status must remain candidate")
        assert_true(bool(candidate.get("author")), f"{title} is missing author")
        assert_true(bool(candidate.get("type")), f"{title} is missing type")
        assert_true(bool(candidate.get("review_notes")), f"{title} is missing review_notes")

        missing_keys = [key for key in REQUIRED_METADATA_KEYS if not metadata.get(key)]
        assert_true(not missing_keys, f"{title} metadata missing keys: {missing_keys}")
        assert_true(metadata.get("bdp_phase") == "BDP-001D", f"{title} metadata bdp_phase is not BDP-001D")
        assert_true(metadata.get("candidate_status") == "candidate", f"{title} metadata candidate_status must remain candidate")
        assert_true(
            "canonical source" in metadata.get("canonical_adoption_boundary", ""),
            f"{title} metadata must preserve canonical adoption boundary",
        )
        assert_true(
            "operator" in metadata.get("operator_review_requirement", "").lower(),
            f"{title} metadata must require operator review",
        )

    assert_true(
        snapshot.get("sources_count") == 0,
        f"BDP-001D must not create canonical sources; sources table has {snapshot.get('sources_count')} rows",
    )
    assert_true(
        snapshot.get("passages_count") == 0,
        f"BDP-001D must not insert passages; passages table has {snapshot.get('passages_count')} rows",
    )
    assert_true(
        snapshot.get("interpretations_count") == 0,
        "BDP-001D must not insert interpretations; "
        f"interpretations table has {snapshot.get('interpretations_count')} rows",
    )

    print("BDP-001D source candidate review verification passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, RuntimeError) as exc:
        print(f"BDP-001D verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
