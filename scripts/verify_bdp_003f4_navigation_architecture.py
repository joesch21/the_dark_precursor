#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
F3_VERIFIER_PATH = ROOT / "scripts" / "verify_bdp_003f3_about_page_running_frontend_review.py"
F4_DOC_PATH = ROOT / "docs" / "BDP_003F4_DARK_PRECURSOR_NAVIGATION_ARCHITECTURE.md"
SELF_PATH = ROOT / "scripts" / "verify_bdp_003f4_navigation_architecture.py"

PHASE = "BDP-003F.4"
RECORD_KEY = "bdp_003f4_dark_precursor_navigation_architecture"
NEXT_STEP = "BDP-003F.5 — Wire navigation architecture only after BDP-003F.4 is committed and pushed."


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read_text(path: Path) -> str:
    require(path.exists(), f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run_verifier(path: Path) -> None:
    require(path.exists(), f"missing verifier: {path.relative_to(ROOT)}")
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")
    require(result.returncode == 0, f"verifier failed: {path.relative_to(ROOT)}")


def require_false(record: dict, key: str) -> None:
    require(record.get(key) is False, f"{key} must be false")


def main() -> None:
    run_verifier(F3_VERIFIER_PATH)

    self_text = read_text(SELF_PATH)
    forbidden_lookup = "first_" + "existing("
    require(forbidden_lookup not in self_text, "F4 verifier must not use first-existing path fallback")
    require('STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"' in self_text, "F4 verifier must hardcode root state path")
    require('HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"' in self_text, "F4 verifier must hardcode root handover path")

    doc = read_text(F4_DOC_PATH)
    for marker in [
        "navigation architecture definition only",
        "cinematic concept stage** remains the primary surface",
        "The **About page** is a supporting explanation surface.",
        "Supporting pages must have a clear return path to the concept stage.",
        "Navigation must preserve cinematic immersion.",
        "Navigation must avoid dashboard drift.",
        "Navigation must not create or imply scholarly authority.",
        "atmosphere is not authority",
        "BDP-003F.4 authorizes no implementation.",
        NEXT_STEP,
    ]:
        require(marker in doc, f"F4 doc missing marker: {marker}")

    for forbidden in [
        "new frontend page routing",
        "new Streamlit controls",
        "backend services",
        "adapter endpoints",
        "database tables",
        "SQL migrations",
        "evidence promotion",
        "citations",
        "concept relations",
        "interpretations",
        "Buchanan-specific claims",
        "adaptive navigation behaviour",
    ]:
        require(forbidden in doc, f"F4 doc missing forbidden boundary: {forbidden}")

    state = json.loads(read_text(STATE_PATH))
    record = state.get(RECORD_KEY)
    require(isinstance(record, dict), "missing F4 state record")

    require(record.get("phase") == PHASE, "F4 phase mismatch")
    require(record.get("status") == "complete", "F4 status mismatch")
    require(record.get("controlled_slice") == "navigation_architecture_definition_only", "F4 controlled slice mismatch")
    require(record.get("definition_only") is True, "F4 must be definition-only")
    require(record.get("primary_surface") == "cinematic_concept_stage", "primary surface must be cinematic concept stage")
    require("about_page" in record.get("supporting_surfaces", []), "About page must be supporting surface")
    require(record.get("review_output") == "docs/BDP_003F4_DARK_PRECURSOR_NAVIGATION_ARCHITECTURE.md", "F4 review output mismatch")
    require(record.get("verifier") == "scripts/verify_bdp_003f4_navigation_architecture.py", "F4 verifier path mismatch")
    require(record.get("next_step") == NEXT_STEP, "F4 next step mismatch")

    for key in [
        "frontend_implementation",
        "backend_services_added",
        "adapter_endpoints_added",
        "database_tables_added",
        "sql_migrations_added",
        "evidence_promotion_added",
        "citations_created",
        "concept_relations_created",
        "interpretations_created",
        "buchanan_claims_created",
        "adaptive_navigation_added",
        "hidden_personalization_added",
    ]:
        require_false(record, key)

    principles = record.get("navigation_principles", [])
    for principle in [
        "preserve_cinematic_immersion",
        "avoid_dashboard_drift",
        "supporting_surfaces_return_to_concept_stage",
        "navigation_does_not_create_authority",
        "no_hidden_adaptation",
    ]:
        require(principle in principles, f"missing navigation principle: {principle}")

    future_surfaces = record.get("future_surface_candidates", [])
    for surface in [
        "concept_stage",
        "about",
        "archive_reviewed_outputs",
        "source_evidence_posture",
        "settings_controls",
        "help_orientation",
    ]:
        require(surface in future_surfaces, f"missing future surface candidate: {surface}")


    handover = read_text(HANDOVER_PATH)
    require("## BDP-003F.4 — Navigation Architecture Definition" in handover, "handover missing F4 section")
    require("The cinematic concept stage remains the primary surface." in handover, "handover missing primary surface statement")
    require("No frontend implementation, backend services, adapter endpoints, database tables, SQL migrations, evidence promotion, citations, concept relations, interpretations, or Buchanan-specific claims are added." in handover, "handover missing implementation boundary")
    require(NEXT_STEP in handover, "handover missing exact next step")

    print("[OK] BDP-003F.4 Dark Precursor navigation architecture verified")


if __name__ == "__main__":
    main()
