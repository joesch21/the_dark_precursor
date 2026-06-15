# BDP-002H — Dark Precursor Style Split

**Status:** Prepared patch slice  
**Type:** Frontend refactor  
**Interface:** `frontend/dark_precursor.py`  
**Authority:** display/refactor only  

## Purpose

The Dark Precursor currently embeds its cinematic theme CSS directly inside `frontend/dark_precursor.py`. This patch separates presentation from application logic by moving the style rules into:

```text
frontend/styles/dark_precursor.css
```

The Python file keeps only a small local stylesheet loader.

## Why This Matters

This keeps the interface easier to maintain as the Differential Reading Engine grows. The app logic should remain concerned with governed panels, prompts, evidence posture, and user interaction. Visual styling should live in a dedicated stylesheet.

## Refactor Contract

1. Preserve the existing visual theme.
2. Do not alter evidence, citations, concepts, relations, or interpretations.
3. Do not change the LLM prompt behaviour in this slice.
4. Ensure `st.set_page_config()` happens before any Streamlit rendering call.
5. Keep the differential engine panel display-only.

## Files Affected

- `frontend/dark_precursor.py`
- `frontend/styles/dark_precursor.css`
- `scripts/apply_bdp_002h_dark_precursor_style_split.py`
- `scripts/update_bdp_002h_dark_precursor_style_split.py`
- `scripts/verify_bdp_002h_dark_precursor_style_split.py`

## Governance Boundary

This patch is presentation structure only.

- Database mutation: **false**
- SQL migration: **false**
- Evidence spine change: **false**
- Buchanan claim creation: **false**
- Interpretation creation: **false**
- Generative prompt change: **false**

## Next Recommended Step

After verification, the next safe frontend step is to decide where the Differential Reading Engine panel should live in the main Dark Precursor flow: top-level panel, sidebar tool, governed reference panel, or result-card companion.
