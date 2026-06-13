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
    Path("sql/011_review_bdp_001k_buchanan_pdf_adoption_readiness.sql"),
    Path("scripts/read_bdp_001k_buchanan_pdf_readiness.py"),
    Path("scripts/verify_bdp_001k_buchanan_pdf_readiness.py"),
]:
    if not path.exists():
        fail(f"missing BDP-001K file: {path}")

ok("BDP-001K files exist")

counts = psql("""
SELECT
  (SELECT COUNT(*) FROM sources),
  (SELECT COUNT(*) FROM source_candidates),
  (SELECT COUNT(*) FROM passages),
  (SELECT COUNT(*) FROM citations),
  (SELECT COUNT(*) FROM concept_mentions),
  (SELECT COUNT(*) FROM concept_relations),
  (SELECT COUNT(*) FROM interpretations),
  (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001J'),
  (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001K');
""")

if counts != "1|3|1|1|1|0|0|1|1":
    fail(f"unexpected BDP-001K invariant: {counts}")

ok("BDP-001K preserves archive invariant and records one readiness migration")

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
    fail("Buchanan candidate not found")

if payload.get("status") != "candidate":
    fail(f"Buchanan candidate must remain candidate-only, got {payload.get('status')}")

metadata = payload.get("metadata") or {}

for key, expected in [
    ("bdp_001k_pdf_availability_reviewed", True),
    ("pdf_access_status", "user_provided_pdf_available"),
    ("pdf_file_name_observed", "7daa2f5c56c085aba493f7cdc309cddb.pdf"),
    ("pdf_page_count_observed", 19),
    ("pdf_title_match", True),
    ("pdf_author_match", True),
    ("pdf_journal_metadata_match", True),
    ("source_text_available_for_review", True),
    ("canonical_metadata_adoption_readiness", "ready_for_metadata_adoption_only"),
    ("canonical_metadata_adoption_recommendation", "ready"),
    ("canonical_adoption_blocked_until_bdp_001l", True),
    ("passage_ingestion_ready", False),
    ("citation_insertion_ready", False),
    ("interpretation_ready", False),
    ("buchanan_claim_ready", False),
]:
    if metadata.get(key) != expected:
        fail(f"metadata {key} expected {expected!r}, got {metadata.get(key)!r}")

ok("PDF availability and metadata-only adoption readiness are recorded")

boundary = metadata.get("bdp_001k_boundary") or {}
for key in [
    "creates_source_candidate",
    "creates_canonical_source",
    "creates_passage",
    "creates_citation",
    "creates_concept_mention",
    "creates_concept_relation",
    "creates_interpretation",
    "creates_buchanan_claim",
]:
    if boundary.get(key) is not False:
        fail(f"BDP-001K boundary {key} must be false")

ok("BDP-001K boundary prevents evidence or interpretation mutation")

state = json.loads(Path("ai_boot/BUCHANAN_SYSTEM_STATE.json").read_text())
current = state.get("current_build_slice", {})

if current.get("phase") != "BDP-001K":
    fail("state current_build_slice.phase is not BDP-001K")

if current.get("type") != "pdf_availability_and_metadata_adoption_readiness_review":
    fail("state current_build_slice.type is not pdf_availability_and_metadata_adoption_readiness_review")

ok("system state records BDP-001K readiness review boundary")

for doc_path, needle in [
    (Path("docs/BUCHANAN_SOURCE_INTAKE_REGISTRY.md"), "BDP-001K PDF Availability and Canonical Metadata Adoption Readiness"),
    (Path("docs/BUCHANAN_CITATION_AND_RIGHTS.md"), "BDP-001K Uploaded PDF Rights Boundary"),
    (Path("docs/BUCHANAN_THREAD_HANDOVER.md"), "BDP-001K Handover Update"),
]:
    if not doc_path.exists():
        fail(f"missing expected doc: {doc_path}")
    if needle not in doc_path.read_text():
        fail(f"{doc_path} missing {needle}")

ok("source intake registry, rights policy, and handover record BDP-001K")

readback = subprocess.run(
    ["python3", "scripts/read_bdp_001k_buchanan_pdf_readiness.py"],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
if readback.returncode != 0:
    print(readback.stdout)
    print(readback.stderr, file=sys.stderr)
    fail("BDP-001K readback failed")

for needle in [
    "PDF readiness:",
    "pdf_access_status: user_provided_pdf_available",
    "canonical_metadata_adoption_readiness: ready_for_metadata_adoption_only",
    "passage_ingestion_ready: False",
    "BDP-001K boundary:",
]:
    if needle not in readback.stdout:
        fail(f"BDP-001K readback missing {needle}")

ok("BDP-001K readback shows PDF readiness and blocked evidence mutation")

print()
print("BDP-001K Buchanan PDF readiness verification passed.")
