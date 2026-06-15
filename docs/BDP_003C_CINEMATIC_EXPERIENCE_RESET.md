# BDP-003C — Dark Precursor Cinematic Experience Reset

**Status:** Prepared patch slice  
**Type:** Frontend / generative surface reset  
**Interface:** `frontend/dark_precursor.py`  
**Authority:** display + provisional cinematic synthesis only  
**Date:** June 2026

## 1. Purpose

BDP-003C corrects the Dark Precursor interface direction.

The interface should not feel like a document viewer with a small chat box. It should be an immersive cinematic conceptual stage: slow, readable, atmospheric, and capable of turning philosophical concepts into scenes, images, storyboard logic, and film-clip briefs.

The central user experience target is:

```text
easy cinematic style experience
large readable text
slow conceptual reveal
concept-to-scene translation
optional film / storyboard brief
governed evidence posture retained
```

## 2. Design Correction

The previous direction mixed too many panels too early. BDP-003C restores a single primary path:

```text
concept input
→ cinematic narrator response
→ differential trace
→ optional film / storyboard brief
→ governed status dock
```

The interface should feel like entering a conceptual cinema, not operating a dashboard.

## 3. Required Frontend Behaviours

1. **Large typography**
   - Narrator text must be large enough to read at distance.
   - The cinematic wall is the dominant surface.

2. **Slow reveal**
   - Text appears in paced chunks.
   - The operator can adjust reveal speed.

3. **Cinematic modes**
   - `Narrator`
   - `Cinematic Treatment`
   - `Storyboard / Film Clip Brief`

4. **Differential method embedded**
   Every generative response should be encouraged to trace:
   - assemblage
   - flow
   - cut / interruption
   - capture / extraction
   - desire
   - affect / intensity
   - qualitative difference
   - line of flight

5. **Governed posture**
   The interface may produce cinematic synthesis, but it must label that synthesis as provisional unless backed by the evidence spine.

6. **No impersonation**
   The platform must not literally claim to be Ian Buchanan. It can use a Buchanan-informed governed voice, but should not impersonate him.

## 4. Film Clip Capacity

BDP-003C does **not** add a video-generation backend.

It adds the interface and prompt contract needed to produce:

```text
cinematic treatment
shot list
visual palette
sound design notes
image / video generation prompt
conceptual explanation
governed evidence posture
```

Future phases may connect this to ComfyUI, Flux, Runway, local video models, or other controlled generation tools.

## 5. Files Affected

```text
frontend/dark_precursor.py
frontend/styles/dark_precursor.css
scripts/update_bdp_003c_cinematic_experience_reset.py
scripts/verify_bdp_003c_cinematic_experience_reset.py
```

## 6. Governance Boundary

```text
database_mutation = false
sql_migration = false
evidence_spine_change = false
source_ingestion = false
citation_creation = false
concept_relation_creation = false
interpretation_insertion = false
buchanan_specific_claim_creation = false
reader_state_tracking = false
psychological_assessment = false
frontend_reset = true
generative_surface_prompt_change = true
cinematic_synthesis_label_required = true
```

## 7. Verification Requirements

The verifier must confirm:

1. CSS is loaded from `frontend/styles/dark_precursor.css`.
2. `st.set_page_config()` occurs before visible Streamlit rendering.
3. Narrator font scale is large in the stylesheet.
4. The app contains cinematic modes.
5. The prompt contains differential method mechanics.
6. The app does not contain `You are Ian Buchanan`.
7. The app includes a film/storyboard brief path.
8. The phase is recorded in system state.

## 8. Next Recommended Step

After BDP-003C verifies, the next safe slice is:

```text
BDP-003E — Define cinematic concept card persistence and optional image/video generation adapter boundary.
```

This should still be governed and should not auto-promote cinematic synthesis into evidence.
