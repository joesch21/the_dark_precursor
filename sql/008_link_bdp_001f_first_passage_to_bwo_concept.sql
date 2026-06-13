-- BDP-001F — Link first cited passage to Body without Organs concept mention
-- Boundary: concept mention only. No sources, passages, citations, interpretations, or concept relations are inserted.

BEGIN;

DO $$
DECLARE
  v_source_id UUID;
  v_passage_id UUID;
  v_concept_id UUID;
BEGIN
  IF EXISTS (SELECT 1 FROM schema_migrations WHERE phase = 'BDP-001F') THEN
    RAISE EXCEPTION 'BDP-001F migration already recorded';
  END IF;

  SELECT id
    INTO v_source_id
  FROM sources
  WHERE title = 'A Thousand Plateaus: Capitalism and Schizophrenia'
    AND status = 'canonical'
    AND rights_status = 'fair_use_reference_only'
    AND reliability_level = 'high'
  LIMIT 1;

  IF v_source_id IS NULL THEN
    RAISE EXCEPTION 'BDP-001F requires the canonical A Thousand Plateaus source';
  END IF;

  SELECT id
    INTO v_concept_id
  FROM concepts
  WHERE name = 'Body without Organs'
  LIMIT 1;

  IF v_concept_id IS NULL THEN
    RAISE EXCEPTION 'BDP-001F requires the Body without Organs concept';
  END IF;

  SELECT p.id
    INTO v_passage_id
  FROM passages p
  WHERE p.source_id = v_source_id
    AND (
      p.page_or_timestamp ILIKE '%150%'
      OR p.citation ILIKE '%150%'
      OR p.chapter_or_section ILIKE '%Body without Organs%'
    )
  ORDER BY p.created_at ASC
  LIMIT 1;

  IF v_passage_id IS NULL THEN
    RAISE EXCEPTION 'BDP-001F requires the first cited passage from p. 150 / Body without Organs section';
  END IF;

  IF EXISTS (
    SELECT 1
    FROM concept_mentions
    WHERE concept_id = v_concept_id
      AND passage_id = v_passage_id
  ) THEN
    RAISE EXCEPTION 'BDP-001F concept mention already exists for Body without Organs and first passage';
  END IF;

  INSERT INTO concept_mentions (
    concept_id,
    passage_id,
    confidence,
    mention_type,
    reviewed_status,
    created_at
  ) VALUES (
    v_concept_id,
    v_passage_id,
    1.0,
    'direct',
    'accepted',
    NOW()
  );

  INSERT INTO schema_migrations (
    id,
    phase,
    description
  ) VALUES (
    'bdp_001f_first_passage_concept_mention',
    'BDP-001F',
    'Link first cited passage to Body without Organs concept mention'
  );
END $$;

COMMIT;
