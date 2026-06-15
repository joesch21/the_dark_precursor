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
