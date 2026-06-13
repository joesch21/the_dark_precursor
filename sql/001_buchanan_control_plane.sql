-- Buchanan Deleuze Intelligence Platform
-- BDP-001A — Schema and Ontology Alignment Before Database Prototype
-- Initial PostgreSQL + pgvector control-plane migration

BEGIN;

-- Required for gen_random_uuid() and vector embeddings.
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS schema_migrations (
  id TEXT PRIMARY KEY,
  phase TEXT NOT NULL,
  description TEXT NOT NULL,
  applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE IF NOT EXISTS source_candidates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  author TEXT,
  url TEXT,
  type TEXT NOT NULL DEFAULT 'other'
    CHECK (type IN (
      'book',
      'article',
      'chapter',
      'lecture',
      'interview',
      'video_transcript',
      'conference_paper',
      'teaching_note',
      'user_note',
      'bibliography_record',
      'other'
    )),
  discovered_by TEXT NOT NULL DEFAULT 'manual',
  status TEXT NOT NULL DEFAULT 'candidate'
    CHECK (status IN ('candidate', 'approved', 'rejected', 'needs_review')),
  review_notes TEXT,
  reviewed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sources (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  candidate_id UUID REFERENCES source_candidates(id) ON DELETE SET NULL,
  title TEXT NOT NULL,
  author TEXT,
  type TEXT NOT NULL DEFAULT 'other'
    CHECK (type IN (
      'book',
      'article',
      'chapter',
      'lecture',
      'interview',
      'video_transcript',
      'conference_paper',
      'teaching_note',
      'user_note',
      'bibliography_record',
      'other'
    )),
  year INTEGER CHECK (year IS NULL OR (year >= 1800 AND year <= 2200)),
  publisher TEXT,
  url_or_reference TEXT,
  rights_status TEXT NOT NULL DEFAULT 'unknown'
    CHECK (rights_status IN (
      'unknown',
      'public_url',
      'licensed',
      'user_provided',
      'fair_use_reference_only',
      'restricted'
    )),
  reliability_level TEXT NOT NULL DEFAULT 'unknown'
    CHECK (reliability_level IN ('unknown', 'primary', 'high', 'medium', 'low', 'unverified')),
  status TEXT NOT NULL DEFAULT 'approved'
    CHECK (status IN (
      'candidate',
      'approved',
      'rejected',
      'imported',
      'cleaned',
      'chunked',
      'embedded',
      'concept_tagged',
      'reviewed',
      'canonical'
    )),
  metadata JSONB NOT NULL DEFAULT '{}'::JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

DROP TRIGGER IF EXISTS trg_sources_updated_at ON sources;
CREATE TRIGGER trg_sources_updated_at
BEFORE UPDATE ON sources
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE IF NOT EXISTS raw_documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
  raw_text TEXT,
  file_path TEXT,
  imported_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  extractor_version TEXT NOT NULL DEFAULT 'manual_v1',
  metadata JSONB NOT NULL DEFAULT '{}'::JSONB,
  CHECK (raw_text IS NOT NULL OR file_path IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS clean_documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
  raw_document_id UUID REFERENCES raw_documents(id) ON DELETE SET NULL,
  cleaned_text TEXT NOT NULL,
  cleaning_version TEXT NOT NULL DEFAULT 'cleaning_v1',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  metadata JSONB NOT NULL DEFAULT '{}'::JSONB
);

CREATE TABLE IF NOT EXISTS passages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
  clean_document_id UUID REFERENCES clean_documents(id) ON DELETE SET NULL,
  text TEXT NOT NULL,
  chunk_index INTEGER CHECK (chunk_index IS NULL OR chunk_index >= 0),
  page_or_timestamp TEXT,
  chapter_or_section TEXT,
  citation TEXT NOT NULL,
  rights_status TEXT NOT NULL DEFAULT 'unknown'
    CHECK (rights_status IN (
      'unknown',
      'public_url',
      'licensed',
      'user_provided',
      'fair_use_reference_only',
      'restricted'
    )),
  extraction_version TEXT NOT NULL DEFAULT 'passage_extraction_v1',
  embedding vector(1536),
  embedding_model TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  metadata JSONB NOT NULL DEFAULT '{}'::JSONB
);

CREATE TABLE IF NOT EXISTS concepts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE,
  aliases TEXT[] NOT NULL DEFAULT '{}'::TEXT[],
  short_description TEXT,
  status TEXT NOT NULL DEFAULT 'proposed'
    CHECK (status IN ('proposed', 'accepted', 'rejected', 'needs_review', 'canonical')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

DROP TRIGGER IF EXISTS trg_concepts_updated_at ON concepts;
CREATE TRIGGER trg_concepts_updated_at
BEFORE UPDATE ON concepts
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE IF NOT EXISTS concept_mentions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  concept_id UUID NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
  passage_id UUID NOT NULL REFERENCES passages(id) ON DELETE CASCADE,
  confidence NUMERIC(4,3) NOT NULL DEFAULT 0.000 CHECK (confidence >= 0 AND confidence <= 1),
  mention_type TEXT NOT NULL DEFAULT 'direct'
    CHECK (mention_type IN ('direct', 'implied', 'contested', 'related', 'metaphorical')),
  reviewed_status TEXT NOT NULL DEFAULT 'proposed'
    CHECK (reviewed_status IN ('proposed', 'accepted', 'rejected', 'needs_review')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (concept_id, passage_id, mention_type)
);

CREATE TABLE IF NOT EXISTS concept_relations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_concept_id UUID NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
  target_concept_id UUID NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
  relation_type TEXT NOT NULL
    CHECK (relation_type IN (
      'explains',
      'depends_on',
      'opposes',
      'modifies',
      'intensifies',
      'emerges_from',
      'is_applied_to',
      'is_contested_by',
      'is_translated_as',
      'is_linked_to',
      'is_example_of',
      'develops',
      'reframes',
      'extends',
      'critiques',
      'operationalises'
    )),
  evidence_passage_id UUID REFERENCES passages(id) ON DELETE SET NULL,
  confidence NUMERIC(4,3) NOT NULL DEFAULT 0.000 CHECK (confidence >= 0 AND confidence <= 1),
  reviewed_status TEXT NOT NULL DEFAULT 'proposed'
    CHECK (reviewed_status IN ('proposed', 'accepted', 'rejected', 'needs_review')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CHECK (source_concept_id <> target_concept_id),
  UNIQUE (source_concept_id, target_concept_id, relation_type, evidence_passage_id)
);

CREATE TABLE IF NOT EXISTS interpretations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  concept_id UUID NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
  interpreter TEXT NOT NULL,
  claim TEXT NOT NULL,
  authority_level TEXT NOT NULL
    CHECK (authority_level IN (
      'primary_text',
      'buchanan_direct',
      'secondary_scholarship',
      'system_synthesis',
      'user_interpretation'
    )),
  evidence_passage_id UUID REFERENCES passages(id) ON DELETE SET NULL,
  confidence NUMERIC(4,3) NOT NULL DEFAULT 0.000 CHECK (confidence >= 0 AND confidence <= 1),
  reviewed_status TEXT NOT NULL DEFAULT 'proposed'
    CHECK (reviewed_status IN ('proposed', 'accepted', 'rejected', 'needs_review')),
  source_trail JSONB NOT NULL DEFAULT '[]'::JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS citations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
  passage_id UUID REFERENCES passages(id) ON DELETE CASCADE,
  interpretation_id UUID REFERENCES interpretations(id) ON DELETE CASCADE,
  citation_text TEXT NOT NULL,
  citation_format TEXT NOT NULL DEFAULT 'plain',
  locator TEXT,
  page_or_timestamp TEXT,
  chapter_or_section TEXT,
  url_or_reference TEXT,
  rights_status TEXT NOT NULL DEFAULT 'unknown'
    CHECK (rights_status IN (
      'unknown',
      'public_url',
      'licensed',
      'user_provided',
      'fair_use_reference_only',
      'restricted'
    )),
  display_rule TEXT NOT NULL DEFAULT 'short_quote_paraphrase_trail'
    CHECK (display_rule IN (
      'stored_only',
      'searchable_only',
      'short_quote_paraphrase_trail',
      'summarizable_only',
      'reference_only'
    )),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  metadata JSONB NOT NULL DEFAULT '{}'::JSONB,
  CHECK (passage_id IS NOT NULL OR interpretation_id IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS ingestion_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id UUID REFERENCES sources(id) ON DELETE CASCADE,
  candidate_id UUID REFERENCES source_candidates(id) ON DELETE SET NULL,
  action TEXT NOT NULL,
  result TEXT NOT NULL DEFAULT 'recorded',
  notes TEXT,
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  metadata JSONB NOT NULL DEFAULT '{}'::JSONB,
  CHECK (source_id IS NOT NULL OR candidate_id IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS user_interactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id TEXT NOT NULL,
  query TEXT NOT NULL,
  selected_concepts TEXT[] NOT NULL DEFAULT '{}'::TEXT[],
  response_mode TEXT,
  useful_response BOOLEAN,
  followup_path TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  metadata JSONB NOT NULL DEFAULT '{}'::JSONB
);

CREATE INDEX IF NOT EXISTS idx_source_candidates_status ON source_candidates(status);
CREATE INDEX IF NOT EXISTS idx_sources_status ON sources(status);
CREATE INDEX IF NOT EXISTS idx_sources_type ON sources(type);
CREATE INDEX IF NOT EXISTS idx_passages_source_id ON passages(source_id);
CREATE INDEX IF NOT EXISTS idx_passages_clean_document_id ON passages(clean_document_id);
CREATE INDEX IF NOT EXISTS idx_concept_mentions_concept_id ON concept_mentions(concept_id);
CREATE INDEX IF NOT EXISTS idx_concept_mentions_passage_id ON concept_mentions(passage_id);
CREATE INDEX IF NOT EXISTS idx_concept_relations_source ON concept_relations(source_concept_id, target_concept_id);
CREATE INDEX IF NOT EXISTS idx_interpretations_concept_id ON interpretations(concept_id);
CREATE INDEX IF NOT EXISTS idx_citations_source_id ON citations(source_id);
CREATE INDEX IF NOT EXISTS idx_citations_passage_id ON citations(passage_id);
CREATE INDEX IF NOT EXISTS idx_ingestion_events_source_id ON ingestion_events(source_id);

INSERT INTO concepts (name, aliases, short_description, status)
VALUES
  ('Body without Organs', ARRAY['BwO', 'body-without-organs'], 'Initial prototype concept for the Buchanan Deleuze Intelligence Platform.', 'proposed'),
  ('organism', ARRAY[]::TEXT[], NULL, 'proposed'),
  ('desire', ARRAY[]::TEXT[], NULL, 'proposed'),
  ('assemblage', ARRAY[]::TEXT[], NULL, 'proposed'),
  ('strata', ARRAY['stratification'], NULL, 'proposed'),
  ('deterritorialisation', ARRAY['deterritorialization'], NULL, 'proposed'),
  ('reterritorialisation', ARRAY['reterritorialization'], NULL, 'proposed'),
  ('schizoanalysis', ARRAY[]::TEXT[], NULL, 'proposed'),
  ('becoming', ARRAY[]::TEXT[], NULL, 'proposed'),
  ('war machine', ARRAY[]::TEXT[], NULL, 'proposed'),
  ('capitalism', ARRAY[]::TEXT[], NULL, 'proposed')
ON CONFLICT (name) DO NOTHING;

INSERT INTO schema_migrations (id, phase, description)
VALUES (
  '001_buchanan_control_plane',
  'BDP-001A',
  'Initial control-plane schema with citations, controlled vocabularies, ingestion staging, concept mentions, concept relations, interpretations, and schema drift ledger.'
)
ON CONFLICT (id) DO NOTHING;

COMMIT;
