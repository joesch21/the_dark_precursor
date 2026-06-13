#!/usr/bin/env python3
import json, os, subprocess, sys
from pathlib import Path

DB = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")
TITLE = "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?"
DOI = "10.1177/1357034X97003003004"

def ok(msg): print(f"[OK] {msg}")
def fail(msg): print(f"[FAIL] {msg}"); raise SystemExit(1)

def psql(query, sep="|"):
    r = subprocess.run(["psql", "-d", DB, "-At", "-F", sep, "-c", query], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode:
        print(r.stderr, file=sys.stderr); raise SystemExit(r.returncode)
    return r.stdout.strip()

for p in [
    "sql/010_specify_bdp_001j_exact_buchanan_source_candidate_review.sql",
    "scripts/read_bdp_001j_exact_buchanan_source.py",
    "scripts/verify_bdp_001j_exact_buchanan_source.py",
]:
    if not Path(p).exists(): fail(f"missing BDP-001J file: {p}")
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
 (SELECT COUNT(*) FROM schema_migrations WHERE phase='BDP-001I'),
 (SELECT COUNT(*) FROM schema_migrations WHERE phase='BDP-001J');
""")
if counts != "1|3|1|1|1|0|0|1|1":
    fail(f"unexpected BDP-001J invariant: {counts}")
ok("BDP-001J archive invariant holds")

raw = psql("""
SELECT jsonb_build_object(
 'status', status,
 'metadata', COALESCE(metadata,'{}'::jsonb)
)::text
FROM source_candidates
WHERE title='Ian Buchanan Body without Organs source candidate'
LIMIT 1;
""", sep="\t")
if not raw: fail("Buchanan candidate missing")
payload = json.loads(raw)
if payload["status"] != "candidate":
    fail("candidate must remain candidate-only")
md = payload.get("metadata", {})
exact = md.get("exact_source", {})
required = {
    "title": TITLE,
    "author": "Ian Buchanan",
    "source_type": "article",
    "journal": "Body & Society",
    "volume": "3",
    "issue": "3",
    "pages": "73-91",
    "publication_date": "September 1997",
    "doi": DOI,
    "url_or_reference": f"https://doi.org/{DOI}",
}
for k, v in required.items():
    if exact.get(k) != v:
        fail(f"exact source {k} expected {v!r}, got {exact.get(k)!r}")
ok("exact Buchanan article metadata recorded")

for k in ["canonical_adoption_blocked", "passage_authority_blocked", "interpretation_authority_blocked"]:
    if md.get(k) is not True:
        fail(f"{k} not preserved")
ok("J-level adoption, passage, and interpretation blocks preserved")

for path, marker in [
    ("docs/BUCHANAN_SOURCE_INTAKE_REGISTRY.md", "BDP-001J Exact Buchanan Source Specification"),
    ("docs/BUCHANAN_CITATION_AND_RIGHTS.md", "BDP-001J Exact Buchanan Source Rights Note"),
    ("docs/BUCHANAN_THREAD_HANDOVER.md", "BDP-001J Handover Update"),
]:
    if marker not in Path(path).read_text():
        fail(f"{path} missing {marker}")
ok("BDP-001J docs markers preserved")
print("\nBDP-001J exact Buchanan source verification passed.")
