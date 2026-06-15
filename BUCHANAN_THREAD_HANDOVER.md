# BDP-003E.2 — Read-only Cinematic Concept Card Export Draft

**Date:** 2026-06-15T17:01:19+00:00  
**Status:** Complete  
**Authority:** Frontend download-only draft export; no database mutation.

## What changed

BDP-003E.2 adds a local export dock to The Dark Precursor after a cinematic response has been generated.

The operator can download:

1. A Markdown cinematic concept card draft.
2. A JSON cinematic concept card data object.

The export is generated in memory from the visible response and current interaction controls.

## Governance

Generated cinematic concept cards are not evidence. They are provisional cinematic synthesis drafts only.

This slice does not add database persistence, backend services, adapter endpoints, server-side file persistence, image generation, video generation, citation creation, concept relation creation, or evidence-spine mutation.

## Files updated

- `frontend/dark_precursor.py`
- `frontend/styles/dark_precursor.css`
- `docs/BDP_003E2_CINEMATIC_CONCEPT_CARD_EXPORT_DRAFT.md`
- `docs/BDP_003E_CINEMATIC_CONCEPT_CARD_PERSISTENCE_CONTRACT.md`
- `scripts/verify_bdp_003e2_cinematic_concept_card_export_draft.py`
- `BUCHANAN_SYSTEM_STATE.json`
- `BUCHANAN_THREAD_HANDOVER.md`

## Verification

Run:

```bash
python3 -m py_compile frontend/dark_precursor.py
python3 scripts/verify_bdp_003c_cinematic_experience_reset.py
python3 scripts/verify_bdp_003d_cinematic_video_front_page.py
python3 scripts/verify_bdp_003e1_cinematic_concept_card_contract.py
python3 scripts/verify_bdp_003e2_cinematic_concept_card_export_draft.py
```

## Next recommended step

BDP-003E.3 — Review exported cinematic concept card samples before any persistence or adapter implementation.

---

# BDP-003E.1 — Cinematic Concept Card Persistence Contract

**Date:** 2026-06-15T16:51:45+00:00  
**Status:** Complete  
**Authority:** Contract only; no runtime implementation.

## What changed

BDP-003E.1 defines the persistence contract for future Dark Precursor cinematic concept cards.

The contract specifies:

1. The minimum card shape.
2. Required governance labels.
3. Evidence-spine separation.
4. Human-review requirements.
5. The optional downstream image/video adapter boundary.
6. The next implementation slice.

## Files updated

- `docs/BDP_003E_CINEMATIC_CONCEPT_CARD_PERSISTENCE_CONTRACT.md`
- `scripts/verify_bdp_003e1_cinematic_concept_card_contract.py`
- `BUCHANAN_SYSTEM_STATE.json`
- `BUCHANAN_THREAD_HANDOVER.md`

## Boundary

No frontend, backend, SQL, database, citation, source-ingestion, or adapter implementation was added.

The phase is contract-only. Generated cinematic cards remain `cinematic_synthesis`, `not_evidence`, `not_promoted`, and `human_review_required`.

## Verification

Run:

```bash
python3 scripts/verify_bdp_003e1_cinematic_concept_card_contract.py
```

## Next recommended step

BDP-003E.2 — Implement read-only cinematic concept card export draft without database mutation.

---

# BDP-003D.2 — Cinematic Video Front Page Closeout

**Date:** 2026-06-15T16:43:10+00:00
**Status:** Complete
**Authority:** Frontend display only; no evidence-spine mutation.

## What changed

BDP-003D is now closed out as the completed cinematic video front page slice.

The committed application already contains the BDP-003D behaviours:

1. Local MP4 cinematic background stream.
2. Fallback cinematic background when the video asset is absent.
3. Title gate before the main interface.
4. `Enter the Vault` transition.
5. `Return to title page` sidebar control.
6. Slowed atmospheric playback.
7. Large cinematic typography and softened translucent panels.

## Files updated

