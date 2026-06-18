#!/usr/bin/env python3
"""Verify BDP-003F.13 Concept Lens UI integration contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = "BDP-003F.13"
PHASE_KEY = "bdp_003f13_concept_lens_ui_integration_contract"
DOC = ROOT / "docs/BDP_003F13_CONCEPT_LENS_UI_INTEGRATION_CONTRACT.md"
STATE = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
FRONTEND = ROOT / "frontend/dark_precursor.py"
F10_VERIFIER = ROOT / "scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py"
F11_VERIFIER = ROOT / "scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py"
F12_VERIFIER = ROOT / "scripts/verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py"
NEXT_STEP = "BDP-003F.14 — Wire the approved Concept Lens read-only evidence posture display into the frontend after contract verification."


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.exists(), f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def verify_doc() -> None:
    doc = read(DOC)
    required = [
        "BDP-003F.13",
        "UI integration contract only",
        "Frontend implementation: No",
        "Streamlit wiring: No",
        "Database mutation: No",
        "SQL migration: No",
        "existing archive readback bridge -> Concept Lens evidence posture service -> rights-aware display model",
        "concepts -> concept_mentions -> passages -> citations -> sources",
        "Archive evidence posture",
        "Archive-grounded match",
        "Source-bound description",
        "Exploratory / unverified",
        "No archive match",
        "Rights-limited display",
        "omitted_by_rights_policy",
        "Body without Organs",
        "we repress because we repeat",
        "assemblage",
        "This panel displays read-only archive evidence posture",
        "frontend wiring",
        "Concept Lens UI dock implementation",
        "Streamlit controls",
        "database mutation",
        "evidence promotion",
        "Buchanan-specific claims",
        "read_concept_lens_archive_evidence_posture_via_existing_archive_bridge",
        NEXT_STEP,
    ]
    for needle in required:
        require(needle in doc, f"F13 doc missing required text: {needle}")


def verify_state() -> None:
    data = json.loads(read(STATE))
    record = data.get(PHASE_KEY) or data.get("phases", {}).get(PHASE)
    require(isinstance(record, dict), "State missing BDP-003F.13 record")
    require(record.get("phase") == PHASE, "F13 state phase mismatch")
    require(record.get("status") == "complete", "F13 status should be complete")
    require(record.get("controlled_slice") == "ui_integration_contract_only", "F13 controlled slice mismatch")
    require(record.get("contract_only") is True, "F13 must be contract-only")
    require(record.get("frontend_implementation") is False, "F13 must not add frontend implementation")
    require(record.get("frontend_wiring_approved") is False, "F13 must not approve wiring in this phase")
    require(record.get("concept_lens_ui_dock_added") is False, "F13 must not add UI dock")
    require(record.get("streamlit_controls_added") is False, "F13 must not add Streamlit controls")
    for blocked in [
        "backend_routes_added",
        "adapter_endpoints_added",
        "sql_migrations_added",
        "database_mutation",
        "citation_creation_added",
        "concept_mention_creation_added",
        "concept_relation_creation_added",
        "interpretation_insertion_added",
        "evidence_promotion_added",
        "buchanan_claims_created",
        "automatic_chat_filtering_added",
        "external_llm_routing_added",
        "source_ingestion_added",
    ]:
        require(record.get(blocked) is False, f"F13 must keep {blocked}=false")
    require(record.get("next_step") == NEXT_STEP, "F13 record next_step mismatch")
    require(data.get("current_phase") == PHASE, "Global current_phase should be BDP-003F.13")
    require(data.get("next_step") == NEXT_STEP, "Global next_step mismatch")


def verify_handover() -> None:
    handover = read(HANDOVER)
    for needle in [
        "BDP-003F.13 — Concept Lens UI Integration Contract for Read-only Evidence Posture Display",
        "UI integration contract only",
        "Archive evidence posture",
        "Body without Organs",
        "we repress because we repeat",
        "assemblage",
        "no frontend wiring",
        "no Concept Lens UI dock implementation",
        NEXT_STEP,
    ]:
        require(needle in handover, f"Handover missing required text: {needle}")


def verify_progression_safe_verifiers() -> None:
    for path in [F10_VERIFIER, F11_VERIFIER, F12_VERIFIER]:
        text = read(path)
        require("BDP-003F.13" in text, f"{path.name} must be F13 progression-aware")
        require("BDP-003F.14" in text, f"{path.name} must allow the F13 next step")


def verify_frontend_not_wired_by_f13() -> None:
    frontend = read(FRONTEND)
    forbidden = [
        "BDP-003F.13 CONCEPT LENS UI INTEGRATION START",
        "Archive evidence posture",
        "read_concept_lens_archive_evidence_posture_via_existing_archive_bridge(",
    ]
    for needle in forbidden:
        require(needle not in frontend, f"F13 must not wire frontend implementation marker/text: {needle}")


def main() -> None:
    verify_doc()
    verify_state()
    verify_handover()
    verify_progression_safe_verifiers()
    verify_frontend_not_wired_by_f13()
    print("[OK] BDP-003F.13 Concept Lens UI integration contract verified")


if __name__ == "__main__":
    main()
