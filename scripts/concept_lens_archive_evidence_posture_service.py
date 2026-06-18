#!/usr/bin/env python3
"""Read-only Concept Lens archive evidence posture service.

BDP-003F.8 implements a bounded readback service behind the BDP-003F.7
contract. It reports what the archive currently supports for a requested
concept. It does not generate interpretations, create records, mutate the
archive, promote evidence, or authorize Buchanan-specific claims.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import subprocess
from pathlib import Path
from typing import Any, Callable, Iterable

RESULT_SCHEMA_ID = "bdp_003f8_concept_lens_archive_evidence_posture_result_v1"
SERVICE_NAME = "concept_lens_archive_evidence_posture_service.v1"

PRIMARY_ARCHIVE_CHAIN = ["concepts", "concept_mentions", "passages", "citations", "sources"]

BLOCKED_ACTIONS = [
    "no database mutation",
    "no citation creation",
    "no concept mention creation",
    "no concept relation creation",
    "no interpretation insertion",
    "no evidence promotion",
    "no Buchanan-specific claim without exact governed evidence",
    "no frontend wiring",
    "no backend route handler",
    "no adapter endpoint",
    "no external LLM routing",
]

READ_ONLY_FORBIDDEN_SQL = re.compile(
    r"\b(insert|update|delete|drop|alter|create|truncate|merge|grant|revoke|vacuum|reindex|copy\s+.+\s+from)\b",
    re.IGNORECASE,
)

CONCEPT_ALIASES = {
    "bwo": "body without organs",
    "body without an organ": "body without organs",
    "body without organs": "body without organs",
    "body-without-organs": "body without organs",
    "assemblage theory": "assemblage",
    "we repress because we repeat": "repetition",
    "repress because we repeat": "repetition",
    "repression and repetition": "repetition",
    "repetition and repression": "repetition",
    "lines of flight": "line of flight",
}


def normalize_concept_query(raw_concept_query: str | None, normalized_concept: str | None = None) -> str:
    """Normalize a concept query into a conservative lookup key."""
    candidate = (normalized_concept or raw_concept_query or "").strip().lower()
    candidate = re.sub(r"[\u2018\u2019]", "'", candidate)
    candidate = re.sub(r"[^a-z0-9'\s\-]", " ", candidate)
    candidate = re.sub(r"\s+", " ", candidate).strip()
    candidate = CONCEPT_ALIASES.get(candidate, candidate)

    # Specific phrase-level safety for common Deleuze/Freud formulation.
    if "repress" in candidate and "repeat" in candidate:
        return "repetition"
    return candidate


def _blank_result(raw_concept_query: str, normalized_concept: str) -> dict[str, Any]:
    return {
        "schema_id": RESULT_SCHEMA_ID,
        "service_name": SERVICE_NAME,
        "concept": raw_concept_query,
        "normalized_concept": normalized_concept,
        "archive_lookup_status": "no_archive_match",
        "evidence_posture": "exploratory_unverified",
        "authority_label": "system_synthesis",
        "buchanan_specific_claim_allowed": False,
        "archive_chain": [],
        "matched_records": {
            "concepts": 0,
            "concept_mentions": 0,
            "passages": 0,
            "citations": 0,
            "sources": 0,
        },
        "primary_archive_readback_chain": PRIMARY_ARCHIVE_CHAIN,
        "rights_display_rule": "reference_only_when_restricted",
        "passage_text_display": "omitted_until_allowed_by_rights_policy",
        "interpretation_available": False,
        "concept_relation_available": False,
        "human_review_required": True,
        "blocked_actions": list(BLOCKED_ACTIONS),
        "notes": [],
    }


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _unique_count(rows: Iterable[dict[str, Any]], key: str) -> int:
    values = {_clean(row.get(key)) for row in rows if _clean(row.get(key))}
    return len(values)


def _is_reviewed(row: dict[str, Any]) -> bool:
    status = _clean(row.get("mention_review_status") or row.get("review_status")).lower()
    return status in {"accepted", "reviewed", "approved"}


def _has_complete_primary_chain(row: dict[str, Any]) -> bool:
    required = ["concept_id", "concept_mention_id", "passage_id", "citation_id", "source_id"]
    return all(_clean(row.get(key)) for key in required) and _is_reviewed(row)


def _is_restricted(row: dict[str, Any]) -> bool:
    rights = _clean(row.get("rights_status")).lower()
    return rights in {"restricted", "fair_use_reference_only", "licensed", "user_provided"}


def _archive_chain_item(row: dict[str, Any]) -> dict[str, Any]:
    rights_status = _clean(row.get("rights_status")) or "unknown"
    passage_display = "omitted_by_rights_policy" if _is_restricted(row) else "omitted_until_allowed_by_rights_policy"
    return {
        "concept_id": _clean(row.get("concept_id")),
        "concept_name": _clean(row.get("concept_name")),
        "concept_mention_id": _clean(row.get("concept_mention_id")),
        "mention_type": _clean(row.get("mention_type")) or "unknown",
        "review_status": _clean(row.get("mention_review_status") or row.get("review_status")) or "unknown",
        "passage_id": _clean(row.get("passage_id")),
        "passage_locator": _clean(row.get("passage_locator")),
        "passage_text_display": passage_display,
        "citation_id": _clean(row.get("citation_id")),
        "source_id": _clean(row.get("source_id")),
        "source_author": _clean(row.get("source_author")),
        "source_title": _clean(row.get("source_title")),
        "rights_status": rights_status,
        "authority_label": "buchanan_direct" if _clean(row.get("source_author")).lower() == "ian buchanan" else "primary_text",
    }


def classify_archive_rows(
    raw_concept_query: str,
    normalized_concept: str,
    archive_rows: Iterable[dict[str, Any]] | None,
) -> dict[str, Any]:
    """Classify supplied archive rows into a Concept Lens evidence posture."""
    rows = [dict(row) for row in (archive_rows or [])]
    result = _blank_result(raw_concept_query, normalized_concept)

    if not rows:
        result["notes"].append("No archive rows were available for this concept; absence is reported, not repaired.")
        return result

    result["matched_records"] = {
        "concepts": _unique_count(rows, "concept_id"),
        "concept_mentions": _unique_count(rows, "concept_mention_id"),
        "passages": _unique_count(rows, "passage_id"),
        "citations": _unique_count(rows, "citation_id"),
        "sources": _unique_count(rows, "source_id"),
    }

    complete_rows = [row for row in rows if _has_complete_primary_chain(row)]
    source_bound_rows = [row for row in rows if _clean(row.get("source_id")) or _clean(row.get("passage_id"))]

    if complete_rows:
        result["archive_chain"] = [_archive_chain_item(row) for row in complete_rows]
        result["evidence_posture"] = "archive_grounded"
        result["authority_label"] = (
            "buchanan_direct"
            if any(_clean(row.get("source_author")).lower() == "ian buchanan" for row in complete_rows)
            else "primary_text"
        )
        result["archive_lookup_status"] = (
            "rights_restricted_match" if any(_is_restricted(row) for row in complete_rows) else "archive_grounded_match"
        )
        result["passage_text_display"] = "omitted_by_rights_policy" if any(_is_restricted(row) for row in complete_rows) else "omitted_until_allowed_by_rights_policy"
        result["notes"].append("Complete primary archive evidence chain found; result remains evidence posture only.")
        return result

    if source_bound_rows:
        result["archive_chain"] = [_archive_chain_item(row) for row in source_bound_rows]
        result["archive_lookup_status"] = "source_bound_match"
        result["evidence_posture"] = "source_bound_description"
        result["authority_label"] = "system_synthesis"
        result["notes"].append("Source-bound material exists, but the reviewed primary concept evidence chain is incomplete.")
        return result

    result["archive_lookup_status"] = "concept_found_without_reviewed_evidence"
    result["evidence_posture"] = "system_synthesis"
    result["authority_label"] = "system_synthesis"
    result["notes"].append("Concept-like archive material exists, but reviewed evidence is not available.")
    return result


def assert_read_only_sql(sql: str) -> None:
    """Fail closed if a SQL string contains obvious mutation verbs."""
    if READ_ONLY_FORBIDDEN_SQL.search(sql):
        raise ValueError("Refusing to run non-read-only SQL for Concept Lens evidence posture service")


def _sql_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def build_postgres_readonly_query(normalized_concept: str) -> str:
    """Build the expected read-only PostgreSQL evidence posture query.

    The query assumes the canonical evidence-spine table names recorded in the
    Buchanan project state. It is intentionally compact and read-only.
    """
    concept_literal = _sql_literal(normalized_concept)
    sql = f"""
