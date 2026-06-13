#!/usr/bin/env python3
"""Verify BDP-001F concept mention boundary."""

import os
import subprocess
import sys

DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")


def psql_scalar(sql: str) -> str:
    result = subprocess.run(
        ["psql", "-d", DB_NAME, "-At", "-F", "|", "-c", sql],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def ok(message: str) -> None:
    print(f"[OK] {message}")


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    sys.exit(1)


def expect(actual: str, expected: str, message: str) -> None:
    if actual != expected:
        fail(f"{message}: expected {expected!r}, got {actual!r}")
    ok(message)


def main() -> None:
    expect(
        psql_scalar("SELECT COUNT(*) FROM schema_migrations WHERE phase = 'BDP-001F';"),
        "1",
        "BDP-001F migration ledger recorded",
    )

    expect(
        psql_scalar("SELECT COUNT(*) FROM sources;"),
        "1",
        "source count remains one",
    )

    expect(
        psql_scalar("SELECT COUNT(*) FROM passages;"),
        "1",
        "passage count remains one",
    )

    expect(
        psql_scalar("SELECT COUNT(*) FROM citations;"),
        "1",
        "citation count remains one",
    )

    expect(
        psql_scalar("SELECT COUNT(*) FROM interpretations;"),
        "0",
        "no interpretations inserted",
    )

    expect(
        psql_scalar("SELECT COUNT(*) FROM concept_relations;"),
        "0",
        "no concept relations inserted",
    )

    mention_count = psql_scalar(
        """
        SELECT COUNT(*)
        FROM concept_mentions cm
        JOIN concepts c ON c.id = cm.concept_id
        JOIN passages p ON p.id = cm.passage_id
        JOIN sources s ON s.id = p.source_id
        WHERE c.name = 'Body without Organs'
          AND s.title = 'A Thousand Plateaus: Capitalism and Schizophrenia'
          AND s.status = 'canonical'
          AND cm.mention_type = 'direct'
          AND cm.reviewed_status = 'accepted'
          AND cm.confidence = 1.0
          AND (
            p.page_or_timestamp ILIKE '%150%'
            OR p.citation ILIKE '%150%'
            OR p.chapter_or_section ILIKE '%Body without Organs%'
          );
        """
    )
    expect(mention_count, "1", "first passage linked to Body without Organs concept mention")

    citation_chain_count = psql_scalar(
        """
        SELECT COUNT(*)
        FROM citations ci
        JOIN passages p ON p.id = ci.passage_id
        JOIN sources s ON s.id = ci.source_id
        JOIN concept_mentions cm ON cm.passage_id = p.id
        JOIN concepts c ON c.id = cm.concept_id
        WHERE ci.interpretation_id IS NULL
          AND ci.rights_status = 'fair_use_reference_only'
          AND ci.display_rule = 'reference_only'
          AND c.name = 'Body without Organs'
          AND s.title = 'A Thousand Plateaus: Capitalism and Schizophrenia';
        """
    )
    expect(citation_chain_count, "1", "citation chain remains reference-only and interpretation-free")

    print("\nBDP-001F concept mention verification passed.")


if __name__ == "__main__":
    main()
