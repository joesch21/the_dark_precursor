-- BDP-001O — Insert reviewed Buchanan passage and citation only.
--
-- Boundary:
-- 1. Insert exactly one canonical Buchanan passage from the reviewed BDP-001N passage candidate.
-- 2. Insert exactly one citation linked to that passage.
-- 3. Do not insert concept_mentions, concept_relations, interpretations, or generated claims.

BEGIN;

DO $$
DECLARE
    v_candidate_count integer;
    v_existing_buchanan_passage_count integer;
    v_candidate_id passage_candidates.id%TYPE;
    v_source_id sources.id%TYPE;
    v_candidate_text text;
    v_page_or_timestamp text;
    v_chapter_or_section text;
    v_url_or_reference text;
    v_passage_id passages.id%TYPE;
    v_citation_text text;
BEGIN
    IF EXISTS (
        SELECT 1
        FROM schema_migrations
        WHERE id = 'bdp_001o_insert_buchanan_passage_and_citation_only'
    ) THEN
        RAISE NOTICE 'BDP-001O already applied; skipping.';
        RETURN;
    END IF;

    SELECT count(*)
    INTO v_candidate_count
    FROM passage_candidates pc
    JOIN sources s ON s.id = pc.source_id
    JOIN concepts c ON c.id = pc.concept_id
    WHERE s.author = 'Ian Buchanan'
      AND s.title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
      AND s.status = 'canonical'
      AND c.name = 'Body without Organs'
      AND pc.candidate_text_status = 'reviewed_short_excerpt'
      AND pc.locator_status = 'reviewed'
      AND pc.review_status = 'approved'
      AND pc.citation_ready = true
      AND pc.inserted_as_passage = false
      AND pc.concept_mention_ready = false
      AND pc.interpretation_ready = false
      AND pc.buchanan_claim_ready = false;

    IF v_candidate_count <> 1 THEN
        RAISE EXCEPTION 'BDP-001O expected exactly one reviewed, citation-ready Buchanan passage candidate, found %', v_candidate_count;
    END IF;

    SELECT pc.id,
           pc.source_id,
           pc.candidate_text,
           pc.page_or_timestamp,
           pc.chapter_or_section,
           s.url_or_reference
    INTO v_candidate_id,
         v_source_id,
         v_candidate_text,
         v_page_or_timestamp,
         v_chapter_or_section,
         v_url_or_reference
    FROM passage_candidates pc
    JOIN sources s ON s.id = pc.source_id
    JOIN concepts c ON c.id = pc.concept_id
    WHERE s.author = 'Ian Buchanan'
      AND s.title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
      AND s.status = 'canonical'
      AND c.name = 'Body without Organs'
      AND pc.candidate_text_status = 'reviewed_short_excerpt'
      AND pc.locator_status = 'reviewed'
      AND pc.review_status = 'approved'
      AND pc.citation_ready = true
      AND pc.inserted_as_passage = false
      AND pc.concept_mention_ready = false
      AND pc.interpretation_ready = false
      AND pc.buchanan_claim_ready = false;

    IF v_candidate_text IS NULL OR length(trim(v_candidate_text)) = 0 THEN
        RAISE EXCEPTION 'BDP-001O candidate text is empty; refusing passage insertion.';
    END IF;

    IF char_length(v_candidate_text) > 600 THEN
        RAISE EXCEPTION 'BDP-001O candidate excerpt is longer than the short-excerpt boundary (% characters).', char_length(v_candidate_text);
    END IF;

    SELECT count(*)
    INTO v_existing_buchanan_passage_count
    FROM passages p
    WHERE p.source_id = v_source_id;

    IF v_existing_buchanan_passage_count <> 0 THEN
        RAISE EXCEPTION 'BDP-001O expected zero existing Buchanan article passages before insertion, found %', v_existing_buchanan_passage_count;
    END IF;

    v_citation_text := 'Ian Buchanan, "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?", Body & Society 3, no. 3 (1997): 73-91; ' || v_page_or_timestamp || '.';

    INSERT INTO passages (
        source_id,
        text,
        page_or_timestamp,
        chapter_or_section,
        citation
    )
    VALUES (
        v_source_id,
        v_candidate_text,
        v_page_or_timestamp,
        v_chapter_or_section,
        v_citation_text
    )
    RETURNING id INTO v_passage_id;

    INSERT INTO citations (
        source_id,
        passage_id,
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
        v_source_id,
        v_passage_id,
        v_citation_text,
        'chicago_reference_only',
        v_page_or_timestamp,
        v_page_or_timestamp,
        v_chapter_or_section,
        v_url_or_reference,
        'restricted',
        'reference_only',
        jsonb_build_object(
            'display_rule_detail', 'reference_only_short_excerpt',
            'bdp_phase', 'BDP-001O',
            'source_treatment', 'canonical_passage_and_citation_only',
            'candidate_id', v_candidate_id::text,
            'concept_mention_inserted', false,
            'concept_relation_inserted', false,
            'interpretation_inserted', false,
            'buchanan_claim_inserted', false,
            'rights_boundary', 'restricted_reference_only_short_excerpt'
        )
    );

    UPDATE passage_candidates
    SET inserted_as_passage = true,
        metadata = COALESCE(metadata, '{}'::jsonb) || jsonb_build_object(
            'inserted_as_passage_phase', 'BDP-001O',
            'inserted_passage_id', v_passage_id::text,
            'citation_inserted', true,
            'concept_mention_inserted', false,
            'concept_relation_inserted', false,
            'interpretation_inserted', false,
            'buchanan_claim_inserted', false
        )
    WHERE id = v_candidate_id;

    INSERT INTO schema_migrations (id, phase, description)
    VALUES (
        'bdp_001o_insert_buchanan_passage_and_citation_only',
        'BDP-001O',
        'Insert reviewed Buchanan passage and citation only; preserve concept mention, relation, interpretation, and claim boundaries.'
    );
END $$;

COMMIT;