SELECT json_agg(row_to_json(t))
FROM (
  SELECT
    c.id::text AS concept_id,
    c.name::text AS concept_name,
    cm.id::text AS concept_mention_id,
    cm.mention_type::text AS mention_type,
    cm.review_status::text AS mention_review_status,
    p.id::text AS passage_id,
    COALESCE(p.page_or_timestamp::text, p.locator::text, p.page_locator::text, '') AS passage_locator,
    ci.id::text AS citation_id,
    s.id::text AS source_id,
    s.author::text AS source_author,
    s.title::text AS source_title,
    COALESCE(s.rights_status::text, 'unknown') AS rights_status
  FROM concepts c
  LEFT JOIN concept_mentions cm ON cm.concept_id = c.id
  LEFT JOIN passages p ON p.id = cm.passage_id
  LEFT JOIN citations ci ON ci.passage_id = p.id
  LEFT JOIN sources s ON s.id = COALESCE(ci.source_id, p.source_id)
  WHERE lower(c.name::text) = lower({concept_literal})
  ORDER BY c.id, cm.id, p.id, ci.id, s.id
) t;
"""
    assert_read_only_sql(sql)
    return sql


def query_postgres_archive(postgres_url: str, normalized_concept: str) -> list[dict[str, Any]]:
    """Query a PostgreSQL archive using psql in read-only mode."""
    sql = build_postgres_readonly_query(normalized_concept)
    env = os.environ.copy()
    env["PGOPTIONS"] = f"{env.get('PGOPTIONS', '')} -c default_transaction_read_only=on".strip()
    completed = subprocess.run(
        ["psql", postgres_url, "-X", "-A", "-t", "-q", "-c", sql],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    payload = completed.stdout.strip()
    if not payload or payload == "null":
        return []
    loaded = json.loads(payload)
    return loaded if isinstance(loaded, list) else []


def query_sqlite_archive(sqlite_db_path: str, normalized_concept: str) -> list[dict[str, Any]]:
    """Query a SQLite archive using a read-only URI.

    This adapter is provided for local test archives and future portability. The
    canonical platform may use PostgreSQL; this function does not mutate either
    way.
    """
    db_path = Path(sqlite_db_path).expanduser().resolve()
    uri = f"file:{db_path}?mode=ro"
    sql = """
