BEGIN;

ALTER TABLE source_candidates
ADD COLUMN IF NOT EXISTS metadata JSONB NOT NULL DEFAULT '{}'::jsonb;

UPDATE source_candidates
SET
    status = 'candidate',
    review_notes = 'Primary Deleuze and Guattari candidate. Review-ready metadata added for bibliographic, rights, reliability, and operator adoption review. Candidate remains non-canonical; no passages or interpretations are authorized by this record.',
    metadata = metadata || jsonb_build_object(
        'phase', 'BDP-001D',
        'candidate_status', 'candidate',
        'bibliographic_edition_or_version_note', 'Requires operator selection of edition before canonical adoption; recommended review target is a stable published English edition with full citation metadata.',
        'rights_status_recommendation', 'fair_use_reference_only',
        'reliability_level_recommendation', 'primary_text',
        'adoption_readiness', 'review_ready_not_adopted',
        'operator_review_requirement', 'Operator must confirm edition, rights handling, citation format, and adoption decision before promotion into sources.',
        'canonical_adoption', false,
        'passages_authorized', false,
        'interpretations_authorized', false,
        'review_notes', 'Candidate metadata only. Bibliographic enrichment is not evidence adoption.'
    )
WHERE title = 'Anti-Oedipus: Capitalism and Schizophrenia';

UPDATE source_candidates
SET
    status = 'candidate',
    review_notes = 'Primary Deleuze and Guattari candidate. Review-ready metadata added for bibliographic, rights, reliability, and operator adoption review. Candidate remains non-canonical; no passages or interpretations are authorized by this record.',
    metadata = metadata || jsonb_build_object(
        'phase', 'BDP-001D',
        'candidate_status', 'candidate',
        'bibliographic_edition_or_version_note', 'Requires operator selection of edition before canonical adoption; recommended review target is a stable published English edition with full citation metadata.',
        'rights_status_recommendation', 'fair_use_reference_only',
        'reliability_level_recommendation', 'primary_text',
        'adoption_readiness', 'review_ready_not_adopted',
        'operator_review_requirement', 'Operator must confirm edition, rights handling, citation format, and adoption decision before promotion into sources.',
        'canonical_adoption', false,
        'passages_authorized', false,
        'interpretations_authorized', false,
        'review_notes', 'Candidate metadata only. Bibliographic enrichment is not evidence adoption.'
    )
WHERE title = 'A Thousand Plateaus: Capitalism and Schizophrenia';

UPDATE source_candidates
SET
    status = 'candidate',
    review_notes = 'Buchanan-specific source candidate enriched for review. This remains a placeholder candidate until an exact Buchanan publication, lecture, transcript, interview, or teaching source is selected and reviewed. Candidate remains non-canonical; no passages or interpretations are authorized by this record.',
    metadata = metadata || jsonb_build_object(
        'phase', 'BDP-001D',
        'candidate_status', 'candidate',
        'bibliographic_edition_or_version_note', 'Exact Buchanan source still required. Replace placeholder with precise publication, lecture, transcript, interview, or teaching-material metadata before canonical adoption.',
        'rights_status_recommendation', 'unknown',
        'reliability_level_recommendation', 'buchanan_direct_pending_source_confirmation',
        'adoption_readiness', 'needs_exact_source_before_adoption',
        'operator_review_requirement', 'Operator must identify exact Buchanan source, confirm rights status, confirm bibliographic metadata, and approve adoption before promotion into sources.',
        'canonical_adoption', false,
        'passages_authorized', false,
        'interpretations_authorized', false,
        'review_notes', 'Candidate metadata only. No Buchanan claim may be made from this placeholder without exact source evidence.'
    )
WHERE title = 'Ian Buchanan Body without Organs source candidate';

INSERT INTO schema_migrations (id, phase, description)
SELECT
    '003_enrich_bdp_001d_source_candidates',
    'BDP-001D',
    'Added structured review metadata to source_candidates and enriched initial candidates without canonical source adoption.'
WHERE NOT EXISTS (
    SELECT 1
    FROM schema_migrations
    WHERE id = '003_enrich_bdp_001d_source_candidates'
);

COMMIT;
