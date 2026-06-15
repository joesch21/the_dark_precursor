#!/usr/bin/env python3
"""
BDP-002G updater.

Updates BUCHANAN_SYSTEM_STATE.json and BUCHANAN_THREAD_HANDOVER.md after applying
the differential reading engine contract patch.

No database access. No SQL migration. No interpretation insertion.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"

PHASE = "BDP-002G"
TITLE = "Add differential reading engine contract"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {
            "project": "buchanan_deleuze_intelligence_platform",
            "schema_version": "0.1.3",
            "phases": {},
        }
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def write_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_state() -> None:
    state = load_state()
    updated_at = now_iso()

    phase_record = {
        "phase": PHASE,
        "title": TITLE,
        "status": "complete",
        "type": "doctrine_application_contract",
        "updated_at": updated_at,
        "summary": (
            "Records the platform as a differential reading engine: a governed method "
            "for tracing assemblage, flow, cut, capture, desire, affect, qualitative "
            "difference, and line of flight."
        ),
        "deliverables": [
            "docs/BDP_002G_DIFFERENTIAL_READING_ENGINE.md",
            "prompts/BUCHANAN_DIFFERENTIAL_READING_SYSTEM_PROMPT.md",
            "data/templates/differential_analysis_card.schema.json",
            "data/templates/differential_analysis_card_social_media_feed.example.json",
            "frontend/differential_engine_panel.py",
            "scripts/update_bdp_002g_differential_engine.py",
            "scripts/verify_bdp_002g_differential_engine.py",
        ],
        "boundaries": {
            "database_mutation": False,
            "sql_migration": False,
            "schema_change": False,
            "canonical_passage_insertion": False,
            "citation_insertion": False,
            "concept_mention_insertion": False,
            "concept_relation_insertion": False,
            "interpretation_insertion": False,
            "buchanan_specific_claim": False,
            "frontend_auto_wiring": False,
            "hidden_personalisation": False,
            "psychological_assessment": False,
        },
        "authority_boundary": {
            "evidence_spine_remains_primary": True,
            "model_inference_does_not_override_citation": True,
            "generated_synthesis_must_be_labelled": True,
            "buchanan_specific_claim_requires_exact_evidence": True,
        },
        "method_fields": [
            "assemblage",
            "flow",
            "cut_or_subtraction",
            "capture_or_extraction",
            "desire",
            "affect_or_intensity",
            "qualitative_difference",
            "line_of_flight",
            "authority_label",
        ],
        "operator_rule": "Do not map everything. Find the cut. Follow the flow. Name the capture. Preserve the difference.",
        "next_recommended_action": (
            "BDP-002G.1 — Wire the optional Differential Engine panel into The Dark "
            "Precursor after operator review, or test the template on one reviewed example."
        ),
    }

    state.setdefault("phases", {})
    state["phases"][PHASE] = phase_record
    state["bdp_002g_differential_reading_engine"] = phase_record
    state["last_updated_phase"] = PHASE
    state["last_updated_utc"] = updated_at
    state["next_recommended_step"] = phase_record["next_recommended_action"]

    write_state(state)


def update_handover() -> None:
    marker = "<!-- BDP-002G DIFFERENTIAL READING ENGINE -->"
    updated_at = now_iso()
    section = f"""
{marker}

## {PHASE} — {TITLE}

**Status:** Complete  
**Updated:** {updated_at}  
**Type:** Doctrine and application contract  
**Database mutation:** No  
**SQL migration:** No  
**Frontend auto-wiring:** No  

### What changed

BDP-002G records the core platform thesis:

> The Buchanan / Deleuze Intelligence Platform is not merely a database. It is a differential reading engine.

The patch adds the governed method for tracing:

1. Assemblage
2. Flow
3. Cut / subtraction
4. Capture / extraction
5. Desire
6. Affect / intensity
7. Qualitative difference
8. Line of flight
9. Authority label

### Added files

- `docs/BDP_002G_DIFFERENTIAL_READING_ENGINE.md`
- `prompts/BUCHANAN_DIFFERENTIAL_READING_SYSTEM_PROMPT.md`
- `data/templates/differential_analysis_card.schema.json`
- `data/templates/differential_analysis_card_social_media_feed.example.json`
- `frontend/differential_engine_panel.py`
- `scripts/update_bdp_002g_differential_engine.py`
- `scripts/verify_bdp_002g_differential_engine.py`

### Boundary

This phase does not create Buchanan-specific claims, insert citations, insert interpretations, mutate the database, or change the schema.

### Next recommended action

BDP-002G.1 — Wire the optional Differential Engine panel into The Dark Precursor after operator review, or test the template on one reviewed example.
"""

    if HANDOVER_PATH.exists():
        text = HANDOVER_PATH.read_text(encoding="utf-8")
        if marker in text:
            before = text.split(marker)[0].rstrip()
            HANDOVER_PATH.write_text(before + "\n\n" + section.lstrip(), encoding="utf-8")
        else:
            HANDOVER_PATH.write_text(text.rstrip() + "\n\n" + section.lstrip(), encoding="utf-8")
    else:
        HANDOVER_PATH.write_text("# Buchanan Thread Handover\n\n" + section.lstrip(), encoding="utf-8")


def main() -> None:
    update_state()
    update_handover()
    print("[OK] BDP-002G state and handover updated")


if __name__ == "__main__":
    main()
