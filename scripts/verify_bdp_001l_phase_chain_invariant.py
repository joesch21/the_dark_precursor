#!/usr/bin/env python3
"""BDP-001L phase-chain invariant verifier.

Checks preserved current-state facts after BDP-001L without requiring older
phase verifiers to freeze candidate metadata in an earlier phase.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")


def psql(sql: str) -> str:
    result = subprocess.run(
        ["psql", "-d", DB_NAME, "-X", "-q", "-t", "-A", "-v", "ON_ERROR_STOP=1", "-c", sql],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> int:
    data = json.loads(psql("""
SELECT jsonb_build_object(
  'sources_count', (SELECT COUNT(*) FROM sources),
  'source_candidates_count', (SELECT COUNT(*) FROM source_candidates),
  'passages_count', (SELECT COUNT(*) FROM passages),
  'citations_count', (SELECT COUNT(*) FROM citations),
  'concept_mentions_count', (SELECT COUNT(*) FROM concept_mentions),
  'concept_relations_count', (SELECT COUNT(*) FROM concept_relations),
  'interpretations_count', (SELECT COUNT(*) FROM interpretations),
  'bdp_001j_migration_count', (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001J'),
  'bdp_001k_migration_count', (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001K'),
  'bdp_001l_migration_count', (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001L')
)::text;
"""))
    expected = {
        "sources_count": 2,
        "source_candidates_count": 3,
        "passages_count": 1,
        "citations_count": 1,
        "concept_mentions_count": 1,
        "concept_relations_count": 0,
        "interpretations_count": 0,
        "bdp_001j_migration_count": 1,
        "bdp_001k_migration_count": 1,
        "bdp_001l_migration_count": 1,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            print(f"[FAIL] {key}: expected {value}, got {data.get(key)}", file=sys.stderr)
            return 1
        print(f"[OK] {key} = {value}")

    print("BDP-001L phase-chain invariant verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
