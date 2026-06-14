# BDP-002C — Richer Semantic Readback Surface

## Purpose

BDP-002C defines and implements a richer read-only semantic readback surface for the anchor concept `Body without Organs`.

It is an evidence card over the governed evidence spine. It is not an interpretation layer, not a relation layer, not a source-ingestion phase, and not a schema change.

## Boundary Confirmation

BDP-002C internalises the current governance boundary:

```text
read-only semantic readback only
existing governed evidence spine only
no source mutation
no passage mutation
no citation mutation
no concept mention mutation
no concept relation mutation
no interpretation mutation
no SQL migration
no psycopg dependency
no psycopg2 dependency
psql subprocess readback only
restricted passage text omitted from display
Buchanan-specific explanation blocked
psycho-linguistic observations experimental only
```

## Current Governed State Reflected

BDP-002C reflects the current known state without inventing new evidence:

```text
sources_count = 2
source_candidates_count = 3
passage_candidates_count = 1
passages_count = 2
citations_count = 2
concept_mentions_count = 2
concept_relations_count = 0
interpretations_count = 0
BDP-001P migration_count = 1
BDP-002C migration_count = 0
```

Supplemental Buchanan evidence-chain counts expected by the readback:

```text
buchanan_article_passage_count = 1
buchanan_article_citation_count = 1
buchanan_article_concept_mention_count = 1
```

Current locator reflected:

```text
printed article page 76 / PDF page 4
```

## Authority Label Contract

Every card section, field, item, and observation must carry one authority label from this controlled set:

```text
concept_record
metadata
citation_backed
citation_backed_passage
primary_text_backed
reviewed_concept_mention
source_bound_description
record_description
rights_display_boundary
buchanan_pending
blocked_until_reviewed_relation_evidence
blocked_until_governed_interpretation_phase
blocked_until_interpretive_authority_exists
needs_review
provisional_synthesis
system_synthesis
user_interpretation
experimental_modelling
```

BDP-002C may use `experimental_modelling` only for psycho-linguistic placeholder observations that are linked to a specific passage locator and flagged as requiring human review.

BDP-002C must not use an unlabelled prose field.

## Description Versus Claim Rule

Allowed source-bound description:

```text
The database records a restricted citation-backed Buchanan passage linked to Body without Organs through a reviewed direct concept mention.
```

Blocked author-position claim:

```text
Buchanan argues that the Body without Organs means X.
```

A description becomes a claim when it attributes a position, argument, intention, conceptual meaning, or theoretical consequence to Buchanan, Deleuze, Guattari, or another author.

BDP-002C does not create claims.

## Rights Display Rule

The BDP-002C card must display the rights boundary as data:

```text
passage_text_display = omitted_by_rights_policy
long_quotation_displayed = false
article_reproduction_authorized = false
```

The card may display bibliographic metadata, locator data, citation status, concept mention status, and evidence posture.

The card must not display restricted passage text.

## Buchanan Explanation Rule

Buchanan-specific explanation remains blocked.

Required card fields:

```text
buchanan_specific_explanation_status = buchanan_pending
buchanan_specific_interpretation_status = blocked_until_governed_interpretation_phase
buchanan_specific_claim_status = blocked_until_interpretive_authority_exists
```

No language may attribute a position, argument, intention, conceptual meaning, or theoretical consequence to Ian Buchanan.

## Psycho-Linguistic Placeholder Rule

BDP-002C may expose psycho-linguistic observation placeholders only under these conditions:

```text
authority_label = experimental_modelling
linked_passage_locator = printed article page 76 / PDF page 4
requires_human_review = true
current_ceiling = Level 2 Embedding Deviation
objective_score_claimed = false
```

Allowed placeholder types:

```text
metaphor_density_placeholder
abstraction_gradient_placeholder
rhetorical_destabilisation_placeholder
semantic_drift_placeholder
```

The placeholders are modelling hooks only. They are not objective scores, not citation authority, and not Buchanan-specific interpretation.

## Expanded 15-Section Card Structure

The BDP-002C card must contain exactly these 15 sections:

1. `concept_identity`
2. `evidence_depth_tier`
3. `canonical_source_metadata`
4. `citation_backed_passage_record`
5. `reviewed_concept_mention_record`
6. `rights_display_boundary`
7. `current_database_invariant`
8. `source_bound_evidence_posture`
9. `buchanan_specific_explanation_boundary`
10. `relation_layer_status`
11. `interpretation_layer_status`
12. `related_concept_candidates`
13. `psycho_linguistic_placeholder_observations`
14. `verification_and_audit_boundary`
15. `next_recommended_operator_action`

Each section must include:

```text
section_id
title
authority_label
fields or observations
```

Each field or observation must include:

```text
field_id or observation_id
label or observation_type
value or observation_text
authority_label
```

Experimental observations must additionally include:

```text
linked_passage_locator
requires_human_review
current_ceiling
objective_score_claimed
```

## SQL Boundary

The readback script may pass only `SELECT` SQL to `psql`.

Forbidden mutation keywords in SQL passed to `psql`:

```text
INSERT
UPDATE
DELETE
CREATE
ALTER
DROP
TRUNCATE
MERGE
UPSERT
GRANT
REVOKE
COPY
CALL
DO
```

The verifier must inspect SQL strings actually passed to the psql helper, not arbitrary explanatory prose.

## Implementation Deliverables

BDP-002C deliverables:

```text
docs/BDP_002C_RICHER_SEMANTIC_READBACK_SURFACE.md
scripts/read_bdp_002c_richer_bwo_semantic_card.py
scripts/verify_bdp_002c_richer_semantic_readback.py
scripts/update_bdp_002c_docs_and_state.py
```

No SQL migration is added.

No frontend renderer is added.

## Verifier Checklist

The dedicated verifier must prove:

1. `psycopg` is not imported.
2. `psycopg2` is not imported.
3. readback uses Python `subprocess` and `psql`.
4. no SQL string passed to `psql` contains mutation keywords.
5. current invariant is correct before readback.
6. current invariant is preserved after readback.
7. `BDP-002C migration_count = 0`.
8. the card has exactly 15 required sections.
9. every section has a controlled authority label.
10. every field, item, and observation has a controlled authority label.
11. Buchanan-specific explanation remains `buchanan_pending`.
12. Buchanan-specific interpretation remains `blocked_until_governed_interpretation_phase`.
13. Buchanan-specific claim remains `blocked_until_interpretive_authority_exists`.
14. no generated text contains blocked author-position phrasing.
15. `passage_text_display = omitted_by_rights_policy`.
16. `long_quotation_displayed = false`.
17. `article_reproduction_authorized = false`.
18. psycho-linguistic observations are labelled `experimental_modelling`.
19. psycho-linguistic observations are linked to the governed passage locator.
20. psycho-linguistic observations are flagged `requires_human_review = true`.
21. Level 2 Embedding Deviation is the current ceiling.
22. no objective metaphor-density score is asserted.
23. no source, passage, citation, concept mention, relation, interpretation, or generated Buchanan claim is created.

## Next Recommended Operator Action

Primary next action:

```text
BDP-001R — Prepare first source-bound Buchanan Body without Organs description candidate, without interpretation.
```

Governance note:

```text
BDP-001R may prepare a description candidate over the existing citation-backed Buchanan passage and reviewed concept mention, but it must still not create a Buchanan interpretation, concept relation, theoretical consequence, or generated author-position claim.
```
