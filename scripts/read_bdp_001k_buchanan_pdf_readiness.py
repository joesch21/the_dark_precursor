#!/usr/bin/env python3
import json
import os
import subprocess
import sys

DB = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")


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


payload = psql_json("""
SELECT jsonb_build_object(
  'candidate_title', title,
  'candidate_author', author,
  'candidate_status', status,
  'candidate_url', url,
  'metadata', COALESCE(metadata, '{}'::jsonb)
)::text
FROM source_candidates
WHERE title = 'Ian Buchanan Body without Organs source candidate'
LIMIT 1;
""")

print("=== BDP-001K — Buchanan PDF availability and adoption readiness readback ===")
print(f"database={DB}")
print()

if payload is None:
    print("[FAIL] Ian Buchanan Body without Organs source candidate not found")
    raise SystemExit(1)

metadata = payload.get("metadata") or {}
exact = metadata.get("exact_source") or {}

print("Candidate:")
print(f"- title: {payload.get('candidate_title')}")
print(f"- author: {payload.get('candidate_author')}")
print(f"- status: {payload.get('candidate_status')}")
print(f"- url: {payload.get('candidate_url')}")
print()

print("Exact source:")
print(f"- title: {exact.get('title')}")
print(f"- journal: {exact.get('journal')}")
print(f"- volume/issue: {exact.get('volume')}({exact.get('issue')})")
print(f"- pages: {exact.get('pages')}")
print(f"- doi: {exact.get('doi')}")
print()

print("PDF readiness:")
for key in [
    "bdp_001k_pdf_availability_reviewed",
    "pdf_access_status",
    "pdf_file_name_observed",
    "pdf_page_count_observed",
    "pdf_title_match",
    "pdf_author_match",
    "pdf_journal_metadata_match",
    "source_text_available_for_review",
    "canonical_metadata_adoption_readiness",
    "canonical_metadata_adoption_recommendation",
    "canonical_adoption_blocked_until_bdp_001l",
    "passage_ingestion_ready",
    "citation_insertion_ready",
    "interpretation_ready",
    "buchanan_claim_ready",
    "rights_status_review",
]:
    print(f"- {key}: {metadata.get(key)}")

print()
print("BDP-001K boundary:")
for key, value in (metadata.get("bdp_001k_boundary") or {}).items():
    print(f"- {key}: {value}")

print()
print("BDP-001K readback complete.")
