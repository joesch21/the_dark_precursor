# BDP-003D — Cinematic Video Front Page

**Status:** Implemented / verified
**Interface:** `frontend/dark_precursor.py`
**Stylesheet:** `frontend/styles/dark_precursor.css`

## Purpose

This slice reworks the Dark Precursor front page so the interface feels less like a dark utility dashboard and more like an easy cinematic entry experience.

The intended change is visual and interaction-level only:

1. Use `frontend/assets/dark_precursor.mp4` as a fitted background stream.
2. Add a title-gate page before the main concept interface starts.
3. Reduce the sidebar/taskbar darkness so it sits over the cinematic field rather than blocking it.
4. Bring Streamlit controls closer to the same serif cinematic typography used by the stage.
5. Preserve the existing governed prompt contract and evidence boundaries.

## Boundary

This patch does not:

- mutate the database
- insert citations
- create Buchanan-specific claims
- alter the evidence spine
- generate video files
- change the LLM prompt authority model

The background video is atmosphere only. It must not be treated as evidence or as part of the conceptual authority layer.

## UX Contract

The front page opens with a title gate:

- The video stream plays behind the opening panel when `frontend/assets/dark_precursor.mp4` exists.
- If the video file is missing, the page falls back to the existing cinematic gradient field.
- The operator enters the main interface with `Enter the Vault`.
- The sidebar includes `Return to title page` for resetting the experience.

## Implementation Notes

- The local MP4 is encoded as a browser-safe data URI using Streamlit cache.
- The CSS uses fixed video coverage with `object-fit: cover`.
- Sidebar and header styling are softened with translucent panels and blur.
- Large readable Georgia-based typography remains the primary visual language.

## Verification

Run from the repository root:

```bash
python3 -m py_compile frontend/dark_precursor.py
streamlit run frontend/dark_precursor.py
```

Then verify manually:

1. The title gate appears before the main interface.
2. The background video fills the viewport without distortion.
3. The sidebar is lighter, translucent, and visually consistent with the page font.
4. Entering the Vault reveals the existing concept interface.
5. Returning to the title page works from the sidebar.
6. Missing video asset still produces a usable fallback page.

## Documentation Follow-up

Completed in BDP-003D.2:

- `BUCHANAN_THREAD_HANDOVER.md` updated.
- `BUCHANAN_SYSTEM_STATE.json` updated.
- `scripts/verify_bdp_003d_cinematic_video_front_page.py` added.

## Closeout Status

BDP-003D is now treated as the completed cinematic video front page slice.

The next feature slice is no longer BDP-003D. It is:

```text
BDP-003E — Define cinematic concept card persistence and optional image/video generation adapter boundary.
```
