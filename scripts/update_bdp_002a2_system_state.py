#!/usr/bin/env python3
"""Record BDP-002A.2 in ai_boot/BUCHANAN_SYSTEM_STATE.json.

This script updates repository state only. It does not touch the database.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "ai_boot" / "BUCHANAN_SYSTEM_STATE.json"

RECORD = {
    "phase": "BDP-002A.2",
    "title": "Record psycho-linguistic semantic architecture doctrine",
    "type": "doctrine_only",
    "database_mutation": False,
    "sql_migration": False,
    "new_tables": False,
    "reader_state_tracking": False,
    "psycho_linguistic_tables": False,
    "buchanan_specific_claim": False,
    "generated_interpretation": False,
    "frontend_renderer": False,
    "doctrine_file": "docs/BUCHANAN_PSYCHOLINGUISTIC_SEMANTIC_ARCHITECTURE.md",
    "governance_boundary": [
        "citation authority outranks model inference",
        "psycho-linguistic observation is not citation authority",
        "LLM inference is not consciousness, mind-reading, or psychological certainty",
        "reader/listener transformation modelling requires later explicit governance",
        "no Buchanan-specific claim without exact passage, citation, and concept link",
    ],
    "next_step": "BDP-001N — Review first Buchanan passage candidate locator and short text, without inserting citation or interpretation.",
}


def main() -> None:
    if not STATE_PATH.exists():
        raise SystemExit(f"Missing state file: {STATE_PATH}")

    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    doctrine_records = state.setdefault("doctrine_records", {})
    doctrine_records["BDP-002A.2"] = {**RECORD, "recorded_at": now}

    # Keep additive, explicit breadcrumbs without assuming the existing state schema.
    state["last_buchanan_platform_phase"] = "BDP-002A.2"
    state["last_buchanan_platform_phase_title"] = RECORD["title"]
    state["last_updated_utc"] = now

    recent = state.setdefault("recent_phase_notes", [])
    note = {
        "phase": "BDP-002A.2",
        "summary": "Recorded psycho-linguistic semantic architecture doctrine as a no-migration, no-database-mutation governance slice.",
        "recorded_at": now,
    }
    if not any(item.get("phase") == "BDP-002A.2" for item in recent if isinstance(item, dict)):
        recent.append(note)

    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Recorded BDP-002A.2 in ai_boot/BUCHANAN_SYSTEM_STATE.json")


if __name__ == "__main__":
    main()
