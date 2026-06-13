#!/usr/bin/env python3
import json
import os
import subprocess
import sys

DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")

def psql_json(sql: str):
    result = subprocess.run(
        ["psql", "-X", "-v", "ON_ERROR_STOP=1", "-d", DB_NAME, "-t", "-A", "-c", sql],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    raw = result.stdout.strip()
    if not raw:
        raise SystemExit("Expected JSON output from psql, got empty output")
    return json.loads(raw)

def assert_equal(actual, expected, label):
    if actual != expected:
        raise SystemExit(f"[FAIL] {label}: expected {expected!r}, got {actual!r}")
    print(f"[OK] {label}: {actual!r}")

def main() -> None:
    counts = psql_json(r"""
    SELECT jsonb_build_object(
        'sources_count', (SELECT COUNT(*) FROM sources),
        'source_candidates_count', (SELECT COUNT(*) FROM source_candidates),
        'passage_candidates_count', (SELECT COUNT(*) FROM passage_candidates),
        'passages_count', (SELECT COUNT(*) FROM passages),
        'citations_count', (SELECT COUNT(*) FROM citations),
        'concept_mentions_count', (SELECT COUNT(*) FROM concept_mentions),
        'concept_relations_count', (SELECT COUNT(*) FROM concept_relations),
        'interpretations_count', (SELECT COUNT(*) FROM interpretations),
        'bdp_001m_migration_count', (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001M'),
        'bdp_001n_migration_count', (SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001N')
    );
    """)

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
        "bdp_001n_migration_count": 1,
    }

    for key, value in expected_counts.items():
        assert_equal(counts.get(key), value, key)

    row = psql_json(r"""
    SELECT jsonb_build_object(
        'candidate_count', COUNT(*),
        'candidate_text', MAX(pc.candidate_text),
        'candidate_text_status', MAX(pc.candidate_text_status),
        'page_or_timestamp', MAX(pc.page_or_timestamp),
        'chapter_or_section', MAX(pc.chapter_or_section),
        'locator_status', MAX(pc.locator_status),
        'review_status', MAX(pc.review_status),
        'extraction_status', MAX(pc.extraction_status),
        'rights_status', MAX(pc.rights_status),
        'display_rule', MAX(pc.display_rule),
        'inserted_as_passage', bool_or(pc.inserted_as_passage),
        'citation_ready', bool_or(pc.citation_ready),
        'concept_mention_ready', bool_or(pc.concept_mention_ready),
        'interpretation_ready', bool_or(pc.interpretation_ready),
        'buchanan_claim_ready', bool_or(pc.buchanan_claim_ready),
        'source_title', MAX(s.title),
        'source_author', MAX(s.author),
        'target_concept', MAX(c.name),
        'metadata', MAX(pc.metadata::text)::jsonb
    )
    FROM passage_candidates pc
    JOIN sources s ON s.id = pc.source_id
    LEFT JOIN concepts c ON c.id = pc.concept_id
    WHERE s.author = 'Ian Buchanan'
      AND s.title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
      AND c.name = 'Body without Organs';
    """)

    assert_equal(row["candidate_count"], 1, "one Buchanan passage candidate")
    assert_equal(row["candidate_text"], "the body without organs is not a primary term", "short candidate excerpt")
    assert_equal(row["candidate_text_status"], "reviewed_short_excerpt", "candidate_text_status")
    assert_equal(row["page_or_timestamp"], "printed article page 76; PDF page 4", "page_or_timestamp")
    assert_equal(row["chapter_or_section"], "opening section before Spinoza", "chapter_or_section")
    assert_equal(row["locator_status"], "reviewed", "locator_status")
    assert_equal(row["review_status"], "approved", "review_status")
    assert_equal(row["extraction_status"], "operator_pdf_reviewed_short_excerpt", "extraction_status")
    assert_equal(row["rights_status"], "restricted", "rights_status")
    assert_equal(row["display_rule"], "reference_only", "display_rule")
    assert_equal(row["inserted_as_passage"], False, "inserted_as_passage")
    assert_equal(row["citation_ready"], True, "citation_ready")
    assert_equal(row["concept_mention_ready"], False, "concept_mention_ready")
    assert_equal(row["interpretation_ready"], False, "interpretation_ready")
    assert_equal(row["buchanan_claim_ready"], False, "buchanan_claim_ready")

    excerpt_words = row["candidate_text"].split()
    if len(excerpt_words) > 12:
        raise SystemExit(f"[FAIL] candidate excerpt too long: {len(excerpt_words)} words")
    print(f"[OK] rights-aware short excerpt word count: {len(excerpt_words)}")

    metadata = row["metadata"]
    assert_equal(metadata.get("review_status_detail"), "reviewed_for_later_passage_insertion", "metadata.review_status_detail")
    assert_equal(metadata.get("display_rule_detail"), "reference_only_short_excerpt_candidate", "metadata.display_rule_detail")
    assert_equal(metadata.get("long_quotation_stored"), False, "metadata.long_quotation_stored")
    assert_equal(metadata.get("article_reproduction_authorized"), False, "metadata.article_reproduction_authorized")
    assert_equal(metadata.get("passage_inserted"), False, "metadata.passage_inserted")
    assert_equal(metadata.get("citation_inserted"), False, "metadata.citation_inserted")
    assert_equal(metadata.get("concept_mention_inserted"), False, "metadata.concept_mention_inserted")
    assert_equal(metadata.get("concept_relation_inserted"), False, "metadata.concept_relation_inserted")
    assert_equal(metadata.get("interpretation_inserted"), False, "metadata.interpretation_inserted")
    assert_equal(metadata.get("buchanan_claim_created"), False, "metadata.buchanan_claim_created")

    print("BDP-001N Buchanan passage candidate review verification passed.")

if __name__ == "__main__":
    main()
