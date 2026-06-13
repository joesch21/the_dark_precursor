BEGIN;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

ALTER TABLE sources
  ADD COLUMN IF NOT EXISTS metadata JSONB NOT NULL DEFAULT '{}'::jsonb;

CREATE TABLE IF NOT EXISTS passage_candidates (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
  concept_id UUID REFERENCES concepts(id) ON DELETE SET NULL,
  candidate_label TEXT NOT NULL,
  candidate_status TEXT NOT NULL DEFAULT 'candidate',
  candidate_scope TEXT NOT NULL DEFAULT 'source_passage_candidate',
  candidate_text TEXT,
  candidate_text_status TEXT NOT NULL DEFAULT 'not_stored_pending_operator_review',
  page_or_timestamp TEXT,
  chapter_or_section TEXT,
  locator_status TEXT NOT NULL DEFAULT 'locator_pending_pdf_review',
  rights_status TEXT NOT NULL DEFAULT 'restricted',
  display_rule TEXT NOT NULL DEFAULT 'reference_only',
  review_status TEXT NOT NULL DEFAULT 'prepared',
  extraction_status TEXT NOT NULL DEFAULT 'not_extracted',
  inserted_as_passage BOOLEAN NOT NULL DEFAULT FALSE,
  citation_ready BOOLEAN NOT NULL DEFAULT FALSE,
  concept_mention_ready BOOLEAN NOT NULL DEFAULT FALSE,
  interpretation_ready BOOLEAN NOT NULL DEFAULT FALSE,
  buchanan_claim_ready BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  reviewed_at TIMESTAMPTZ,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  CONSTRAINT passage_candidates_candidate_status_check CHECK (candidate_status IN ('candidate', 'prepared', 'needs_review', 'approved_for_passage_insertion', 'rejected', 'inserted')),
  CONSTRAINT passage_candidates_review_status_check CHECK (review_status IN ('prepared', 'needs_review', 'approved', 'rejected')),
  CONSTRAINT passage_candidates_display_rule_check CHECK (display_rule IN ('reference_only', 'short_quote_only', 'internal_review_only')),
  CONSTRAINT passage_candidates_unique_source_label UNIQUE (source_id, candidate_label)
);

CREATE INDEX IF NOT EXISTS idx_passage_candidates_source_id ON passage_candidates(source_id);
CREATE INDEX IF NOT EXISTS idx_passage_candidates_concept_id ON passage_candidates(concept_id);
CREATE INDEX IF NOT EXISTS idx_passage_candidates_status ON passage_candidates(candidate_status, review_status);

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
      FROM sources
     WHERE author = 'Ian Buchanan'
       AND title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
       AND status = 'canonical'
       AND COALESCE(metadata->>'doi', '') = '10.1177/1357034X97003003004'
  ) THEN
    RAISE EXCEPTION 'BDP-001M requires the BDP-001L canonical Buchanan article source before passage-candidate preparation.';
  END IF;
END $$;

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM concepts WHERE name = 'Body without Organs'
  ) THEN
    RAISE EXCEPTION 'BDP-001M requires canonical concept Body without Organs before passage-candidate preparation.';
  END IF;
END $$;

