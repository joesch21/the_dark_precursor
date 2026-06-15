# BDP-003E.5 — Local Reviewed Concept Card Archive Schema Candidate

**Status:** Implemented / verified  
**Type:** Design contract / schema candidate only  
**Date:** 2026-06-15T17:25:27+00:00  
**Authority:** Review/archive design only; no implementation  

## 1. Purpose

BDP-003E.5 defines a **local reviewed concept card archive schema candidate** for cinematic concept cards that have already been exported and reviewed.

This phase does not implement storage. It names the record shape that a later phase may use if the project decides to add a local archive mechanism.

The purpose is to prevent the next build from jumping directly from export drafts into uncontrolled persistence.

## 2. Decision

The platform is not yet ready for automatic persistence or database-backed storage.

It is ready to define a local archive schema candidate for reviewed cinematic concept card drafts only.

This schema candidate is intended for future local archive evaluation. It is not an implementation.

## 3. Boundary

```text
schema_candidate_only = true
frontend_change = false
backend_change = false
database_mutation = false
sql_migration = false
file_writer = false
local_archive_implementation = false
adapter_endpoint = false
adapter_invocation = false
evidence_spine_change = false
source_ingestion = false
citation_creation = false
concept_relation_creation = false
interpretation_insertion = false
buchanan_specific_claim_creation = false
image_generation = false
video_generation = false
```

No frontend implementation is added in BDP-003E.5.

No backend implementation is added in BDP-003E.5.

No database migration, database table, file writer, folder persistence, archive writer, adapter endpoint, image generator, video generator, or runtime export mechanism is implemented in this phase.

Generated material is not evidence.

Reviewed cinematic concept cards remain provisional synthesis unless a later governed evidence-review phase explicitly promotes a specific claim with citation support.

## 4. Candidate Archive Record

A future local reviewed concept card archive record should contain the following fields:

```json
{
  "schema_version": "bdp_003e5_local_reviewed_concept_card_archive_candidate_v1",
  "archive_record_id": "reviewed-card-archive-<slug>-<digest>",
  "source_card_id": "concept-card-draft-<slug>-<digest>",
  "created_utc": "ISO-8601 timestamp",
  "reviewed_utc": "ISO-8601 timestamp or null",
  "review_status": "reviewed_candidate",
  "review_decision": "retain_as_provisional_cinematic_synthesis",
  "archive_authority_label": "local_reviewed_archive_candidate_not_evidence",
  "source_authority_label": "provisional_cinematic_synthesis_not_evidence",
  "concept_query": "string",
  "cinematic_mode": "string",
  "site_context": "string",
  "includes_film_clip_brief": false,
  "reviewer_notes": [],
  "review_findings": {
    "conceptual_fidelity_checked": false,
    "evidence_boundary_checked": false,
    "cinematic_usefulness_checked": false,
    "adapter_readiness_checked": false
  },
  "governance": {
    "generated_material_is_evidence": false,
    "evidence_promotion_allowed": false,
    "database_mutation": false,
    "adapter_invocation": false,
    "server_file_persistence": false,
    "human_review_required": true
  },
  "blocked_actions": [
    "automatic_evidence_promotion",
    "database_persistence_without_future_phase",
    "adapter_invocation_without_future_phase",
    "buchanan_specific_claim_creation_without_citation_review"
  ],
  "source_export": {
    "markdown_available": true,
    "json_available": true,
    "source_export_schema_version": "bdp_003e2_cinematic_concept_card_export_draft_v1"
  }
}
```

## 5. Required Review Rules

Before a future archive implementation can use this schema, a later phase must confirm:

1. The exported card has been reviewed by a human operator.
2. The card is labelled as provisional cinematic synthesis.
3. Any evidence-backed claim is clearly distinguished from generated synthesis.
4. No generated phrase is treated as a Buchanan claim.
5. No generated phrase is inserted into the citation layer.
6. No concept relation is created from cinematic text alone.
7. No image or video adapter receives archive material without a separate adapter-boundary phase.

## 6. Explicit Non-Goals

BDP-003E.5 does not create:

1. A save button.
2. A local archive folder.
3. A JSON writer.
4. A Markdown writer.
5. A database table.
6. A migration.
7. A backend service.
8. A frontend archive browser.
9. An adapter endpoint.
10. Any evidence-spine promotion path.

## 7. Readiness Result

Decision: **schema candidate only**.

The project may define a local reviewed archive record shape, but it is not ready to implement archive persistence in this phase.

## 8. Verification

Run:

```bash
python3 -m py_compile frontend/dark_precursor.py
python3 scripts/verify_bdp_003c_cinematic_experience_reset.py
python3 scripts/verify_bdp_003d_cinematic_video_front_page.py
python3 scripts/verify_bdp_003e1_cinematic_concept_card_contract.py
python3 scripts/verify_bdp_003e2_cinematic_concept_card_export_draft.py
python3 scripts/verify_bdp_003e3_cinematic_concept_card_sample_review.py
python3 scripts/verify_bdp_003e4_concept_card_persistence_readiness_decision.py
python3 scripts/verify_bdp_003e5_local_reviewed_concept_card_archive_schema_candidate.py
```

## 9. Next Recommended Step

```text
BDP-003E.6 — Review local reviewed concept card archive schema candidate against exported samples before implementation.
```

That next phase should review the schema candidate against real exported examples. It should still not implement persistence.

<!-- BDP-003E.6-FOLLOW-UP-NOTE-START -->
## BDP-003E.6 Follow-up Review Note

BDP-003E.6 reviewed this BDP-003E.5 local reviewed concept card archive schema candidate against the BDP-003E.3 exported cinematic concept card sample cases.

Decision: the candidate is suitable for reviewed sample comparison.

Implementation is still not approved. This note does not authorize persistence, frontend archive buttons, backend services, SQL migrations, local file writers, archive folders, adapter endpoints, evidence promotion, citations, concept relations, interpretations, or Buchanan-specific claims.

Next step:

`BDP-003E.7 — Define local reviewed concept card archive writer contract only, without implementation.`
<!-- BDP-003E.6-FOLLOW-UP-NOTE-END -->