SELECT
  c.id AS concept_id,
  c.name AS concept_name,
  cm.id AS concept_mention_id,
  cm.mention_type AS mention_type,
  cm.review_status AS mention_review_status,
  p.id AS passage_id,
  COALESCE(p.page_or_timestamp, p.locator, p.page_locator, '') AS passage_locator,
  ci.id AS citation_id,
  s.id AS source_id,
  s.author AS source_author,
  s.title AS source_title,
  COALESCE(s.rights_status, 'unknown') AS rights_status
FROM concepts c
LEFT JOIN concept_mentions cm ON cm.concept_id = c.id
LEFT JOIN passages p ON p.id = cm.passage_id
LEFT JOIN citations ci ON ci.passage_id = p.id
LEFT JOIN sources s ON s.id = COALESCE(ci.source_id, p.source_id)
WHERE lower(c.name) = lower(?)
ORDER BY c.id, cm.id, p.id, ci.id, s.id
"""
    assert_read_only_sql(sql)
    with sqlite3.connect(uri, uri=True) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(sql, (normalized_concept,)).fetchall()
    return [dict(row) for row in rows]


def read_concept_lens_archive_evidence_posture(
    raw_concept_query: str,
    normalized_concept: str | None = None,
    archive_rows: Iterable[dict[str, Any]] | None = None,
    sqlite_db_path: str | None = None,
    postgres_url: str | None = None,
    lookup_adapter: Callable[[str], Iterable[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    """Return a read-only evidence posture result for a requested concept."""
    normalized = normalize_concept_query(raw_concept_query, normalized_concept)

    if archive_rows is not None:
        return classify_archive_rows(raw_concept_query, normalized, archive_rows)

    if lookup_adapter is not None:
        return classify_archive_rows(raw_concept_query, normalized, lookup_adapter(normalized))

    if sqlite_db_path:
        return classify_archive_rows(raw_concept_query, normalized, query_sqlite_archive(sqlite_db_path, normalized))

    if postgres_url:
        return classify_archive_rows(raw_concept_query, normalized, query_postgres_archive(postgres_url, normalized))

    result = classify_archive_rows(raw_concept_query, normalized, [])
    result["notes"].append("No live archive adapter was configured; service returned explicit no-archive-match posture.")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read Concept Lens archive evidence posture for a concept.")
    parser.add_argument("concept", help="Concept phrase or query fragment")
    parser.add_argument("--normalized-concept", default=None, help="Optional normalized concept override")
    parser.add_argument("--sqlite-db", default=None, help="Optional read-only SQLite archive path")
    parser.add_argument("--postgres-url", default=None, help="Optional PostgreSQL URL for psql read-only lookup")
    parser.add_argument("--indent", type=int, default=2, help="JSON indentation")
    args = parser.parse_args(argv)

    result = read_concept_lens_archive_evidence_posture(
        raw_concept_query=args.concept,
        normalized_concept=args.normalized_concept,
        sqlite_db_path=args.sqlite_db,
        postgres_url=args.postgres_url,
    )
    print(json.dumps(result, indent=args.indent, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# BDP-003F.11 EXISTING ARCHIVE READBACK BRIDGE INTEGRATION START
def read_concept_lens_archive_evidence_posture_via_existing_archive_bridge(
    concept: str,
    *,
    repo_root=None,
    require_live_readback: bool = True,
    bridge_rows=None,
):
    """Classify Concept Lens posture through the BDP-003F.11 read-only bridge."""
    import inspect
    from concept_lens_existing_archive_evidence_readback_bridge import (
        read_existing_archive_evidence_rows_for_concept,
    )

    rows = bridge_rows
    if rows is None:
        rows = read_existing_archive_evidence_rows_for_concept(
            concept,
            repo_root=repo_root,
            require_live_readback=require_live_readback,
        )

    classifier = read_concept_lens_archive_evidence_posture
    signature = inspect.signature(classifier)
    params = signature.parameters

    for candidate_name in (
        "archive_rows",
        "supplied_archive_rows",
        "evidence_rows",
        "rows",
    ):
        if candidate_name in params:
            return classifier(concept, **{candidate_name: rows})

    positional = [
        param
        for param in params.values()
        if param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD)
    ]
    if len(positional) >= 2:
        return classifier(concept, rows)

    raise TypeError(
        "BDP-003F.11 bridge could not locate a supported supplied-row parameter "
        "on read_concept_lens_archive_evidence_posture."
    )
# BDP-003F.11 EXISTING ARCHIVE READBACK BRIDGE INTEGRATION END
