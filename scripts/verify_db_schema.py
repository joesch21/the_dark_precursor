#!/usr/bin/env python3
"""Verify live PostgreSQL schema for Buchanan platform BDP-001B."""

import os
import subprocess
import sys

DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")

REQUIRED_TABLES = {
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
}

REQUIRED_EXTENSIONS = {"pgcrypto", "vector"}

REQUIRED_COLUMNS = {
    "passages": {
        "id",
        "source_id",
        "text",
        "citation",
        "rights_status",
        "embedding",
        "embedding_model",
    },
    "citations": {
        "id",
        "source_id",
        "passage_id",
        "interpretation_id",
        "citation_text",
        "rights_status",
        "display_rule",
    },
    "interpretations": {
        "id",
        "concept_id",
        "interpreter",
        "claim",
        "authority_level",
        "evidence_passage_id",
        "source_trail",
    },
    "concept_relations": {
        "id",
        "source_concept_id",
        "target_concept_id",
        "relation_type",
        "evidence_passage_id",
    },
}

REQUIRED_CONSTRAINT_TERMS = {
    "concept_relations": ["operationalises", "reframes", "critiques", "depends_on"],
    "interpretations": ["buchanan_direct", "primary_text", "system_synthesis"],
    "sources": ["fair_use_reference_only", "restricted", "canonical"],
    "concept_mentions": ["metaphorical", "contested", "needs_review"],
}


def run_sql(sql: str) -> str:
    cmd = [
        "sudo",
        "-u",
        "postgres",
        "psql",
        "-d",
        DB_NAME,
        "-X",
        "-v",
        "ON_ERROR_STOP=1",
        "-Atc",
        sql,
    ]
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        print("[FAIL] SQL command failed")
        print(result.stderr.strip())
        sys.exit(1)
    return result.stdout.strip()


def ok(message: str) -> None:
    print(f"[OK] {message}")


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    sys.exit(1)


extensions = set(filter(None, run_sql("""
SELECT extname
FROM pg_extension
WHERE extname IN ('pgcrypto', 'vector')
ORDER BY extname;
""").splitlines()))

missing_extensions = REQUIRED_EXTENSIONS - extensions
if missing_extensions:
    fail(f"missing extensions: {sorted(missing_extensions)}")
ok("required extensions installed")

tables = set(filter(None, run_sql("""
SELECT tablename
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;
""").splitlines()))

missing_tables = REQUIRED_TABLES - tables
if missing_tables:
    fail(f"missing tables: {sorted(missing_tables)}")
ok("required tables exist")

for table, required in REQUIRED_COLUMNS.items():
    columns = set(filter(None, run_sql(f"""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name = '{table}'
    ORDER BY column_name;
    """).splitlines()))

    missing_columns = required - columns
    if missing_columns:
        fail(f"{table} missing columns: {sorted(missing_columns)}")
    ok(f"{table} required columns exist")

for table, terms in REQUIRED_CONSTRAINT_TERMS.items():
    constraint_text = run_sql(f"""
    SELECT COALESCE(string_agg(pg_get_constraintdef(c.oid), ' '), '')
    FROM pg_constraint c
    JOIN pg_class t ON c.conrelid = t.oid
    JOIN pg_namespace n ON t.relnamespace = n.oid
    WHERE n.nspname = 'public'
      AND t.relname = '{table}';
    """)

    missing_terms = [term for term in terms if term not in constraint_text]
    if missing_terms:
        fail(f"{table} constraints missing terms: {missing_terms}")
    ok(f"{table} controlled vocabulary constraints aligned")

migration_rows = run_sql("""
SELECT COUNT(*)
FROM schema_migrations
WHERE id = '001_buchanan_control_plane';
""")

if migration_rows != "1":
    fail("schema_migrations does not contain 001_buchanan_control_plane")
ok("schema migration ledger recorded")

print()
print("BDP-001B live database schema verification passed.")
