#!/usr/bin/env python3
import os, subprocess, sys
from pathlib import Path

DB = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")

def ok(msg): print(f"[OK] {msg}")
def fail(msg): print(f"[FAIL] {msg}"); raise SystemExit(1)

def psql(query):
    r = subprocess.run(["psql", "-d", DB, "-At", "-F", "|", "-c", query], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode:
        print(r.stderr, file=sys.stderr); raise SystemExit(r.returncode)
    return r.stdout.strip()

doc = Path("docs/BUCHANAN_CONCEPT_EVIDENCE_DEPTH_TIERS.md")
if not doc.exists(): fail("missing concept evidence depth tiers doc")
text = doc.read_text()
for needle in [
    "Not every concept requires full-source treatment.",
    "Tier 1 — Anchor Concepts",
    "Tier 2 — Supporting Concepts",
    "Tier 3 — Contextual Terms",
    "No Buchanan-specific claim may be made without an exact Buchanan source passage.",
]:
    if needle not in text: fail(f"missing doctrine marker: {needle}")
ok("concept evidence depth tiers doctrine is preserved")

counts = psql("""
SELECT
 (SELECT COUNT(*) FROM sources),
 (SELECT COUNT(*) FROM passages),
 (SELECT COUNT(*) FROM citations),
 (SELECT COUNT(*) FROM concept_mentions),
 (SELECT COUNT(*) FROM concept_relations),
 (SELECT COUNT(*) FROM interpretations),
 (SELECT COUNT(*) FROM schema_migrations WHERE phase='BDP-001I'),
 (SELECT COUNT(*) FROM schema_migrations WHERE phase='BDP-001J.0');
""")
if counts != "1|1|1|1|0|0|1|0":
    fail(f"unexpected BDP-001J.0 invariant: {counts}")
ok("BDP-001J.0 docs-only invariant preserved")
print("\nBDP-001J.0 concept evidence depth tiers verification passed.")
