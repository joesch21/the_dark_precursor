#!/usr/bin/env python3
import json, os, subprocess, sys
from pathlib import Path

DB = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")

def ok(msg): print(f"[OK] {msg}")
def fail(msg): print(f"[FAIL] {msg}"); raise SystemExit(1)

def psql(query, sep="|"):
    r = subprocess.run(["psql", "-d", DB, "-At", "-F", sep, "-c", query], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode:
        print(r.stderr, file=sys.stderr); raise SystemExit(r.returncode)
    return r.stdout.strip()

for p in [
    "sql/009_select_bdp_001i_buchanan_placeholder_candidate_only.sql",
    "scripts/read_bdp_001i_buchanan_candidate_selection.py",
    "scripts/verify_bdp_001i_buchanan_candidate_selection.py",
]:
    if not Path(p).exists(): fail(f"missing BDP-001I file: {p}")
ok("BDP-001I files exist")

counts = psql("""
SELECT
 (SELECT COUNT(*) FROM sources),
 (SELECT COUNT(*) FROM passages),
 (SELECT COUNT(*) FROM citations),
 (SELECT COUNT(*) FROM concept_mentions),
 (SELECT COUNT(*) FROM concept_relations),
 (SELECT COUNT(*) FROM interpretations),
 (SELECT COUNT(*) FROM schema_migrations WHERE phase='BDP-001I');
""")
if counts != "1|1|1|1|0|0|1":
    fail(f"unexpected BDP-001I invariant: {counts}")
ok("BDP-001I archive invariant still holds")

raw = psql("""
SELECT jsonb_build_object(
 'status', status,
 'notes', COALESCE(review_notes,''),
 'metadata', COALESCE(metadata,'{}'::jsonb)
)::text
FROM source_candidates
WHERE title='Ian Buchanan Body without Organs source candidate'
LIMIT 1;
""", sep="\t")
if not raw: fail("Buchanan candidate missing")
payload = json.loads(raw)
if payload["status"] != "candidate":
    fail(f"candidate no longer candidate-only: {payload['status']}")
combined = json.dumps(payload.get("metadata", {})) + "\n" + payload.get("notes", "")
if "Body without Organs" not in combined:
    fail("Body without Organs concept link missing")
if "canonical" not in combined.lower() or "block" not in combined.lower():
    fail("canonical adoption block missing")
ok("Buchanan candidate remains selected/candidate-only with adoption block")
print("\nBDP-001I Buchanan candidate selection verification passed.")
