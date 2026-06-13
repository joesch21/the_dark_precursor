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


for path in [
    Path("sql/009_select_bdp_001i_buchanan_placeholder_candidate_only.sql"),
    Path("scripts/read_bdp_001i_buchanan_candidate_selection.py"),
    Path("scripts/verify_bdp_001i_buchanan_candidate_selection.py"),
    Path("docs/BUCHANAN_PATCH_BUNDLE_WORKFLOW.md"),
]:
    if not path.exists():
        fail(f"missing BDP-001I file: {path}")

ok("BDP-001I files exist")

workflow = Path("docs/BUCHANAN_PATCH_BUNDLE_WORKFLOW.md").read_text()
for needle in [
    "make patch bundle",
    "download zip",
    "git apply --check",
    "run verifiers",
    "commit/push from local repo",
]:
    if needle not in workflow:
        fail(f"patch bundle workflow missing: {needle}")

ok("patch bundle workflow records preferred application method")

counts = psql("""
SELECT
  (SELECT COUNT(*) FROM sources),
  (SELECT COUNT(*) FROM passages),
  (SELECT COUNT(*) FROM citations),
  (SELECT COUNT(*) FROM concept_mentions),
  (SELECT COUNT(*) FROM concept_relations),
  (SELECT COUNT(*) FROM interpretations),
  (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001I');
""")

if counts != "1|1|1|1|0|0|1":
    fail(f"unexpected BDP-001I invariant: {counts}")

ok("BDP-001I preserves archive invariant and records one selection migration")

candidate = psql("""
SELECT
  status,
  COALESCE(review_notes, ''),
  COALESCE(metadata::text, '')
FROM source_candidates
WHERE title = 'Ian Buchanan Body without Organs source candidate'
LIMIT 1;
""")

if not candidate:
    fail("Buchanan placeholder candidate not found")

status, review_notes, metadata = candidate.split("|", 2)
combined = f"{status}\n{review_notes}\n{metadata}"

if status != "candidate":
    fail(f"Buchanan placeholder candidate must remain candidate, got {status}")

for needle in [
    "placeholder_candidate_selected_only",
    "Body without Organs",
]:
    if needle not in combined:
        fail(f"Buchanan candidate selection metadata missing: {needle}")

if "canonical" not in combined.lower() or "block" not in combined.lower():
    fail("Buchanan candidate does not record canonical adoption block")

if "exact" not in combined.lower():
    fail("Buchanan candidate does not record exact source requirement")

ok("Buchanan placeholder candidate selected while remaining candidate-only")
ok("canonical Buchanan source adoption remains blocked")

readback = subprocess.run(
    ["python3", "scripts/read_bdp_001i_buchanan_candidate_selection.py"],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
if readback.returncode != 0:
    print(readback.stdout)
    print(readback.stderr, file=sys.stderr)
    fail("BDP-001I readback failed")

for needle in [
    "BDP-001I",
    "Selected for review: true",
    "Canonical adoption blocked: true",
    "BDP-001I boundary:",
]:
    if needle not in readback.stdout:
        fail(f"BDP-001I readback missing: {needle}")

ok("BDP-001I readback shows selection and canonical adoption block")

print()
print("BDP-001I Buchanan candidate selection verification passed.")
