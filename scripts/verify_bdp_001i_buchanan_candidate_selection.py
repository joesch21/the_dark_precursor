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


required_files = [
    Path("docs/BUCHANAN_PATCH_BUNDLE_WORKFLOW.md"),
    Path("sql/009_select_bdp_001i_buchanan_placeholder_candidate_only.sql"),
    Path("scripts/read_bdp_001i_buchanan_candidate_selection.py"),
    Path("scripts/verify_bdp_001i_buchanan_candidate_selection.py"),
]

for path in required_files:
    if not path.exists():
        fail(f"missing required BDP-001I file: {path}")

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
        fail(f"patch bundle workflow missing required phrase: {needle}")

ok("patch bundle workflow records preferred application method")

state = json.loads(Path("ai_boot/BUCHANAN_SYSTEM_STATE.json").read_text())

if state.get("current_build_slice", {}).get("phase") != "BDP-001I":
    fail("state current_build_slice.phase is not BDP-001I")

if state.get("current_build_slice", {}).get("type") != "selection_only_exact_source_block":
    fail("state current_build_slice.type is not selection_only_exact_source_block")

ok("system state records BDP-001I selection-only boundary")

counts = psql("""
SELECT
  (SELECT COUNT(*) FROM sources),
  (SELECT COUNT(*) FROM passages),
  (SELECT COUNT(*) FROM citations),
  (SELECT COUNT(*) FROM concept_mentions),
  (SELECT COUNT(*) FROM concept_relations),
  (SELECT COUNT(*) FROM interpretations),
  (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001F'),
  (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001H'),
  (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001I'),
  (SELECT COUNT(*) FROM source_candidates);
""")

if counts != "1|1|1|1|0|0|1|0|1|3":
    fail(f"unexpected BDP-001I invariant: {counts}")

ok("BDP-001I preserves archive invariant and records one selection migration")

selected = psql("""
SELECT COUNT(*)
FROM source_candidates
WHERE title = 'Ian Buchanan Body without Organs source candidate'
  AND author = 'Ian Buchanan'
  AND status = 'candidate'
  AND metadata->>'bdp_001i_selected_for_review' = 'true'
  AND metadata->>'exact_source_required' = 'true'
  AND metadata->>'canonical_adoption_blocked' = 'true'
  AND metadata->>'intended_concept_link' = 'Body without Organs';
""")

if selected != "1":
    fail(f"expected exactly one selected Buchanan placeholder candidate, got {selected}")

ok("Buchanan placeholder candidate selected while remaining candidate-only")

ian_sources = psql("""
SELECT COUNT(*)
FROM sources
WHERE author ILIKE '%Ian Buchanan%';
""")

if ian_sources != "0":
    fail(f"expected no canonical Ian Buchanan source, got {ian_sources}")

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
    fail("BDP-001I readback script failed")

for needle in [
    "BDP-001I — Buchanan candidate selection readback",
    "Selected for review: true",
    "Exact source required: true",
    "Canonical adoption blocked: true",
    "selection only",
]:
    if needle not in readback.stdout:
        fail(f"BDP-001I readback missing required text: {needle}")

ok("BDP-001I readback shows selection and canonical adoption block")

print()
print("BDP-001I Buchanan candidate selection verification passed.")
