#!/usr/bin/env python3
"""Verify BDP-003C cinematic experience reset."""

from __future__ import annotations

import ast
import json
from pathlib import Path


REQUIRED_FILES = [
    Path("docs/BDP_003C_CINEMATIC_EXPERIENCE_RESET.md"),
    Path("frontend/dark_precursor.py"),
    Path("frontend/styles/dark_precursor.css"),
    Path("scripts/update_bdp_003c_cinematic_experience_reset.py"),
    Path("scripts/verify_bdp_003c_cinematic_experience_reset.py"),
]


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def verify_files() -> None:
    for path in REQUIRED_FILES:
        require(path.exists(), f"missing required file: {path}")


def verify_python_compile() -> None:
    for path in [
        Path("frontend/dark_precursor.py"),
        Path("scripts/update_bdp_003c_cinematic_experience_reset.py"),
        Path("scripts/verify_bdp_003c_cinematic_experience_reset.py"),
    ]:
        ast.parse(read(path), filename=str(path))


def verify_streamlit_order() -> None:
    text = read(Path("frontend/dark_precursor.py"))
    config_pos = text.find("st.set_page_config")
    require(config_pos >= 0, "st.set_page_config not found")

    render_markdown_pos = text.find("st.markdown(")
    require(render_markdown_pos >= 0, "st.markdown not found")
    require(
        config_pos < render_markdown_pos,
        "st.set_page_config must occur before visible Streamlit rendering",
    )

    require('load_local_css("styles/dark_precursor.css")' in text, "stylesheet loader call missing")
    require("render_differential_engine_panel()" in text, "differential panel optional render missing")


def verify_prompt_contract() -> None:
    text = read(Path("frontend/dark_precursor.py"))
    require("You are Ian Buchanan" not in text, "app must not impersonate Ian Buchanan")
    require("You are not Ian Buchanan" in text, "non-impersonation instruction missing")

    required_terms = [
        "assemblage",
        "flow",
        "cut",
        "interruption",
        "capture",
        "desire",
        "affect",
        "qualitative difference",
        "line of flight",
    ]
    lowered = text.lower()
    for term in required_terms:
        require(term in lowered, f"differential method term missing: {term}")

    for term in ["Storyboard / Film Clip Brief", "Film Clip Brief", "shot sequence"]:
        require(term in text, f"cinematic film/storyboard capacity missing: {term}")


def verify_css() -> None:
    css = read(Path("frontend/styles/dark_precursor.css"))
    for selector in [".dp-stage", ".dp-narrator-text", ".dp-hero", ".dp-title"]:
        require(selector in css, f"missing CSS selector: {selector}")

    require("clamp(2rem" in css or "clamp(2.0rem" in css, "large narrator font scale missing")
    require("styles/dark_precursor.css" not in css, "CSS file should not reference itself")


def verify_state() -> None:
    state_candidates = [
        Path("BUCHANAN_SYSTEM_STATE.json"),
        Path("ai_boot/BUCHANAN_SYSTEM_STATE.json"),
    ]
    existing = [p for p in state_candidates if p.exists()]
    require(existing, "no BUCHANAN_SYSTEM_STATE.json found after update script")

    found = False
    for path in existing:
        state = json.loads(read(path))
        if "bdp_003c_cinematic_experience_reset" in state:
            record = state["bdp_003c_cinematic_experience_reset"]
            require(record.get("database_mutation") is False, f"{path}: database boundary wrong")
            require(record.get("sql_migration") is False, f"{path}: sql boundary wrong")
            require(record.get("film_storyboard_brief_generation") is True, f"{path}: storyboard flag missing")
            found = True

    require(found, "BDP-003C state record not found")


def verify_docs() -> None:
    doc = read(Path("docs/BDP_003C_CINEMATIC_EXPERIENCE_RESET.md"))
    for phrase in [
        "large readable text",
        "slow conceptual reveal",
        "concept-to-scene translation",
        "film / storyboard brief",
        "No impersonation",
    ]:
        require(phrase in doc, f"documentation phrase missing: {phrase}")


def main() -> None:
    verify_files()
    verify_python_compile()
    verify_streamlit_order()
    verify_prompt_contract()
    verify_css()
    verify_docs()
    verify_state()
    print("[OK] BDP-003C cinematic experience reset verified")


if __name__ == "__main__":
    main()
