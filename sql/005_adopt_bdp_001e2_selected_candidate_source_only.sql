BEGIN;

DO $$
DECLARE
    v_candidate_id uuid;
    v_source_id uuid;
BEGIN
    SELECT id
    INTO v_candidate_id
    FROM source_candidates
    WHERE title = 'A Thousand Plateaus: Capitalism and Schizophrenia'
      AND metadata->>'first_adoption_candidate_selected' = 'true'
      AND metadata->>'selection_lock' = 'true'
      AND metadata->>'selection_lock_phase' = 'BDP-001E.1'
    LIMIT 1;

    IF v_candidate_id IS NULL THEN
        RAISE EXCEPTION 'BDP-001E.2 blocked: selected BDP-001E.1 candidate not found.';
    END IF;

    SELECT id
    INTO v_source_id
    FROM sources
    WHERE title = 'A Thousand Plateaus: Capitalism and Schizophrenia'
    LIMIT 1;

    IF v_source_id IS NULL THEN
        INSERT INTO sources (
            id,
            title,
            author,
            type,
            year,
            publisher,
            url_or_reference,
            rights_status,
            reliability_level,
            status
        )
        VALUES (
            gen_random_uuid(),
            'A Thousand Plateaus: Capitalism and Schizophrenia',
            'Gilles Deleuze and Félix Guattari; translated by Brian Massumi',
            'book',
            1987,
            'University of Minnesota Press',
            'University of Minnesota Press English translation; ISBN 9780816614028.',
            'fair_use_reference_only',
            'high',
            'canonical'
        )
        RETURNING id INTO v_source_id;
    END IF;

    UPDATE source_candidates
    SET
        status = 'approved',
        review_notes = review_notes || ' BDP-001E.2: adopted into canonical sources only. No passages, citations, or interpretations were created.',
        metadata = metadata || jsonb_build_object(
            'phase_latest', 'BDP-001E.2',
            'source_adoption_created', true,
            'canonical_source_id', v_source_id::text,
            'candidate_record_is_canonical', false,
            'passage_inserted', false,
            'citation_inserted', false,
            'interpretation_created', false,
            'adoption_scope', 'canonical_source_only'
        )
    WHERE id = v_candidate_id;
END
$$;

INSERT INTO schema_migrations (id, phase, description)
SELECT
    '005_adopt_bdp_001e2_selected_candidate_source_only',
    'BDP-001E.2',
    'Adopted selected A Thousand Plateaus candidate into canonical sources only; no passages, citations, or interpretations inserted.'
WHERE NOT EXISTS (
    SELECT 1
    FROM schema_migrations
    WHERE id = '005_adopt_bdp_001e2_selected_candidate_source_only'
);

COMMIT;
