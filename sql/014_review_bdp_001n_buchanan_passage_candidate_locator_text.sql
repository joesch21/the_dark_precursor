-- BDP-001N — Review first Buchanan passage candidate locator and short text only.
--
-- Boundary:
-- - Updates only the existing passage_candidates row for the Buchanan article.
-- - Does not insert a canonical passage.
-- - Does not insert a citation.
-- - Does not insert a concept mention.
-- - Does not insert a concept relation.
-- - Does not insert an interpretation.
-- - Does not create a Buchanan-specific claim.
-- - Stores only a short rights-aware candidate excerpt.

BEGIN;

DO $$
DECLARE
    updated_count integer;
BEGIN
    WITH target AS (
        SELECT pc.id
        FROM passage_candidates pc
        JOIN sources s ON s.id = pc.source_id
        LEFT JOIN concepts c ON c.id = pc.concept_id
        WHERE s.author = 'Ian Buchanan'
          AND s.title = 'The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?'
          AND c.name = 'Body without Organs'
          AND pc.candidate_label = 'BDP-001M first Buchanan passage candidate for Body without Organs'
        ORDER BY pc.created_at, pc.id
        LIMIT 1
    )
    UPDATE passage_candidates pc
    SET
        candidate_text = 'the body without organs is not a primary term',
        candidate_text_status = 'reviewed_short_excerpt',
        page_or_timestamp = 'printed article page 76; PDF page 4',
        chapter_or_section = 'opening section before Spinoza',
        locator_status = 'reviewed',
        review_status = 'approved',
        extraction_status = 'operator_pdf_reviewed_short_excerpt',
        inserted_as_passage = FALSE,
        citation_ready = TRUE,
        concept_mention_ready = FALSE,
        interpretation_ready = FALSE,
        buchanan_claim_ready = FALSE,
        reviewed_at = NOW(),
        metadata = COALESCE(pc.metadata, '{}'::jsonb) || jsonb_build_object(
            'bdp_phase', 'BDP-001N',
            'review_type', 'passage_candidate_locator_text_review_only',
            'candidate_text_status', 'reviewed_short_excerpt',
            'candidate_text_word_count', 9,
            'locator_status', 'reviewed',
            'locator_pdf_page', 4,
            'locator_printed_article_page', 76,
            'locator_line_window', 'lines 8-10 from operator pdftotext review',
            'chapter_or_section', 'opening section before Spinoza',
            'review_status', 'approved',
        'review_status_detail', 'reviewed_for_later_passage_insertion',
            'citation_ready', true,
            'concept_mention_ready', false,
            'interpretation_ready', false,
            'buchanan_claim_ready', false,
            'inserted_as_passage', false,
            'passage_inserted', false,
            'citation_inserted', false,
            'concept_mention_inserted', false,
            'concept_relation_inserted', false,
            'interpretation_inserted', false,
            'buchanan_claim_created', false,
            'rights_status', 'restricted',
            'display_rule', 'reference_only',
        'display_rule_detail', 'reference_only_short_excerpt_candidate',
            'long_quotation_stored', false,
            'article_reproduction_authorized', false,
            'next_step', 'BDP-001O — Insert reviewed Buchanan passage and citation only, if operator approves.'
        )
    FROM target
    WHERE pc.id = target.id;

    GET DIAGNOSTICS updated_count = ROW_COUNT;

    IF updated_count <> 1 THEN
        RAISE EXCEPTION 'BDP-001N expected to update exactly one passage_candidates row, updated %', updated_count;
    END IF;
END $$;

INSERT INTO schema_migrations (id, phase, description)
VALUES (
    '014_review_bdp_001n_buchanan_passage_candidate_locator_text',
    'BDP-001N',
    'Review first Buchanan passage candidate locator and short excerpt only; no canonical passage, citation, concept mention, relation, interpretation, or Buchanan claim inserted.'
)
ON CONFLICT (id) DO NOTHING;

COMMIT;
