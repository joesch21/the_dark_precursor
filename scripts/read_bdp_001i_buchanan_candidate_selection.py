#!/usr/bin/env python3
import os
import subprocess
import sys

DB = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")


def psql(query: str) -> str:
    result = subprocess.run(
        ["psql", "-d", DB, "-At", "-F", "\t", "-c", query],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    return result.stdout.strip()


print("=== BDP-001I — Buchanan candidate selection readback ===")
print(f"database={DB}")
print()

rows = psql("""
SELECT
  COALESCE(title, ''),
  COALESCE(author, ''),
  COALESCE(type, ''),
  COALESCE(status, ''),
  COALESCE(metadata->>'bdp_001i_selected_for_review', 'false'),
  COALESCE(metadata->>'selection_status', ''),
  COALESCE(metadata->>'exact_source_required', 'false'),
  COALESCE(metadata->>'canonical_adoption_blocked', 'false'),
  COALESCE(metadata->>'canonical_adoption_blocker', ''),
  COALESCE(metadata->>'intended_concept_link', ''),
  COALESCE(review_notes, '')
FROM source_candidates
WHERE title = 'Ian Buchanan Body without Organs source candidate'
ORDER BY created_at ASC;
""")

if not rows:
    print("No Ian Buchanan Body without Organs placeholder candidate found.")
    raise SystemExit(1)

for idx, row in enumerate(rows.splitlines(), start=1):
    (
        title,
        author,
        source_type,
        status,
        selected,
        selection_status,
        exact_source_required,
        canonical_adoption_blocked,
        canonical_adoption_blocker,
        intended_concept_link,
        review_notes,
    ) = row.split("\t")

    print(f"--- candidate card {idx} ---")
    print(f"Title: {title}")
    print(f"Author: {author}")
    print(f"Type: {source_type}")
    print(f"Status: {status}")
    print(f"Selected for review: {selected}")
    print(f"Selection status: {selection_status}")
    print(f"Exact source required: {exact_source_required}")
    print(f"Canonical adoption blocked: {canonical_adoption_blocked}")
    print(f"Blocker: {canonical_adoption_blocker}")
    print(f"Intended concept link: {intended_concept_link}")
    print(f"Review notes: {review_notes}")

print()
print("BDP-001I boundary:")
print("- selection only")
print("- placeholder candidate remains candidate")
print("- canonical adoption is blocked until exact Buchanan source is specified")
print("- no source, passage, citation, concept mention, relation, interpretation, or Buchanan claim is created")
print()
print("BDP-001I readback complete.")
