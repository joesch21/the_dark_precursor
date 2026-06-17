# BDP-003F.5 — Dark Precursor Navigation Wiring

**Status:** Complete  
**Controlled slice:** minimal frontend navigation wiring only  
**App target:** `frontend/dark_precursor.py`

## Purpose

BDP-003F.5 wires the already-approved navigation architecture into the existing Dark Precursor frontend.

This phase converts the current raw Streamlit session-state surface strings into explicit governed surface constants and helper functions.

It does not add pages.

It does not add a dashboard.

It does not add backend/database/evidence/citation/interpretation/concept-relation work.

## Launch authority

The verified launch authority is README/docs.

The verified launch method is:

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
. ./venv/bin/activate
python -m streamlit run frontend/dark_precursor.py
```

The app target remains:

```text
frontend/dark_precursor.py
```

## Implemented frontend wiring

BDP-003F.5 adds explicit approved surface keys:

```python
SURFACE_STAGE = "stage"
SURFACE_ABOUT = "about"
APPROVED_DARK_PRECURSOR_SURFACES = {SURFACE_STAGE, SURFACE_ABOUT}
```

It adds governed surface helpers:

```python
def get_dark_precursor_surface() -> str:
    surface = st.session_state.get("dark_precursor_view", SURFACE_STAGE)
    if surface not in APPROVED_DARK_PRECURSOR_SURFACES:
        return SURFACE_STAGE
    return surface


def set_dark_precursor_surface(surface_key: str) -> None:
    if surface_key not in APPROVED_DARK_PRECURSOR_SURFACES:
        raise ValueError(f"Unsupported Dark Precursor surface: {surface_key}")
    st.session_state["dark_precursor_view"] = surface_key
```

The About button and Return to concept stage button now route through those helpers.

The About route check now uses:

```python
get_dark_precursor_surface() == SURFACE_ABOUT
```

## Explicit non-changes

BDP-003F.5 does not add new public pages, dashboard surfaces, backend services, adapter endpoints, database tables, SQL migrations, archive workflow expansion, evidence promotion, citations, concept relations, interpretations, or Buchanan-specific claims.

It does not introduce hidden adaptive navigation or personalized navigation.

## Verification

Verifier:

```text
scripts/verify_bdp_003f5_navigation_wiring.py
```
