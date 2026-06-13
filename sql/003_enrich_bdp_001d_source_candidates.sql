-- BDP-001D — Review and enrich source candidates before canonical source adoption
-- Boundary: candidate enrichment only.
-- This migration does not create canonical sources, passages, or interpretations.

BEGIN;

INSERT INTO schema_migrations (phase, description)
SELECT
    'BDP-001D',
    'Add structured review metadata to source_candidates and enrich initial Buchanan/Deleuze source candidates without canonical adoption.'
WHERE NOT EXISTS (
    SELECT 1 FROM schema_migrations WHERE phase = 'BDP-001D'
);

ALTER TABLE source_candidates
    ADD COLUMN IF NOT EXISTS metadata JSONB NOT NULL DEFAULT '{}'::jsonb;

COMMENT ON COLUMN source_candidates.metadata IS
    'Structured candidate-review metadata. Candidate metadata is not source evidence, canonical adoption, passage text, or interpretive authority.';

UPDATE source_candidates
SET
    author = 'Gilles Deleuze and Félix Guattari',
    type = 'book',
    status = 'candidate',
    review_notes = 'BDP-001D review-ready candidate metadata added. Primary-text candidate only. Requires operator confirmation of exact edition/translation, rights basis, and locator strategy before canonical source adoption.',
    metadata = metadata || jsonb_build_object(
        'candidate_status', 'candidate',
        'review_notes', 'Primary Deleuze and Guattari source candidate. Candidate remains non-canonical until operator adoption review is explicitly recorded.',
        'bibliographic_edition_or_version_note', 'Review candidate for Anti-Oedipus: Capitalism and Schizophrenia. Confirm exact edition, translation, publisher, year, and locator scheme before adoption.',
        'rights_status_recommendation', 'fair_use_reference_only',
        'reliability_level_recommendation', 'high_after_edition_confirmation_primary_text',
        'adoption_readiness', 'review_ready_not_adoption_ready',
        'operator_review_requirement', 'operator must approve canonical source adoption before any source record, passage extraction, citation claim, or interpretation is created',
        'canonical_adoption_boundary', 'source candidate ≠ canonical source; bibliographic metadata ≠ source evidence; review readiness ≠ adoption; source adoption ≠ interpretive authority',
        'bdp_phase', 'BDP-001D'
    )
WHERE title = 'Anti-Oedipus: Capitalism and Schizophrenia';

UPDATE source_candidates
SET
    author = 'Gilles Deleuze and Félix Guattari',
    type = 'book',
    status = 'candidate',
    review_notes = 'BDP-001D review-ready candidate metadata added. Primary-text candidate only. Requires operator confirmation of exact edition/translation, rights basis, and locator strategy before canonical source adoption.',
    metadata = metadata || jsonb_build_object(
        'candidate_status', 'candidate',
        'review_notes', 'Primary Deleuze and Guattari source candidate. Candidate remains non-canonical until operator adoption review is explicitly recorded.',
        'bibliographic_edition_or_version_note', 'Review candidate for A Thousand Plateaus: Capitalism and Schizophrenia. Confirm exact edition, translation, publisher, year, and locator scheme before adoption.',
        'rights_status_recommendation', 'fair_use_reference_only',
        'reliability_level_recommendation', 'high_after_edition_confirmation_primary_text',
        'adoption_readiness', 'review_ready_not_adoption_ready',
        'operator_review_requirement', 'operator must approve canonical source adoption before any source record, passage extraction, citation claim, or interpretation is created',
        'canonical_adoption_boundary', 'source candidate ≠ canonical source; bibliographic metadata ≠ source evidence; review readiness ≠ adoption; source adoption ≠ interpretive authority',
        'bdp_phase', 'BDP-001D'
    )
WHERE title = 'A Thousand Plateaus: Capitalism and Schizophrenia';

UPDATE source_candidates
SET
    author = 'Ian Buchanan',
    type = 'bibliography_record',
    status = 'candidate',
    review_notes = 'BDP-001D review-ready candidate metadata added. Buchanan-source candidate only. Requires operator identification of exact Buchanan work, bibliographic version, rights basis, and source locator before canonical source adoption.',
    metadata = metadata || jsonb_build_object(
        'candidate_status', 'candidate',
        'review_notes', 'Buchanan source candidate for Body without Organs research. Candidate remains non-canonical until exact source identity and rights status are reviewed by the operator.',
        'bibliographic_edition_or_version_note', 'Placeholder candidate for a Buchanan Body without Organs source. Confirm exact title, publication form, edition/version, publisher or URL, date, and locator scheme before adoption.',
        'rights_status_recommendation', 'unknown',
        'reliability_level_recommendation', 'medium_pending_source_identification_buchanan_direct_candidate',
        'adoption_readiness', 'not_ready_for_adoption_until_exact_source_identified',
        'operator_review_requirement', 'operator must identify and approve exact Buchanan source before any canonical source record, passage extraction, citation claim, or interpretation is created',
        'canonical_adoption_boundary', 'source candidate ≠ canonical source; bibliographic metadata ≠ source evidence; review readiness ≠ adoption; source adoption ≠ interpretive authority',
        'bdp_phase', 'BDP-001D'
    )
WHERE title = 'Ian Buchanan Body without Organs source candidate';

DO $$
DECLARE
    expected_count INTEGER;
    sources_count INTEGER;
    passages_count INTEGER;
    interpretations_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO expected_count
    FROM source_candidates
    WHERE title IN (
        'Anti-Oedipus: Capitalism and Schizophrenia',
        'A Thousand Plateaus: Capitalism and Schizophrenia',
        'Ian Buchanan Body without Organs source candidate'
    )
      AND status = 'candidate'
      AND metadata->>'bdp_phase' = 'BDP-001D'
      AND metadata ? 'operator_review_requirement'
      AND metadata ? 'canonical_adoption_boundary';

    IF expected_count <> 3 THEN
        RAISE EXCEPTION 'BDP-001D expected 3 enriched candidate records, found %', expected_count;
    END IF;

    SELECT COUNT(*) INTO sources_count FROM sources;
    IF sources_count <> 0 THEN
        RAISE EXCEPTION 'BDP-001D must not create canonical sources; sources table contains % rows', sources_count;
    END IF;

    SELECT COUNT(*) INTO passages_count FROM passages;
    IF passages_count <> 0 THEN
        RAISE EXCEPTION 'BDP-001D must not insert passages; passages table contains % rows', passages_count;
    END IF;

    SELECT COUNT(*) INTO interpretations_count FROM interpretations;
    IF interpretations_count <> 0 THEN
        RAISE EXCEPTION 'BDP-001D must not insert interpretations; interpretations table contains % rows', interpretations_count;
    END IF;
END $$;

COMMIT;
