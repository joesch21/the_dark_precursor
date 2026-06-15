#!/usr/bin/env python3
"""Local reviewed concept card archive writer for BDP-003E.11.

This module implements a local/manual writer only. It has no frontend,
backend, adapter, database, or evidence-spine integration.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

INPUT_SCHEMA_VERSION = "bdp-003e5-local-reviewed-concept-card-archive-v1"
OUTPUT_SCHEMA_VERSION = "bdp-003e11-local-reviewed-concept-card-archive-record-v1"
WRITER_PHASE = "BDP-003E.11"

SAFE_RECORD_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{2,120}$")

REQUIRED_TOP_LEVEL_KEYS = [
    "schema_version",
    "archive_record_id",
    "review_status",
    "reviewed_at",
    "reviewed_by",
    "concept",
    "card",
    "governance",
    "source_trace",
]

REQUIRED_GOVERNANCE_FALSE_KEYS = [
    "evidence_promotion_approved",
    "citations_created",
    "concept_relations_created",
    "interpretations_created",
    "buchanan_claims_created",
]


class ArchiveWriterError(ValueError):
    """Raised when a payload cannot be archived safely."""


def _require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ArchiveWriterError(f"{label} must be an object")
    return value


def _require_non_empty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ArchiveWriterError(f"{label} must be a non-empty string")
    return value.strip()


def _canonical_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def validate_reviewed_concept_card(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate and return a defensive copy of a reviewed concept card payload."""

    payload = _require_mapping(payload, "payload")

    missing = [key for key in REQUIRED_TOP_LEVEL_KEYS if key not in payload]
    if missing:
        raise ArchiveWriterError(f"payload missing required keys: {', '.join(missing)}")

    schema_version = _require_non_empty_string(payload.get("schema_version"), "schema_version")
    if schema_version != INPUT_SCHEMA_VERSION:
        raise ArchiveWriterError(f"schema_version must be {INPUT_SCHEMA_VERSION}")

    review_status = _require_non_empty_string(payload.get("review_status"), "review_status")
    if review_status != "locally_reviewed":
        raise ArchiveWriterError("review_status must be locally_reviewed")

    record_id = _require_non_empty_string(payload.get("archive_record_id"), "archive_record_id")
    if not SAFE_RECORD_ID.fullmatch(record_id) or ".." in record_id or "/" in record_id or "\\" in record_id:
        raise ArchiveWriterError("archive_record_id is not a safe local file stem")

    _require_non_empty_string(payload.get("reviewed_at"), "reviewed_at")
    _require_non_empty_string(payload.get("reviewed_by"), "reviewed_by")

    concept = _require_mapping(payload.get("concept"), "concept")
    _require_non_empty_string(concept.get("concept_id"), "concept.concept_id")
    _require_non_empty_string(concept.get("label"), "concept.label")

    card = _require_mapping(payload.get("card"), "card")
    _require_non_empty_string(card.get("title"), "card.title")
    _require_non_empty_string(card.get("summary"), "card.summary")
    _require_non_empty_string(card.get("cinematic_prompt"), "card.cinematic_prompt")

    governance = _require_mapping(payload.get("governance"), "governance")
    for key in REQUIRED_GOVERNANCE_FALSE_KEYS:
        if governance.get(key) is not False:
            raise ArchiveWriterError(f"governance.{key} must be false")

    source_trace = _require_mapping(payload.get("source_trace"), "source_trace")
    for key in [
        "export_phase",
        "schema_phase",
        "sample_review_phase",
        "writer_contract_phase",
        "implementation_boundary_phase",
    ]:
        _require_non_empty_string(source_trace.get(key), f"source_trace.{key}")

    return json.loads(_canonical_json(payload))


def build_archive_record(payload: dict[str, Any]) -> dict[str, Any]:
    """Build the deterministic archive record written to disk."""

    reviewed_payload = validate_reviewed_concept_card(payload)
    return {
        "archive_schema_version": OUTPUT_SCHEMA_VERSION,
        "archive_writer_phase": WRITER_PHASE,
        "archive_writer_scope": "local writer only",
        "integration_boundaries": {
            "frontend_archive_controls": False,
            "backend_services": False,
            "adapter_endpoints": False,
            "database_tables": False,
            "sql_migrations": False,
            "evidence_promotion": False,
            "citations": False,
            "concept_relations": False,
            "interpretations": False,
            "buchanan_specific_claims": False,
        },
        "reviewed_concept_card": reviewed_payload,
    }


def archive_path_for(payload: dict[str, Any], archive_root: str | Path) -> Path:
    """Return the safe target path for a reviewed payload inside archive_root."""

    reviewed_payload = validate_reviewed_concept_card(payload)
    root = Path(archive_root).expanduser()
    if root.exists() and not root.is_dir():
        raise ArchiveWriterError("archive_root exists and is not a directory")
    file_name = f"{reviewed_payload['archive_record_id']}.json"
    return root / file_name


def write_reviewed_concept_card_archive(payload: dict[str, Any], archive_root: str | Path, *, create_root: bool = True) -> dict[str, Any]:
    """Write a reviewed concept card archive record idempotently."""

    record = build_archive_record(payload)
    target = archive_path_for(payload, archive_root)
    root = target.parent

    if create_root:
        root.mkdir(parents=True, exist_ok=True)
    elif not root.exists():
        raise ArchiveWriterError("archive_root does not exist and create_root is false")

    content = _canonical_json(record)
    digest = _sha256_text(content)

    if target.exists():
        existing = target.read_text()
        if existing != content:
            raise ArchiveWriterError(f"refusing to overwrite conflicting archive file: {target}")
        return {"path": str(target), "sha256": digest, "created": False, "idempotent": True}

    target.write_text(content)
    return {"path": str(target), "sha256": digest, "created": True, "idempotent": False}


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    return _require_mapping(value, "input JSON")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write a local reviewed concept card archive record.")
    parser.add_argument("--input", required=True, help="Path to reviewed concept card JSON payload")
    parser.add_argument("--archive-root", required=True, help="Explicit local archive root")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print target path without writing")
    args = parser.parse_args(argv)

    payload = _load_json(Path(args.input))
    target = archive_path_for(payload, args.archive_root)
    if args.dry_run:
        print(_canonical_json({"valid": True, "target": str(target)}), end="")
        return 0

    result = write_reviewed_concept_card_archive(payload, args.archive_root)
    print(_canonical_json(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
