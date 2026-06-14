#!/usr/bin/env python3
"""
BDP-002D.1 verifier — Interaction Adaptation vs Text Psycho-Linguistics Boundary.

Verifies docs/state only.
No DB connection required.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path.cwd()

REQUIRED_DOCS = [
    ROOT / "docs" / "BDP_002D1_INTERACTION_ADAPTATION_VS_TEXT_PSYCHOLINGUISTICS.md",
    ROOT / "docs" / "BDP_002D_RELATIONAL_ADAPTIVE_PRESENTATION.md",
    ROOT / "docs" / "BUCHANAN_SEMANTIC_WORKBENCH.md",
    ROOT / "docs" / "BUCHANAN_PSYCHOLINGUISTIC_SEMANTIC_ARCHITECTURE.md",
    ROOT / "docs" / "BUCHANAN_ARCHITECTURE.md",
    ROOT / "docs" / "BUCHANAN_THREAD_HANDOVER.md",
]

STATE_PATH = ROOT / "ai_boot" / "BUCHANAN_SYSTEM_STATE.json"

REQUIRED_PHRASES = [
    "Text Psycho-Linguistics",
    "Interaction Adaptation",
    "Focus: how language moves, pressures, and transforms meaning in the texts",
    "Focus: how the interface responds to the user's engagement style during a session",
    "Allowed signals: navigation choices, time spent on visuals vs text, question style, metaphor preference, depth of exploration",
    "does not analyse psychological state or cognitive profile",
    "How this view is adapting",
    "what interaction signals were observed",
    "inspect, pause, reset, or manually adjust",
    "session_scoped_by_default = true",
    "long_term_profile_storage_default = false",
    "persistence_requires_explicit_informed_consent = true",
    "psychological_assessment_allowed = false",
    "objective_psychological_insight_claim_allowed = false",
    "psycho_linguistic_analysis_remains_text_focused = true",
]

STATE_KEY = "bdp_002d1_interaction_adaptation_vs_text_psycholinguistics"

BAD_PATTERNS = [
    r"psychological assessment allowed\s*=\s*true",
    r"psychological_state_analysis_allowed[\"']?\s*:\s*true",
    r"cognitive_profile_analysis_allowed[\"']?\s*:\s*true",
    r"long_term_user_profile_storage[\"']?\s*:\s*true",
    r"reader_state_tracking[\"']?\s*:\s*true",
    r"objective_psychological_insight_claim_allowed[\"']?\s*:\s*true",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def check_docs() -> None:
    missing = [str(path) for path in REQUIRED_DOCS if not path.exists()]
    if missing:
        fail("missing required docs: " + ", ".join(missing))

    for path in REQUIRED_DOCS:
        text = path.read_text()
        for phrase in REQUIRED_PHRASES:
            if phrase not in text:
                fail(f"{path} missing required phrase: {phrase}")
        ok(f"{path} contains BDP-002D.1 boundary text")

    combined = "\n".join(path.read_text() for path in REQUIRED_DOCS)
    lower = combined.lower()

    for pattern in BAD_PATTERNS:
        if re.search(pattern, lower, flags=re.IGNORECASE):
            fail(f"blocked governance inversion found: {pattern}")

    ok("docs contain no blocked governance inversion")


def check_state() -> None:
    if not STATE_PATH.exists():
        fail(f"missing state file: {STATE_PATH}")

    state = json.loads(STATE_PATH.read_text())
    entry = state.get(STATE_KEY)

    if not isinstance(entry, dict):
        fail(f"missing state entry: {STATE_KEY}")

    required_false = [
        "database_mutation",
        "sql_migration",
        "schema_change",
        "frontend_implementation",
        "reader_state_tracking",
        "long_term_user_profile_storage",
        "psychological_assessment",
        "buchanan_specific_claim",
        "generated_interpretation",
    ]

    for key in required_false:
        if entry.get(key) is not False:
            fail(f"state {STATE_KEY}.{key} must be false")

    adaptation = entry.get("interaction_adaptation", {})
    checks = {
        "explanatory_layer_required": True,
        "inspect_pause_reset_override_required": True,
        "session_scoped_by_default": True,
        "persistence_requires_explicit_informed_consent": True,
        "psychological_state_analysis_allowed": False,
        "cognitive_profile_analysis_allowed": False,
        "objective_psychological_insight_claim_allowed": False,
    }

    for key, expected in checks.items():
        if adaptation.get(key) is not expected:
            fail(f"state interaction_adaptation.{key} expected {expected}")

    text_layer = entry.get("text_psycholinguistics", {})
    if text_layer.get("authority_label") != "experimental_modelling":
        fail("text psycholinguistics authority label must be experimental_modelling")
    if text_layer.get("linked_to_governed_passage_locator") is not True:
        fail("text psycholinguistics must require governed passage locator")
    if text_layer.get("requires_human_review") is not True:
        fail("text psycholinguistics must require human review")
    if text_layer.get("buchanan_claim_authorized") is not False:
        fail("text psycholinguistics must not authorize Buchanan claims")

    ok("state entry preserves BDP-002D.1 governance boundary")


def main() -> None:
    print("=== BDP-002D.1 interaction adaptation boundary verifier ===")
    check_docs()
    check_state()
    print("\n[OK] BDP-002D.1 verification passed")


if __name__ == "__main__":
    main()
