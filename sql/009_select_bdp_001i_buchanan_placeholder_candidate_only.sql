-- BDP-001I — Select first Buchanan source candidate for Body without Organs
-- Boundary: selection-only metadata update. No source adoption, passages, citations, concept mentions, relations, or interpretations.

BEGIN;

DO $$
DECLARE
  v_candidate_id UUID;
  v_match_count INTEGER;
BEGIN
  IF EXISTS (SELECT 1 FROM schema_migrations WHERE phase = 'BDP-001I') THEN
    RAISE EXCEPTION 'BDP-001I migration already recorded';
  END IF;

  SELECT COUNT(*)
    INTO v_match_count
  FROM source_candidates
  WHERE title = 'Ian Buchanan Body without Organs source candidate'
    AND author = 'Ian Buchanan'
    AND status = 'candidate';

  IF v_match_count != 1 THEN
    RAISE EXCEPTION 'BDP-001I requires exactly one Ian Buchanan placeholder candidate; found %', v_match_count;
  END IF;

  SELECT id
    INTO v_candidate_id
  FROM source_candidates
  WHERE title = 'Ian Buchanan Body without Organs source candidate'
    AND author = 'Ian Buchanan'
    AND status = 'candidate'
  LIMIT 1;

  UPDATE source_candidates
  SET
    metadata = COALESCE(metadata, '{}'::jsonb) || jsonb_build_object(
      'bdp_phase', 'BDP-001I',
      'bdp_001i_selected_for_review', true,
      'selection_status', 'placeholder_candidate_selected_only',
      'selection_boundary', 'selection_only_no_canonical_adoption',
      'exact_source_required', true,
      'canonical_adoption_blocked', true,
      'canonical_adoption_blocker', 'Exact Buchanan publication, lecture, transcript, interview, or teaching source has not yet been specified.',
      'candidate_status_after_selection', 'candidate',
      'intended_concept_link', 'Body without Organs',
      'next_phase', 'BDP-001J — Specify exact Buchanan source for Body without Organs candidate review'
    ),
    review_notes = review_notes || ' BDP-001I: selected as placeholder candidate only for exact Buchanan source resolution. Canonical adoption is hard-blocked until an exact Buchanan publication, lecture, transcript, interview, or teaching source is specified.'
  WHERE id = v_candidate_id;

  INSERT INTO schema_migrations (
    id,
    phase,
    description
  ) VALUES (
    'bdp_001i_select_buchanan_placeholder_candidate_only',
    'BDP-001I',
    'Select Ian Buchanan Body without Organs placeholder candidate only and block canonical adoption until exact source is specified'
  );
END $$;

COMMIT;