- `docs/BDP_003D_CINEMATIC_VIDEO_FRONT_PAGE.md`
- `docs/BDP_003C_CINEMATIC_EXPERIENCE_RESET.md`
- `BUCHANAN_SYSTEM_STATE.json`
- `scripts/verify_bdp_003d_cinematic_video_front_page.py`

## Verification

Run:

```bash
python3 -m py_compile frontend/dark_precursor.py
python3 scripts/verify_bdp_003c_cinematic_experience_reset.py
python3 scripts/verify_bdp_003d_cinematic_video_front_page.py
```

## Boundary

No database mutation, citation insertion, source ingestion, concept relation creation, interpretation insertion, or video generation backend was added.

The video remains atmosphere only. It is not evidence and does not carry conceptual authority.

## Next recommended step

BDP-003E — Define cinematic concept card persistence and optional image/video generation adapter boundary.

---

# Buchanan Thread Handover

<!-- BDP-002G DIFFERENTIAL READING ENGINE -->

## BDP-002G — Add differential reading engine contract

**Status:** Complete  
**Updated:** 2026-06-15T03:12:20+00:00  
**Type:** Doctrine and application contract  
**Database mutation:** No  
**SQL migration:** No  
**Frontend auto-wiring:** No  

### What changed

BDP-002G records the core platform thesis:

> The Buchanan / Deleuze Intelligence Platform is not merely a database. It is a differential reading engine.

The patch adds the governed method for tracing:

1. Assemblage
2. Flow
3. Cut / subtraction
4. Capture / extraction
5. Desire
6. Affect / intensity
7. Qualitative difference
8. Line of flight
9. Authority label

### Added files

- `docs/BDP_002G_DIFFERENTIAL_READING_ENGINE.md`
- `prompts/BUCHANAN_DIFFERENTIAL_READING_SYSTEM_PROMPT.md`
- `data/templates/differential_analysis_card.schema.json`
- `data/templates/differential_analysis_card_social_media_feed.example.json`
- `frontend/differential_engine_panel.py`
- `scripts/update_bdp_002g_differential_engine.py`
- `scripts/verify_bdp_002g_differential_engine.py`

### Boundary

This phase does not create Buchanan-specific claims, insert citations, insert interpretations, mutate the database, or change the schema.

### Next recommended action

BDP-002G.1 — Wire the optional Differential Engine panel into The Dark Precursor after operator review, or test the template on one reviewed example.

## BDP-002H — Dark Precursor Style Split

**Status:** complete  
**Type:** frontend refactor  
**Updated:** 2026-06-15T03:18:11+00:00  

### What changed

- Moved the cinematic Streamlit CSS from `frontend/dark_precursor.py` into `frontend/styles/dark_precursor.css`.
- Added a local CSS loader in `frontend/dark_precursor.py`.
- Moved `render_differential_engine_panel()` so it executes after `st.set_page_config()`.

### Boundaries

- No database mutation.
- No SQL migration.
- No evidence spine change.
- No Buchanan claim or interpretation created.
- No generative prompt change.

### Next recommended step

BDP-002I — Decide where the Differential Reading Engine panel belongs inside the main Dark Precursor flow.


<!-- BDP-003C CINEMATIC EXPERIENCE RESET -->

## BDP-003C — Dark Precursor Cinematic Experience Reset

**Status:** Prepared  
**Updated:** 2026-06-15T03:26:40+00:00  
**Type:** Frontend / generative surface reset

### Summary

BDP-003C resets The Dark Precursor toward the intended cinematic experience:

- large readable narrator text.
- slower chunked reveal.
- simplified concept-first stage.
- cinematic treatment and storyboard / film clip brief modes.
- differential method mechanics embedded in the prompt.
- CSS isolated in `frontend/styles/dark_precursor.css`.
- no impersonation claim that the app is Ian Buchanan.
- no database mutation, SQL migration, evidence-spine change, interpretation insertion, or Buchanan-specific claim creation.

### Boundary

Film/video backend generation is not implemented in this slice. The patch creates the governed cinematic brief pathway only.

### Next Recommended Step

BDP-003D — Add cinematic concept card output persistence and optional image/video generation adapter boundary.
