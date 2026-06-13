#!/usr/bin/env python3
"""BDP-001M verifier. This script does not mutate the database."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any

DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")
DOI = "10.1177/1357034X97003003004"
TITLE = "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?"
LABEL = "BDP-001M first Buchanan passage candidate for Body without Organs"


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
    table_exists = psql("SELECT to_regclass('public.passage_candidates') IS NOT NULL;")
    check(table_exists == "t", "passage_candidates staging table exists")

    counts = json_value(
        """
SELECT jsonb_build_object(
  'sources_count', (SELECT COUNT(*) FROM sources),
  'source_candidates_count', (SELECT COUNT(*) FROM source_candidates),
  'passage_candidates_count', (SELECT COUNT(*) FROM passage_candidates),
  'passages_count', (SELECT COUNT(*) FROM passages),
  'citations_count', (SELECT COUNT(*) FROM citations),
  'concept_mentions_count', (SELECT COUNT(*) FROM concept_mentions),
  'concept_relations_count', (SELECT COUNT(*) FROM concept_relations),
  'interpretations_count', (SELECT COUNT(*) FROM interpretations),
  'bdp_001m_migration_count', (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001M')
)::text;
"""
    )

    expected_counts = {
        "sources_count": 2,
        "source_candidates_count": 3,
        "passage_candidates_count": 1,
        "passages_count": 1,
        "citations_count": 1,
        "concept_mentions_count": 1,
        "concept_relations_count": 0,
        "interpretations_count": 0,
        "bdp_001m_migration_count": 1,
    }
    for key, expected in expected_counts.items():
        check(counts.get(key) == expected, f"{key} = {expected}")

    payload = json_value(
        f"""
WITH target_source AS (
  SELECT *
    FROM sources
   WHERE author = 'Ian Buchanan'
     AND title = '{TITLE}'
     AND status = 'canonical'
     AND COALESCE(metadata->>'doi', '') = '{DOI}'
   LIMIT 1
),
target_candidate AS (
  SELECT pc.*, c.name AS concept_name, s.metadata AS source_metadata
    FROM passage_candidates pc
    JOIN target_source s ON s.id = pc.source_id
    LEFT JOIN concepts c ON c.id = pc.concept_id
   WHERE pc.candidate_label = '{LABEL}'
   LIMIT 1
)
SELECT jsonb_build_object(
  'source', COALESCE((SELECT to_jsonb(target_source) FROM target_source), '{{}}'::jsonb),
  'candidate', COALESCE((SELECT to_jsonb(target_candidate) FROM target_candidate), '{{}}'::jsonb),
  'buchanan_article_passages_count', COALESCE((SELECT COUNT(*) FROM passages p WHERE p.source_id = (SELECT id FROM target_source)), 0),
  'buchanan_article_citations_count', COALESCE((SELECT COUNT(*) FROM citations ct WHERE ct.source_id = (SELECT id FROM target_source)), 0),
  'buchanan_article_interpretations_count', COALESCE((
    SELECT COUNT(*)
      FROM interpretations i
      JOIN passages p ON p.id = i.evidence_passage_id
     WHERE p.source_id = (SELECT id FROM target_source)
  ), 0)
)::text;
"""
    )

    source = payload["source"]
    candidate = payload["candidate"]
    metadata = candidate.get("metadata") or {}
    source_metadata = source.get("metadata") or {}
    source_bdp_001m = source_metadata.get("bdp_001m_first_passage_candidate") or {}

    check(bool(source.get("id")), "canonical Buchanan source exists")
    check(source.get("title") == TITLE, "canonical source title is exact")
    check(source.get("author") == "Ian Buchanan", "canonical source author is Ian Buchanan")
    check(source.get("status") == "canonical", "canonical source remains canonical")

    check(bool(candidate.get("id")), "first Buchanan passage candidate exists")
    check(candidate.get("source_id") == source.get("id"), "passage candidate is linked to adopted Buchanan article source")
    check(candidate.get("concept_name") == "Body without Organs", "passage candidate is staged for Body without Organs")
    check(candidate.get("candidate_label") == LABEL, "passage candidate label is exact")
    check(candidate.get("candidate_status") == "candidate", "passage candidate remains candidate-only")
    check(candidate.get("candidate_scope") == "passage_candidate_envelope_metadata_only", "candidate scope is metadata-only envelope")
    check(candidate.get("review_status") == "prepared", "passage candidate review status is prepared")
    check(candidate.get("extraction_status") == "not_extracted", "candidate text extraction has not occurred")
    check(candidate.get("candidate_text") is None, "no Buchanan article text is stored in the candidate")
    check(candidate.get("candidate_text_status") == "not_stored_pending_operator_review", "candidate text remains pending operator review")
    check(candidate.get("page_or_timestamp") is None, "no page or locator has been asserted yet")
    check(candidate.get("locator_status") == "locator_pending_operator_pdf_review", "locator remains pending operator PDF review")
    check(candidate.get("rights_status") == "restricted", "candidate rights status is restricted")
    check(candidate.get("display_rule") == "reference_only", "candidate display rule is reference_only")

    for field in [
        "inserted_as_passage",
        "citation_ready",
        "concept_mention_ready",
        "interpretation_ready",
        "buchanan_claim_ready",
    ]:
        check(candidate.get(field) is False, f"{field} remains false")

    check(metadata.get("bdp_phase") == "BDP-001M", "candidate metadata phase is BDP-001M")
    check(metadata.get("prepared_from_adopted_source_metadata") is True, "candidate was prepared from adopted source metadata")
    check(metadata.get("candidate_text_stored") is False, "metadata confirms no candidate text stored")
    check(metadata.get("long_quotation_stored") is False, "metadata confirms no long quotation stored")
    check(metadata.get("passage_inserted") is False, "metadata confirms no passage inserted")
    check(metadata.get("citation_inserted") is False, "metadata confirms no citation inserted")
    check(metadata.get("concept_relation_inserted") is False, "metadata confirms no concept relation inserted")
    check(metadata.get("interpretation_inserted") is False, "metadata confirms no interpretation inserted")
    check(metadata.get("buchanan_claim_created") is False, "metadata confirms no Buchanan claim created")

    check(source_bdp_001m.get("bdp_phase") == "BDP-001M", "source metadata records BDP-001M passage candidate preparation")
    check(source_bdp_001m.get("passage_candidate_id") == candidate.get("id"), "source metadata links to passage candidate id")
    check(source_bdp_001m.get("passage_inserted") is False, "source metadata confirms no passage insertion")
    check(source_bdp_001m.get("citation_inserted") is False, "source metadata confirms no citation insertion")
    check(source_bdp_001m.get("interpretation_inserted") is False, "source metadata confirms no interpretation insertion")
    check(source_bdp_001m.get("buchanan_claim_created") is False, "source metadata confirms no Buchanan claim")

    check(payload.get("buchanan_article_passages_count") == 0, "no canonical passage is attached to the Buchanan article")
    check(payload.get("buchanan_article_citations_count") == 0, "no citation is attached to the Buchanan article")
    check(payload.get("buchanan_article_interpretations_count") == 0, "no interpretation is attached to the Buchanan article")

    print("BDP-001M first Buchanan passage candidate verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
