#!/usr/bin/env python3
"""
BDP-002D verifier — relational/adaptive presentation governance.

Verifies docs/state only. No database access.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REQUIRED_FILES = [
    Path("docs/BDP_002D_RELATIONAL_ADAPTIVE_PRESENTATION.md"),
    Path("docs/BUCHANAN_SEMANTIC_WORKBENCH.md"),
    Path("docs/BUCHANAN_PSYCHOLINGUISTIC_SEMANTIC_ARCHITECTURE.md"),
    Path("docs/BUCHANAN_ARCHITECTURE.md"),
    Path("docs/BUCHANAN_THREAD_HANDOVER.md"),
    Path("ai_boot/BUCHANAN_SYSTEM_STATE.json"),
]

REQUIRED_STRINGS = [
    "How I am adapting this view",
    "inspect",
    "pause",
    "reset",
    "manual override",
    "No long-term user profile",
    "psychological assessment",
    "navigation patterns",
    "metaphor selection",
    "time spent on visual versus textual content",
    "question style",
    "depth of follow-up",
    "preference for visual or conceptual framing",
    "Adaptive presentation changes display only",
    "does not change citation authority",
    "does not create a Buchanan-specific claim",
]

BLOCKED_WEAKENING_PATTERNS = [
    r"psychological assessment\s*=\s*true",
    r"long_term_user_profile\s*=\s*true",
    r"reader_state_tracking\s*=\s*true",
    r"hidden_personalisation\s*=\s*true",
    r"database_mutation\s*=\s*true",
    r"sql_migration\s*=\s*true",
]

STATE_KEY = "bdp_002d_relational_adaptive_presentation_governance"


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing required file: {path}")
    return path.read_text()


def check_files() -> None:
    for path in REQUIRED_FILES:
        if not path.exists():
            fail(f"missing required file: {path}")
    ok("all required BDP-002D files are present")


def check_doctrine_strings() -> None:
    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    lower = combined.lower()

    for needle in REQUIRED_STRINGS:
        if needle.lower() not in lower:
            fail(f"missing required governance string: {needle}")

    ok("required adaptive-presentation governance strings present")

    for pattern in BLOCKED_WEAKENING_PATTERNS:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            fail(f"blocked weakening pattern found: {pattern}")

    ok("blocked profiling/storage/schema weakening patterns absent")


def check_state() -> None:
    state = json.loads(Path("ai_boot/BUCHANAN_SYSTEM_STATE.json").read_text())
    record = state.get(STATE_KEY)
    if not isinstance(record, dict):
        fail(f"missing state key: {STATE_KEY}")

    expected_false = [
        "sql_migration",
        "database_mutation",
        "frontend_implementation",
        "reader_state_tracking",
        "long_term_user_profile",
        "psychological_assessment",
        "hidden_personalisation",
    ]
    for key in expected_false:
        if record.get(key) is not False:
            fail(f"state field {key} must be false")

    if record.get("required_explanatory_layer") != "How I am adapting this view":
        fail("required explanatory layer not recorded correctly")

    controls = set(record.get("required_controls", []))
    for expected in {
        "inspect_adaptation",
        "pause_adaptation",
        "reset_adaptation",
        "manual_override",
        "return_to_canonical_evidence_first_view",
    }:
        if expected not in controls:
            fail(f"missing required control in state: {expected}")

    ok("state records BDP-002D governance boundaries")


def main() -> None:
    print("=== BDP-002D relational/adaptive presentation verifier ===")
    check_files()
    check_doctrine_strings()
    check_state()
    print("\n[OK] BDP-002D verification passed")


if __name__ == "__main__":
    main()
