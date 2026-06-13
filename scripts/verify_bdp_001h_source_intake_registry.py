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
    Path("docs/BUCHANAN_SOURCE_INTAKE_REGISTRY.md"),
    Path("scripts/read_bdp_001h_source_intake_registry.py"),
    Path("scripts/preview_bdp_001h_candidate_creation.py"),
]

for path in required_files:
    if not path.exists():
        fail(f"missing required BDP-001H file: {path}")

ok("BDP-001H source intake registry files exist")

registry = Path("docs/BUCHANAN_SOURCE_INTAKE_REGISTRY.md").read_text()

for needle in [
    "A preview is not a candidate.",
    "A candidate is not a canonical source.",
    "No SQL migration.",
    "No database mutation.",
    "BDP-001I — Select first Buchanan source candidate for Body without Organs.",
]:
    if needle not in registry:
        fail(f"source intake registry missing required boundary text: {needle}")

ok("source intake registry records candidate and canonical adoption boundaries")

state = json.loads(Path("ai_boot/BUCHANAN_SYSTEM_STATE.json").read_text())

if state.get("current_build_slice", {}).get("phase") != "BDP-001H":
    fail("state current_build_slice.phase is not BDP-001H")

if state.get("current_build_slice", {}).get("type") != "read_only_source_intake_registry":
    fail("state current_build_slice.type is not read_only_source_intake_registry")

ok("system state records BDP-001H as read-only source intake registry")

counts = psql("""
SELECT
  (SELECT COUNT(*) FROM sources),
  (SELECT COUNT(*) FROM passages),
  (SELECT COUNT(*) FROM citations),
  (SELECT COUNT(*) FROM concept_mentions),
  (SELECT COUNT(*) FROM concept_relations),
  (SELECT COUNT(*) FROM interpretations),
  (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001F'),
  (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001H');
""")

if counts != "1|1|1|1|0|0|1|0":
    fail(f"unexpected BDP-001H invariant: {counts}")

ok("BDP-001H preserves verified database invariant and adds no migration")

readback = subprocess.run(
    ["python3", "scripts/read_bdp_001h_source_intake_registry.py"],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
if readback.returncode != 0:
    print(readback.stdout)
    print(readback.stderr, file=sys.stderr)
    fail("source intake registry readback script failed")

for needle in [
    "BDP-001H — Source intake registry readback",
    "Allowed intake modes:",
    "BDP-001H boundary:",
    "no candidate insertion",
]:
    if needle not in readback.stdout:
        fail(f"source intake registry readback missing: {needle}")

ok("source intake registry readback resolves current intake state")

preview = subprocess.run(
    ["python3", "scripts/preview_bdp_001h_candidate_creation.py"],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
if preview.returncode != 0:
    print(preview.stdout)
    print(preview.stderr, file=sys.stderr)
    fail("candidate creation preview script failed")

payload = json.loads(preview.stdout)

if payload.get("writes_database") is not False:
    fail("candidate creation preview must be read-only")

if payload.get("hard_boundaries", {}).get("creates_source_candidate") is not False:
    fail("candidate creation preview must not create a source candidate")

ok("candidate creation preview is read-only and non-mutating")

print()
print("BDP-001H source intake registry verification passed.")
