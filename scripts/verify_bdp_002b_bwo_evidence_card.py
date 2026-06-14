#!/usr/bin/env python3
"""Verify BDP-002B operator evidence card boundaries."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
READ_SCRIPT = ROOT / "scripts" / "read_bdp_002b_bwo_evidence_card.py"
DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")

EXPECTED_COUNTS = {
    "sources_count": 2,
    "source_candidates_count": 3,
    "passage_candidates_count": 1,
    "passages_count": 2,
    "citations_count": 2,
    "concept_mentions_count": 2,
    "concept_relations_count": 0,
    "interpretations_count": 0,
    "BDP-002B migration_count": 0,
}

MUTATION_SQL_RE = re.compile(
    r"\b(insert|update|delete|drop|alter|create|truncate|merge|copy|grant|revoke)\b",
    re.IGNORECASE,
)
PASSAGE_TEXT_SQL_RE = re.compile(r"\b(p|passages)\.text\b", re.IGNORECASE)
INTERPRETIVE_CLAIM_RE = re.compile(
    r"Buchanan\s+(argues|claims|contends|maintains|defines|interprets|means|suggests\s+that)\b|"
    r"Buchanan['’]s\s+(view|position|argument|interpretation|meaning)\b|"
    r"Body\s+without\s+Organs\s+means\b",
    re.IGNORECASE,
)


def psql_json(sql: str) -> dict[str, Any]:
    result = subprocess.run(
        ["psql", "-X", "-v", "ON_ERROR_STOP=1", "-d", DB_NAME, "-At", "-c", sql],
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(result.stdout.strip())


def database_counts() -> dict[str, Any]:
    return psql_json(
        """
SELECT json_build_object(
  'sources_count', (SELECT count(*) FROM sources),
  'source_candidates_count', (SELECT count(*) FROM source_candidates),
  'passage_candidates_count', (SELECT count(*) FROM passage_candidates),
  'passages_count', (SELECT count(*) FROM passages),
  'citations_count', (SELECT count(*) FROM citations),
  'concept_mentions_count', (SELECT count(*) FROM concept_mentions),
  'concept_relations_count', (SELECT count(*) FROM concept_relations),
  'interpretations_count', (SELECT count(*) FROM interpretations),
  'BDP-001P migration_count', (
    SELECT count(*) FROM schema_migrations WHERE phase = 'BDP-001P'
  ),
  'BDP-001Q migration_count', (
    SELECT count(*) FROM schema_migrations WHERE phase = 'BDP-001Q'
  ),
  'BDP-002B migration_count', (
    SELECT count(*) FROM schema_migrations WHERE phase = 'BDP-002B'
  )
);
"""
    )


def load_read_module() -> Any:
    spec = importlib.util.spec_from_file_location("read_bdp_002b", READ_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {READ_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_read_script_sql_boundaries() -> None:
    module = load_read_module()
    sql_values = [
        value for key, value in vars(module).items() if key.startswith("SQL_") and isinstance(value, str)
    ]
    if not sql_values:
        raise AssertionError("No SQL_* constants found in read script")

    for sql in sql_values:
        if MUTATION_SQL_RE.search(sql):
            raise AssertionError(f"Mutating SQL keyword found in read script SQL: {sql}")
        if PASSAGE_TEXT_SQL_RE.search(sql):
            raise AssertionError("Read script SQL must not select restricted passage text")

    source = READ_SCRIPT.read_text()
    if "psycopg" in source or "psycopg2" in source:
        raise AssertionError("Read script must not depend on psycopg drivers")


def run_card_json() -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, str(READ_SCRIPT), "--format", "json"],
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(result.stdout)


def recursively_find_missing_labels(value: Any, path: str = "card") -> list[str]:
    missing: list[str] = []
    if isinstance(value, dict):
        if any(key in value for key in ("text", "record", "status", "layer")):
            if "authority_label" not in value and path not in {
                "card",
                "card.database_invariant",
                "card.evidence_chain[0]",
                "card.evidence_chain[1]",
                "card.evidence_chain[2]",
            }:
                missing.append(path)
        for key, child in value.items():
            missing.extend(recursively_find_missing_labels(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            missing.extend(recursively_find_missing_labels(child, f"{path}[{index}]"))
    return missing


def verify_card(card: dict[str, Any]) -> None:
    serialized = json.dumps(card, sort_keys=True)

    if INTERPRETIVE_CLAIM_RE.search(serialized):
        raise AssertionError("Card contains an interpretive Buchanan claim pattern")

    if re.search(r'"passage_text"\s*:', serialized):
        raise AssertionError("Card must not expose a passage_text field")

    rights = card.get("rights_display_rules", {})
    if rights.get("passage_text_display") != "omitted_by_rights_policy":
        raise AssertionError("Restricted passage text must be omitted by rights policy")
    if rights.get("long_quotation_displayed") is not False:
        raise AssertionError("Long quotation display must be false")
    if rights.get("article_reproduction_authorized") is not False:
        raise AssertionError("Article reproduction must remain unauthorized")

    blocked_layers = {item.get("layer"): item for item in card.get("blocked_layers", [])}
    for required in ("concept_relation", "interpretation", "buchanan_specific_claim"):
        if blocked_layers.get(required, {}).get("status") != "blocked":
            raise AssertionError(f"Missing blocked layer: {required}")

    source_bound = card.get("source_bound_description", {})
    if source_bound.get("authority_label") != "source_bound_description":
        raise AssertionError("Source-bound description must carry source_bound_description authority")
    if source_bound.get("claim_status") != "non_interpretive_record_description":
        raise AssertionError("Source-bound description must be marked non-interpretive")

    missing_labels = recursively_find_missing_labels(card)
    if missing_labels:
        raise AssertionError("Missing authority labels: " + ", ".join(missing_labels))

    invariant = card.get("database_invariant", {})
    for key, expected in EXPECTED_COUNTS.items():
        if invariant.get(key) != expected:
            raise AssertionError(f"Expected {key}={expected}, got {invariant.get(key)}")


def main() -> int:
    verify_read_script_sql_boundaries()

    before = database_counts()
    card = run_card_json()
    after = database_counts()

    if before != after:
        raise AssertionError(f"Database invariant changed during readback: before={before}, after={after}")

    for key, expected in EXPECTED_COUNTS.items():
        if after.get(key) != expected:
            raise AssertionError(f"Expected {key}={expected}, got {after.get(key)}")

    verify_card(card)

    print("BDP-002B evidence card verification passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.stderr or str(exc))
        raise SystemExit(exc.returncode)
