# BDP-003E.1 — Cinematic Concept Card Persistence Contract

**Status:** Implemented / verified  
**Type:** Governance / persistence contract only  
**Authority:** Contract only; no runtime persistence implementation  
**Date:** June 2026

## 1. Purpose

BDP-003E.1 defines how The Dark Precursor may later persist cinematic concept cards without confusing generated cinematic material with evidence.

This phase is deliberately contract-only. It does not add a save button, database table, file writer, adapter call, frontend panel, backend route, or video/image generation integration.

The contract prepares the next implementation slice by defining:

1. What a cinematic concept card is.
2. Which fields a persisted card must carry.
3. Which authority labels are mandatory.
4. Which actions are explicitly forbidden.
5. How a future image/video adapter may receive a card without gaining evidence authority.

## 2. Core Boundary

```text
contract_only = true
runtime_persistence = false
frontend_change = false
backend_change = false
database_mutation = false
sql_migration = false
evidence_spine_change = false
source_ingestion = false
citation_creation = false
concept_relation_creation = false
interpretation_insertion = false
buchanan_specific_claim_creation = false
image_generation_backend = false
video_generation_backend = false
adapter_boundary_only = true
```

## 3. Definition: Cinematic Concept Card

A cinematic concept card is a saved representation of a Dark Precursor output.

It may preserve:

1. The operator's concept query.
2. The selected cinematic mode.
3. The generated cinematic response.
4. A differential trace.
5. A storyboard or film-clip brief.
6. An image/video generation prompt intended for a later adapter.
7. Evidence posture labels.
8. Human review status.

It is not:

1. A Buchanan citation.
2. A source passage.
3. A concept mention.
4. A concept relation.
5. A scholarly interpretation inserted into the evidence spine.
6. A database-backed evidence record.
7. Proof that Buchanan made the generated claim.

## 4. Required Authority Labels

Every future persisted cinematic concept card must include these labels:

```json
{
  "authority": "cinematic_synthesis",
  "evidence_status": "not_evidence",
  "promotion_status": "not_promoted",
  "human_review_required": true,
  "adapter_boundary": "optional_downstream_generation_only",
  "evidence_spine_mutation": false
}
```

A card may optionally include a link to source-backed evidence if that evidence has already been reviewed elsewhere, but the card itself must remain separate from the evidence spine.

## 5. Minimum Future Card Shape

Future implementation should use a stable shape equivalent to:

```json
{
  "card_id": "generated_stable_identifier",
  "created_at": "ISO-8601 timestamp",
  "phase": "BDP-003E",
  "concept_query": "operator supplied concept or question",
  "mode": "Narrator | Cinematic Treatment | Storyboard / Film Clip Brief",
  "site_or_scene": "optional operator context",
  "cinematic_response_markdown": "generated response text",
  "differential_trace": {
    "assemblage": "optional generated trace",
    "flow": "optional generated trace",
    "cut_or_interruption": "optional generated trace",
    "capture_or_extraction": "optional generated trace",
    "desire": "optional generated trace",
    "affect_or_intensity": "optional generated trace",
    "qualitative_difference": "optional generated trace",
    "line_of_flight": "optional generated trace"
  },
  "film_brief": {
    "shot_list": [],
    "visual_palette": [],
    "sound_design_notes": [],
    "image_prompt": "optional downstream prompt",
    "video_prompt": "optional downstream prompt"
  },
  "governance": {
    "authority": "cinematic_synthesis",
    "evidence_status": "not_evidence",
    "promotion_status": "not_promoted",
    "human_review_required": true,
    "adapter_boundary": "optional_downstream_generation_only",
    "evidence_spine_mutation": false
  },
  "review": {
    "review_status": "unreviewed",
    "reviewer": null,
    "review_notes": null,
    "reviewed_at": null
  }
}
```

## 6. Persistence Location Boundary

BDP-003E.1 does not choose the final persistence mechanism.

Future slices may consider one of these options:

1. Local Markdown export.
2. Local JSON export.
3. A governed `generated_cards/` directory.
4. A future database table.
5. A future operator-reviewed media pipeline queue.

The next safe implementation should start with local file export only. Database persistence should come later, after explicit schema review.

## 7. Adapter Boundary

A future image/video generation adapter may consume a cinematic concept card only as downstream creative material.

The adapter must not:

1. Promote generated text to evidence.
2. Insert citations.
3. Create concept mentions.
4. Create concept relations.
5. Rewrite reviewed passages.
6. Claim generated images or videos are Buchanan scholarship.
7. Mutate the evidence spine.

The adapter may:

1. Read the card's `image_prompt` or `video_prompt`.
2. Produce a visual artefact.
3. Attach governance metadata to that artefact.
4. Mark the artefact as generated and review-required.

## 8. Verification Requirements

The verifier must confirm:

1. This contract document exists.
2. The phase is contract-only.
3. Runtime persistence is explicitly false.
4. Database mutation is explicitly false.
5. Evidence-spine mutation is explicitly false.
6. The required card governance labels are present.
7. The adapter boundary is downstream-only.
8. The phase is recorded in `BUCHANAN_SYSTEM_STATE.json`.
9. `BUCHANAN_THREAD_HANDOVER.md` records the phase closeout.
10. The next recommended step points to BDP-003E.2.

## 9. Next Recommended Step

```text
BDP-003E.2 — Implement read-only cinematic concept card export draft without database mutation.
```

This should create a local export mechanism only. It should not create a database schema, adapter endpoint, or automatic evidence promotion.
