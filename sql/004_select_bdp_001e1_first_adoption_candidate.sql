BEGIN;

ALTER TABLE source_candidates
ADD COLUMN IF NOT EXISTS metadata JSONB NOT NULL DEFAULT '{}'::jsonb;

UPDATE source_candidates
SET metadata =
    metadata
    - 'first_adoption_candidate_selected'
    - 'adoption_selection_status'
    - 'selection_lock'
    - 'selection_lock_phase'
    - 'selection_lock_note'
    - 'source_adoption_created'
    - 'passage_inserted'
    - 'citation_inserted'
    - 'interpretation_created'
WHERE title IN (
    'Anti-Oedipus: Capitalism and Schizophrenia',
    'A Thousand Plateaus: Capitalism and Schizophrenia',
    'Ian Buchanan Body without Organs source candidate'
);

UPDATE source_candidates
SET
    status = 'candidate',
    review_notes = review_notes || ' BDP-001E.1: selected and locked as the first candidate for canonical adoption review. No canonical source, passage, citation, or interpretation was created in this phase.',
    metadata = metadata || jsonb_build_object(
        'phase_latest', 'BDP-001E.1',
        'first_adoption_candidate_selected', true,
        'adoption_selection_status', 'selected_for_canonical_adoption_review',
        'selection_lock', true,
        'selection_lock_phase', 'BDP-001E.1',
        'selection_lock_note', 'Selected as the first adoption candidate only. This lock does not create a canonical source record or authorize passage insertion.',
        'source_adoption_created', false,
        'passage_inserted', false,
        'citation_inserted', false,
        'interpretation_created', false
    )
WHERE title = 'A Thousand Plateaus: Capitalism and Schizophrenia';

INSERT INTO schema_migrations (id, phase, description)
SELECT
    '004_select_bdp_001e1_first_adoption_candidate',
    'BDP-001E.1',
    'Selected and locked A Thousand Plateaus as first source adoption candidate without canonical source adoption.'
WHERE NOT EXISTS (
    SELECT 1
    FROM schema_migrations
    WHERE id = '004_select_bdp_001e1_first_adoption_candidate'
);

COMMIT;
