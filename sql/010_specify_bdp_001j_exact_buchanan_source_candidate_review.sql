-- BDP-001J — Specify exact Buchanan source for Body without Organs candidate review
-- Boundary: metadata refinement only. No canonical source, passage, citation, concept mention, relation, interpretation, or Buchanan claim is created.

BEGIN;

DO $$
DECLARE
  v_candidate_id source_candidates.id%TYPE;
BEGIN
  IF EXISTS (SELECT 1 FROM schema_migrations WHERE phase = 'BDP-001J') THEN
    RAISE EXCEPTION 'BDP-001J migration already recorded';
  END IF;

  SELECT id
    INTO v_candidate_id
  FROM source_candidates
  WHERE title = 'Ian Buchanan Body without Organs source candidate'
    AND author = 'Ian Buchanan'
    AND status = 'candidate'
  LIMIT 1;

  IF v_candidate_id IS NULL THEN
    RAISE EXCEPTION 'BDP-001J requires the Ian Buchanan Body without Organs placeholder candidate to exist and remain candidate-only';
  END IF;

  UPDATE source_candidates
  SET
    url = 'https://doi.org/10.1177/1357034X97003003004',
    review_notes =
      CASE
        WHEN review_notes LIKE '%BDP-001J:%' THEN review_notes
        ELSE CONCAT(
          COALESCE(review_notes, ''),
          ' BDP-001J: exact Buchanan source specified for candidate review: Ian Buchanan, "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?", Body & Society 3(3), September 1997, pp. 73-91, DOI 10.1177/1357034X97003003004. Candidate remains non-canonical; canonical adoption remains blocked until operator review. No passages, citations, concept mentions, relations, interpretations, or Buchanan claims are authorized by this metadata refinement.'
        )
      END,
    metadata = COALESCE(metadata, '{}'::jsonb) || jsonb_build_object(
      'bdp_001j_phase', 'BDP-001J',
      'bdp_001j_exact_source_specified', true,
      'selection_status', 'exact_buchanan_source_specified_for_review',
      'placeholder_candidate_resolved_to_exact_source', true,
      'exact_source_review_status', 'specified_not_reviewed_for_canonical_adoption',
      'canonical_adoption_blocked', true,
      'canonical_adoption_blocker', 'Operator review required after exact source specification; no source adoption may occur in BDP-001J.',
      'passage_authority_blocked', true,
      'interpretation_authority_blocked', true,
      'intended_concept_link', 'Body without Organs',
      'exact_source', jsonb_build_object(
        'title', 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?',
        'author', 'Ian Buchanan',
        'source_type', 'article',
        'journal', 'Body & Society',
        'volume', '3',
        'issue', '3',
        'pages', '73-91',
        'publication_date', 'September 1997',
        'doi', '10.1177/1357034X97003003004',
        'url_or_reference', 'https://doi.org/10.1177/1357034X97003003004',
        'publisher', 'SAGE Publications',
        'rights_status_recommendation', 'restricted',
        'display_rule', 'reference_only',
        'reliability_level_recommendation', 'high',
        'bibliographic_source_confirmation', 'SAGE Journals article record'
      ),
      'bdp_001j_boundary', jsonb_build_object(
        'creates_source_candidate', false,
        'creates_canonical_source', false,
        'creates_passage', false,
        'creates_citation', false,
        'creates_concept_mention', false,
        'creates_concept_relation', false,
        'creates_interpretation', false,
        'creates_buchanan_claim', false
      ),
      'next_step', 'BDP-001K — Review exact Buchanan source candidate for canonical adoption readiness.'
    )
  WHERE id = v_candidate_id;

  INSERT INTO schema_migrations (
    id,
    phase,
    description
  ) VALUES (
    'bdp_001j_specify_exact_buchanan_source_candidate_review',
    'BDP-001J',
    'Specify exact Buchanan source for Body without Organs candidate review without canonical adoption'
  );
END $$;

COMMIT;
