#!/usr/bin/env python3
from pathlib import Path
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


tier_doc = Path("docs/BUCHANAN_CONCEPT_EVIDENCE_DEPTH_TIERS.md")
if not tier_doc.exists():
    fail("missing docs/BUCHANAN_CONCEPT_EVIDENCE_DEPTH_TIERS.md")

text = tier_doc.read_text()
for needle in [
    "Not every concept requires full-source treatment.",
    "Every concept requires only the evidence needed for the authority level it is allowed to carry.",
    "Tier 1 — Anchor Concepts",
    "Tier 2 — Supporting Concepts",
    "Tier 3 — Contextual Terms",
    "No Buchanan-specific claim may be made without an exact Buchanan source passage.",
]:
    if needle not in text:
        fail(f"concept evidence tier doc missing: {needle}")

ok("concept evidence depth tiers doctrine is recorded")

for doc_path, needle in [
    (Path("docs/BUCHANAN_CONCEPT_ONTOLOGY.md"), "BDP-001J.0 Concept Evidence Depth Tiers"),
    (Path("docs/BUCHANAN_INGESTION_WORKFLOW.md"), "BDP-001J.0 Concept Evidence Depth Tiers"),
    (Path("docs/BUCHANAN_THREAD_HANDOVER.md"), "BDP-001J.0 Handover Update"),
]:
    if not doc_path.exists():
        fail(f"missing expected doc: {doc_path}")
    if needle not in doc_path.read_text():
        fail(f"{doc_path} missing {needle}")

ok("ontology, ingestion workflow, and handover preserve BDP-001J.0")

counts = psql("""
SELECT
  (SELECT COUNT(*) FROM sources),
  (SELECT COUNT(*) FROM passages),
  (SELECT COUNT(*) FROM citations),
  (SELECT COUNT(*) FROM concept_mentions),
  (SELECT COUNT(*) FROM concept_relations),
  (SELECT COUNT(*) FROM interpretations),
  (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001I'),
  (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001J.0');
""")

if counts != "1|1|1|1|0|0|1|0":
    fail(f"unexpected BDP-001J.0 invariant: {counts}")

ok("BDP-001J.0 preserves database invariant and adds no migration")

print()
print("BDP-001J.0 concept evidence depth tiers verification passed.")
