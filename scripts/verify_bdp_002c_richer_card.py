#!/usr/bin/env python3
"""
BDP-002C — Richer Semantic Readback Surface Verifier

Default mode performs a live read-only verifier using psql subprocess.
Use --static-only only when the execution environment has no psql/database; static
mode checks code/card governance but does not prove live DB invariants.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "scripts" / "read_bdp_002c_bwo_richer_card.py"
DB_NAME = __import__("os").environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")

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
    "buchanan_article_passage_count": 1,
    "buchanan_article_citation_count": 1,
    "buchanan_article_concept_mention_count": 1,
}

CONTROLLED_AUTHORITY_LABELS = {
    "concept_record",
    "metadata",
    "citation_backed",
    "citation_backed_passage",
    "primary_text_backed",
    "reviewed_concept_mention",
    "source_bound_description",
    "record_description",
    "rights_display_boundary",
    "buchanan_pending",
    "blocked_until_reviewed_relation_evidence",
    "blocked_until_governed_interpretation_phase",
    "blocked_until_interpretive_authority_exists",
    "needs_review",
    "provisional_synthesis",
    "system_synthesis",
    "user_interpretation",
    "experimental_modelling",
    "secondary_scholarship",
}

REQUIRED_SECTION_IDS = [
    "concept_identity",
    "evidence_depth_tier",
    "canonical_source_metadata",
    "citation_backed_passage_record",
    "reviewed_concept_mention_record",
    "rights_display_boundary",
    "current_database_invariant",
    "source_bound_evidence_posture",
    "buchanan_specific_explanation_boundary",
    "relation_layer_status",
    "interpretation_layer_status",
    "related_concept_candidates",
    "psycho_linguistic_placeholder_observations",
    "verification_and_audit_boundary",
    "next_recommended_operator_action",
]

FORBIDDEN_SQL_KEYWORDS = {
    "INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP", "TRUNCATE",
    "MERGE", "UPSERT", "GRANT", "REVOKE", "COPY", "CALL", "DO",
}

BLOCKED_AUTHOR_POSITION_PATTERNS = [
    r"\bBuchanan\s+argues\b",
    r"\bBuchanan\s+claims\b",
    r"\bBuchanan['’]s\s+view\s+is\b",
    r"\bBuchanan\s+means\b",
    r"\bBuchanan\s+intends\b",
    r"\bBuchanan['’]s\s+interpretation\s+of\s+the\s+Body\s+without\s+Organs\s+is\b",
]


def load_generator_module():
    spec = importlib.util.spec_from_file_location("bdp_002c_generator", GENERATOR_PATH)
    if not spec or not spec.loader:
        raise RuntimeError(f"Unable to import generator at {GENERATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ok(message: str) -> None:
    print(f"[OK] {message}")


def fail(errors: List[str], message: str) -> None:
    print(f"[FAIL] {message}")
    errors.append(message)


def run_psql_query(query: str) -> str:
    compact = " ".join(query.strip().split())
    tokens = {token.strip(";,()") for token in compact.upper().split()}
    if not compact.upper().startswith("SELECT"):
        raise RuntimeError(f"Verifier blocked non-SELECT SQL: {compact[:120]}")
    forbidden = sorted(FORBIDDEN_SQL_KEYWORDS.intersection(tokens))
    if forbidden:
        raise RuntimeError(f"Verifier blocked mutation keyword(s): {', '.join(forbidden)}")
    cmd = ["psql", "-d", DB_NAME, "-t", "-A", "-F", "|", "-c", query]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except FileNotFoundError as exc:
        raise RuntimeError("psql binary not found; run full verifier inside the local PostgreSQL environment or use --static-only for repository-only checks") from exc
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "psql readback failed")
    return result.stdout.strip()


def get_live_invariant(module) -> Dict[str, int]:
    raw = run_psql_query(module.SQL_QUERIES["current_invariant"])
    values = [int(value or 0) for value in raw.split("|")]
    return dict(zip(EXPECTED_INVARIANT.keys(), values))


def check_no_psycopg_imports(errors: List[str], source: str) -> None:
    if re.search(r"^\s*(import|from)\s+psycopg\b", source, re.MULTILINE):
        fail(errors, "generator imports psycopg")
    elif re.search(r"^\s*(import|from)\s+psycopg2\b", source, re.MULTILINE):
        fail(errors, "generator imports psycopg2")
    else:
        ok("no psycopg/psycopg2 imports")


def check_psql_subprocess_pattern(errors: List[str], source: str) -> None:
    if "subprocess.run" in source and '"psql"' in source:
        ok("generator uses subprocess + psql pattern")
    else:
        fail(errors, "generator does not show subprocess + psql pattern")


def check_sql_strings(errors: List[str], module) -> None:
    for name, sql in module.SQL_QUERIES.items():
        compact = " ".join(sql.strip().split())
        tokens = {token.strip(";,()") for token in compact.upper().split()}
        if not compact.upper().startswith("SELECT"):
            fail(errors, f"SQL query {name} is not SELECT-only")
        else:
            ok(f"SQL query {name} starts with SELECT")
        forbidden = sorted(FORBIDDEN_SQL_KEYWORDS.intersection(tokens))
        if forbidden:
            fail(errors, f"SQL query {name} contains forbidden mutation keyword(s): {', '.join(forbidden)}")
        else:
            ok(f"SQL query {name} contains no mutation keywords")


def iter_text_values(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_text_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_text_values(item)


def check_card_shape_and_labels(errors: List[str], card: Dict[str, Any], expected_invariant: Dict[str, int]) -> None:
    sections = card.get("sections")
    if not isinstance(sections, list):
        fail(errors, "card sections is not a list")
        return

    section_ids = [section.get("section_id") for section in sections]
    if section_ids == REQUIRED_SECTION_IDS:
        ok("card has exactly the 15 required sections in order")
    else:
        fail(errors, f"card section order mismatch: {section_ids}")

    for section in sections:
        label = section.get("authority_label")
        if label not in CONTROLLED_AUTHORITY_LABELS:
            fail(errors, f"section {section.get('section_id')} has invalid authority label: {label}")
        for item in section.get("fields", []):
            item_label = item.get("authority_label")
            if item_label not in CONTROLLED_AUTHORITY_LABELS:
                fail(errors, f"field {item.get('field_id')} has invalid authority label: {item_label}")
            if "field_id" not in item or "label" not in item or "value" not in item:
                fail(errors, f"field missing required keys: {item}")
        for item in section.get("observations", []):
            item_label = item.get("authority_label")
            if item_label != "experimental_modelling":
                fail(errors, f"observation {item.get('observation_id')} is not experimental_modelling")
            for required_key in ["observation_id", "observation_type", "observation_text", "linked_passage_locator", "requires_human_review", "current_ceiling", "objective_score_claimed"]:
                if required_key not in item:
                    fail(errors, f"observation missing {required_key}: {item}")
            if item.get("linked_passage_locator") != "printed article page 76 / PDF page 4":
                fail(errors, f"observation locator mismatch: {item}")
            if item.get("requires_human_review") is not True:
                fail(errors, f"observation does not require human review: {item}")
            if item.get("current_ceiling") != "Level 2 Embedding Deviation":
                fail(errors, f"observation ceiling mismatch: {item}")
            if item.get("objective_score_claimed") is not False:
                fail(errors, f"observation claims objective score: {item}")

    ok("authority labels and field/observation keys checked")

    invariant_section = next((section for section in sections if section.get("section_id") == "current_database_invariant"), {})
    invariant_fields = invariant_section.get("fields", [])
    invariant_value = invariant_fields[0].get("value") if invariant_fields else None
    if invariant_value != expected_invariant:
        fail(errors, f"card invariant mismatch: expected {expected_invariant}, actual {invariant_value}")
    else:
        ok("card invariant matches expected readback invariant")

    all_text = "\n".join(iter_text_values(card))
    for pattern in BLOCKED_AUTHOR_POSITION_PATTERNS:
        if re.search(pattern, all_text, re.IGNORECASE):
            fail(errors, f"blocked author-position phrasing found: {pattern}")
    ok("blocked author-position phrasing not found")

    required_strings = {
        "buchanan_pending",
        "blocked_until_governed_interpretation_phase",
        "blocked_until_interpretive_authority_exists",
        "omitted_by_rights_policy",
    }
    missing = sorted(item for item in required_strings if item not in all_text)
    if missing:
        fail(errors, f"required boundary strings missing from card: {missing}")
    else:
        ok("Buchanan and rights boundary strings present")

    if "long_quotation_displayed" in all_text and "article_reproduction_authorized" in all_text:
        ok("rights flags are displayed")
    else:
        fail(errors, "rights flags are missing")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify BDP-002C richer semantic readback surface.")
    parser.add_argument("--static-only", action="store_true", help="Skip live psql invariant checks; use offline preview card only.")
    args = parser.parse_args()

    errors: List[str] = []
    print("=== BDP-002C richer semantic readback verifier ===")

    if not GENERATOR_PATH.exists():
        fail(errors, f"missing generator: {GENERATOR_PATH}")
        print("\n[FAIL] BDP-002C verification failed")
        return 1

    source = GENERATOR_PATH.read_text()
    module = load_generator_module()

    check_no_psycopg_imports(errors, source)
    check_psql_subprocess_pattern(errors, source)
    check_sql_strings(errors, module)

    if args.static_only:
        print("[WARN] static-only mode: live database invariant is not proven in this environment")
        expected_invariant = dict(EXPECTED_INVARIANT)
        card = module.generate_bdp_002c_card(offline_preview=True)
        check_card_shape_and_labels(errors, card, expected_invariant)
    else:
        try:
            before = get_live_invariant(module)
            if before != EXPECTED_INVARIANT:
                fail(errors, f"pre-readback invariant mismatch: expected {EXPECTED_INVARIANT}, actual {before}")
            else:
                ok("pre-readback database invariant matches expected state")

            card = module.generate_bdp_002c_card(offline_preview=False)
            check_card_shape_and_labels(errors, card, before)

            after = get_live_invariant(module)
            if after != before:
                fail(errors, f"post-readback invariant changed: before {before}, after {after}")
            else:
                ok("post-readback database invariant preserved")
        except RuntimeError as exc:
            fail(errors, str(exc))

    if errors:
        print("\n[FAIL] BDP-002C verification failed")
        for error in errors:
            print(f" - {error}")
        return 1

    print("\n[OK] BDP-002C verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
