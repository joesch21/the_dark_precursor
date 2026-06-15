#!/usr/bin/env python3
"""BDP-002H: split Dark Precursor inline CSS into frontend/styles/dark_precursor.css.

Run from the repository root:
    python3 scripts/apply_bdp_002h_dark_precursor_style_split.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "frontend" / "dark_precursor.py"
CSS_PATH = ROOT / "frontend" / "styles" / "dark_precursor.css"

DEFAULT_CSS = """.stApp {
    background-color: #050505;
    color: #e8e8e8;
}
.cinematic-wall {
    background-color: #0a0a0a;
    border: 1px solid #2a2a2a;
    border-radius: 10px;
    padding: 60px 80px;
    margin: 25px 0;
    box-shadow: 0 0 70px rgba(0,0,0,0.55);
}
.narrator-text {
    font-family: 'Georgia', serif;
    font-size: 1.55rem;
    line-height: 1.9;
    color: #e8e8e8;
    letter-spacing: 0.2px;
}
.section-label {
    font-family: 'Georgia', serif;
    color: #d4af37;
    font-size: 1.1rem;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
}
.stButton > button {
    background-color: #1a1a1a;
    color: #d4af37;
    border: 1px solid #3a3a3a;
}
.stButton > button:hover {
    background-color: #d4af37;
    color: #050505;
}
"""

STYLE_BLOCK_RE = re.compile(
    r"# === Cinematic \+ Sensual Minimalist Theme ===\s*\n"
    r"st\.markdown\(\"\"\"\s*\n"
    r"<style>\s*\n"
    r"(?P<css>.*?)"
    r"\n</style>\s*\n"
    r"\"\"\",\s*unsafe_allow_html=True\)\s*\n",
    re.DOTALL,
)

LOADER_BLOCK = '''# === Cinematic + Sensual Minimalist Theme ===
def load_local_css(relative_path: str) -> None:
    """Load a local CSS file into Streamlit."""
    css_path = Path(__file__).resolve().parent / relative_path
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>\\n{css}\\n</style>", unsafe_allow_html=True)
    else:
        st.warning(f"Stylesheet not found: {css_path}")

load_local_css("styles/dark_precursor.css")
'''

PANEL_BLOCK = '''
# ============================================================
# DIFFERENTIAL READING ENGINE PANEL
# ============================================================
render_differential_engine_panel()
'''


def ensure_target_exists() -> None:
    if not TARGET.exists():
        raise SystemExit(f"Missing target file: {TARGET}")


def extract_or_create_css(text: str) -> tuple[str, bool]:
    """Return updated Python text and whether a CSS block was extracted."""
    match = STYLE_BLOCK_RE.search(text)
    if not match:
        if not CSS_PATH.exists():
            CSS_PATH.parent.mkdir(parents=True, exist_ok=True)
            CSS_PATH.write_text(DEFAULT_CSS, encoding="utf-8")
        return text, False

    css = match.group("css").strip() + "\n"
    CSS_PATH.parent.mkdir(parents=True, exist_ok=True)
    CSS_PATH.write_text(css, encoding="utf-8")

    updated = text[: match.start()] + LOADER_BLOCK + "\n" + text[match.end() :]
    return updated, True


def ensure_panel_after_page_config(text: str) -> str:
    """Move render_differential_engine_panel() after page config/style load."""
    # Remove any standalone panel render calls. The import remains untouched.
    text = re.sub(r"\n\s*render_differential_engine_panel\(\)\s*\n", "\n\n", text)

    if "from differential_engine_panel import render_differential_engine_panel" not in text:
        return text

    if "render_differential_engine_panel()" in text:
        return text

    anchor = 'load_local_css("styles/dark_precursor.css")\n'
    if anchor in text:
        return text.replace(anchor, anchor + PANEL_BLOCK, 1)

    page_config_match = re.search(r"st\.set_page_config\([^\n]*\)\s*\n", text)
    if page_config_match:
        return text[: page_config_match.end()] + PANEL_BLOCK + text[page_config_match.end() :]

    raise SystemExit("Could not locate safe insertion point after st.set_page_config().")


def main() -> None:
    ensure_target_exists()

    original = TARGET.read_text(encoding="utf-8")
    updated, extracted = extract_or_create_css(original)
    updated = ensure_panel_after_page_config(updated)

    if updated != original:
        TARGET.write_text(updated, encoding="utf-8")

    print(f"[OK] stylesheet path: {CSS_PATH}")
    print(f"[OK] CSS {'extracted from inline block' if extracted else 'created/preserved'}")
    print(f"[OK] updated: {TARGET}")


if __name__ == "__main__":
    main()
