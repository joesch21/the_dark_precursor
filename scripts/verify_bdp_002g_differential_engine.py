#!/usr/bin/env python3
"""
Verifier for BDP-002G Differential Reading Engine Contract.

This verifier checks only filesystem and state documentation.
It does not access the database.
"""

from __future__ import annotations

from pathlib import Path
import ast
import json
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/BDP_002G_DIFFERENTIAL_READING_ENGINE.md",
    "prompts/BUCHANAN_DIFFERENTIAL_READING_SYSTEM_PROMPT.md",
    "data/templates/differential_analysis_card.schema.json",
    "data/templates/differential_analysis_card_social_media_feed.example.json",
    "frontend/differential_engine_panel.py",
    "scripts/update_bdp_002g_differential_engine.py",
    "scripts/verify_bdp_002g_differential_engine.py",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    sys.exit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def read(path: str) -> str:
    full = ROOT / path
    if not full.exists():
        fail(f"missing required file: {path}")
    return full.read_text(encoding="utf-8")


def verify_files() -> None:
    for path in REQUIRED_FILES:
        if not (ROOT / path).exists():
            fail(f"missing required file: {path}")
    ok("required files exist")


def verify_doctrine() -> None:
    text = read("docs/BDP_002G_DIFFERENTIAL_READING_ENGINE.md")
    required_phrases = [
        "differential reading engine",
        "assemblage",
        "flow",
        "cut",
        "capture",
        "desire",
        "affect",
        "qualitative difference",
        "line of flight",
        "evidence spine remains primary",
        "Model inference never outranks citation",
    ]
    missing = [phrase for phrase in required_phrases if phrase.lower() not in text.lower()]
    if missing:
        fail(f"doctrine missing phrases: {missing}")
    ok("doctrine contains differential engine contract")


def verify_prompt() -> None:
    text = read("prompts/BUCHANAN_DIFFERENTIAL_READING_SYSTEM_PROMPT.md")
    required = [
        "Do not map everything",
        "Find the cut",
        "Follow the flow",
        "Name the capture",
        "Preserve the difference",
        "authority label",
    ]
    missing = [phrase for phrase in required if phrase.lower() not in text.lower()]
    if missing:
        fail(f"prompt missing phrases: {missing}")
    ok("LLM prompt contract verified")


def verify_schema_and_example() -> None:
    schema_path = ROOT / "data/templates/differential_analysis_card.schema.json"
    example_path = ROOT / "data/templates/differential_analysis_card_social_media_feed.example.json"

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    example = json.loads(example_path.read_text(encoding="utf-8"))

    for field in schema.get("required", []):
        if field not in example:
            fail(f"example card missing schema-required field: {field}")

    if example["evidence_posture"]["buchanan_specific_claim_authorized"] is not False:
        fail("example must not authorize Buchanan-specific claim")

    if example["authority_label"] != "system_synthesis_example_not_buchanan_claim":
        fail("example authority label must block Buchanan-specific authority")

    ok("schema and example card verified")


def verify_frontend_module_syntax() -> None:
    path = ROOT / "frontend/differential_engine_panel.py"
    ast.parse(path.read_text(encoding="utf-8"))
    ok("frontend panel module syntax verified")


def verify_state_if_present() -> None:
    state_path = ROOT / "BUCHANAN_SYSTEM_STATE.json"
    if not state_path.exists():
        ok("state file not present; updater can create it")
        return

    state = json.loads(state_path.read_text(encoding="utf-8"))
    record = state.get("phases", {}).get("BDP-002G") or state.get("bdp_002g_differential_reading_engine")
    if not record:
        fail("BDP-002G missing from BUCHANAN_SYSTEM_STATE.json; run scripts/update_bdp_002g_differential_engine.py first")

    boundaries = record.get("boundaries", {})
    for key in [
        "database_mutation",
        "sql_migration",
        "citation_insertion",
        "concept_relation_insertion",
        "interpretation_insertion",
        "buchanan_specific_claim",
    ]:
        if boundaries.get(key) is not False:
            fail(f"state boundary must be false: {key}")

    ok("state boundary record verified")


def verify_handover_if_present() -> None:
    path = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
    if not path.exists():
        ok("handover not present; updater can create it")
        return

    text = path.read_text(encoding="utf-8")
    if "BDP-002G" not in text or "differential reading engine" not in text.lower():
        fail("handover missing BDP-002G differential reading engine section")
    ok("handover record verified")


def main() -> None:
    verify_files()
    verify_doctrine()
    verify_prompt()
    verify_schema_and_example()
    verify_frontend_module_syntax()
    verify_state_if_present()
    verify_handover_if_present()
    print("[OK] BDP-002G differential reading engine contract verified")


if __name__ == "__main__":
    main()
