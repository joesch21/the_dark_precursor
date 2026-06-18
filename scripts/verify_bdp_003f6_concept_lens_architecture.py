#!/usr/bin/env python3
"""Verify BDP-003F.6 Concept Lens architecture slice.

This verifier confirms that BDP-003F.6 remains architecture-only:
- doctrine document exists and contains required architecture markers;
- BUCHANAN_SYSTEM_STATE.json records the phase and blocks implementation;
- BUCHANAN_THREAD_HANDOVER.md records the handover section;
- no frontend, backend, SQL, evidence, citation, relation, interpretation, or Buchanan-claim implementation is approved.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BDP_003F6_CONCEPT_LENS_ARCHITECTURE.md"
STATE = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER = ROOT / "BUCHANAN_THREAD_HANDOVER.md"

REQUIRED_DOC_MARKERS = [
    "BDP-003F.6 — Concept Lens Architecture",
    "architecture definition only",
    "Concept Lens",
    "future dock inside the concept stage",
    "concepts\n  → concept_mentions\n  → passages\n  → citations\n  → sources",
    "archive_grounded",
    "source_bound_description",
    "system_synthesis",
    "Fidelity warning layer",
    "Define read-only Concept Lens archive evidence posture service contract before implementation",
]

BLOCKED_FALSE_FIELDS = [
    "frontend_implementation",
    "backend_services_added",
    "adapter_endpoints_added",
    "database_tables_added",
    "sql_migrations_added",
    "database_mutation",
    "source_ingestion_added",
    "citation_creation_added",
    "concept_mention_creation_added",
    "concept_relation_creation_added",
    "interpretation_insertion_added",
    "evidence_promotion_added",
    "buchanan_claims_created",
    "automatic_chat_filtering_added",
    "hidden_personalization_added",
    "psychological_assessment_added",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(DOC.exists(), f"missing document: {DOC}")
    require(STATE.exists(), f"missing state file: {STATE}")
    require(HANDOVER.exists(), f"missing handover file: {HANDOVER}")

    doc_text = DOC.read_text(encoding="utf-8")
    for marker in REQUIRED_DOC_MARKERS:
        require(marker in doc_text, f"missing BDP-003F.6 doc marker: {marker}")

    state = json.loads(STATE.read_text(encoding="utf-8"))
    record = state.get("bdp_003f6_concept_lens_architecture")
    require(isinstance(record, dict), "missing bdp_003f6_concept_lens_architecture state record")
    require(record.get("phase") == "BDP-003F.6", "incorrect phase")
    require(record.get("status") == "complete", "BDP-003F.6 not complete")
    require(record.get("controlled_slice") == "architecture_definition_only", "incorrect controlled slice")
    require(record.get("concept_lens_defined") is True, "Concept Lens not marked defined")
    require(record.get("placement") == "future_dock_inside_cinematic_concept_stage", "incorrect placement")
    require(record.get("new_navigation_surface_keys_added") is False, "navigation surface keys were added")
    require(record.get("implementation_approved") is False, "implementation unexpectedly approved")

    for field in BLOCKED_FALSE_FIELDS:
        require(record.get(field) is False, f"blocked field must be false: {field}")

    required_layers = [
        "plain_explanation",
        "technical_deleuzian_explanation",
        "archive_evidence_posture",
        "fidelity_warning",
    ]
    require(record.get("future_answer_layers") == required_layers, "future answer layers changed")

    required_chain = ["concepts", "concept_mentions", "passages", "citations", "sources"]
    require(record.get("future_archive_readback_chain") == required_chain, "archive readback chain changed")

    handover = HANDOVER.read_text(encoding="utf-8")
    require("## BDP-003F.6 — Concept Lens Architecture" in handover, "missing handover section")
    require("BDP-003F.7 — Define read-only Concept Lens archive evidence posture service contract before implementation." in handover, "missing next safe step")

    print("[OK] BDP-003F.6 Concept Lens architecture verified")


if __name__ == "__main__":
    main()
