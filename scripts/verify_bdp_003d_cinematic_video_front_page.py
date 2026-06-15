#!/usr/bin/env python3
"""
BDP-003D — Cinematic Video Front Page verifier.

This verifier confirms that the committed Dark Precursor frontend contains the
cinematic video/title-gate behaviours documented by BDP-003D, without treating
video atmosphere as evidence or adding generation backend authority.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

APP = ROOT / "frontend" / "dark_precursor.py"
CSS = ROOT / "frontend" / "styles" / "dark_precursor.css"
DOC = ROOT / "docs" / "BDP_003D_CINEMATIC_VIDEO_FRONT_PAGE.md"
STATE = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER = ROOT / "BUCHANAN_THREAD_HANDOVER.md"

required_files = [APP, CSS, DOC, STATE, HANDOVER]
missing = [str(p.relative_to(ROOT)) for p in required_files if not p.exists()]
if missing:
    raise SystemExit(f"[FAIL] Missing required files: {missing}")

app = APP.read_text(encoding="utf-8")
css = CSS.read_text(encoding="utf-8")
doc = DOC.read_text(encoding="utf-8")
state_text = STATE.read_text(encoding="utf-8")
handover = HANDOVER.read_text(encoding="utf-8")
state = json.loads(state_text)

checks = {
    "video_data_uri_loader": "def load_video_data_uri" in app and "data:video/mp4;base64" in app,
    "background_stream_renderer": "def render_background_stream" in app and "assets/dark_precursor.mp4" in app,
    "video_element_present": "dp-background-video" in app and "<video" in app,
    "fallback_present": "dp-background-fallback" in app,
    "slow_video_rate": "playbackRate = 0.42" in app,
    "title_gate_state": "dark_precursor_gate_open" in app,
    "enter_vault_button": "Enter the Vault" in app,
    "return_title_button": "Return to title page" in app,
    "bdp_003d_caption": "BDP-003D" in app,
    "css_phase_marker": "BDP-003D" in css,
    "css_video_cover": ".dp-background-video" in css and "object-fit: cover" in css,
    "css_title_gate": ".dp-title-gate" in css and ".dp-title-panel" in css,
    "css_large_gate_title": ".dp-gate-title" in css and "clamp(4.2rem" in css,
    "doc_implemented": "Implemented / verified" in doc,
    "doc_boundary_video_not_evidence": "The background video is atmosphere only" in doc,
    "state_phase_recorded": "bdp_003d_cinematic_video_front_page" in state,
    "state_next_bdp_003e": "BDP-003E" in state.get("next_recommended_step", ""),
    "handover_phase_recorded": "BDP-003D.2" in handover and "cinematic video front page closeout" in handover.lower(),
    "no_impersonation": "You are Ian Buchanan" not in app,
    "no_video_backend_claim": "This phase does not generate video files directly" in app,
}

failed = [name for name, ok in checks.items() if not ok]

if failed:
    print("=== BDP-003D verifier failures ===")
    for name in failed:
        print(f"[FAIL] {name}")
    raise SystemExit(1)

print("[OK] BDP-003D cinematic video front page verified")
