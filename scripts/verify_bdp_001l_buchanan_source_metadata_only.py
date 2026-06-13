#!/usr/bin/env python3
"""BDP-001L verifier. This script does not mutate the database."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any

DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")
DOI = "10.1177/1357034X97003003004"
TITLE = "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?"


def psql(sql: str) -> str:
    result = subprocess.run(
        ["psql", "-d", DB_NAME, "-X", "-q", "-t", "-A", "-v", "ON_ERROR_STOP=1", "-c", sql],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def json_value(sql: str) -> Any:
    raw = psql(sql)
    if not raw:
        return None
    return json.loads(raw)


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def check(condition: bool, message: str) -> None:
    if not condition:
        fail(message)
    print(f"[OK] {message}")


def main() -> int:
    counts = json_value(
        """
SELECT jsonb_build_object(
  'sources_count', (SELECT COUNT(*) FROM sources),
  'source_candidates_count', (SELECT COUNT(*) FROM source_candidates),
  'passages_count', (SELECT COUNT(*) FROM passages),
  'citations_count', (SELECT COUNT(*) FROM citations),
  'concept_mentions_count', (SELECT COUNT(*) FROM concept_mentions),
  'concept_relations_count', (SELECT COUNT(*) FROM concept_relations),
  'interpretations_count', (SELECT COUNT(*) FROM interpretations),
  'bdp_001l_migration_count', (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001L')
)::text;
"""
    )

    expected_counts = {
        "sources_count": 2,
        "source_candidates_count": 3,
        "passages_count": 1,
        "citations_count": 1,
        "concept_mentions_count": 1,
        "concept_relations_count": 0,
        "interpretations_count": 0,
        "bdp_001l_migration_count": 1,
    }

    for key, expected in expected_counts.items():
        check(counts.get(key) == expected, f"{key} = {expected}")

    source = json_value(
        f"""
SELECT COALESCE(to_jsonb(s)::text, '{{}}')
  FROM sources s
 WHERE s.author = 'Ian Buchanan'
   AND (
        COALESCE(s.metadata->>'doi', '') = '{DOI}'
     OR COALESCE(s.url_or_reference, '') = 'https://doi.org/{DOI}'
     OR s.title = '{TITLE}'
   )
 LIMIT 1;
"""
    )
    check(bool(source), "canonical Buchanan article source exists")
    check(source.get("title") == TITLE, "canonical source title is exact")
    check(source.get("author") == "Ian Buchanan", "canonical source author is Ian Buchanan")
    check(source.get("type") == "article", "canonical source type is article")
    publication_year = source.get("year", source.get("publication_year"))
    check(str(publication_year) == "1997", "canonical source publication year is 1997")
    check(source.get("publisher") == "SAGE Publications", "canonical source publisher is SAGE Publications")
    check(source.get("url_or_reference") == f"https://doi.org/{DOI}", "canonical source DOI URL is recorded")
    check(source.get("rights_status") == "restricted", "canonical source rights_status is restricted")
    check(source.get("reliability_level") == "high", "canonical source reliability_level is high")
    check(source.get("status") == "canonical", "canonical source status is canonical")

    metadata = source.get("metadata") or {}
    check(metadata.get("doi") == DOI, "metadata DOI is exact")
    check(metadata.get("journal") == "Body & Society", "metadata journal is Body & Society")
    check(str(metadata.get("volume")) == "3", "metadata volume is 3")
    check(str(metadata.get("issue")) == "3", "metadata issue is 3")
    check(metadata.get("pages") in {"73-91", "73–91"}, "metadata pages are 73-91")
    check(metadata.get("display_rule") == "reference_only", "metadata display rule is reference_only")
    check(metadata.get("pdf_access_status") == "user_provided_pdf_available", "PDF availability is metadata only")
    check(metadata.get("source_text_available_for_review") is True, "source text availability is recorded for review only")
    check(metadata.get("passage_ingestion_ready") is False, "passage ingestion remains blocked")
    check(metadata.get("citation_insertion_ready") is False, "citation insertion remains blocked")
    check(metadata.get("concept_mention_ready") is False, "concept mention insertion remains blocked")
    check(metadata.get("concept_relation_ready") is False, "concept relation insertion remains blocked")
    check(metadata.get("interpretation_ready") is False, "interpretation remains blocked")
    check(metadata.get("buchanan_claim_ready") is False, "Buchanan claims remain blocked")
    check(metadata.get("bdp_phase") == "BDP-001L", "metadata phase is BDP-001L")

    candidate = json_value(
        f"""
SELECT COALESCE(to_jsonb(sc)::text, '{{}}')
  FROM source_candidates sc
 WHERE sc.author = 'Ian Buchanan'
   AND (
        COALESCE(sc.metadata::text, '') ILIKE '%{DOI}%'
     OR COALESCE(sc.url, '') ILIKE '%{DOI}%'
     OR sc.title ILIKE '%Problem of the Body%'
   )
 ORDER BY sc.created_at DESC NULLS LAST
 LIMIT 1;
"""
    )
    check(bool(candidate), "review-history source candidate still exists")
    check(candidate.get("status") == "approved", "review-history source candidate status is approved")
    candidate_metadata = candidate.get("metadata") or {}
    check(candidate_metadata.get("canonical_metadata_adoption_status") == "adopted_metadata_only", "candidate records metadata-only adoption")
    check(candidate_metadata.get("candidate_history_status") == "approved_adopted_metadata_history", "candidate records approved/adopted review history")
    check(candidate_metadata.get("passage_ingestion_ready") is False, "candidate keeps passage ingestion blocked")
    check(candidate_metadata.get("citation_insertion_ready") is False, "candidate keeps citation insertion blocked")
    check(candidate_metadata.get("interpretation_ready") is False, "candidate keeps interpretation blocked")
    check(candidate_metadata.get("buchanan_claim_ready") is False, "candidate keeps Buchanan claims blocked")

    attached = json_value(
        f"""
SELECT jsonb_build_object(
  'buchanan_source_passages', (
    SELECT COUNT(*)
      FROM passages p
      JOIN sources s ON p.source_id = s.id
     WHERE s.author = 'Ian Buchanan'
       AND COALESCE(s.metadata->>'doi', '') = '{DOI}'
  ),
  'buchanan_source_citations', (
    SELECT COUNT(*)
      FROM citations c
      JOIN sources s ON c.source_id = s.id
     WHERE s.author = 'Ian Buchanan'
       AND COALESCE(s.metadata->>'doi', '') = '{DOI}'
  )
)::text;
"""
    )
    check(attached.get("buchanan_source_passages") == 0, "no passage is attached to the newly adopted Buchanan source")
    check(attached.get("buchanan_source_citations") == 0, "no citation is attached to the newly adopted Buchanan source")

    print("BDP-001L canonical Buchanan source metadata-only verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
