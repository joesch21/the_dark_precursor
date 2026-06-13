BEGIN;

DO $$
DECLARE
    v_source_id uuid;
    v_passage_id uuid;
BEGIN
    SELECT id
    INTO v_source_id
    FROM sources
    WHERE title = 'A Thousand Plateaus: Capitalism and Schizophrenia'
      AND status = 'canonical'
    LIMIT 1;

    IF v_source_id IS NULL THEN
        RAISE EXCEPTION 'BDP-001E.4 blocked: canonical A Thousand Plateaus source not found.';
    END IF;

    SELECT id
    INTO v_passage_id
    FROM passages
    WHERE source_id = v_source_id
      AND page_or_timestamp = 'p. 150'
      AND chapter_or_section = 'Plateau 6: How Do You Make Yourself a Body without Organs?'
    LIMIT 1;

    IF v_passage_id IS NULL THEN
        RAISE EXCEPTION 'BDP-001E.4 blocked: first cited passage not found.';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM citations
        WHERE source_id = v_source_id
          AND passage_id = v_passage_id
          AND interpretation_id IS NULL
          AND citation_format = 'short_note'
    ) THEN
        INSERT INTO citations (
            id,
            source_id,
            passage_id,
            interpretation_id,
            citation_text,
            citation_format,
            locator,
            page_or_timestamp,
            chapter_or_section,
            url_or_reference,
            rights_status,
            display_rule,
            metadata
        )
        VALUES (
            gen_random_uuid(),
            v_source_id,
            v_passage_id,
            NULL,
            'Deleuze and Guattari, A Thousand Plateaus: Capitalism and Schizophrenia, trans. Brian Massumi, University of Minnesota Press, 1987, p. 150.',
            'short_note',
            'p. 150',
            'p. 150',
            'Plateau 6: How Do You Make Yourself a Body without Organs?',
            'University of Minnesota Press English translation; ISBN 9780816614028.',
            'fair_use_reference_only',
            'reference_only',
            jsonb_build_object(
                'phase', 'BDP-001E.4',
                'source_id', v_source_id::text,
                'passage_id', v_passage_id::text,
                'citation_record_inserted', true,
                'interpretation_created', false,
                'rights_boundary', 'citation record only; no interpretation inserted'
            )
        );
    END IF;

    UPDATE source_candidates
    SET metadata = metadata || jsonb_build_object(
        'phase_latest', 'BDP-001E.4',
        'citation_inserted', true,
        'interpretation_created', false,
        'first_citation_scope', 'citation record only',
        'first_citation_display_rule', 'reference_only'
    )
    WHERE title = 'A Thousand Plateaus: Capitalism and Schizophrenia';
END
$$;

INSERT INTO schema_migrations (id, phase, description)
SELECT
    '007_add_bdp_001e4_first_passage_citation_only',
    'BDP-001E.4',
    'Added one citation record for the first cited passage only; no interpretation inserted.'
WHERE NOT EXISTS (
    SELECT 1
    FROM schema_migrations
    WHERE id = '007_add_bdp_001e4_first_passage_citation_only'
);

COMMIT;
