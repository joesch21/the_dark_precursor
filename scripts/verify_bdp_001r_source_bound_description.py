#!/usr/bin/env python3
"""
BDP-001R verifier.

Verifies the source-bound description candidate remains read-only, labelled,
rights-aware, and non-interpretive.

Repair note:
The SQL mutation checker strips quoted SQL literals before scanning keywords,
so article titles such as "What Can a Body Do?" do not trigger false DO matches.
"""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable

SCRIPT_PATH = Path("scripts/read_bdp_001r_bwo_source_bound_description.py")
DOC_PATH = Path("docs/BDP_001R_BWO_SOURCE_BOUND_DESCRIPTION.md")
STATE_PATH = Path("ai_boot/BUCHANAN_SYSTEM_STATE.json")

FORBIDDEN_SQL = re.compile(
    r"\b(INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|TRUNCATE|MERGE|UPSERT|GRANT|REVOKE|COPY|CALL|DO)\b",
    re.IGNORECASE,
)

FORBIDDEN_AUTHOR_POSITION_PHRASES = [
    "buchanan argues",
    "buchanan claims",
    "buchanan thinks",
    "buchanan's view",
    "buchanan means",
    "body without organs means",
    "deleuze argues",
    "guattari argues",
    "deleuze and guattari argue",
    "for buchanan, the body without organs is",
    "for deleuze and guattari, the body without organs is",
]

EXPECTED_INVARIANT = {
    "sources_count": 2,
    "source_candidates_count": 3,
    "passage_candidates_count": 1,
    "passages_count": 2,
    "citations_count": 2,
    "concept_mentions_count": 2,
    "concept_relations_count": 0,
    "interpretations_count": 0,
    "BDP-001P migration_count": 1,
    "BDP-002C migration_count": 0,
    "BDP-001R migration_count": 0,
    "buchanan_article_passage_count": 1,
    "buchanan_article_citation_count": 1,
    "buchanan_article_concept_mention_count": 1,
}

REQUIRED_SECTIONS = [
    "evidence_chain_summary",
    "buchanan_1997_article_posture",
    "secondary_scholarship_posture",
    "blocked_layers_status",
    "rights_display_status",
    "current_evidence_posture_statement",
    "next_recommended_governed_action",
    "authority_label_summary",
]

