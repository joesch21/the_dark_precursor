-- BDP-001L — Adopt reviewed Buchanan source metadata into canonical sources only
--
-- Boundary:
-- - Inserts one canonical source metadata record only.
-- - Preserves the reviewed source candidate as approved/adopted review history.
-- - Preserves uploaded PDF availability as metadata only.
-- - Does not insert passages, citations, concept mentions, concept relations,
--   interpretations, generated synthesis, or Buchanan-specific claims.

BEGIN;

ALTER TABLE sources
  ADD COLUMN IF NOT EXISTS metadata JSONB NOT NULL DEFAULT '{}'::jsonb;

DO $$
DECLARE
  v_candidate RECORD;
  v_source_exists INTEGER;
  v_cols TEXT[];
  v_vals TEXT[];
  v_sql TEXT;
  v_metadata JSONB;
BEGIN
  SELECT *
    INTO v_candidate
    FROM source_candidates
   WHERE author = 'Ian Buchanan'
     AND (
          title ILIKE '%Problem of the Body%'
       OR COALESCE(url, '') ILIKE '%10.1177/1357034X97003003004%'
       OR COALESCE(metadata::text, '') ILIKE '%10.1177/1357034X97003003004%'
     )
   ORDER BY created_at DESC NULLS LAST
   LIMIT 1;

  IF NOT FOUND THEN
    RAISE EXCEPTION 'BDP-001L expected the reviewed Ian Buchanan source candidate to exist.';
  END IF;

  IF NOT (
       COALESCE(v_candidate.metadata::text, '') ILIKE '%ready_for_metadata_adoption_only%'
    OR COALESCE(v_candidate.metadata::text, '') ILIKE '%canonical_metadata_adoption_recommendation%'
    OR COALESCE(v_candidate.metadata::text, '') ILIKE '%BDP-001K%'
  ) THEN
    RAISE EXCEPTION 'BDP-001L expected BDP-001K metadata-only readiness on the Buchanan source candidate.';
  END IF;

  v_metadata := jsonb_build_object(
    'doi', '10.1177/1357034X97003003004',
    'journal', 'Body & Society',
    'volume', '3',
    'issue', '3',
    'pages', '73-91',
    'publication_date', 'September 1997',
    'publication_year', 1997,
    'publisher', 'SAGE Publications',
    'url_or_reference', 'https://doi.org/10.1177/1357034X97003003004',
    'rights_status', 'restricted',
    'rights_status_basis', 'user_provided_pdf_available_but_reference_only',
    'display_rule', 'reference_only',
    'pdf_access_status', 'user_provided_pdf_available',
    'source_text_available_for_review', true,
    'canonical_metadata_adoption_readiness', 'ready_for_metadata_adoption_only',
    'canonical_metadata_adoption_recommendation', 'ready',
    'adopted_from_phases', jsonb_build_array('BDP-001J', 'BDP-001K'),
    'adopted_from_candidate_id', v_candidate.id::text,
    'passage_ingestion_ready', false,
    'citation_insertion_ready', false,
    'concept_mention_ready', false,
    'concept_relation_ready', false,
    'interpretation_ready', false,
    'buchanan_claim_ready', false,
    'bdp_phase', 'BDP-001L'
  );

  SELECT COUNT(*)
    INTO v_source_exists
    FROM sources
   WHERE author = 'Ian Buchanan'
     AND (
          title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
       OR COALESCE(metadata->>'doi', '') = '10.1177/1357034X97003003004'
       OR COALESCE(url_or_reference, '') = 'https://doi.org/10.1177/1357034X97003003004'
     );

  IF v_source_exists = 0 THEN
    v_cols := ARRAY['title', 'author', 'type'];
    v_vals := ARRAY[
      quote_literal('The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'),
      quote_literal('Ian Buchanan'),
      quote_literal('article')
    ];

    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'sources' AND column_name = 'year') THEN
      v_cols := array_append(v_cols, 'year');
      v_vals := array_append(v_vals, '1997');
    ELSIF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'sources' AND column_name = 'publication_year') THEN
      v_cols := array_append(v_cols, 'publication_year');
      v_vals := array_append(v_vals, '1997');
    END IF;

    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'sources' AND column_name = 'journal') THEN
      v_cols := array_append(v_cols, 'journal');
      v_vals := array_append(v_vals, quote_literal('Body & Society'));
    END IF;

    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'sources' AND column_name = 'volume') THEN
      v_cols := array_append(v_cols, 'volume');
      v_vals := array_append(v_vals, quote_literal('3'));
    END IF;

    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'sources' AND column_name = 'issue') THEN
      v_cols := array_append(v_cols, 'issue');
      v_vals := array_append(v_vals, quote_literal('3'));
    END IF;

    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'sources' AND column_name = 'pages') THEN
      v_cols := array_append(v_cols, 'pages');
      v_vals := array_append(v_vals, quote_literal('73-91'));
    END IF;

    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'sources' AND column_name = 'doi') THEN
      v_cols := array_append(v_cols, 'doi');
      v_vals := array_append(v_vals, quote_literal('10.1177/1357034X97003003004'));
    END IF;

    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'sources' AND column_name = 'publisher') THEN
      v_cols := array_append(v_cols, 'publisher');
      v_vals := array_append(v_vals, quote_literal('SAGE Publications'));
    END IF;

    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'sources' AND column_name = 'url_or_reference') THEN
      v_cols := array_append(v_cols, 'url_or_reference');
      v_vals := array_append(v_vals, quote_literal('https://doi.org/10.1177/1357034X97003003004'));
    END IF;

    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'sources' AND column_name = 'rights_status') THEN
      v_cols := array_append(v_cols, 'rights_status');
      v_vals := array_append(v_vals, quote_literal('restricted'));
    END IF;

    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'sources' AND column_name = 'reliability_level') THEN
      v_cols := array_append(v_cols, 'reliability_level');
      v_vals := array_append(v_vals, quote_literal('high'));
    END IF;

    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'sources' AND column_name = 'status') THEN
      v_cols := array_append(v_cols, 'status');
      v_vals := array_append(v_vals, quote_literal('canonical'));
    END IF;

    v_cols := array_append(v_cols, 'metadata');
    v_vals := array_append(v_vals, quote_literal(v_metadata::text) || '::jsonb');

    SELECT format(
      'INSERT INTO sources (%s) VALUES (%s);',
      array_to_string(ARRAY(SELECT quote_ident(c) FROM unnest(v_cols) AS c), ', '),
      array_to_string(v_vals, ', ')
    )
    INTO v_sql;

    EXECUTE v_sql;
  END IF;

  UPDATE source_candidates
     SET status = 'approved',
         review_notes = CASE
           WHEN COALESCE(review_notes, '') ILIKE '%BDP-001L canonical metadata adoption%'
             THEN review_notes
           ELSE CONCAT_WS(E'\n', review_notes, 'BDP-001L canonical metadata adoption: adopted into sources as metadata only; candidate preserved as review history.')
         END,
         metadata = COALESCE(metadata, '{}'::jsonb) || jsonb_build_object(
           'status_before_bdp_001l', COALESCE(v_candidate.status, 'unknown'),
           'candidate_history_status', 'approved_adopted_metadata_history',
           'canonical_metadata_adoption_status', 'adopted_metadata_only',
           'canonical_source_status', 'canonical',
           'canonical_source_title', 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?',
           'canonical_source_author', 'Ian Buchanan',
           'canonical_source_type', 'article',
           'doi', '10.1177/1357034X97003003004',
           'adopted_from_phases', jsonb_build_array('BDP-001J', 'BDP-001K'),
           'pdf_access_status', 'user_provided_pdf_available',
           'display_rule', 'reference_only',
           'passage_ingestion_ready', false,
           'citation_insertion_ready', false,
           'concept_mention_ready', false,
           'concept_relation_ready', false,
           'interpretation_ready', false,
           'buchanan_claim_ready', false,
           'bdp_phase', 'BDP-001L'
         )
   WHERE id = v_candidate.id;
