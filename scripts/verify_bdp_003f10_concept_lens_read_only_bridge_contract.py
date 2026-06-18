#!/usr/bin/env python3
"""Verify BDP-003F.10 Concept Lens read-only bridge contract."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BDP_003F10_CONCEPT_LENS_READ_ONLY_BRIDGE_CONTRACT.md"
STATE = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
F8_SERVICE = ROOT / "scripts" / "concept_lens_archive_evidence_posture_service.py"
F9_DOC = ROOT / "docs" / "BDP_003F9_CONCEPT_LENS_EVIDENCE_POSTURE_OUTPUT_REVIEW.md"

PHASE_KEY = "bdp_003f10_concept_lens_existing_archive_readback_bridge_contract"
NEXT_STEP = "BDP-003F.11 — Implement the approved read-only bridge from existing archive evidence readback into the Concept Lens service."


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.exists(), f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def verify_python_compile(path: Path) -> None:
    require(path.exists(), f"Missing Python file: {path.relative_to(ROOT)}")
    subprocess.run(["python3", "-m", "py_compile", str(path)], check=True, cwd=ROOT)


def verify_doc() -> None:
    text = read(DOC)
    required = [
        "BDP-003F.10",
        "read-only bridge contract definition only",
        "BDP-003F.9 recorded Outcome C",
        "concept_lens_existing_archive_evidence_readback_bridge.v1",
        "scripts/concept_lens_existing_archive_evidence_readback_bridge.py",
        "read_existing_archive_evidence_rows_for_concept",
        "scripts/read_bdp_001r_bwo_source_bound_description.py",
        "scripts/read_bdp_002b_bwo_evidence_card.py",
        "scripts/concept_lens_archive_evidence_posture_service.py",
        "read_concept_lens_archive_evidence_posture",
        "concepts -> concept_mentions -> passages -> citations -> sources",
        "archive_lookup_status: archive_grounded_match",
        "evidence_posture: archive_grounded",
        "omitted_by_rights_policy",
        "UI integration remains blocked",
        NEXT_STEP,
    ]
    for needle in required:
        require(needle in text, f"F10 doc missing required text: {needle}")

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
        "the F8 service implementation.",
    ]
    for needle in blocked_terms:
        require(needle in text, f"F10 doc missing blocked boundary: {needle}")


def verify_state() -> None:
    data = json.loads(read(STATE))
    record = data.get(PHASE_KEY) or data.get("phases", {}).get("BDP-003F.10")
    require(isinstance(record, dict), "State missing BDP-003F.10 record")
    require(record.get("phase") == "BDP-003F.10", "State phase mismatch")
    require(record.get("status") == "complete", "State status must be complete")
    require(record.get("contract_only") is True, "F10 must be contract-only")
    require(record.get("definition_only") is True, "F10 must be definition-only")
    require(record.get("bridge_contract_defined") is True, "Bridge contract must be defined")
    require(record.get("bridge_implemented") is False, "F10 must not implement bridge")
    require(record.get("service_modified") is False, "F10 must not modify F8 service")
    require(record.get("frontend_implementation") is False, "F10 must not add frontend")
    require(record.get("database_mutation") is False, "F10 must not mutate database")
    require(record.get("sql_migration_added") is False, "F10 must not add SQL migration")
    require(record.get("adapter_endpoint_added") is False, "F10 must not add adapter endpoint")
    require(record.get("evidence_promotion_added") is False, "F10 must not promote evidence")
    require(record.get("buchanan_claims_created") is False, "F10 must not create Buchanan claims")
    require(record.get("next_step") == NEXT_STEP, "State next step mismatch")
    require(data.get("current_phase") == "BDP-003F.10", "Global current_phase should be BDP-003F.10")
    require(data.get("next_step") == NEXT_STEP, "Global next_step mismatch")


def verify_handover() -> None:
    text = read(HANDOVER)
    required = [
        "BDP-003F.10 — Concept Lens Existing Archive Evidence Readback Bridge Contract",
        "read-only bridge contract definition only",
        "concept_lens_existing_archive_evidence_readback_bridge.v1",
        "scripts/read_bdp_001r_bwo_source_bound_description.py",
        "scripts/read_bdp_002b_bwo_evidence_card.py",
        "concepts -> concept_mentions -> passages -> citations -> sources",
        "UI integration remains blocked",
        NEXT_STEP,
    ]
    for needle in required:
        require(needle in text, f"Handover missing required text: {needle}")


def verify_existing_phase_anchors() -> None:
    f9_text = read(F9_DOC)
    require("Outcome C" in f9_text, "F9 Outcome C anchor missing")
    verify_python_compile(F8_SERVICE)


def main() -> None:
    verify_doc()
    verify_state()
    verify_handover()
    verify_existing_phase_anchors()
    print("[OK] BDP-003F.10 Concept Lens read-only bridge contract verified")


if __name__ == "__main__":
    main()
