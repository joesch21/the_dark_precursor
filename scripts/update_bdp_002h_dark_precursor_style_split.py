#!/usr/bin/env python3
"""Record BDP-002H Dark Precursor CSS split in system state and handover."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_CANDIDATES = [
    ROOT / "BUCHANAN_THREAD_HANDOVER.md",
    ROOT / "docs" / "BUCHANAN_THREAD_HANDOVER.md",
]
PHASE = "BDP-002H"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def update_state() -> None:
    if STATE_PATH.exists():
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    else:
        state = {
            "project": "buchanan_deleuze_intelligence_platform",
            "schema_version": "0.1.3",
        }

    phases = state.setdefault("phases", {})
    phases[PHASE] = {
        "status": "complete",
        "type": "frontend_refactor",
        "description": "Split Dark Precursor inline CSS into frontend/styles/dark_precursor.css and ensure page config runs before differential panel render.",
        "completed_at": utc_now(),
        "deliverables": [
            "docs/BDP_002H_DARK_PRECURSOR_STYLE_SPLIT.md",
            "frontend/styles/dark_precursor.css",
            "scripts/apply_bdp_002h_dark_precursor_style_split.py",
            "scripts/update_bdp_002h_dark_precursor_style_split.py",
            "scripts/verify_bdp_002h_dark_precursor_style_split.py",
        ],
        "boundaries": {
            "database_mutation": False,
            "sql_migration": False,
            "evidence_spine_change": False,
            "buchanan_claim": False,
            "interpretation": False,
            "generative_prompt_change": False,
        },
    }

    state["last_updated_phase"] = PHASE
    state["last_updated_utc"] = utc_now()
    state["next_recommended_step"] = (
        "BDP-002I — Decide where the Differential Reading Engine panel belongs "
        "inside the main Dark Precursor flow after verified CSS split."
    )

    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[OK] updated {STATE_PATH}")


def update_handover() -> None:
    existing = [path for path in HANDOVER_CANDIDATES if path.exists()]
    if not existing:
        existing = [ROOT / "BUCHANAN_THREAD_HANDOVER.md"]

    marker = "## BDP-002H — Dark Precursor Style Split"
    entry = f"""

{marker}

**Status:** complete  
**Type:** frontend refactor  
**Updated:** {utc_now()}  

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
"""

    for path in existing:
        path.parent.mkdir(parents=True, exist_ok=True)
        text = path.read_text(encoding="utf-8") if path.exists() else "# Buchanan Thread Handover\n"
        if marker not in text:
            path.write_text(text.rstrip() + entry + "\n", encoding="utf-8")
            print(f"[OK] updated {path}")
        else:
            print(f"[OK] handover already records {PHASE}: {path}")


def main() -> None:
    update_state()
    update_handover()


if __name__ == "__main__":
    main()
