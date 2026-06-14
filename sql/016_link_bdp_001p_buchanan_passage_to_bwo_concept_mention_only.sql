-- BDP-001P — Link inserted Buchanan passage to Body without Organs through one reviewed concept mention only.
--
-- Boundary:
-- - No new source.
-- - No new passage.
-- - No new citation.
-- - No concept relation.
-- - No interpretation.
-- - No generated Buchanan claim.
-- - No frontend work.
--
-- Database mutation:
-- - Insert exactly one concept_mentions row for the existing Buchanan passage.
-- - Insert one schema_migrations ledger row for BDP-001P.

\set ON_ERROR_STOP on

BEGIN;

DO $$
DECLARE
    v_concept_id concepts.id%TYPE;
    v_source_id sources.id%TYPE;
    v_passage_id passages.id%TYPE;
    v_existing_mentions integer;
    v_source_count integer;
    v_passage_count integer;
    v_citation_count integer;
BEGIN
    IF EXISTS (
        SELECT 1
        FROM schema_migrations
        WHERE id = '016_link_bdp_001p_buchanan_passage_to_bwo_concept_mention_only'
           OR phase = 'BDP-001P'
    ) THEN
        RAISE EXCEPTION 'BDP-001P migration already recorded; refusing duplicate concept mention insertion.';
    END IF;

    IF (SELECT COUNT(*) FROM sources) <> 2 THEN
        RAISE EXCEPTION 'BDP-001P preflight failed: expected sources_count = 2.';
    END IF;

    IF (SELECT COUNT(*) FROM source_candidates) <> 3 THEN
        RAISE EXCEPTION 'BDP-001P preflight failed: expected source_candidates_count = 3.';
    END IF;

    IF (SELECT COUNT(*) FROM passage_candidates) <> 1 THEN
        RAISE EXCEPTION 'BDP-001P preflight failed: expected passage_candidates_count = 1.';
    END IF;

    IF (SELECT COUNT(*) FROM passages) <> 2 THEN
        RAISE EXCEPTION 'BDP-001P preflight failed: expected passages_count = 2.';
    END IF;

    IF (SELECT COUNT(*) FROM citations) <> 2 THEN
        RAISE EXCEPTION 'BDP-001P preflight failed: expected citations_count = 2.';
    END IF;

    IF (SELECT COUNT(*) FROM concept_mentions) <> 1 THEN
        RAISE EXCEPTION 'BDP-001P preflight failed: expected concept_mentions_count = 1 before insertion.';
    END IF;

    IF (SELECT COUNT(*) FROM concept_relations) <> 0 THEN
        RAISE EXCEPTION 'BDP-001P preflight failed: expected concept_relations_count = 0.';
    END IF;

    IF (SELECT COUNT(*) FROM interpretations) <> 0 THEN
        RAISE EXCEPTION 'BDP-001P preflight failed: expected interpretations_count = 0.';
    END IF;

    SELECT COUNT(*)
    INTO v_source_count
    FROM sources
    WHERE author = 'Ian Buchanan'
      AND title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
      AND status = 'canonical';

    IF v_source_count <> 1 THEN
        RAISE EXCEPTION 'BDP-001P preflight failed: expected exactly one canonical Buchanan article source, found %.', v_source_count;
    END IF;

    SELECT id
    INTO v_source_id
    FROM sources
    WHERE author = 'Ian Buchanan'
      AND title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
      AND status = 'canonical';

    SELECT COUNT(*)
    INTO v_passage_count
    FROM passages
    WHERE source_id = v_source_id;

    IF v_passage_count <> 1 THEN
        RAISE EXCEPTION 'BDP-001P preflight failed: expected exactly one canonical Buchanan article passage, found %.', v_passage_count;
    END IF;

    SELECT id
    INTO v_passage_id
    FROM passages
    WHERE source_id = v_source_id
    ORDER BY created_at DESC
    LIMIT 1;

    SELECT COUNT(*)
    INTO v_citation_count
    FROM citations
    WHERE source_id = v_source_id
      AND passage_id = v_passage_id;

    IF v_citation_count <> 1 THEN
        RAISE EXCEPTION 'BDP-001P preflight failed: expected exactly one citation for the inserted Buchanan passage, found %.', v_citation_count;
    END IF;

    SELECT id
    INTO v_concept_id
    FROM concepts
    WHERE name = 'Body without Organs';

    IF v_concept_id IS NULL THEN
        RAISE EXCEPTION 'BDP-001P preflight failed: Body without Organs concept not found.';
    END IF;

    SELECT COUNT(*)
    INTO v_existing_mentions
    FROM concept_mentions
    WHERE concept_id = v_concept_id
      AND passage_id = v_passage_id;

    IF v_existing_mentions <> 0 THEN
        RAISE EXCEPTION 'BDP-001P preflight failed: Buchanan passage is already linked to Body without Organs.';
    END IF;

    INSERT INTO concept_mentions (
        concept_id,
        passage_id,
        confidence,
        mention_type,
        reviewed_status,
        created_at
    )
    VALUES (
        v_concept_id,
        v_passage_id,
        1.0,
        'direct',
        'accepted',
        now()
    );
END $$;

INSERT INTO schema_migrations (id, phase, description)
VALUES (
    '016_link_bdp_001p_buchanan_passage_to_bwo_concept_mention_only',
    'BDP-001P',
    'Link the inserted citation-backed Buchanan passage to Body without Organs through one reviewed direct concept mention only.'
);

DO $$
BEGIN
    IF (SELECT COUNT(*) FROM sources) <> 2 THEN
        RAISE EXCEPTION 'BDP-001P postflight failed: sources_count changed.';
    END IF;

    IF (SELECT COUNT(*) FROM source_candidates) <> 3 THEN
        RAISE EXCEPTION 'BDP-001P postflight failed: source_candidates_count changed.';
    END IF;

    IF (SELECT COUNT(*) FROM passage_candidates) <> 1 THEN
        RAISE EXCEPTION 'BDP-001P postflight failed: passage_candidates_count changed.';
    END IF;

    IF (SELECT COUNT(*) FROM passages) <> 2 THEN
        RAISE EXCEPTION 'BDP-001P postflight failed: passages_count changed.';
    END IF;

    IF (SELECT COUNT(*) FROM citations) <> 2 THEN
        RAISE EXCEPTION 'BDP-001P postflight failed: citations_count changed.';
    END IF;

    IF (SELECT COUNT(*) FROM concept_mentions) <> 2 THEN
        RAISE EXCEPTION 'BDP-001P postflight failed: expected concept_mentions_count = 2.';
    END IF;

    IF (SELECT COUNT(*) FROM concept_relations) <> 0 THEN
        RAISE EXCEPTION 'BDP-001P postflight failed: concept_relations_count changed.';
    END IF;

    IF (SELECT COUNT(*) FROM interpretations) <> 0 THEN
        RAISE EXCEPTION 'BDP-001P postflight failed: interpretations_count changed.';
    END IF;
END $$;

COMMIT;
