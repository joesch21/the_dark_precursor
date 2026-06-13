-- Buchanan Deleuze Intelligence Platform
-- BDP-001C — Seed first canonical concept and source candidate records
-- Boundary:
--   - concept seed only
--   - source candidates only
--   - no canonical source adoption
--   - no passage or interpretation claims yet

BEGIN;

INSERT INTO concepts (
  name,
  aliases,
  short_description,
  status
)
VALUES
  (
    'Body without Organs',
    ARRAY['BwO', 'body without organs'],
    'Initial canonical concept target for the Buchanan Deleuze Intelligence Platform. Interpretive content must be added only through cited passages or reviewed synthesis.',
    'canonical'
  ),
  (
    'organism',
    ARRAY['the organism'],
    'Related concept in the initial Body without Organs cluster. Relation claims require cited evidence before acceptance.',
    'proposed'
  ),
  (
    'desire',
    ARRAY[]::TEXT[],
    'Related concept in the initial Body without Organs cluster. Relation claims require cited evidence before acceptance.',
    'proposed'
  ),
  (
    'assemblage',
    ARRAY['agencement'],
    'Related concept in the initial Body without Organs cluster. Relation claims require cited evidence before acceptance.',
    'proposed'
  ),
  (
    'strata',
    ARRAY['stratification'],
    'Related concept in the initial Body without Organs cluster. Relation claims require cited evidence before acceptance.',
    'proposed'
  )
ON CONFLICT (name) DO UPDATE
SET
  aliases = EXCLUDED.aliases,
  short_description = EXCLUDED.short_description,
  status = EXCLUDED.status,
  updated_at = NOW();

INSERT INTO source_candidates (
  title,
  author,
  url,
  type,
  discovered_by,
  status,
  review_notes
)
VALUES
  (
    'Anti-Oedipus: Capitalism and Schizophrenia',
    'Gilles Deleuze and Félix Guattari',
    NULL,
    'book',
    'BDP-001C_seed',
    'candidate',
    'Primary Deleuze and Guattari candidate. Requires bibliographic edition, rights status, and operator review before source adoption.'
  ),
  (
    'A Thousand Plateaus: Capitalism and Schizophrenia',
    'Gilles Deleuze and Félix Guattari',
    NULL,
    'book',
    'BDP-001C_seed',
    'candidate',
    'Primary Deleuze and Guattari candidate. Requires bibliographic edition, rights status, and operator review before source adoption.'
  ),
  (
    'Ian Buchanan Body without Organs source candidate',
    'Ian Buchanan',
    NULL,
    'other',
    'BDP-001C_seed',
    'candidate',
    'Placeholder candidate for Buchanan publication, lecture, transcript, or teaching material directly relevant to Body without Organs. Must be replaced or enriched with exact bibliographic/source metadata before adoption.'
  )
ON CONFLICT DO NOTHING;

INSERT INTO schema_migrations (
  id,
  phase,
  description
)
VALUES (
  '002_seed_bdp_001c',
  'BDP-001C',
  'Seeded first canonical concept target and initial source candidate records without canonical source adoption.'
)
ON CONFLICT (id) DO NOTHING;

COMMIT;
