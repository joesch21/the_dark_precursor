BEGIN;

DO $$
DECLARE
    v_source_id uuid;
    v_existing_passage_id uuid;
BEGIN
    SELECT id
    INTO v_source_id
    FROM sources
    WHERE title = 'A Thousand Plateaus: Capitalism and Schizophrenia'
      AND status = 'canonical'
    LIMIT 1;

    IF v_source_id IS NULL THEN
        RAISE EXCEPTION 'BDP-001E.3 blocked: canonical A Thousand Plateaus source not found.';
    END IF;

    SELECT id
    INTO v_existing_passage_id
    FROM passages
    WHERE source_id = v_source_id
      AND page_or_timestamp = 'p. 150'
      AND chapter_or_section = 'Plateau 6: How Do You Make Yourself a Body without Organs?'
    LIMIT 1;

    IF v_existing_passage_id IS NULL THEN
        INSERT INTO passages (
            id,
            source_id,
            text,
            page_or_timestamp,
            chapter_or_section,
            citation
        )
        VALUES (
            gen_random_uuid(),
            v_source_id,
            'You never reach the Body without Organs; you can''t reach it, you are forever attaining it, it is a limit.',
            'p. 150',
            'Plateau 6: How Do You Make Yourself a Body without Organs?',
            'Deleuze and Guattari, A Thousand Plateaus: Capitalism and Schizophrenia, trans. Brian Massumi, University of Minnesota Press, 1987, p. 150.'
        );
    END IF;

    UPDATE source_candidates
    SET metadata = metadata || jsonb_build_object(
        'phase_latest', 'BDP-001E.3',
        'passage_inserted', true,
        'citation_inserted', false,
        'interpretation_created', false,
        'first_passage_locator', 'p. 150',
        'first_passage_scope', 'short cited passage only'
    )
    WHERE title = 'A Thousand Plateaus: Capitalism and Schizophrenia';
END
$$;

INSERT INTO schema_migrations (id, phase, description)
SELECT
    '006_insert_bdp_001e3_first_cited_passage_only',
    'BDP-001E.3',
    'Inserted one short cited passage from the adopted A Thousand Plateaus source only; no citation-table row or interpretation inserted.'
WHERE NOT EXISTS (
    SELECT 1
    FROM schema_migrations
    WHERE id = '006_insert_bdp_001e3_first_cited_passage_only'
);

COMMIT;
