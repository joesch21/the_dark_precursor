#!/usr/bin/env python3
"""Verify BDP-002A.2 psycho-linguistic semantic architecture doctrine.

This verifier is intentionally file/doctrine only.
It performs no database writes and does not require psycopg/psycopg2.
"""

from __future__ import annotations

import json
import ast
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/BUCHANAN_PSYCHOLINGUISTIC_SEMANTIC_ARCHITECTURE.md",
    "docs/BUCHANAN_ARCHITECTURE.md",
    "docs/BUCHANAN_SEMANTIC_WORKBENCH.md",
    "docs/BUCHANAN_CONCEPT_ONTOLOGY.md",
    "docs/BUCHANAN_SCHEMA_CONTROL.md",
    "docs/BUCHANAN_THREAD_HANDOVER.md",
    "scripts/update_bdp_002a2_system_state.py",
    "scripts/verify_bdp_002a2_psycholinguistic_architecture.py",
]

REQUIRED_MARKERS = {
    "docs/BUCHANAN_PSYCHOLINGUISTIC_SEMANTIC_ARCHITECTURE.md": [
        "BDP-002A.2",
        "Four-Layer Interpretive Stack",
        "Citation and Provenance Layer",
        "Semantic Concept Layer",
        "Psycho-Linguistic Modelling Layer",
        "Reader / Listener Transformation Layer",
        "not proof of consciousness, mind-reading, or psychological certainty",
        "sql_migration = false",
        "database_mutation = false",
        "reader_state_tracking = false",
        "buchanan_specific_claim = false",
    ],
    "docs/BUCHANAN_ARCHITECTURE.md": [
        "BDP-002A.2 Psycho-Linguistic Semantic Architecture",
        "four interpretive layers",
        "No SQL migration.",
        "No database mutation.",
    ],
    "docs/BUCHANAN_SEMANTIC_WORKBENCH.md": [
        "BDP-002A.2 Psycho-Linguistic Workbench Direction",
        "Psycho-linguistic observation is not citation authority.",
        "LLM inference is not mind-reading or psychological certainty.",
    ],
    "docs/BUCHANAN_CONCEPT_ONTOLOGY.md": [
        "BDP-002A.2 Psycho-Linguistic Concept Boundary",
        "Psycho-linguistic modelling may describe how language moves.",
        "It may not upgrade authority beyond the available source evidence.",
    ],
    "docs/BUCHANAN_SCHEMA_CONTROL.md": [
        "BDP-002A.2 Psycho-Linguistic Architecture Doctrine",
        "sql_migration = false",
        "database_mutation = false",
        "new_tables = false",
        "reader_state_tracking = false",
    ],
    "docs/BUCHANAN_THREAD_HANDOVER.md": [
        "BDP-002A.2 Handover Update",
        "No psycho-linguistic tables.",
        "No reader-state tracking.",
        "BDP-001N — Review first Buchanan passage candidate locator and short text",
    ],
}

FORBIDDEN_SQL_FILES = [
    "sql/014_bdp_002a2",
    "sql/014_record_bdp_002a2",
    "sql/bdp_002a2",
]

def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    sys.exit(1)


def read(path: str) -> str:
    full = ROOT / path
    if not full.exists():
        fail(f"missing required file: {path}")
    return full.read_text(encoding="utf-8")


def git_status() -> str:
    try:
        return subprocess.check_output(
            ["git", "status", "--short"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.STDOUT,
        )
    except Exception:
        return ""


def main() -> None:
    for path in REQUIRED_FILES:
        if not (ROOT / path).exists():
            fail(f"missing required file: {path}")

    for path, markers in REQUIRED_MARKERS.items():
        text = read(path)
        for marker in markers:
            if marker not in text:
                fail(f"missing marker in {path}: {marker}")

    for forbidden in FORBIDDEN_SQL_FILES:
        if list(ROOT.glob(f"{forbidden}*")):
            fail(f"BDP-002A.2 must not add SQL migration files matching: {forbidden}*")

    def imported_modules(path: str) -> set[str]:
        tree = ast.parse(read(path))
        modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    modules.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module.split(".")[0])
        return modules

    for script in [
        "scripts/verify_bdp_002a2_psycholinguistic_architecture.py",
        "scripts/update_bdp_002a2_system_state.py",
    ]:
        bad = imported_modules(script) & {"psycopg", "psycopg2"}
        if bad:
            fail(f"{script} must not depend on psycopg drivers: {sorted(bad)}")

    state_path = ROOT / "ai_boot/BUCHANAN_SYSTEM_STATE.json"
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"system state JSON is invalid: {exc}")
        state_raw = json.dumps(state)
        if "BDP-002A.2" not in state_raw:
            fail("system state does not record BDP-002A.2; run scripts/update_bdp_002a2_system_state.py")
        if "psycho-linguistic" not in state_raw and "psycholinguistic" not in state_raw:
            fail("system state does not record psycho-linguistic architecture doctrine")

    status = git_status()
    if "sql/014" in status or "bdp_002a2" in "\n".join(
        line for line in status.splitlines() if line.startswith("?? sql/")
    ):
        fail("git status suggests a BDP-002A.2 SQL file was added")

    print("BDP-002A.2 psycho-linguistic architecture doctrine verification passed.")


if __name__ == "__main__":
    main()
