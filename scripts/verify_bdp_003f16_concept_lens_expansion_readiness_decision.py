#!/usr/bin/env python3
"""Verify BDP-003F.16 Concept Lens expansion readiness decision."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
PHASE = "BDP-003F.16"
DOC_PATH = ROOT / "docs" / "BDP_003F16_CONCEPT_LENS_EXPANSION_READINESS_DECISION.md"
PATCH_README_PATH = ROOT / "BDP_003F16_PATCH_README.md"
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"

FORBIDDEN_MODIFIED_FILES = {
    "frontend/dark_precursor.py",
    "scripts/concept_lens_archive_evidence_posture_service.py",
    "scripts/concept_lens_existing_archive_evidence_readback_bridge.py",
}

REQUIRED_DOC_SNIPPETS = [
    "BDP-003F.16 records a decision only.",
    "F15 running frontend review is the input.",
    "Outcome C — Ready for both contract tracks, but implementation remains blocked.",
    "No frontend changes were made.",
    "No service or bridge changes were made.",
    "No controls were added.",
    "No concept examples were added.",
    "No free-text search was added.",
    "No citation, claim, interpretation, concept relation, or database record creation path was added.",
    "The read-only evidence posture boundary remains intact.",
    "BDP-003F.17 — Define Concept Lens limited control expansion contract after F16 readiness decision.",
]

REQUIRED_README_SNIPPETS = [
    "This is a decision-only patch bundle.",
    "Ready for both separate later contract tracks, but implementation remains blocked.",
    "no frontend changes",
    "no new frontend controls",
    "no new concept search box",
    "no new concept examples",
    "no SQL mutation",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require_snippets(label: str, text: str, snippets: Iterable[str]) -> None:
    missing = [snippet for snippet in snippets if snippet not in text]
    if missing:
        fail(f"{label} missing required snippets: {missing}")


def git_changed_files() -> set[str]:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"Could not inspect git status: {exc}")

    changed: set[str] = set()
    for raw_line in result.stdout.splitlines():
        if not raw_line.strip():
            continue
        path = raw_line[3:]
        if " -> " in path:
            old, new = path.split(" -> ", 1)
            changed.add(old.strip())
            changed.add(new.strip())
        else:
            changed.add(path.strip())
    return changed


def verify_no_forbidden_file_modifications() -> None:
    changed = git_changed_files()
    forbidden = sorted(path for path in changed if path in FORBIDDEN_MODIFIED_FILES)
    if forbidden:
        fail(f"F16 must not modify frontend/service/bridge files: {forbidden}")


def verify_state() -> None:
    if not STATE_PATH.exists():
        fail("Missing BUCHANAN_SYSTEM_STATE.json")
    data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    record = data.get("bdp_003f16_concept_lens_expansion_readiness_decision")
    if not isinstance(record, dict):
        fail("Missing bdp_003f16_concept_lens_expansion_readiness_decision state record")
    if record.get("phase") != PHASE:
        fail("F16 state record has wrong phase")
    if record.get("controlled_slice") != "decision_only_no_implementation":
        fail("F16 state record must be decision-only")
    if "BDP-003F.15" not in str(record.get("input_phase", "")):
        fail("F16 state record must name F15 as input")
    if "Outcome C" not in str(record.get("readiness_outcome", "")):
        fail("F16 state record must record Outcome C")
    if "BDP-003F.17" not in str(record.get("next_safe_step", "")):
        fail("F16 state record must record BDP-003F.17 as next safe step")

    boundaries = record.get("boundaries")
    if not isinstance(boundaries, dict):
        fail("F16 state record missing boundaries")
    expected_false = [
        "frontend_changes",
        "service_changes",
        "bridge_changes",
        "new_frontend_controls",
        "new_concept_search_box",
        "new_concept_examples",
        "backend_route",
        "adapter_endpoint",
        "sql_mutation",
        "database_writes",
        "archive_row_creation",
        "citation_creation",
        "concept_mention_creation",
        "concept_relation_creation",
        "interpretation_insertion",
        "evidence_promotion",
        "external_llm_routing",
        "source_ingestion",
        "unrestricted_passage_reproduction",
        "buchanan_specific_interpretive_claim_generation",
        "general_chat_filtering",
    ]
    bad = [key for key in expected_false if boundaries.get(key) is not False]
    if bad:
        fail(f"F16 boundaries must remain false for: {bad}")


def verify_handover() -> None:
    text = read_text(HANDOVER_PATH)
    require_snippets(
        "BUCHANAN_THREAD_HANDOVER.md",
        text,
        [
            "BDP-003F.16 — Concept Lens expansion readiness decision",
            "Outcome C — Ready for both separate later contract tracks, but implementation remains blocked.",
            "No frontend changes were made.",
            "No controls were added.",
            "No concept examples were added.",
            "No citation, claim, interpretation, concept relation, or database record creation path was added.",
            "BDP-003F.17 — Define Concept Lens limited control expansion contract after F16 readiness decision.",
        ],
    )


def main() -> None:
    doc_text = read_text(DOC_PATH)
    readme_text = read_text(PATCH_README_PATH)
    require_snippets("F16 decision doc", doc_text, REQUIRED_DOC_SNIPPETS)
    require_snippets("F16 patch README", readme_text, REQUIRED_README_SNIPPETS)
    verify_state()
    verify_handover()
    verify_no_forbidden_file_modifications()
    print("[OK] BDP-003F.16 Concept Lens expansion readiness decision verified")


if __name__ == "__main__":
    main()
