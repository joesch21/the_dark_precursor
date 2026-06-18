#!/usr/bin/env python3
"""Verify BDP-003F.12 Concept Lens bridge output smoke review.

Historical-phase safe: BDP-003F.13 may advance global current_phase/next_step
without invalidating the F12 phase record.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = "BDP-003F.12"
PHASE_KEY = "bdp_003f12_concept_lens_bridge_output_smoke_review"
DOC = ROOT / "docs/BDP_003F12_CONCEPT_LENS_BRIDGE_OUTPUT_SMOKE_REVIEW.md"
STATE = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
F11_BRIDGE = ROOT / "scripts/concept_lens_existing_archive_evidence_readback_bridge.py"
F8_SERVICE = ROOT / "scripts/concept_lens_archive_evidence_posture_service.py"
F12_NEXT_STEP = "BDP-003F.13 — Define Concept Lens UI integration contract for read-only evidence posture display before frontend wiring."

ALLOWED_CURRENT_PHASES = {'BDP-003F.12', 'BDP-003F.13', 'BDP-003F.14', 'BDP-003F.15', "BDP-003F.16"}
ALLOWED_NEXT_PREFIXES = ('BDP-003F.12', 'BDP-003F.13', 'BDP-003F.14', 'BDP-003F.15', 'BDP-003F.16')


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.exists(), f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def verify_doc() -> None:
    doc = read(DOC)
    for needle in [
        "BDP-003F.12",
        "read-only bridge output smoke review only",
        "Body without Organs",
        "we repress because we repeat",
        "assemblage",
        "concepts -> concept_mentions -> passages -> citations -> sources",
        "UI integration remains blocked",
        "no Concept Lens UI dock",
        "no database mutation",
        "no SQL migration",
        F12_NEXT_STEP,
    ]:
        require(needle in doc, f"F12 doc missing required text: {needle}")


def verify_existing_bridge_boundary() -> None:
    bridge = read(F11_BRIDGE)
    service = read(F8_SERVICE)
    require("concept_lens" in bridge.lower(), "F11 bridge should remain Concept Lens scoped")
    require("read" in bridge.lower(), "F11 bridge should expose read-oriented logic")
    require("concept_lens" in service.lower(), "F8 service should remain Concept Lens scoped")
    combined = bridge + "\n" + service
    for needle in [
        "st.button(\"Concept Lens",
        "st.text_input(\"Concept Lens",
        "CREATE TABLE concept_lens",
        "INSERT INTO concept_mentions",
        "INSERT INTO citations",
        "INSERT INTO concept_relations",
        "INSERT INTO interpretations",
    ]:
        require(needle not in combined, f"Forbidden implementation expansion found: {needle}")


def verify_state() -> None:
    data = json.loads(read(STATE))
    record = data.get(PHASE_KEY) or data.get("phases", {}).get(PHASE)
    require(isinstance(record, dict), "State missing BDP-003F.12 record")
    require(record.get("phase") == PHASE, "State phase mismatch")
    require(record.get("status") == "complete", "F12 status should be complete")
    require(record.get("controlled_slice") == "read_only_bridge_output_smoke_review_only", "F12 controlled slice mismatch")
    require(record.get("read_only_bridge_reviewed") is True, "F12 should record read_only_bridge_reviewed=true")
    for blocked in [
        "frontend_wiring_approved",
        "concept_lens_ui_dock_added",
        "streamlit_controls_added",
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
    ]:
        require(record.get(blocked) is False, f"F12 must keep {blocked}=false")
    require(record.get("next_step") == F12_NEXT_STEP, "F12 record next_step mismatch")
    require(data.get("current_phase") in ALLOWED_CURRENT_PHASES, "Global current_phase should remain in approved F12-F16 progression")
    require(data.get("next_step", "").startswith(ALLOWED_NEXT_PREFIXES), "Global next_step should remain in approved F12-F16 progression")


def verify_handover() -> None:
    handover = read(HANDOVER)
    for needle in [
        "BDP-003F.12 — Concept Lens Bridge Output Smoke Review Before UI Integration",
        "Body without Organs",
        "we repress because we repeat",
        "assemblage",
        "concepts -> concept_mentions -> passages -> citations -> sources",
        "no Concept Lens UI dock",
        F12_NEXT_STEP,
    ]:
        require(needle in handover, f"Handover missing required text: {needle}")


def main() -> None:
    verify_doc()
    verify_existing_bridge_boundary()
    verify_state()
    verify_handover()
    print("[OK] BDP-003F.12 Concept Lens bridge output smoke review verified")


if __name__ == "__main__":
    main()
