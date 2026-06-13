#!/usr/bin/env python3
"""BDP-002A read-only semantic workbench verifier.

Uses psql through subprocess, matching the existing Buchanan verifier style.
No psycopg dependency.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

PHASE = "BDP-002A"
DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")
REPO_ROOT = Path(__file__).resolve().parents[1]
READBACK_SCRIPT = REPO_ROOT / "scripts" / "read_bdp_002a_bwo_semantic_workbench.py"

EXPECTED_COUNTS = {
    "sources": 2,
    "source_candidates": 3,
    "passage_candidates": 1,
    "passages": 1,
    "citations": 1,
    "concept_mentions": 1,
    "concept_relations": 0,
    "interpretations": 0,
}

ALLOWED_AUTHORITY_LABELS = {
    "citation_backed",
    "primary_text_backed",
    "buchanan_pending",
    "provisional_synthesis",
    "needs_review",
    "user_interpretation",
    "system_synthesis",
}

FORBIDDEN_BUCHANAN_CLAIM_PHRASES = [
    "buchanan argues",
    "buchanan claims",
    "buchanan thinks",
    "buchanan's view is",
    "buchanan says",
]

MUTATING_SQL_PATTERN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|ALTER|CREATE|DROP|TRUNCATE)\b",
    re.IGNORECASE,
)


def psql(sql: str) -> str:
    result = subprocess.run(
        [
            "psql",
            "-d",
            DB_NAME,
            "-X",
            "-q",
            "-t",
            "-A",
            "-v",
            "ON_ERROR_STOP=1",
            "-c",
            sql,
        ],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise AssertionError(
            "psql verifier query failed\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )
    return result.stdout.strip()


def sql_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def count_table(table: str) -> int:
    return int(psql(f"SELECT COUNT(*) FROM {table};"))


def migration_count(phase: str) -> int:
    return int(
        psql(
            "SELECT COUNT(*) "
            "FROM schema_migrations "
            f"WHERE phase = {sql_literal(phase)};"
        )
    )


def snapshot_counts() -> dict[str, int]:
    counts = {table: count_table(table) for table in EXPECTED_COUNTS}
    counts[f"{PHASE}_migration_count"] = migration_count(PHASE)
    return counts


def assert_expected_counts(counts: dict[str, int], label: str) -> None:
    for table, expected in EXPECTED_COUNTS.items():
        actual = counts.get(table)
        if actual != expected:
            raise AssertionError(
                f"{label}: {table}_count expected {expected}, got {actual}"
            )

    migration_key = f"{PHASE}_migration_count"
    if counts.get(migration_key) != 0:
        raise AssertionError(f"{label}: {migration_key} must remain 0")


def assert_readback_script_is_read_only() -> None:
    text = READBACK_SCRIPT.read_text(encoding="utf-8")

    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if MUTATING_SQL_PATTERN.search(stripped):
            raise AssertionError(
                f"mutating SQL keyword found in readback script on line {line_no}: {stripped}"
            )

    sql_files = sorted(REPO_ROOT.glob("sql/*002a*.sql")) + sorted(
        REPO_ROOT.glob("sql/*BDP-002A*.sql")
    )
    if sql_files:
        raise AssertionError(
            "BDP-002A must not add SQL migration files: "
            + ", ".join(str(path) for path in sql_files)
        )


def run_readback() -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, str(READBACK_SCRIPT)],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise AssertionError(
            "readback script failed\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            f"readback did not emit valid JSON: {exc}\n{result.stdout}"
        ) from exc


def assert_card_boundary(card: dict[str, Any]) -> None:
    if card.get("phase") != PHASE:
        raise AssertionError(f"unexpected phase: {card.get('phase')}")

    if card.get("read_only") is not True:
        raise AssertionError("workbench card must mark itself read_only=true")

    workbench = card.get("semantic_workbench", {})
    for key in ["plain_explanation", "technical_explanation", "buchanan_explanation"]:
        section = workbench.get(key)
        if not isinstance(section, dict):
            raise AssertionError(f"missing semantic workbench section: {key}")

        authority = section.get("authority")
        if authority not in ALLOWED_AUTHORITY_LABELS:
            raise AssertionError(
                f"{key} has invalid or missing authority label: {authority}"
            )

    buchanan = workbench["buchanan_explanation"]
    if buchanan.get("text") is not None:
        raise AssertionError(
            "Buchanan-specific explanation text must remain null in BDP-002A"
        )

    if buchanan.get("authority") != "buchanan_pending":
        raise AssertionError(
            "Buchanan-specific explanation must use authority=buchanan_pending"
        )

    if "blocked" not in str(buchanan.get("evidence_status", "")):
        raise AssertionError("Buchanan-specific explanation must be marked blocked")

    evidence_chain = card.get("evidence_chain", {})
    if evidence_chain.get("buchanan_citation") is not False:
        raise AssertionError("Buchanan citation must remain false in BDP-002A")

    if evidence_chain.get("buchanan_interpretation") is not False:
        raise AssertionError("Buchanan interpretation must remain false in BDP-002A")

    invariant = card.get("database_invariant", {})
    for table, expected in EXPECTED_COUNTS.items():
        key = f"{table}_count"
        if invariant.get(key) != expected:
            raise AssertionError(
                f"card invariant {key} expected {expected}, got {invariant.get(key)}"
            )

    if invariant.get("BDP-002A_migration_count") != 0:
        raise AssertionError("card invariant BDP-002A_migration_count must remain 0")

    serialized = json.dumps(card, sort_keys=True).lower()
    for phrase in FORBIDDEN_BUCHANAN_CLAIM_PHRASES:
        if phrase in serialized:
            raise AssertionError(f"forbidden Buchanan claim phrase generated: {phrase}")


def main() -> int:
    assert_readback_script_is_read_only()

    before = snapshot_counts()
    assert_expected_counts(before, "before readback")

    card = run_readback()

    after = snapshot_counts()
    assert_expected_counts(after, "after readback")

    if before != after:
        raise AssertionError(
            f"BDP-002A readback changed database counts: before={before}, after={after}"
        )

    assert_card_boundary(card)

    print("BDP-002A semantic workbench verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
