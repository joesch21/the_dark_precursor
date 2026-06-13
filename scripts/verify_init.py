#!/usr/bin/env python3
"""Verify BDP-001A Buchanan platform scaffold alignment.

This is a repository-shape and control-plane verifier. It does not require a
running PostgreSQL server. It checks that the initial migration, state JSON, and
canonical docs agree on the minimum BDP-001A schema contract.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_FILES = [
    ROOT / "README.md",
    ROOT / "sql" / "001_buchanan_control_plane.sql",
    ROOT / "scripts" / "verify_init.py",
    ROOT / "ai_boot" / "BUCHANAN_SYSTEM_STATE.json",
    ROOT / "docs" / "BUCHANAN_ARCHITECTURE.md",
    ROOT / "docs" / "BUCHANAN_SCHEMA_CONTROL.md",
    ROOT / "docs" / "BUCHANAN_INGESTION_WORKFLOW.md",
    ROOT / "docs" / "BUCHANAN_CONCEPT_ONTOLOGY.md",
    ROOT / "docs" / "BUCHANAN_CITATION_AND_RIGHTS.md",
    ROOT / "docs" / "BUCHANAN_THREAD_HANDOVER.md",
]

REQUIRED_TABLES = [
    "schema_migrations",
    "source_candidates",
    "sources",
    "raw_documents",
    "clean_documents",
    "passages",
    "concepts",
    "concept_mentions",
    "concept_relations",
    "interpretations",
    "citations",
    "ingestion_events",
    "user_interactions",
]

AUTHORITY_LEVELS = [
    "primary_text",
    "buchanan_direct",
    "secondary_scholarship",
    "system_synthesis",
    "user_interpretation",
]

RELATION_TYPES = [
    "explains",
    "depends_on",
    "opposes",
    "modifies",
    "intensifies",
    "emerges_from",
    "is_applied_to",
    "is_contested_by",
    "is_translated_as",
    "is_linked_to",
    "is_example_of",
    "develops",
    "reframes",
    "extends",
    "critiques",
    "operationalises",
]

RIGHTS_STATUSES = [
    "unknown",
    "public_url",
    "licensed",
    "user_provided",
    "fair_use_reference_only",
    "restricted",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"Missing file: {path.relative_to(ROOT)}")


def require_all(haystack: str, needles: Iterable[str], label: str) -> None:
    missing = [needle for needle in needles if needle not in haystack]
    if missing:
        fail(f"{label} missing: {', '.join(missing)}")
    ok(f"{label} aligned")


def main() -> int:
    missing = [str(path.relative_to(ROOT)) for path in EXPECTED_FILES if not path.exists()]
    if missing:
        fail("Missing expected files:\n - " + "\n - ".join(missing))
    ok("expected scaffold files exist")

    sql_path = ROOT / "sql" / "001_buchanan_control_plane.sql"
    state_path = ROOT / "ai_boot" / "BUCHANAN_SYSTEM_STATE.json"
    schema_doc_path = ROOT / "docs" / "BUCHANAN_SCHEMA_CONTROL.md"
    ontology_doc_path = ROOT / "docs" / "BUCHANAN_CONCEPT_ONTOLOGY.md"
    rights_doc_path = ROOT / "docs" / "BUCHANAN_CITATION_AND_RIGHTS.md"

    sql = read_text(sql_path)
    schema_doc = read_text(schema_doc_path)
    ontology_doc = read_text(ontology_doc_path)
    rights_doc = read_text(rights_doc_path)

    try:
        state = json.loads(read_text(state_path))
    except json.JSONDecodeError as exc:
        fail(f"Invalid BUCHANAN_SYSTEM_STATE.json: {exc}")

    if re.search(r"CREATE\s+EXTENSION\s+IF\s+NOT\s+EXISTS\s+pgvector", sql, re.I):
        fail("SQL uses extension name 'pgvector'; expected PostgreSQL extension name 'vector'")
    if not re.search(r"CREATE\s+EXTENSION\s+IF\s+NOT\s+EXISTS\s+vector", sql, re.I):
        fail("SQL does not create pgvector extension with 'CREATE EXTENSION IF NOT EXISTS vector'")
    ok("pgvector extension name is correct")

    for table in REQUIRED_TABLES:
        pattern = rf"CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS\s+{table}\b"
        if not re.search(pattern, sql, re.I):
            fail(f"SQL missing table: {table}")
    ok("SQL contains all required BDP-001A tables")

    require_all(sql, AUTHORITY_LEVELS, "SQL authority levels")
    require_all(sql, RELATION_TYPES, "SQL relation types")
    require_all(sql, RIGHTS_STATUSES, "SQL rights statuses")

    scope = state.get("current_build_slice", {}).get("database_scope", [])
    missing_scope = [table for table in REQUIRED_TABLES if table not in scope]
    if missing_scope:
        fail("BUCHANAN_SYSTEM_STATE.json database_scope missing: " + ", ".join(missing_scope))
    ok("state database_scope matches required tables")

    state_authority = state.get("authority_levels", [])
    missing_authority = [item for item in AUTHORITY_LEVELS if item not in state_authority]
    if missing_authority:
        fail("BUCHANAN_SYSTEM_STATE.json authority_levels missing: " + ", ".join(missing_authority))
    ok("state authority levels aligned")

    require_all(schema_doc, ["### citations", "schema_migrations", "BDP-001A"], "schema-control doc")
    require_all(ontology_doc, RELATION_TYPES, "ontology relation vocabulary")
    require_all(rights_doc, ["short quotation + citation + paraphrase + source trail", "Authority Labels"], "citation policy")

    print("\nBDP-001A initialization check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
