#!/usr/bin/env python3
"""Verify BDP-003F.15 Concept Lens running-frontend review record."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

PHASE = "BDP-003F.15"
PHASE_KEY = "bdp_003f15_concept_lens_running_frontend_review"
DOC_PATH = Path("docs/BDP_003F15_CONCEPT_LENS_RUNNING_FRONTEND_REVIEW.md")
STATE_PATH = Path("BUCHANAN_SYSTEM_STATE.json")
HANDOVER_PATH = Path("BUCHANAN_THREAD_HANDOVER.md")
README_PATH = Path("BDP_003F15_PATCH_README.md")
UPDATE_SCRIPT = Path("scripts/update_bdp_003f15_concept_lens_running_frontend_review.py")
VERIFY_SCRIPT = Path("scripts/verify_bdp_003f15_concept_lens_running_frontend_review.py")

BLOCKED_MODIFIED_FILES = {
    "frontend/dark_precursor.py",
    "scripts/concept_lens_archive_evidence_posture_service.py",
    "scripts/concept_lens_existing_archive_evidence_readback_bridge.py",
}

ALLOWED_CHANGED_FILES = {
    str(DOC_PATH),
    str(STATE_PATH),
    str(HANDOVER_PATH),
    str(README_PATH),
    str(UPDATE_SCRIPT),
    str(VERIFY_SCRIPT),
}

CONTROLLED_EXAMPLES = [
    "Body without Organs",
    "we repress because we repeat",
    "assemblage",
]

REQUIRED_DOC_PHRASES = [
    "running-frontend review only",
    "Body without Organs",
    "we repress because we repeat",
    "assemblage",
    "Archive grounded",
    "Source-bound description",
    "Exploratory / unverified",
    "No archive match",
    "Rights-limited display",
    "Read-only archive evidence posture",
    "This panel displays read-only archive evidence posture. It does not create citations, claims, interpretations, concept relations, or database records.",
    "No free-text concept search input",
    "No create / save / promote / cite / interpret controls",
    "no database writes",
    "no citation creation",
    "no concept relation creation",
    "no interpretation insertion",
    "no evidence promotion",
]

BLOCKED_FLAGS_FALSE = [
    "frontend_modified_by_bdp_003f15",
    "service_modified_by_bdp_003f15",
    "bridge_modified_by_bdp_003f15",
    "new_frontend_controls_added",
    "free_text_search_input_added",
    "concept_search_box_added",
    "expanded_concept_coverage",
    "backend_route_added",
    "adapter_endpoint_added",
    "sql_migration_added",
    "database_mutation",
    "database_writes_added",
    "archive_row_creation_added",
    "source_ingestion_added",
    "citation_creation_added",
    "claim_creation_added",
    "concept_mention_creation_added",
    "concept_relation_creation_added",
    "interpretation_insertion_added",
    "evidence_promotion_added",
    "buchanan_claims_created",
    "external_llm_routing_added",
    "automatic_chat_filtering_added",
    "unrestricted_passage_reproduction_added",
]


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read_text(path: Path) -> str:
    require(path.exists(), f"Missing required file: {path}")
    return path.read_text(encoding="utf-8")


def load_state() -> dict[str, Any]:
    require(STATE_PATH.exists(), f"Missing required state file: {STATE_PATH}")
    with STATE_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def git_changed_files() -> set[str]:
    try:
        proc = subprocess.run(
            ["git", "status", "--short"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"Unable to inspect git status: {exc}")

    changed: set[str] = set()
    for raw_line in proc.stdout.splitlines():
        if not raw_line.strip():
            continue
        # Porcelain format: XY path OR XY old -> new. Use the final path for renames.
        path = raw_line[3:].strip()
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[1].strip()
        changed.add(path)
    return changed


def verify_git_boundary() -> None:
    changed = git_changed_files()
    blocked_changed = sorted(changed.intersection(BLOCKED_MODIFIED_FILES))
    require(not blocked_changed, f"F15 must not modify frontend/service/bridge files: {blocked_changed}")

    unexpected = sorted(path for path in changed if path.startswith(("frontend/", "backend/", "data/", "prompts/")))
    require(not unexpected, f"F15 must remain documentation/review-only; unexpected changed files: {unexpected}")


def verify_documents() -> None:
    doc = read_text(DOC_PATH)
    readme = read_text(README_PATH)
    handover = read_text(HANDOVER_PATH)
    update_script = read_text(UPDATE_SCRIPT)

    for phrase in REQUIRED_DOC_PHRASES:
        require(phrase in doc, f"Review doc missing required phrase: {phrase}")

    require("Do not commit automatically" in readme, "Patch README must warn not to commit automatically")
    require("BDP-003F.15 — Concept Lens Running Frontend Review" in handover, "Handover missing BDP-003F.15 section")
    require("Files intentionally not modified" in handover, "Handover must record unmodified frontend/service/bridge boundary")
    require("BDP-003F.16" in handover, "Handover must record next safe step")
    require("frontend/dark_precursor.py" in update_script, "Updater must record frontend target as reviewed/unmodified")
    require("database_writes_added" in update_script, "Updater must preserve no database writes flag")



def global_next_step_is_allowed(value: object, f15_next_safe_step: object) -> bool:
    """Allow F15 verifier to pass after later approved F16/F17 progression.

    During F15 itself, global next-step fields should match the F15 record.
    After F16, those same global fields may validly advance to the F16
    readiness decision or the F17 limited-control contract next step.
    """
    text = str(value or "")
    f15_text = str(f15_next_safe_step or "")
    return (
        text == f15_text
        or text.startswith("BDP-003F.16")
        or text.startswith("BDP-003F.17")
        or "Decide Concept Lens control and concept coverage expansion readiness" in text
        or "Define Concept Lens limited control expansion contract after F16 readiness decision" in text
    )

def verify_state() -> None:
    state = load_state()
    phases = state.get("phases", {})
    require(PHASE in phases, "State missing phases.BDP-003F.15")
    require(PHASE_KEY in state, f"State missing top-level {PHASE_KEY}")

    phase_record = phases[PHASE]
    top_record = state[PHASE_KEY]
    require(phase_record == top_record, "Top-level F15 record must match phases.BDP-003F.15")

    require(phase_record.get("phase") == PHASE, "F15 record has wrong phase id")
    require(phase_record.get("status") == "complete", "F15 record must be complete after update script runs")
    require(phase_record.get("controlled_slice") == "running_frontend_review_only", "F15 must be a running-frontend review-only slice")
    require(phase_record.get("review_only") is True, "F15 must record review_only=true")
    require(phase_record.get("manual_frontend_inspection_recorded") is True, "F15 must record manual frontend inspection")

    require(phase_record.get("controlled_concept_examples_reviewed") == CONTROLLED_EXAMPLES, "F15 must record the three controlled examples only")
    require("This panel displays read-only archive evidence posture" in phase_record.get("boundary_note", ""), "F15 must record boundary note")

    for flag in BLOCKED_FLAGS_FALSE:
        require(phase_record.get(flag) is False, f"F15 blocked flag must remain false: {flag}")

    result = phase_record.get("running_frontend_review_result")
    require(result in {"pass", "repair_needed"}, "F15 must record review result as pass or repair_needed")
    require(isinstance(phase_record.get("running_frontend_review_passed"), bool), "F15 must record boolean pass/fail state")

    if result == "pass":
        require(phase_record.get("running_frontend_review_passed") is True, "Pass result must set running_frontend_review_passed=true")
        require("Decide Concept Lens control and concept coverage expansion readiness" in phase_record.get("next_safe_step", ""), "Passed F15 must point to readiness decision next")
    else:
        require(phase_record.get("running_frontend_review_passed") is False, "repair_needed result must set running_frontend_review_passed=false")
        require(phase_record.get("running_frontend_review_findings"), "repair_needed result must record findings")
        require("Repair the Concept Lens read-only evidence posture display" in phase_record.get("next_safe_step", ""), "Repair-needed F15 must point to bounded repair next")

    for key in ["next_recommended_step", "current_next_step", "next_step", "recommended_next_step", "next_safe_step"]:
        require(
            global_next_step_is_allowed(state.get(key), phase_record.get("next_safe_step")),
            f"Global {key} must match F15 next safe step or approved F16/F17 progression",
        )


def main() -> int:
    verify_git_boundary()
    verify_documents()
    verify_state()
    print("[OK] BDP-003F.15 Concept Lens running frontend review verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
