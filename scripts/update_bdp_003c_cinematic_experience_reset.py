#!/usr/bin/env python3
"""Record BDP-003C cinematic experience reset in state and handover docs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


PHASE_KEY = "bdp_003c_cinematic_experience_reset"
PHASE_RECORD = {
    "phase": "BDP-003C",
    "title": "Dark Precursor cinematic experience reset",
    "status": "prepared",
    "type": "frontend_generative_surface_reset",
    "database_mutation": False,
    "sql_migration": False,
    "evidence_spine_change": False,
    "buchanan_specific_claim_creation": False,
    "interpretation_insertion": False,
    "reader_state_tracking": False,
    "psychological_assessment": False,
    "frontend_reset": True,
    "generative_surface_prompt_change": True,
    "film_clip_backend_integration": False,
    "film_storyboard_brief_generation": True,
    "deliverables": [
        "docs/BDP_003C_CINEMATIC_EXPERIENCE_RESET.md",
        "frontend/dark_precursor.py",
        "frontend/styles/dark_precursor.css",
        "scripts/update_bdp_003c_cinematic_experience_reset.py",
        "scripts/verify_bdp_003c_cinematic_experience_reset.py",
    ],
    "next_recommended_step": "BDP-003D — Add cinematic concept card output persistence and optional image/video generation adapter boundary.",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def state_paths() -> list[Path]:
    return [
        Path("BUCHANAN_SYSTEM_STATE.json"),
        Path("ai_boot/BUCHANAN_SYSTEM_STATE.json"),
    ]


def update_state(path: Path) -> None:
    if path.exists():
        state = json.loads(path.read_text(encoding="utf-8"))
    else:
        state = {
            "project": "buchanan_deleuze_intelligence_platform",
            "created_by": "BDP-003C update script",
        }

    record = dict(PHASE_RECORD)
    record["updated_at"] = now_iso()

    state[PHASE_KEY] = record
    phases = state.setdefault("phases", {})
    phases["BDP-003C"] = {
        "status": "prepared",
        "type": "frontend_generative_surface_reset",
        "description": PHASE_RECORD["title"],
        "updated_at": record["updated_at"],
        "boundaries": {
            "database_mutation": False,
            "sql_migration": False,
            "evidence_spine_change": False,
            "buchanan_specific_claim_creation": False,
            "actual_video_generation_backend": False,
        },
    }
    state["last_updated_phase"] = "BDP-003C"
    state["next_recommended_step"] = PHASE_RECORD["next_recommended_step"]

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[OK] updated {path}")


def handover_paths() -> list[Path]:
    return [
        Path("BUCHANAN_THREAD_HANDOVER.md"),
        Path("docs/BUCHANAN_THREAD_HANDOVER.md"),
    ]


def update_handover(path: Path) -> None:
    marker = "<!-- BDP-003C CINEMATIC EXPERIENCE RESET -->"
    section = f"""
{marker}

## BDP-003C — Dark Precursor Cinematic Experience Reset

**Status:** Prepared  
**Updated:** {now_iso()}  
**Type:** Frontend / generative surface reset

### Summary

BDP-003C resets The Dark Precursor toward the intended cinematic experience:

- large readable narrator text.
- slower chunked reveal.
- simplified concept-first stage.
- cinematic treatment and storyboard / film clip brief modes.
- differential method mechanics embedded in the prompt.
- CSS isolated in `frontend/styles/dark_precursor.css`.
- no impersonation claim that the app is Ian Buchanan.
- no database mutation, SQL migration, evidence-spine change, interpretation insertion, or Buchanan-specific claim creation.

### Boundary

Film/video backend generation is not implemented in this slice. The patch creates the governed cinematic brief pathway only.

### Next Recommended Step

BDP-003D — Add cinematic concept card output persistence and optional image/video generation adapter boundary.
"""

    existing = path.read_text(encoding="utf-8") if path.exists() else "# Buchanan Thread Handover\n"
    if marker in existing:
        before = existing.split(marker)[0].rstrip()
        existing = before + "\n\n" + section
    else:
        existing = existing.rstrip() + "\n\n" + section

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(existing.rstrip() + "\n", encoding="utf-8")
    print(f"[OK] updated {path}")


def main() -> None:
    updated_any_state = False
    for path in state_paths():
        if path.exists():
            update_state(path)
            updated_any_state = True

    if not updated_any_state:
        update_state(Path("BUCHANAN_SYSTEM_STATE.json"))

    updated_any_handover = False
    for path in handover_paths():
        if path.exists():
            update_handover(path)
            updated_any_handover = True

    if not updated_any_handover:
        update_handover(Path("BUCHANAN_THREAD_HANDOVER.md"))


if __name__ == "__main__":
    main()
