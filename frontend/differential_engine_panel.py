"""
BDP-002G Differential Engine Panel

Standalone Streamlit panel for The Dark Precursor.

This module is intentionally not auto-wired into frontend/dark_precursor.py.
Import and call render_differential_engine_panel() only after operator review.

Boundary:
- display only
- no database mutation
- no citation insertion
- no interpretation insertion
- no hidden personalisation
"""

from __future__ import annotations

from pathlib import Path
import json

try:
    import streamlit as st
except Exception:  # pragma: no cover - lets verifier import file without streamlit
    st = None


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "data" / "templates" / "differential_analysis_card.schema.json"
EXAMPLE_PATH = ROOT / "data" / "templates" / "differential_analysis_card_social_media_feed.example.json"
PROMPT_PATH = ROOT / "prompts" / "BUCHANAN_DIFFERENTIAL_READING_SYSTEM_PROMPT.md"


def _read_text(path: Path) -> str:
    if not path.exists():
        return f"[Missing file: {path}]"
    return path.read_text(encoding="utf-8")


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {"error": f"Missing file: {path}"}
    return json.loads(path.read_text(encoding="utf-8"))


def render_differential_engine_panel() -> None:
    """Render the BDP-002G differential reading engine contract panel."""
    if st is None:
        raise RuntimeError("streamlit is required to render this panel")

    st.subheader("Differential Reading Engine")
    st.caption(
        "Governed method layer. Display-only. Does not create Buchanan claims, "
        "citations, concept relations, or interpretations."
    )

    st.markdown(
        """
The platform is not merely a database. It is a differential reading engine.

**Operator rule:** Do not map everything. Find the cut. Follow the flow. Name the capture. Preserve the difference.
"""
    )

    with st.expander("Analysis template", expanded=True):
        st.markdown(
            """
1. **Assemblage** — what specific machine/system/practice is being analysed?
2. **Flow** — what is moving: desire, affect, attention, images, bodies, signs, data?
3. **Cut / subtraction** — what interruption, threshold, filter, or removal organizes the flow?
4. **Capture / extraction** — what value, attention, subjectivity, data, or intensity is captured?
5. **Desire** — what desire is being assembled, organized, or redirected?
6. **Affect / intensity** — what mood, charge, capacity, or body is produced?
7. **Qualitative difference** — what difference matters beyond material similarity?
8. **Line of flight** — where can the flow escape, mutate, or become otherwise?
9. **Authority label** — what evidence posture supports the analysis?
"""
        )

    with st.expander("Example card: social media image-feed", expanded=False):
        st.json(_read_json(EXAMPLE_PATH))

    with st.expander("LLM system prompt", expanded=False):
        st.code(_read_text(PROMPT_PATH), language="markdown")

    with st.expander("JSON schema", expanded=False):
        st.json(_read_json(SCHEMA_PATH))

    st.warning(
        "Boundary: this panel is methodological guidance only until connected to governed evidence. "
        "Do not present generated synthesis as Buchanan-specific authority."
    )
