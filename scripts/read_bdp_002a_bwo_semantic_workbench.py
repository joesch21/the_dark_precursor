#!/usr/bin/env python3
"""BDP-002A Body without Organs semantic workbench readback.

Read-only operator card. Uses the existing repository pattern:
Python subprocess -> psql CLI -> JSON readback.

No psycopg dependency.
No database mutation.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any

PHASE = "BDP-002A"
CONCEPT_NAME = "Body without Organs"
DB_NAME = os.environ.get("BUCHANAN_DB_NAME", "buchanan_platform_dev")

ALLOWED_AUTHORITY_LABELS = [
    "citation_backed",
    "primary_text_backed",
    "buchanan_pending",
    "provisional_synthesis",
    "needs_review",
    "user_interpretation",
    "system_synthesis",
]

RELATED_CONCEPT_CANDIDATES = ["organism", "desire", "assemblage", "strata"]

TABLES = [
    "sources",
    "source_candidates",
    "passage_candidates",
    "passages",
    "citations",
    "concept_mentions",
    "concept_relations",
    "interpretations",
]


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
        raise RuntimeError(
            "psql readback failed\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )
    return result.stdout.strip()


def psql_json(sql: str) -> Any:
    raw = psql(sql)
    if not raw:
        raise RuntimeError("psql returned empty JSON payload")
    return json.loads(raw)


def sql_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def table_count(table: str) -> int:
    return int(psql(f"SELECT COUNT(*) FROM {table};"))


def migration_count(phase: str) -> int:
    return int(
        psql(
            "SELECT COUNT(*) "
            "FROM schema_migrations "
            f"WHERE phase = {sql_literal(phase)};"
        )
    )


def concept_record() -> dict[str, Any]:
    return psql_json(
        """
        SELECT json_build_object(
            'id', id,
            'name', name,
            'status', status
        )
        FROM concepts
        WHERE lower(name) = lower('Body without Organs')
        LIMIT 1;
        """
    )


def primary_chain_counts() -> dict[str, int]:
    payload = psql_json(
        """
        SELECT json_build_object(
            'primary_text_passages', COUNT(DISTINCT p.id),
            'primary_text_citations', COUNT(DISTINCT ci.id)
        )
        FROM concepts c
        JOIN concept_mentions cm ON cm.concept_id = c.id
        JOIN passages p ON p.id = cm.passage_id
        LEFT JOIN citations ci ON ci.passage_id = p.id
        LEFT JOIN sources s ON s.id = p.source_id
        WHERE lower(c.name) = lower('Body without Organs')
          AND (s.author IS NULL OR lower(s.author) NOT LIKE '%ian buchanan%');
        """
    )
    return {
        "primary_text_passages": int(payload.get("primary_text_passages") or 0),
        "primary_text_citations": int(payload.get("primary_text_citations") or 0),
    }


def buchanan_evidence() -> dict[str, Any]:
    payload = psql_json(
        """
        SELECT json_build_object(
            'buchanan_source_metadata',
                EXISTS (
                    SELECT 1
                    FROM sources
                    WHERE lower(author) LIKE '%ian buchanan%'
                      AND lower(title) LIKE '%problem of the body%'
                      AND status = 'canonical'
                ),
            'buchanan_passage_candidate',
                EXISTS (
                    SELECT 1
                    FROM passage_candidates pc
                    JOIN sources s ON s.id = pc.source_id
                    JOIN concepts c ON c.id = pc.concept_id
                    WHERE lower(s.author) LIKE '%ian buchanan%'
                      AND lower(c.name) = lower('Body without Organs')
                ),
            'buchanan_citation',
                EXISTS (
                    SELECT 1
                    FROM citations ci
                    JOIN sources s ON s.id = ci.source_id
                    WHERE lower(s.author) LIKE '%ian buchanan%'
                ),
            'buchanan_interpretation',
                EXISTS (
                    SELECT 1
                    FROM interpretations
                )
        );
        """
    )
    return {
        "buchanan_source_metadata": bool(payload.get("buchanan_source_metadata")),
        "buchanan_passage_candidate": bool(payload.get("buchanan_passage_candidate")),
        "buchanan_citation": bool(payload.get("buchanan_citation")),
        "buchanan_interpretation": bool(payload.get("buchanan_interpretation")),
    }


def related_concepts() -> list[str]:
    payload = psql_json(
        """
        SELECT COALESCE(json_agg(name ORDER BY name), '[]'::json)
        FROM concepts
        WHERE lower(name) IN ('organism', 'desire', 'assemblage', 'strata');
        """
    )
    found = list(payload or [])
    found_lower = {str(name).lower() for name in found}
    missing = [
        name
        for name in RELATED_CONCEPT_CANDIDATES
        if name.lower() not in found_lower
    ]
    return found + missing


def build_card() -> dict[str, Any]:
    counts = {f"{table}_count": table_count(table) for table in TABLES}
    counts["BDP-002A_migration_count"] = migration_count(PHASE)

    concept = concept_record()
    primary_counts = primary_chain_counts()
    buchanan = buchanan_evidence()
    evidence_chain = {**primary_counts, **buchanan}

    card: dict[str, Any] = {
        "phase": PHASE,
        "read_only": True,
        "concept": {
            "name": concept.get("name") or CONCEPT_NAME,
            "status": concept.get("status") or "canonical_or_existing",
        },
        "semantic_workbench": {
            "plain_explanation": {
                "text": (
                    "Provisional teaching scaffold: the Body without Organs can be introduced as a way "
                    "of thinking a body by capacities, intensities, and organization limits rather than "
                    "as a fixed organism."
                ),
                "authority": "provisional_synthesis",
                "evidence_status": "partly_supported",
            },
            "technical_explanation": {
                "text": (
                    "Provisional technical scaffold: the concept marks a controlled distinction between "
                    "an intensive field of possible connections and the stabilized organization that "
                    "turns a body into an organism. This remains a scaffold until more cited passages "
                    "and relation evidence are added."
                ),
                "authority": "provisional_synthesis",
                "evidence_status": "needs_more_evidence",
            },
            "buchanan_explanation": {
                "text": None,
                "authority": "buchanan_pending",
                "evidence_status": "blocked_until_buchanan_passage_citation",
            },
        },
        "evidence_chain": evidence_chain,
        "database_invariant": counts,
        "related_concepts": related_concepts(),
        "authority_labels": {
            "primary_text_chain": (
                "primary_text_backed"
                if primary_counts["primary_text_passages"] >= 1
                else "needs_review"
            ),
            "existing_citation_chain": (
                "citation_backed"
                if primary_counts["primary_text_citations"] >= 1
                else "needs_review"
            ),
            "plain_explanation": "provisional_synthesis",
            "technical_explanation": "provisional_synthesis",
            "buchanan_explanation": "buchanan_pending",
        },
        "confirmed": [
            "Concept exists in the platform.",
            "At least one cited primary-text concept mention exists.",
            "Buchanan article metadata has been adopted.",
            "A Buchanan passage candidate envelope has been prepared.",
        ],
        "provisional": [
            "Plain-language explanation requires fuller review.",
            "Technical explanation is not yet Buchanan-backed.",
            "Buchanan-specific explanation remains blocked.",
        ],
        "open_gaps": [
            "Review Buchanan passage candidate locator and short text.",
            "Insert Buchanan cited passage in later phase.",
            "Link Buchanan passage to concept mention in later phase.",
            "Create interpretation only after evidence exists.",
        ],
        "next_recommended_action": (
            "BDP-001N for evidence-first continuation, or BDP-002B for workbench-first frontend preview."
        ),
        "allowed_authority_labels": ALLOWED_AUTHORITY_LABELS,
    }

    return card


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read BDP-002A Body without Organs semantic workbench card."
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Print compact JSON instead of indented JSON.",
    )
    args = parser.parse_args()

    card = build_card()
    print(json.dumps(card, indent=None if args.compact else 2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
