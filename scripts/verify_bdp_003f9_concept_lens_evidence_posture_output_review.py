#!/usr/bin/env python3
"""Verify BDP-003F.9 Concept Lens evidence posture output review."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BDP_003F9_CONCEPT_LENS_EVIDENCE_POSTURE_OUTPUT_REVIEW.md"
STATE = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
F8_SERVICE = ROOT / "scripts" / "concept_lens_archive_evidence_posture_service.py"

PHASE_KEY = "bdp_003f9_concept_lens_evidence_posture_output_review"
NEXT_STEP = "BDP-003F.10 — Define approved read-only bridge from existing archive evidence readback into the Concept Lens service."


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.exists(), f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def verify_doc() -> None:
    text = read(DOC)
    required = [
        "BDP-003F.9",
        "review-only",
        "Outcome C",
        "The archive evidence exists in governed project state, but no approved live readback adapter is currently exposed for the Concept Lens service default path.",
        "Body without Organs",
        "archive_lookup_status: no_archive_match",
        "evidence_posture: exploratory_unverified",
        "No live archive adapter was configured",
        "concepts -> concept_mentions -> passages -> citations -> sources",
        "F8 is safe as a local read-only service shell",
        "UI integration remains blocked",
        NEXT_STEP,
    ]
    for needle in required:
        require(needle in text, f"Review doc missing required text: {needle}")

    blocked_terms = [
        "frontend wiring;",
        "Concept Lens UI dock;",
        "backend routes;",
        "adapter endpoints;",
        "SQL migrations;",
        "database mutation;",
        "citation creation;",
        "concept mention creation;",
        "concept relation creation;",
        "interpretation insertion;",
        "evidence promotion;",
        "Buchanan-specific claims;",
    ]
    for needle in blocked_terms:
        require(needle in text, f"Review doc missing blocked boundary: {needle}")


def verify_state() -> None:
    data = json.loads(read(STATE))
    record = data.get(PHASE_KEY)
    require(isinstance(record, dict), f"State missing {PHASE_KEY}")
    require(record.get("status") == "complete", "F9 state status must be complete")
    require(record.get("review_only") is True, "F9 must be review-only")
    require(record.get("finding") == "outcome_c_existing_archive_evidence_not_currently_reachable_by_default_service_path", "F9 finding must be Outcome C")
    require(record.get("known_archive_case") == "Body without Organs", "F9 known archive case must be Body without Organs")
    require(record.get("f8_service_intentionally_non_live_by_default") is True, "F8 must be marked intentionally non-live by default")
    require(record.get("ui_integration_blocked") is True, "UI integration must remain blocked")
    require(record.get("live_sql_archive_adapter_contract_needed_next") is True, "Adapter/bridge contract must be required next")
    require(record.get("next_step") == NEXT_STEP, "F9 next step mismatch")

    false_fields = [
        "frontend_implementation",
        "concept_lens_ui_dock_added",
        "streamlit_controls_added",
        "new_navigation_surface_keys_added",
        "backend_route_added",
        "adapter_endpoint_added",
        "sql_migration_added",
        "database_tables_added",
        "database_mutation",
        "source_ingestion_added",
        "citation_creation_added",
        "concept_mention_creation_added",
        "concept_relation_creation_added",
        "interpretation_insertion_added",
        "evidence_promotion_added",
        "buchanan_claims_created",
        "automatic_chat_filtering_added",
        "external_llm_routing_added",
    ]
    for key in false_fields:
        require(record.get(key) is False, f"F9 boundary must remain false: {key}")


def verify_handover() -> None:
    text = read(HANDOVER)
    for needle in [
        "## BDP-003F.9 — Concept Lens Evidence Posture Output Review",
        "Finding: Outcome C.",
        "Concept Lens UI integration remains blocked.",
        "scripts/verify_bdp_003f9_concept_lens_evidence_posture_output_review.py",
        NEXT_STEP,
    ]:
        require(needle in text, f"Handover missing required text: {needle}")


def verify_f8_service_not_modified_by_f9() -> None:
    # This verifier does not assert a git diff, because the operator may have local
    # changes before applying. It does ensure the F8 service still exists and compiles.
    require(F8_SERVICE.exists(), "F8 service module missing")
    subprocess.run(["python3", "-m", "py_compile", str(F8_SERVICE)], check=True)


def main() -> None:
    verify_doc()
    verify_state()
    verify_handover()
    verify_f8_service_not_modified_by_f9()
    print("[OK] BDP-003F.9 Concept Lens evidence posture output review verified")


if __name__ == "__main__":
    main()