CONTROLLED_AUTHORITY_LABELS = {
    "source_bound_description",
    "record_description",
    "secondary_scholarship",
    "buchanan_pending",
    "blocked_until_governed_interpretation_phase",
    "blocked_until_reviewed_relation_evidence",
    "blocked_until_interpretive_authority_exists",
    "rights_display_boundary",
    "metadata",
}


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def load_generator():
    if not SCRIPT_PATH.exists():
        fail(f"missing generator script: {SCRIPT_PATH}")
    spec = importlib.util.spec_from_file_location("bdp001r_generator", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        fail("could not load generator module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def walk_values(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for v in value.values():
            yield from walk_values(v)
    elif isinstance(value, list):
        for v in value:
            yield from walk_values(v)
    else:
        yield str(value)


def strip_sql_literals_and_comments(sql: str) -> str:
    sql = re.sub(r"--.*?$", " ", sql, flags=re.MULTILINE)
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.DOTALL)
    sql = re.sub(r"'(?:''|[^'])*'", "''", sql)
    sql = re.sub(r'"(?:""|[^"])*"', '""', sql)
    return sql


def check_script_static() -> None:
    text = SCRIPT_PATH.read_text()
    if re.search(r"^\s*import\s+psycopg\b|^\s*import\s+psycopg2\b", text, flags=re.MULTILINE):
        fail("generator imports psycopg/psycopg2")
    if "subprocess.run" not in text or "psql" not in text:
        fail("generator does not use subprocess + psql pattern")
    ok("no psycopg/psycopg2 imports and psql subprocess pattern present")


def check_sql_boundaries(module) -> None:
    queries = getattr(module, "SQL_QUERIES", None)
    if not isinstance(queries, dict) or not queries:
        fail("generator exposes no SQL_QUERIES dictionary")

    for name, sql in queries.items():
        stripped = sql.strip()
        sql_without_literals = strip_sql_literals_and_comments(stripped)

        if not sql_without_literals.upper().lstrip().startswith("SELECT"):
            fail(f"SQL query {name} does not start with SELECT")

        match = FORBIDDEN_SQL.search(sql_without_literals)
        if match:
            fail(f"SQL query {name} contains mutation keyword: {match.group(1)}")

        ok(f"SQL query {name} is SELECT-only")


def check_card(card: Dict[str, Any]) -> None:
    sections = card.get("sections")
    if not isinstance(sections, list):
        fail("card sections are not a list")

    actual_ids = [s.get("section_id") for s in sections]
    if actual_ids != REQUIRED_SECTIONS:
        fail(f"section order mismatch: {actual_ids}")
    ok("all required sections present in order")

    for sec in sections:
        label = sec.get("authority_label")
        if label not in CONTROLLED_AUTHORITY_LABELS:
            fail(f"section {sec.get('section_id')} has invalid authority label {label}")

        fields = sec.get("fields")
        if not isinstance(fields, list) or not fields:
            fail(f"section {sec.get('section_id')} has no fields")

        for item in fields:
            if item.get("authority_label") not in CONTROLLED_AUTHORITY_LABELS:
                fail(f"field {item.get('field_id')} has invalid authority label {item.get('authority_label')}")
            if "field_id" not in item or "value" not in item:
                fail(f"field missing field_id or value in section {sec.get('section_id')}")

    ok("all sections and fields carry controlled authority labels")

    invariant = card.get("invariant_at_generation")
    if invariant != EXPECTED_INVARIANT:
        fail(f"invariant mismatch\nExpected: {EXPECTED_INVARIANT}\nActual:   {invariant}")
    ok("database invariant matches BDP-001R expected state")

    combined = "\n".join(walk_values(card)).lower()
    for phrase in FORBIDDEN_AUTHOR_POSITION_PHRASES:
        if phrase in combined:
            fail(f"blocked author-position phrase found: {phrase}")
    ok("no blocked author-position phrasing found")

    required_strings = [
        "buchanan_pending",
        "blocked_until_governed_interpretation_phase",
        "blocked_until_reviewed_relation_evidence",
        "blocked_until_interpretive_authority_exists",
        "omitted_by_rights_policy",
        "long_quotation_displayed",
        "article_reproduction_authorized",
        "metadata-only",
    ]
    for needle in required_strings:
        if needle.lower() not in combined:
            fail(f"required boundary string missing: {needle}")

    ok("Buchanan, blocked-layer, metadata-only, and rights boundaries present")


def run_generator_json() -> Dict[str, Any]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        fail(result.stderr.strip() or "generator failed")
    return json.loads(result.stdout)


def main() -> None:
    print("=== BDP-001R source-bound description verifier ===")
    module = load_generator()

    check_script_static()
    check_sql_boundaries(module)

    before = module.read_json_query("current_invariant")
    if before != EXPECTED_INVARIANT:
        fail(f"pre-readback invariant mismatch\nExpected: {EXPECTED_INVARIANT}\nActual:   {before}")
    ok("pre-readback database invariant matches expected state")

    card = run_generator_json()
    check_card(card)

    after = module.read_json_query("current_invariant")
    if after != before:
        fail(f"post-readback invariant changed\nBefore: {before}\nAfter:  {after}")
    ok("post-readback database invariant preserved")

    if DOC_PATH.exists():
        doc = DOC_PATH.read_text().lower()
        for phrase in FORBIDDEN_AUTHOR_POSITION_PHRASES:
            if phrase in doc:
                fail(f"blocked author-position phrase found in {DOC_PATH}: {phrase}")
        ok("generated Markdown description has no blocked author-position phrasing")

    if STATE_PATH.exists():
        state_text = STATE_PATH.read_text()
        if "bdp_001r_source_bound_description_candidate" in state_text:
            ok("BDP-001R state registration present")
        else:
            print("[WARN] BDP-001R state registration not found yet")

    print("\n[OK] BDP-001R verification passed")


if __name__ == "__main__":
    main()
