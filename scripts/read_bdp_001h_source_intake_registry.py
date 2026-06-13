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


print("=== BDP-001H — Source intake registry readback ===")
print(f"database={DB}")
print()

counts = psql("""
SELECT
  (SELECT COUNT(*) FROM sources),
  (SELECT COUNT(*) FROM source_candidates),
  (SELECT COUNT(*) FROM passages),
  (SELECT COUNT(*) FROM citations),
  (SELECT COUNT(*) FROM concept_mentions),
  (SELECT COUNT(*) FROM concept_relations),
  (SELECT COUNT(*) FROM interpretations);
""")

(
    sources_count,
    source_candidates_count,
    passages_count,
    citations_count,
    concept_mentions_count,
    concept_relations_count,
    interpretations_count,
) = counts.split("\t")

print("Current archive state:")
print(f"- canonical sources: {sources_count}")
print(f"- source candidates: {source_candidates_count}")
print(f"- passages: {passages_count}")
print(f"- citations: {citations_count}")
print(f"- concept mentions: {concept_mentions_count}")
print(f"- concept relations: {concept_relations_count}")
print(f"- interpretations: {interpretations_count}")
print()

print("Allowed intake modes:")
for mode in [
    "manual_upload",
    "curated_import",
    "assisted_discovery",
    "operator_note",
    "bibliography_seed",
    "transcript_seed",
]:
    print(f"- {mode}")

print()
print("Current source candidates:")

rows = psql("""
SELECT
  COALESCE(title, ''),
  COALESCE(author, ''),
  COALESCE(type, ''),
  COALESCE(status, ''),
  COALESCE(review_notes, '')
FROM source_candidates
ORDER BY created_at ASC, title ASC;
""")

if not rows:
    print("- none")
else:
    for idx, row in enumerate(rows.splitlines(), start=1):
        title, author, source_type, status, review_notes = row.split("\t")
        print(f"{idx}. {title}")
        print(f"   author: {author}")
        print(f"   type: {source_type}")
        print(f"   status: {status}")
        print(f"   notes: {review_notes}")

print()
print("BDP-001H boundary:")
print("- read-only registry")
print("- no candidate insertion")
print("- no canonical source insertion")
print("- no passage/citation/concept/interpretation mutation")
print()
print("BDP-001H readback complete.")
