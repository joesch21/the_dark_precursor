#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")

required_docs = [
    "docs/BUCHANAN_THREAD_HANDOVER.md",
    "docs/BUCHANAN_SCHEMA_CONTROL.md",
    "docs/BUCHANAN_CITATION_AND_RIGHTS.md",
    "docs/BUCHANAN_INGESTION_WORKFLOW.md",
    "docs/BUCHANAN_SEMANTIC_WORKBENCH.md",
    "docs/BUCHANAN_CONCEPT_ONTOLOGY.md",
]

required_phrases = [
    "description ≠ claim",
    "A description becomes a claim when it attributes",
    "Descriptions must carry authority labels",
    "Claims require stronger governed evidence",
    "source-bound description",
]

def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")

def ok(message: str) -> None:
    print(f"[OK] {message}")

def psql_scalar(sql: str) -> str:
    result = subprocess.run(
        ["psql", "-X", "-v", "ON_ERROR_STOP=1", "-d", DB_NAME, "-t", "-A", "-c", sql],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    return result.stdout.strip()

def main() -> None:
    state_path = ROOT / "ai_boot/BUCHANAN_SYSTEM_STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    record = state.get("bdp_001n1_description_rule")
    if not record:
        fail("missing bdp_001n1_description_rule in system state")
    ok("system state includes bdp_001n1_description_rule")

    if record.get("sql_migration") is not False:
        fail("BDP-001N.1 must be sql_migration=false")
    ok("sql_migration=false")

    if record.get("database_mutation") is not False:
        fail("BDP-001N.1 must be database_mutation=false")
    ok("database_mutation=false")

    ladder = record.get("authority_ladder", [])
    expected_ladder = [
        "metadata",
        "locator",
        "short_excerpt",
        "source_bound_description",
        "citation_backed_passage",
        "concept_mention",
        "interpretation",
        "synthesis",
    ]
    if ladder != expected_ladder:
        fail(f"authority ladder mismatch: {ladder}")
    ok("authority ladder recorded")

    combined = ""
    for rel in required_docs:
        path = ROOT / rel
        if not path.exists():
            fail(f"missing required doc {rel}")
        text = path.read_text(encoding="utf-8")
        combined += "\n" + text
        ok(f"doc exists: {rel}")

    for phrase in required_phrases:
        if phrase not in combined:
            fail(f"missing doctrine phrase: {phrase}")
        ok(f"found doctrine phrase: {phrase}")

    migration_count = psql_scalar("SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001N.1';")
    if migration_count != "0":
        fail(f"BDP-001N.1 migration count must be 0, got {migration_count}")
    ok("BDP-001N.1 migration_count=0")

    counts = psql_scalar("""
    SELECT concat_ws(',',
      (SELECT COUNT(*) FROM sources),
      (SELECT COUNT(*) FROM source_candidates),
      (SELECT COUNT(*) FROM passage_candidates),
      (SELECT COUNT(*) FROM passages),
      (SELECT COUNT(*) FROM citations),
      (SELECT COUNT(*) FROM concept_mentions),
      (SELECT COUNT(*) FROM concept_relations),
      (SELECT COUNT(*) FROM interpretations)
    );
    """)
    expected = "2,3,1,1,1,1,0,0"
    if counts != expected:
        fail(f"database invariant mismatch: expected {expected}, got {counts}")
    ok("database invariant preserved: sources=2, candidates=3, passage_candidates=1, passages=1, citations=1, concept_mentions=1, relations=0, interpretations=0")

    print("BDP-001N.1 description rule verification passed.")

if __name__ == "__main__":
    main()
