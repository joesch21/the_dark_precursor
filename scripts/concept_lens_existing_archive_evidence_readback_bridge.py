#!/usr/bin/env python3
"""Read-only bridge from existing archive evidence readback into Concept Lens rows.

BDP-003F.11 implements the bridge contract defined by BDP-003F.10.
The bridge prepares in-memory rows for the BDP-003F.8 posture service.
It does not create evidence, mutate a database, add citations, or create claims.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

BRIDGE_CONTRACT = "concept_lens_existing_archive_evidence_readback_bridge.v1"
SUPPORTED_REVIEW_CASE = "Body without Organs"
SUPPORTED_NORMALIZED_REVIEW_CASE = "body without organs"
OMITTED_BY_RIGHTS = "omitted_by_rights_policy"

APPROVED_READBACK_CANDIDATES = (
    "scripts/read_bdp_002b_bwo_evidence_card.py",
    "scripts/read_bdp_001r_bwo_source_bound_description.py",
)

REQUIRED_BWO_SIGNAL_GROUPS = (
    ("body without organs", "bwo"),
    ("ian buchanan", "buchanan"),
    ("the problem of the body in deleuze and guattari", "what can a body do"),
    ("citation", "citations"),
    ("concept mention", "concept_mentions", "concept mention count", "concept_mention"),
    ("source", "sources"),
)


def normalize_concept(concept: str) -> str:
    """Normalize a concept label for conservative matching."""
    return " ".join((concept or "").strip().lower().split())


def is_supported_review_case(concept: str) -> bool:
    return normalize_concept(concept) == SUPPORTED_NORMALIZED_REVIEW_CASE


def _has_signal(text: str, variants: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(variant in lowered for variant in variants)


def readback_text_confirms_bwo_chain(readback_text: str) -> bool:
    """Return true only when readback text contains enough governed BWO signals."""
    if not readback_text or not readback_text.strip():
        return False
    return all(_has_signal(readback_text, variants) for variants in REQUIRED_BWO_SIGNAL_GROUPS)


def _extract_locator(readback_text: str) -> str:
    patterns = (
        r"printed article page\s*76[^\n,;]*[,;]?\s*PDF page\s*4",
        r"PDF page\s*4",
        r"page\s*76",
    )
    for pattern in patterns:
        match = re.search(pattern, readback_text, flags=re.IGNORECASE)
        if match:
            return match.group(0).strip()
    return "printed article page 76; PDF page 4"


def _bwo_archive_row(bridge_source: str, bridge_source_script: str | None, readback_text: str) -> dict[str, Any]:
    """Construct the bounded F8-compatible row for the confirmed BWO case."""
    locator = _extract_locator(readback_text)
    return {
        "bridge_contract": BRIDGE_CONTRACT,
        "bridge_source": bridge_source,
        "bridge_source_script": bridge_source_script,
        "bridge_review_case": SUPPORTED_REVIEW_CASE,
        "concept": SUPPORTED_REVIEW_CASE,
        "concept_name": SUPPORTED_REVIEW_CASE,
        "concept_label": SUPPORTED_REVIEW_CASE,
        "normalized_concept": SUPPORTED_NORMALIZED_REVIEW_CASE,
        "concept_review_status": "accepted",
        "concept_status": "accepted",
        "concept_mention_review_status": "accepted",
        "mention_review_status": "accepted",
        "mention_type": "direct",
        "passage_id": "bdp_001o_buchanan_bwo_passage_readback",
        "citation_id": "bdp_001o_buchanan_bwo_citation_readback",
        "source_id": "bdp_001l_buchanan_body_society_1997_source_readback",
        "source_author": "Ian Buchanan",
        "source_title": "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?",
        "source_type": "article",
        "source_year": 1997,
        "publication_year": 1997,
        "source_doi": "10.1177/1357034X97003003004",
        "doi": "10.1177/1357034X97003003004",
        "locator": locator,
        "page_or_timestamp": locator,
        "rights_status": "restricted",
        "rights_display_rule": "reference_only",
        "display_rule": "reference_only",
        "authority_label": "buchanan_direct",
        "passage_text_display": OMITTED_BY_RIGHTS,
        "passage_text": OMITTED_BY_RIGHTS,
        "restricted_passage_text_display": OMITTED_BY_RIGHTS,
        "chain_complete": True,
        "complete_chain": True,
        "has_concept": True,
        "has_concept_mention": True,
        "has_reviewed_concept_mention": True,
        "has_passage": True,
        "has_citation": True,
        "has_source": True,
        "concept_relation_available": False,
        "interpretation_available": False,
        "buchanan_specific_claim_allowed": False,
        "evidence_created_by_bridge": False,
        "database_mutation": False,
    }


def read_existing_archive_evidence_rows_from_readback_text(
    concept: str,
    readback_text: str,
    *,
    bridge_source: str = "supplied_readback_text",
    bridge_source_script: str | None = None,
) -> list[dict[str, Any]]:
    """Translate already-read governed readback text into F8 rows."""
    if not is_supported_review_case(concept):
        return []
    if not readback_text_confirms_bwo_chain(readback_text):
        return []
    return [_bwo_archive_row(bridge_source, bridge_source_script, readback_text)]


def _repo_root_from_here() -> Path:
    return Path(__file__).resolve().parents[1]


def _run_candidate_script(repo_root: Path, script_path: Path) -> str:
    """Run one approved local readback script in read-only subprocess mode."""
    completed = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
        check=False,
        timeout=20,
    )
    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    if completed.returncode != 0:
        return ""
    return output


def read_existing_archive_evidence_rows_for_concept(
    concept: str,
    *,
    repo_root: str | Path | None = None,
    require_live_readback: bool = True,
) -> list[dict[str, Any]]:
    """Read approved existing archive readback paths and return F8-compatible rows."""
    if not is_supported_review_case(concept):
        return []

    root = Path(repo_root) if repo_root is not None else _repo_root_from_here()
    root = root.resolve()

    for candidate in APPROVED_READBACK_CANDIDATES:
        script_path = (root / candidate).resolve()
        if root not in script_path.parents and script_path != root:
            continue
        if not script_path.exists():
            continue
        readback_text = _run_candidate_script(root, script_path)
        rows = read_existing_archive_evidence_rows_from_readback_text(
            concept,
            readback_text,
            bridge_source="approved_existing_readback_script",
            bridge_source_script=candidate,
        )
        if rows:
            return rows

    if require_live_readback:
        return []
    return []


def main() -> None:
    parser = argparse.ArgumentParser(description="Read existing archive evidence rows for a Concept Lens concept.")
    parser.add_argument("concept", help="Concept label to read, e.g. Body without Organs.")
    parser.add_argument("--repo-root", default=None, help="Repository root. Defaults to the parent of this script directory.")
    parser.add_argument("--allow-empty", action="store_true", help="Return an empty list rather than treating no bridge rows as an error.")
    args = parser.parse_args()

    rows = read_existing_archive_evidence_rows_for_concept(args.concept, repo_root=args.repo_root)
    if not rows and not args.allow_empty:
        print(json.dumps({"rows": [], "status": "no_confirmed_existing_archive_readback"}, indent=2))
        raise SystemExit(1)
    print(json.dumps({"rows": rows, "status": "ok" if rows else "empty"}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
