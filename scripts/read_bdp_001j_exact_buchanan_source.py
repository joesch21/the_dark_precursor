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
  'candidate_type', type,
  'candidate_status', status,
  'candidate_url', url,
  'review_notes', review_notes,
  'metadata', COALESCE(metadata, '{}'::jsonb)
)::text
FROM source_candidates
WHERE title = 'Ian Buchanan Body without Organs source candidate'
LIMIT 1;
""")

print("=== BDP-001J — Exact Buchanan source candidate review readback ===")
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
print(f"- row type: {payload.get('candidate_type')}")
print(f"- status: {payload.get('candidate_status')}")
print(f"- url: {payload.get('candidate_url')}")
print()

print("Exact Buchanan source specified for review:")
for key in [
    "title",
    "author",
    "source_type",
    "journal",
    "volume",
    "issue",
    "pages",
    "publication_date",
    "doi",
    "url_or_reference",
    "publisher",
    "rights_status_recommendation",
    "display_rule",
    "reliability_level_recommendation",
]:
    print(f"- {key}: {exact.get(key)}")

print()
print("Review state:")
print(f"- exact source specified: {metadata.get('bdp_001j_exact_source_specified')}")
print(f"- selection status: {metadata.get('selection_status')}")
print(f"- review status: {metadata.get('exact_source_review_status')}")
print(f"- canonical adoption blocked: {metadata.get('canonical_adoption_blocked')}")
print(f"- blocker: {metadata.get('canonical_adoption_blocker')}")
print(f"- intended concept link: {metadata.get('intended_concept_link')}")

print()
print("BDP-001J boundary:")
for key, value in (metadata.get("bdp_001j_boundary") or {}).items():
    print(f"- {key}: {value}")

print()
print("BDP-001J readback complete.")