END $$;

INSERT INTO schema_migrations (id, phase, description)
VALUES (
  '012_adopt_bdp_001l_buchanan_source_metadata_only',
  'BDP-001L',
  'Adopt reviewed Ian Buchanan article metadata into canonical sources only; preserve source candidate as approved review history; no passage/citation/interpretation insertion.'
)
ON CONFLICT (id) DO NOTHING;

DO $$
DECLARE
  v_sources_count INTEGER;
  v_source_candidates_count INTEGER;
  v_passages_count INTEGER;
  v_citations_count INTEGER;
  v_concept_mentions_count INTEGER;
  v_concept_relations_count INTEGER;
  v_interpretations_count INTEGER;
  v_migration_count INTEGER;
  v_buchanan_source_passages INTEGER;
  v_buchanan_source_citations INTEGER;
BEGIN
  SELECT COUNT(*) INTO v_sources_count FROM sources;
  SELECT COUNT(*) INTO v_source_candidates_count FROM source_candidates;
  SELECT COUNT(*) INTO v_passages_count FROM passages;
  SELECT COUNT(*) INTO v_citations_count FROM citations;
  SELECT COUNT(*) INTO v_concept_mentions_count FROM concept_mentions;
  SELECT COUNT(*) INTO v_concept_relations_count FROM concept_relations;
  SELECT COUNT(*) INTO v_interpretations_count FROM interpretations;
  SELECT COUNT(*) INTO v_migration_count FROM schema_migrations WHERE phase = 'BDP-001L';

  SELECT COUNT(*)
    INTO v_buchanan_source_passages
    FROM passages p
    JOIN sources s ON p.source_id = s.id
   WHERE s.author = 'Ian Buchanan'
     AND COALESCE(s.metadata->>'doi', '') = '10.1177/1357034X97003003004';

  SELECT COUNT(*)
    INTO v_buchanan_source_citations
    FROM citations c
    JOIN sources s ON c.source_id = s.id
   WHERE s.author = 'Ian Buchanan'
     AND COALESCE(s.metadata->>'doi', '') = '10.1177/1357034X97003003004';

  IF v_sources_count <> 2 THEN
    RAISE EXCEPTION 'BDP-001L expected sources_count = 2, got %', v_sources_count;
  END IF;
  IF v_source_candidates_count <> 3 THEN
    RAISE EXCEPTION 'BDP-001L expected source_candidates_count = 3, got %', v_source_candidates_count;
  END IF;
  IF v_passages_count <> 1 THEN
    RAISE EXCEPTION 'BDP-001L expected passages_count = 1, got %', v_passages_count;
  END IF;
  IF v_citations_count <> 1 THEN
    RAISE EXCEPTION 'BDP-001L expected citations_count = 1, got %', v_citations_count;
  END IF;
  IF v_concept_mentions_count <> 1 THEN
    RAISE EXCEPTION 'BDP-001L expected concept_mentions_count = 1, got %', v_concept_mentions_count;
  END IF;
  IF v_concept_relations_count <> 0 THEN
    RAISE EXCEPTION 'BDP-001L expected concept_relations_count = 0, got %', v_concept_relations_count;
  END IF;
  IF v_interpretations_count <> 0 THEN
    RAISE EXCEPTION 'BDP-001L expected interpretations_count = 0, got %', v_interpretations_count;
  END IF;
  IF v_migration_count <> 1 THEN
    RAISE EXCEPTION 'BDP-001L expected migration_count = 1, got %', v_migration_count;
  END IF;
  IF v_buchanan_source_passages <> 0 THEN
    RAISE EXCEPTION 'BDP-001L must not attach passages to the adopted Buchanan article; got %', v_buchanan_source_passages;
  END IF;
  IF v_buchanan_source_citations <> 0 THEN
    RAISE EXCEPTION 'BDP-001L must not attach citations to the adopted Buchanan article; got %', v_buchanan_source_citations;
  END IF;
END $$;

COMMIT;