WITH target_source AS (
  SELECT id
    FROM sources
   WHERE author = 'Ian Buchanan'
     AND title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
     AND status = 'canonical'
     AND COALESCE(metadata->>'doi', '') = '10.1177/1357034X97003003004'
   LIMIT 1
),
target_concept AS (
  SELECT id
    FROM concepts
   WHERE name = 'Body without Organs'
   LIMIT 1
)
INSERT INTO passage_candidates (
  source_id,
  concept_id,
  candidate_label,
  candidate_status,
  candidate_scope,
  candidate_text,
  candidate_text_status,
  page_or_timestamp,
  chapter_or_section,
  locator_status,
  rights_status,
  display_rule,
  review_status,
  extraction_status,
  inserted_as_passage,
  citation_ready,
  concept_mention_ready,
  interpretation_ready,
  buchanan_claim_ready,
  metadata
)
SELECT
  target_source.id,
  target_concept.id,
  'BDP-001M first Buchanan passage candidate for Body without Organs',
  'candidate',
  'passage_candidate_envelope_metadata_only',
  NULL,
  'not_stored_pending_operator_review',
  NULL,
  NULL,
  'locator_pending_operator_pdf_review',
  'restricted',
  'reference_only',
  'prepared',
  'not_extracted',
  FALSE,
  FALSE,
  FALSE,
  FALSE,
  FALSE,
  jsonb_build_object(
    'bdp_phase', 'BDP-001M',
    'candidate_kind', 'first_buchanan_passage_candidate_envelope',
    'source_title', 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?',
    'source_author', 'Ian Buchanan',
    'source_doi', '10.1177/1357034X97003003004',
    'source_journal', 'Body & Society',
    'source_year', 1997,
    'target_concept', 'Body without Organs',
    'prepared_from_adopted_source_metadata', TRUE,
    'source_text_available_for_operator_review', TRUE,
    'pdf_access_status', 'user_provided_pdf_available',
    'candidate_text_stored', FALSE,
    'long_quotation_stored', FALSE,
    'article_reproduction_authorized', FALSE,
    'passage_inserted', FALSE,
    'citation_inserted', FALSE,
    'concept_mention_inserted', FALSE,
    'concept_relation_inserted', FALSE,
    'interpretation_inserted', FALSE,
    'buchanan_claim_created', FALSE,
    'passage_insertion_ready', FALSE,
    'citation_insertion_ready', FALSE,
    'concept_mention_ready', FALSE,
    'concept_relation_ready', FALSE,
    'interpretation_ready', FALSE,
    'buchanan_claim_ready', FALSE,
    'locator_requirement', 'operator must select and review exact page or passage locator from the user-provided PDF in a later phase',
    'rights_boundary', 'reference_only_metadata_until_short_excerpt_review',
    'next_step', 'BDP-001N — Review selected Buchanan passage candidate text and locator before any citation or interpretation insertion.'
  )
FROM target_source, target_concept
WHERE NOT EXISTS (
  SELECT 1
    FROM passage_candidates pc
   WHERE pc.source_id = target_source.id
     AND pc.candidate_label = 'BDP-001M first Buchanan passage candidate for Body without Organs'
);

WITH target_source AS (
  SELECT id
    FROM sources
   WHERE author = 'Ian Buchanan'
     AND title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
     AND status = 'canonical'
     AND COALESCE(metadata->>'doi', '') = '10.1177/1357034X97003003004'
   LIMIT 1
),
target_candidate AS (
  SELECT pc.id
    FROM passage_candidates pc
    JOIN target_source ts ON ts.id = pc.source_id
   WHERE pc.candidate_label = 'BDP-001M first Buchanan passage candidate for Body without Organs'
   LIMIT 1
)
UPDATE sources s
   SET metadata = jsonb_set(
       COALESCE(s.metadata, '{}'::jsonb),
       '{bdp_001m_first_passage_candidate}',
       jsonb_build_object(
         'bdp_phase', 'BDP-001M',
         'passage_candidate_id', (SELECT id::text FROM target_candidate),
         'candidate_label', 'BDP-001M first Buchanan passage candidate for Body without Organs',
         'candidate_status', 'candidate',
         'review_status', 'prepared',
         'target_concept', 'Body without Organs',
         'candidate_text_stored', FALSE,
         'locator_selected', FALSE,
         'passage_inserted', FALSE,
         'citation_inserted', FALSE,
         'interpretation_inserted', FALSE,
         'buchanan_claim_created', FALSE,
         'display_rule', 'reference_only',
         'rights_status', 'restricted'
       ),
       TRUE
     ),
       updated_at = now()
 WHERE s.id = (SELECT id FROM target_source);

INSERT INTO schema_migrations (id, phase, description)
SELECT
  '013_prepare_bdp_001m_first_buchanan_passage_candidate',
  'BDP-001M',
  'Create passage_candidates staging table and prepare first Buchanan article passage candidate envelope without canonical passage, citation, concept relation, interpretation, or claim insertion.'
WHERE NOT EXISTS (
  SELECT 1
    FROM schema_migrations
   WHERE id = '013_prepare_bdp_001m_first_buchanan_passage_candidate'
      OR phase = 'BDP-001M'
);

DO $$
DECLARE
  candidate_count INTEGER;
BEGIN
  SELECT COUNT(*) INTO candidate_count
    FROM passage_candidates pc
    JOIN sources s ON s.id = pc.source_id
   WHERE s.author = 'Ian Buchanan'
     AND s.title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
     AND pc.candidate_label = 'BDP-001M first Buchanan passage candidate for Body without Organs';

  IF candidate_count <> 1 THEN
    RAISE EXCEPTION 'BDP-001M expected exactly one first Buchanan passage candidate, found %', candidate_count;
  END IF;
END $$;

COMMIT;
