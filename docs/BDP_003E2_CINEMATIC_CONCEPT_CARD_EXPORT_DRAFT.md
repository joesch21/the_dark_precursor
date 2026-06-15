# BDP-003E.2 — Read-only Cinematic Concept Card Export Draft

**Status:** Implemented / verified  
**Type:** Frontend export draft / local download only  
**Interface:** `frontend/dark_precursor.py`  
**Authority:** provisional cinematic synthesis only  
**Date:** June 2026

## 1. Purpose

BDP-003E.2 implements the first runtime surface for cinematic concept card drafts.

The goal is intentionally narrow:

```text
existing cinematic response
→ structured concept card draft object
→ local Markdown / JSON download
→ human review required
```

This is not database persistence. It is not an image or video generation adapter. It is not evidence creation.

## 2. Implemented Behaviour

When The Dark Precursor has a generated response in session state, the interface now exposes a collapsed export dock:

```text
🗂 Cinematic concept card export draft
```

The dock allows the operator to download:

1. A Markdown concept card draft.
2. A JSON concept card data object.

Both exports are generated in memory from the visible response and current interaction controls.

## 3. Card Draft Schema

The export object uses:

```text
bdp_003e2_cinematic_concept_card_export_draft_v1
```

Required fields include:

1. `schema_version`
2. `card_id`
3. `created_utc`
4. `authority_label`
5. `storage_posture`
6. `review_status`
7. `concept_query`
8. `cinematic_mode`
9. `site_context`
10. `includes_film_clip_brief`
11. `generated_material_is_evidence`
12. `evidence_spine_mutation`
13. `database_mutation`
14. `adapter_invocation`
15. `promotion_allowed`
16. `response_markdown`
17. `required_human_review`
18. `blocked_actions`
19. `next_safe_action`

## 4. Governance Labels

Every generated export draft must carry these labels:

```text
authority_label = provisional_cinematic_synthesis_not_evidence
storage_posture = download_only_no_database_mutation
review_status = draft_unreviewed
generated_material_is_evidence = false
database_mutation = false
evidence_spine_mutation = false
adapter_invocation = false
promotion_allowed = false
```

## 5. Boundary

BDP-003E.2 does not:

1. Mutate the database.
2. Add a SQL migration.
3. Create a backend service.
4. Create an adapter endpoint.
5. Call an image model.
6. Call a video model.
7. Persist files on the server.
8. Insert citations.
9. Create concept relations.
10. Create Buchanan-specific claims.
11. Promote generated material into the evidence spine.

Generated cinematic concept cards are not evidence. They are provisional cinematic synthesis drafts only.

## 6. Files Affected

```text
frontend/dark_precursor.py
frontend/styles/dark_precursor.css
docs/BDP_003E2_CINEMATIC_CONCEPT_CARD_EXPORT_DRAFT.md
scripts/verify_bdp_003e2_cinematic_concept_card_export_draft.py
BUCHANAN_SYSTEM_STATE.json
BUCHANAN_THREAD_HANDOVER.md
```

## 7. Verification

Run:

```bash
python3 -m py_compile frontend/dark_precursor.py
python3 scripts/verify_bdp_003c_cinematic_experience_reset.py
python3 scripts/verify_bdp_003d_cinematic_video_front_page.py
python3 scripts/verify_bdp_003e1_cinematic_concept_card_contract.py
python3 scripts/verify_bdp_003e2_cinematic_concept_card_export_draft.py
```

## 8. Next Recommended Step

```text
BDP-003E.3 — Review exported cinematic concept card samples before any persistence or adapter implementation.
```

The next step should review real exported examples before any persistence, adapter boundary, or external generation feature is added.
