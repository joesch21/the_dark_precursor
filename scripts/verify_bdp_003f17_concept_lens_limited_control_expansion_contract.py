#!/usr/bin/env python3
"""Verify BDP-003F.17 Concept Lens limited control expansion contract."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
PHASE = "BDP-003F.17"
PHASE_KEY = "bdp_003f17_concept_lens_limited_control_expansion_contract"
DOC_PATH = ROOT / "docs" / "BDP_003F17_CONCEPT_LENS_LIMITED_CONTROL_EXPANSION_CONTRACT.md"
PATCH_README_PATH = ROOT / "BDP_003F17_PATCH_README.md"
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
NEXT_SAFE_STEP = "BDP-003F.18 — Define Concept Lens controlled concept coverage expansion contract after F17 control boundary."

FORBIDDEN_MODIFIED_FILES = {
    "frontend/dark_precursor.py",
    "scripts/concept_lens_archive_evidence_posture_service.py",
    "scripts/concept_lens_existing_archive_evidence_readback_bridge.py",
}

REQUIRED_DOC_SNIPPETS = [
    "BDP-003F.17 defines the first bounded control expansion contract",
    "This phase is a contract phase only. It does not implement controls.",
    "Outcome C — Ready for both separate later contract tracks, but implementation remains blocked.",
    "No frontend changes were made.",
    "No service changes were made.",
    "No bridge changes were made.",
    "No new frontend controls were added.",
    "No concept examples were added.",
    "No free-text search was added.",
    "The read-only evidence posture boundary remains intact.",
    "Controlled preset selector",
    "Display density control",
    "Evidence detail expander",
    "Rights boundary explainer",
    "Reset to default Concept Lens view",
    "Concept coverage expansion is not authorized by BDP-003F.17.",
    NEXT_SAFE_STEP,
]

REQUIRED_README_SNIPPETS = [
    "contract-only patch bundle",
    "no frontend changes",
    "no service or bridge changes",
    "no new frontend controls are implemented",
    "no concept examples are added",
    "no free-text concept search",
    "BDP-003F.18",
]

EXPECTED_FALSE_RECORD_FLAGS = [
    "implementation_added",
    "frontend_modified_by_bdp_003f17",
    "service_modified_by_bdp_003f17",
    "bridge_modified_by_bdp_003f17",
    "new_frontend_controls_added",
    "concept_coverage_expanded",
    "free_text_search_input_added",
    "concept_search_box_added",
    "new_concept_examples_added",
]

EXPECTED_FALSE_BOUNDARIES = [
    "frontend_changes",
    "service_changes",
    "bridge_changes",
    "new_frontend_controls",
    "new_concept_search_box",
    "new_concept_examples",
    "concept_coverage_expansion",
    "backend_route",
    "adapter_endpoint",
    "sql_migration",
    "sql_mutation",
    "database_writes",
    "archive_row_creation",
    "citation_creation",
    "claim_creation",
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

EXPECTED_ALLOWED_CONTROLS = [
    "controlled_preset_selector_existing_examples_only",
    "display_density_control",
    "read_only_evidence_detail_expander",
    "rights_boundary_explainer_toggle",
    "reset_to_default_concept_lens_view",
]

CONTROLLED_EXAMPLES = [
    "Body without Organs",
    "we repress because we repeat",
    "assemblage",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read_text(path: Path) -> str:
    require(path.exists(), f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require_snippets(label: str, text: str, snippets: Iterable[str]) -> None:
    missing = [snippet for snippet in snippets if snippet not in text]
    require(not missing, f"{label} missing required snippets: {missing}")


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
        path = raw_line[3:].strip()
        if " -> " in path:
            old, new = path.split(" -> ", 1)
            changed.add(old.strip())
            changed.add(new.strip())
        else:
            changed.add(path)
    return changed


def verify_no_forbidden_file_modifications() -> None:
    changed = git_changed_files()
    forbidden = sorted(path for path in changed if path in FORBIDDEN_MODIFIED_FILES)
    require(not forbidden, f"F17 must not modify frontend/service/bridge files: {forbidden}")


def verify_state() -> None:
    state = json.loads(read_text(STATE_PATH))
    require(isinstance(state, dict), "BUCHANAN_SYSTEM_STATE.json must be an object")
    phases = state.get("phases", {})
    require(isinstance(phases, dict), "state phases field must be an object")
    require(PHASE in phases, "State missing phases.BDP-003F.17")
    require(PHASE_KEY in state, f"State missing top-level {PHASE_KEY}")

    record = phases[PHASE]
    top_record = state[PHASE_KEY]
    require(record == top_record, "Top-level F17 record must match phases.BDP-003F.17")
    require(record.get("phase") == PHASE, "F17 state record has wrong phase")
    require(record.get("status") == "complete", "F17 state record must be complete")
    require(record.get("controlled_slice") == "limited_control_expansion_contract_only", "F17 must be contract-only")
    require(record.get("contract_only") is True, "F17 must record contract_only=true")
    require("BDP-003F.16" in str(record.get("input_phase", "")), "F17 must name F16 as input")
    require("Outcome C" in str(record.get("input_outcome", "")), "F17 must preserve F16 Outcome C input")
    require(record.get("allowed_later_controls_defined") is True, "F17 must define allowed later controls")
    require(record.get("allowed_later_controls") == EXPECTED_ALLOWED_CONTROLS, "F17 allowed later controls changed unexpectedly")
    require(record.get("controlled_concept_examples_unchanged") == CONTROLLED_EXAMPLES, "F17 must preserve controlled examples unchanged")
    require(record.get("next_safe_step") == NEXT_SAFE_STEP, "F17 must record F18 as next safe step")

    for flag in EXPECTED_FALSE_RECORD_FLAGS:
        require(record.get(flag) is False, f"F17 record flag must remain false: {flag}")

    boundaries = record.get("boundaries")
    require(isinstance(boundaries, dict), "F17 state record missing boundaries")
    for flag in EXPECTED_FALSE_BOUNDARIES:
        require(boundaries.get(flag) is False, f"F17 boundary flag must remain false: {flag}")

    for key in ["current_phase", "last_updated_phase"]:
        require(state.get(key) == PHASE, f"Global {key} must be BDP-003F.17")
    for key in ["next_recommended_step", "current_next_step", "next_step", "recommended_next_step", "next_safe_step"]:
        require(state.get(key) == NEXT_SAFE_STEP, f"Global {key} must match F17 next safe step")


def verify_handover() -> None:
    text = read_text(HANDOVER_PATH)
    require_snippets(
        "BUCHANAN_THREAD_HANDOVER.md",
        text,
        [
            "BDP-003F.17 — Concept Lens limited control expansion contract",
            "limited-control contract only",
            "No frontend changes were made.",
            "No service or bridge changes were made.",
            "No new frontend controls were added.",
            "No concept examples were added.",
            "No free-text search was added.",
            NEXT_SAFE_STEP,
        ],
    )


def main() -> None:
    doc_text = read_text(DOC_PATH)
    readme_text = read_text(PATCH_README_PATH)
    require_snippets("F17 contract doc", doc_text, REQUIRED_DOC_SNIPPETS)
    require_snippets("F17 patch README", readme_text, REQUIRED_README_SNIPPETS)
    verify_state()
    verify_handover()
    verify_no_forbidden_file_modifications()
    print("[OK] BDP-003F.17 Concept Lens limited control expansion contract verified")


if __name__ == "__main__":
    main()
