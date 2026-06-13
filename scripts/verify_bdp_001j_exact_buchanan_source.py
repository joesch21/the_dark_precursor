#!/usr/bin/env python3
from pathlib import Path
import json
import os
import subprocess
import sys

DB = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")


def ok(message: str) -> None:
    print(f"[OK] {message}")


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def psql(query: str) -> str:
    result = subprocess.run(
        ["psql", "-d", DB, "-At", "-F", "|", "-c", query],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    return result.stdout.strip()


def psql_json(query: str):
    result = subprocess.run(
        ["psql", "-d", DB, "-At", "-c", query],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    out = result.stdout.strip()
    if not out:
        return None
    return json.loads(out)


for path in [
    Path("sql/010_specify_bdp_001j_exact_buchanan_source_candidate_review.sql"),
    Path("scripts/read_bdp_001j_exact_buchanan_source.py"),
    Path("scripts/verify_bdp_001j_exact_buchanan_source.py"),
]:
    if not path.exists():
        fail(f"missing BDP-001J file: {path}")

ok("BDP-001J files exist")

counts = psql("""
SELECT
  (SELECT COUNT(*) FROM sources),
  (SELECT COUNT(*) FROM source_candidates),
  (SELECT COUNT(*) FROM passages),
  (SELECT COUNT(*) FROM citations),
  (SELECT COUNT(*) FROM concept_mentions),
  (SELECT COUNT(*) FROM concept_relations),
  (SELECT COUNT(*) FROM interpretations),
  (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001I'),
  (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001J');
""")

if counts != "1|3|1|1|1|0|0|1|1":
    fail(f"unexpected BDP-001J invariant: {counts}")

ok("BDP-001J preserves archive invariant and records one exact-source metadata migration")

payload = psql_json("""
SELECT jsonb_build_object(
  'status', status,
  'metadata', COALESCE(metadata, '{}'::jsonb)
)::text
FROM source_candidates
WHERE title = 'Ian Buchanan Body without Organs source candidate'
LIMIT 1;
""")

if payload is None:
    fail("Ian Buchanan placeholder candidate not found")

if payload.get("status") != "candidate":
    fail(f"Buchanan candidate must remain candidate-only, got {payload.get('status')}")

metadata = payload.get("metadata") or {}
exact = metadata.get("exact_source") or {}

required_exact = {
    "title": "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?",
    "author": "Ian Buchanan",
    "source_type": "article",
    "journal": "Body & Society",
    "volume": "3",
    "issue": "3",
    "pages": "73-91",
    "publication_date": "September 1997",
    "doi": "10.1177/1357034X97003003004",
    "url_or_reference": "https://doi.org/10.1177/1357034X97003003004",
}

for key, expected in required_exact.items():
    if exact.get(key) != expected:
        fail(f"exact source {key} expected {expected!r}, got {exact.get(key)!r}")

ok("exact Buchanan article metadata recorded for candidate review")

if metadata.get("canonical_adoption_blocked") is not True:
    fail("BDP-001J canonical adoption block not preserved")

if metadata.get("passage_authority_blocked") is not True:
    fail("BDP-001J passage authority block not preserved")

if metadata.get("interpretation_authority_blocked") is not True:
    fail("BDP-001J interpretation authority block not preserved")

ok("canonical adoption, passage authority, and interpretation authority remain blocked at BDP-001J level")

for doc_path, needle in [
    (Path("docs/BUCHANAN_SOURCE_INTAKE_REGISTRY.md"), "BDP-001J Exact Buchanan Source Specification"),
    (Path("docs/BUCHANAN_CITATION_AND_RIGHTS.md"), "BDP-001J Exact Buchanan Source Rights Note"),
    (Path("docs/BUCHANAN_THREAD_HANDOVER.md"), "BDP-001J Handover Update"),
]:
    if not doc_path.exists():
        fail(f"missing expected doc: {doc_path}")
    if needle not in doc_path.read_text():
        fail(f"{doc_path} missing {needle}")

ok("source intake registry, rights policy, and handover preserve BDP-001J")

print()
print("BDP-001J exact Buchanan source verification passed.")
