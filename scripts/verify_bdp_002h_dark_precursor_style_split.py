#!/usr/bin/env python3
"""Verify BDP-002H Dark Precursor CSS split."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "frontend" / "dark_precursor.py"
CSS_PATH = ROOT / "frontend" / "styles" / "dark_precursor.css"
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_CANDIDATES = [
    ROOT / "BUCHANAN_THREAD_HANDOVER.md",
    ROOT / "docs" / "BUCHANAN_THREAD_HANDOVER.md",
]


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def verify_files() -> tuple[str, str]:
    require(TARGET.exists(), f"missing {TARGET}")
    require(CSS_PATH.exists(), f"missing {CSS_PATH}")
    py_text = TARGET.read_text(encoding="utf-8")
    css_text = CSS_PATH.read_text(encoding="utf-8")
    return py_text, css_text


def verify_css(py_text: str, css_text: str) -> None:
    require("load_local_css" in py_text, "dark_precursor.py must define/use load_local_css")
    require('load_local_css("styles/dark_precursor.css")' in py_text, "dark_precursor.py must load styles/dark_precursor.css")
    require("# === Cinematic + Sensual Minimalist Theme ===" in py_text, "theme marker missing")

    inline_theme = re.search(
        r"# === Cinematic \+ Sensual Minimalist Theme ===\s*\n\s*st\.markdown\(\"\"\"\s*\n\s*<style>",
        py_text,
    )
    require(inline_theme is None, "inline theme <style> block still exists in dark_precursor.py")

    for token in [
        ".stApp",
        ".cinematic-wall",
        ".narrator-text",
        ".section-label",
        ".stButton > button",
    ]:
        require(token in css_text, f"CSS token missing from stylesheet: {token}")


def verify_streamlit_order(py_text: str) -> None:
    page_config_index = py_text.find("st.set_page_config")
    render_index = py_text.find("render_differential_engine_panel()")
    loader_call_index = py_text.find('load_local_css("styles/dark_precursor.css")')

    require(page_config_index != -1, "st.set_page_config not found")
    require(render_index != -1, "render_differential_engine_panel() call not found")
    require(loader_call_index != -1, "local stylesheet loader call not found")
    require(page_config_index < loader_call_index, "st.set_page_config must run before CSS loader")
    require(page_config_index < render_index, "st.set_page_config must run before differential panel render")
    require(loader_call_index < render_index, "stylesheet should load before differential panel render")


def verify_python_syntax(py_text: str) -> None:
    try:
        ast.parse(py_text, filename=str(TARGET))
    except SyntaxError as exc:
        fail(f"Python syntax error in {TARGET}: {exc}")


def verify_state_and_handover() -> None:
    require(STATE_PATH.exists(), f"missing {STATE_PATH}; run update script")
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    phase = state.get("phases", {}).get("BDP-002H")
    require(isinstance(phase, dict), "BUCHANAN_SYSTEM_STATE.json missing phases.BDP-002H; run update script")
    require(phase.get("status") == "complete", "BDP-002H status must be complete")
    require(phase.get("boundaries", {}).get("database_mutation") is False, "BDP-002H must record database_mutation false")
    require(phase.get("boundaries", {}).get("sql_migration") is False, "BDP-002H must record sql_migration false")

    handovers = [path for path in HANDOVER_CANDIDATES if path.exists()]
    require(bool(handovers), "no BUCHANAN_THREAD_HANDOVER.md found")
    require(
        any("BDP-002H — Dark Precursor Style Split" in path.read_text(encoding="utf-8") for path in handovers),
        "handover missing BDP-002H entry; run update script",
    )


def main() -> None:
    py_text, css_text = verify_files()
    verify_css(py_text, css_text)
    verify_streamlit_order(py_text)
    verify_python_syntax(py_text)
    verify_state_and_handover()
    print("[OK] BDP-002H Dark Precursor CSS split verified")


if __name__ == "__main__":
    main()
