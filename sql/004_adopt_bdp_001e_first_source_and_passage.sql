BEGIN;

DO $$
DECLARE
    v_source_id uuid;
    v_passage_id uuid;
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM source_candidates
        WHERE title = 'A Thousand Plateaus: Capitalism and Schizophrenia'
    ) THEN
        RAISE EXCEPTION 'Required source candidate missing: A Thousand Plateaus';
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
            'ISBN 9780816614028; University of Minnesota Press edition, published December 21, 1987.',
            'fair_use_reference_only',
            'primary_text',
            'canonical'
        )
        RETURNING id INTO v_source_id;
    END IF;

    SELECT id
    INTO v_passage_id
    FROM passages
    WHERE source_id = v_source_id
      AND page_or_timestamp = 'p. 150'
      AND chapter_or_section = 'Plateau 6: How Do You Make Yourself a Body without Organs?'
    LIMIT 1;

    IF v_passage_id IS NULL THEN
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
            'Deleuze and Guattari, A Thousand Plateaus: Capitalism and Schizophrenia, trans. Brian Massumi (Minneapolis: University of Minnesota Press, 1987), p. 150.'
        )
        RETURNING id INTO v_passage_id;
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM citations
        WHERE source_id = v_source_id
          AND passage_id = v_passage_id
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
            'Deleuze and Guattari, A Thousand Plateaus: Capitalism and Schizophrenia, trans. Brian Massumi (Minneapolis: University of Minnesota Press, 1987), p. 150.',
            'short_note',
            'p. 150',
            'p. 150',
            'Plateau 6: How Do You Make Yourself a Body without Organs?',
            'ISBN 9780816614028; University of Minnesota Press edition.',
            'fair_use_reference_only',
            'short_quote_plus_citation_only',
            jsonb_build_object(
                'phase', 'BDP-001E',
                'source_adoption', true,
                'passage_inserted', true,
                'interpretation_created', false,
                'rights_boundary', 'short quotation only; citation required; no long passage display'
            )
        );
    END IF;

    UPDATE source_candidates
    SET
        status = 'approved',
        review_notes = 'Adopted into canonical sources in BDP-001E as the first reviewed primary-text source. Candidate record remains staging history and is not itself canonical. One short cited passage was inserted; no interpretation was created.',
        metadata = metadata || jsonb_build_object(
            'phase_latest', 'BDP-001E',
            'candidate_status', 'approved',
            'adopted_to_canonical_source', true,
            'candidate_record_is_canonical', false,
            'canonical_source_id', v_source_id::text,
            'first_passage_id', v_passage_id::text,
            'interpretations_authorized', false,
            'operator_adoption_decision', 'approved_for_first_canonical_source',
            'adoption_note', 'Adoption creates a canonical source record and one cited passage only. It does not create interpretive authority.'
        )
    WHERE title = 'A Thousand Plateaus: Capitalism and Schizophrenia';
END
$$;

INSERT INTO schema_migrations (id, phase, description)
SELECT
    '004_adopt_bdp_001e_first_source_and_passage',
    'BDP-001E',
    'Adopted A Thousand Plateaus as first canonical source and inserted one short cited passage without creating interpretations.'
WHERE NOT EXISTS (
    SELECT 1
    FROM schema_migrations
    WHERE id = '004_adopt_bdp_001e_first_source_and_passage'
);

COMMIT;
