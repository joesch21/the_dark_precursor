#!/usr/bin/env python3
"""Verify BDP-001C seed records for Buchanan platform."""

import os
import subprocess
import sys

DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")

REQUIRED_CONCEPTS = {
    "Body without Organs": "canonical",
    "organism": "proposed",
    "desire": "proposed",
    "assemblage": "proposed",
    "strata": "proposed",
}

REQUIRED_SOURCE_CANDIDATES = {
    "Anti-Oedipus: Capitalism and Schizophrenia",
    "A Thousand Plateaus: Capitalism and Schizophrenia",
    "Ian Buchanan Body without Organs source candidate",
}


def run_sql(sql: str) -> str:
    cmd = [
        "sudo",
        "-u",
        "postgres",
        "psql",
        "-d",
        DB_NAME,
        "-X",
        "-v",
        "ON_ERROR_STOP=1",
        "-Atc",
        sql,
    ]
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        print("[FAIL] SQL command failed")
        print(result.stderr.strip())
        sys.exit(1)
    return result.stdout.strip()


def ok(message: str) -> None:
    print(f"[OK] {message}")


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    sys.exit(1)


rows = run_sql("""
SELECT name || '|' || status
FROM concepts
WHERE name IN (
  'Body without Organs',
  'organism',
  'desire',
  'assemblage',
  'strata'
)
ORDER BY name;
""").splitlines()

found_concepts = {}
for row in rows:
    name, status = row.split("|", 1)
    found_concepts[name] = status

for name, expected_status in REQUIRED_CONCEPTS.items():
    actual_status = found_concepts.get(name)
    if actual_status != expected_status:
        fail(f"concept {name!r} expected status {expected_status!r}, found {actual_status!r}")

ok("required concept seed records exist with expected statuses")

candidate_rows = run_sql("""
SELECT title
FROM source_candidates
WHERE discovered_by = 'BDP-001C_seed'
ORDER BY title;
""").splitlines()

found_candidates = set(candidate_rows)
missing_candidates = REQUIRED_SOURCE_CANDIDATES - found_candidates

if missing_candidates:
    fail(f"missing source candidates: {sorted(missing_candidates)}")

ok("required source candidate seed records exist")

canonical_sources = run_sql("""
SELECT COUNT(*)
FROM sources
WHERE candidate_id IN (
  SELECT id
  FROM source_candidates
  WHERE discovered_by = 'BDP-001C_seed'
);
""")

if canonical_sources != "0":
    fail("BDP-001C seed candidates were incorrectly adopted into canonical sources")

ok("source candidates remain non-canonical")

migration_rows = run_sql("""
SELECT COUNT(*)
FROM schema_migrations
WHERE id = '002_seed_bdp_001c'
  AND phase = 'BDP-001C';
""")

if migration_rows != "1":
    fail("BDP-001C migration ledger row missing")

ok("BDP-001C migration ledger recorded")

print()
print("BDP-001C seed verification passed.")
