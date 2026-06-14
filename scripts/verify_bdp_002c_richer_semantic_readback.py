#!/usr/bin/env python3
"""Verifier for BDP-002C richer semantic readback surface."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

PHASE = "BDP-002C"
READER_SCRIPT = Path(__file__).with_name("read_bdp_002c_richer_bwo_semantic_card.py")
DOCTRINE_FILE = Path("docs/BDP_002C_RICHER_SEMANTIC_READBACK_SURFACE.md")
DEFAULT_DB_NAME = "buchanan_platform_dev"

FORBIDDEN_SQL_KEYWORDS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|TRUNCATE|MERGE|UPSERT|GRANT|REVOKE|COPY|CALL|DO)\b",
    re.IGNORECASE,
)

BLOCKED_CLAIM_PATTERNS = [
    re.compile(r"\bBuchanan\s+(argues|claims|thinks|intends|means|shows|demonstrates)\b", re.IGNORECASE),
    re.compile(r"\bBuchanan's\s+(view|position|argument|interpretation|claim)\b", re.IGNORECASE),
    re.compile(r"\bBuchanan-specific\s+(meaning|argument|position|theoretical consequence)\b", re.IGNORECASE),
]


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def ok(message: str) -> None:
    print(f"[OK] {message}")


def load_reader_module() -> Any:
    spec = importlib.util.spec_from_file_location("bdp_002c_reader", READER_SCRIPT)
    if spec is None or spec.loader is None:
        fail(f"Unable to load reader script at {READER_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_no_driver_dependency() -> None:
    text = READER_SCRIPT.read_text(encoding="utf-8")
    if re.search(r"^\s*import\s+psycopg\b|^\s*from\s+psycopg\b", text, re.MULTILINE):
        fail("Reader imports psycopg")
    if re.search(r"^\s*import\s+psycopg2\b|^\s*from\s+psycopg2\b", text, re.MULTILINE):
        fail("Reader imports psycopg2")
    if "subprocess.run" not in text or '"psql"' not in text:
        fail("Reader does not clearly use subprocess + psql pattern")
    ok("reader uses psql subprocess pattern and imports no psycopg/psycopg2")


def assert_sql_read_only(reader: Any) -> None:
    for name, sql in reader.SQL_QUERIES.items():
        match = FORBIDDEN_SQL_KEYWORDS.search(sql)
        if match:
            fail(f"SQL query {name} contains forbidden mutation keyword {match.group(1)}")
    ok("all SQL query strings passed to psql are mutation-keyword clean")


def assert_expected_invariant(label: str, state: dict[str, Any], reader: Any) -> None:
    for key, expected in reader.EXPECTED_INVARIANT.items():
        actual = state.get(key)
        if actual != expected:
            fail(f"{label}: {key} expected {expected}, got {actual}")
    for key, expected in {
        "buchanan_article_passage_count": 1,
        "buchanan_article_citation_count": 1,
        "buchanan_article_concept_mention_count": 1,
    }.items():
        actual = state.get(key)
        if actual != expected:
            fail(f"{label}: {key} expected {expected}, got {actual}")
    ok(f"{label} invariant matches expected BDP-002C readback state")


def walk_dicts(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_dicts(child)


def assert_authority_labels(card: dict[str, Any], reader: Any) -> None:
    allowed = set(reader.ALLOWED_AUTHORITY_LABELS)
    for node in walk_dicts(card):
        needs_label = any(
            key in node
            for key in (
                "section_id",
                "field_id",
                "observation_id",
                "authority_label_contract",
            )
        ) or node is card
        if needs_label and "authority_label" not in node:
            fail(f"Unlabelled node found: {node}")
        if "authority_label" in node and node["authority_label"] not in allowed:
            fail(f"Uncontrolled authority label: {node['authority_label']}")
    ok("all card sections, fields, items, and observations carry controlled authority labels")


def find_section(card: dict[str, Any], section_id: str) -> dict[str, Any]:
    for section in card.get("sections", []):
        if section.get("section_id") == section_id:
            return section
    fail(f"Missing section {section_id}")


def section_field_value(section: dict[str, Any], field_id: str) -> Any:
    for field in section.get("fields", []):
        if field.get("field_id") == field_id:
            return field.get("value")
    fail(f"Missing field {field_id} in section {section.get('section_id')}")


def assert_card_structure(card: dict[str, Any], reader: Any) -> None:
    section_ids = [section.get("section_id") for section in card.get("sections", [])]
    if section_ids != reader.REQUIRED_SECTION_IDS:
        fail(f"Card section IDs differ from required contract. Got: {section_ids}")
    ok("card contains the required 15 sections in order")


def assert_buchanan_explanation_blocked(card: dict[str, Any]) -> None:
    section_data = find_section(card, "buchanan_specific_explanation_boundary")
    expected = {
        "buchanan_specific_explanation_status": "buchanan_pending",
        "buchanan_specific_interpretation_status": "blocked_until_governed_interpretation_phase",
        "buchanan_specific_claim_status": "blocked_until_interpretive_authority_exists",
    }
    for field_id, value in expected.items():
        actual = section_field_value(section_data, field_id)
        if actual != value:
            fail(f"{field_id} expected {value}, got {actual}")
    ok("Buchanan-specific explanation, interpretation, and claim remain blocked")


def assert_rights_boundary(card: dict[str, Any]) -> None:
    rights = find_section(card, "rights_display_boundary")
    expected = {
        "passage_text_display": "omitted_by_rights_policy",
        "long_quotation_displayed": False,
        "article_reproduction_authorized": False,
    }
    for field_id, value in expected.items():
        actual = section_field_value(rights, field_id)
        if actual != value:
            fail(f"rights field {field_id} expected {value}, got {actual}")
    ok("rights boundary omits restricted passage text and blocks long quotation/article reproduction")


def assert_no_blocked_claim_language(card: dict[str, Any], markdown_text: str) -> None:
    payload = json.dumps(card, sort_keys=True) + "\n" + markdown_text
    for pattern in BLOCKED_CLAIM_PATTERNS:
        match = pattern.search(payload)
        if match:
            fail(f"Blocked Buchanan claim language found: {match.group(0)}")
    ok("no blocked Buchanan author-position phrasing appears in generated card")


def assert_psycholinguistic_placeholders(card: dict[str, Any]) -> None:
    sec = find_section(card, "psycho_linguistic_placeholder_observations")
    observations = sec.get("observations", [])
    if not observations:
        fail("No psycho-linguistic placeholder observations found")
    for obs in observations:
        if obs.get("authority_label") != "experimental_modelling":
            fail(f"Observation {obs.get('observation_id')} is not labelled experimental_modelling")
        if obs.get("requires_human_review") is not True:
            fail(f"Observation {obs.get('observation_id')} does not require human review")
        if obs.get("current_ceiling") != "Level 2 Embedding Deviation":
            fail(f"Observation {obs.get('observation_id')} has wrong modelling ceiling")
        if obs.get("objective_score_claimed") is not False:
            fail(f"Observation {obs.get('observation_id')} claims an objective score")
        if not obs.get("linked_passage_locator"):
            fail(f"Observation {obs.get('observation_id')} lacks linked passage locator")
    ok("psycho-linguistic placeholders remain experimental, locator-linked, and human-review gated")


def assert_doctrine_file() -> None:
    if not DOCTRINE_FILE.exists():
        fail(f"Missing doctrine file: {DOCTRINE_FILE}")
    text = DOCTRINE_FILE.read_text(encoding="utf-8")
    required = [
        "Expanded 15-Section Card Structure",
        "Authority Label Contract",
        "Verifier Checklist",
        "passage_text_display = omitted_by_rights_policy",
        "BDP-001R — Prepare first source-bound Buchanan Body without Organs description candidate, without interpretation.",
    ]
    for marker in required:
        if marker not in text:
            fail(f"Doctrine file missing marker: {marker}")
    ok("BDP-002C doctrine file contains card contract and verifier checklist")


def main() -> int:
    db_name = os.environ.get("BUCHANAN_DB_NAME", DEFAULT_DB_NAME)
    reader = load_reader_module()

    assert_no_driver_dependency()
    assert_sql_read_only(reader)
    assert_doctrine_file()

    before = reader.collect_database_state(db_name)
    assert_expected_invariant("pre-readback", before, reader)

    with tempfile.TemporaryDirectory(prefix="bdp_002c_verify_") as tmp:
        completed = subprocess.run(
            [sys.executable, str(READER_SCRIPT), "--db-name", db_name, "--out-dir", tmp],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            fail("readback script failed during verifier run\n" + completed.stderr)
        json_path = Path(tmp) / "bdp_002c_richer_bwo_semantic_card.json"
        md_path = Path(tmp) / "bdp_002c_richer_bwo_semantic_card.md"
        if not json_path.exists() or not md_path.exists():
            fail("readback script did not produce expected JSON and Markdown outputs")
        card = json.loads(json_path.read_text(encoding="utf-8"))
        markdown_text = md_path.read_text(encoding="utf-8")

    assert_card_structure(card, reader)
    assert_authority_labels(card, reader)
    assert_buchanan_explanation_blocked(card)
    assert_rights_boundary(card)
    assert_no_blocked_claim_language(card, markdown_text)
    assert_psycholinguistic_placeholders(card)

    after = reader.collect_database_state(db_name)
    assert_expected_invariant("post-readback", after, reader)
    if before != after:
        fail(f"Database state changed during readback. before={before}; after={after}")
    ok("database invariant is preserved before and after readback")

    print("BDP-002C richer semantic readback verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
