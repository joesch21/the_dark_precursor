-- BDP-001K — Review exact Buchanan source candidate for canonical adoption readiness
-- Boundary: readiness review only. No canonical source, passage, citation, concept mention, relation, interpretation, or Buchanan claim is created.

BEGIN;

DO $$
DECLARE
  v_candidate_id source_candidates.id%TYPE;
BEGIN
  IF EXISTS (SELECT 1 FROM schema_migrations WHERE phase = 'BDP-001K') THEN
    RAISE EXCEPTION 'BDP-001K migration already recorded';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM schema_migrations WHERE phase = 'BDP-001J') THEN
    RAISE EXCEPTION 'BDP-001K requires BDP-001J exact Buchanan source specification first';
  END IF;

  SELECT id
    INTO v_candidate_id
  FROM source_candidates
  WHERE title = 'Ian Buchanan Body without Organs source candidate'
    AND author = 'Ian Buchanan'
    AND status = 'candidate'
    AND COALESCE(metadata, '{}'::jsonb)->>'bdp_001j_exact_source_specified' = 'true'
  LIMIT 1;

  IF v_candidate_id IS NULL THEN
    RAISE EXCEPTION 'BDP-001K requires the exact Buchanan source candidate to exist and remain candidate-only';
  END IF;

  UPDATE source_candidates
  SET
    review_notes =
      CASE
        WHEN review_notes LIKE '%BDP-001K:%' THEN review_notes
        ELSE CONCAT(
          COALESCE(review_notes, ''),
          ' BDP-001K: uploaded PDF availability reviewed. Uploaded file matches the exact Buchanan article metadata sufficiently for canonical source metadata adoption readiness. Candidate remains non-canonical. BDP-001L may adopt source metadata only. Passage ingestion, citation insertion, concept relation, interpretation, and Buchanan claims remain blocked until later evidence phases.'
        )
      END,
    metadata = COALESCE(metadata, '{}'::jsonb) || jsonb_build_object(
      'bdp_001k_phase', 'BDP-001K',
      'bdp_001k_pdf_availability_reviewed', true,
      'pdf_access_status', 'user_provided_pdf_available',
      'pdf_file_name_observed', '7daa2f5c56c085aba493f7cdc309cddb.pdf',
      'pdf_page_count_observed', 19,
      'pdf_title_match', true,
      'pdf_author_match', true,
      'pdf_journal_metadata_match', true,
      'source_text_available_for_review', true,
      'canonical_metadata_adoption_readiness', 'ready_for_metadata_adoption_only',
      'canonical_metadata_adoption_recommendation', 'ready',
      'canonical_adoption_blocked_until_bdp_001l', true,
      'passage_ingestion_ready', false,
      'citation_insertion_ready', false,
      'interpretation_ready', false,
      'buchanan_claim_ready', false,
      'rights_status_review', 'user_provided_pdf_reference_only_short_quotation_later',
      'display_rule_review', 'metadata_reference_only_in_bdp_001k',
      'bdp_001k_boundary', jsonb_build_object(
        'creates_source_candidate', false,
        'creates_canonical_source', false,
        'creates_passage', false,
        'creates_citation', false,
        'creates_concept_mention', false,
        'creates_concept_relation', false,
        'creates_interpretation', false,
        'creates_buchanan_claim', false
      ),
      'next_step', 'BDP-001L — Adopt reviewed Buchanan source metadata into canonical sources only.'
    )
  WHERE id = v_candidate_id;

  INSERT INTO schema_migrations (
    id,
    phase,
    description
  ) VALUES (
    'bdp_001k_review_buchanan_pdf_source_adoption_readiness',
    'BDP-001K',
    'Review exact Buchanan source candidate and uploaded PDF availability for metadata-only canonical adoption readiness'
  );
END $$;

COMMIT;
