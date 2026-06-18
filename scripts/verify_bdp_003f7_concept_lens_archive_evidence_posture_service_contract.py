#!/usr/bin/env python3
"""Verify BDP-003F.7 Concept Lens archive evidence posture service contract.

This verifier confirms that BDP-003F.7 remains contract-only:
- the doctrine document exists and contains required service-contract markers;
- BUCHANAN_SYSTEM_STATE.json records the phase and blocks implementation;
- BUCHANAN_THREAD_HANDOVER.md records the handover section;
- no frontend, backend, SQL, database, evidence, citation, relation, interpretation, or Buchanan-claim implementation is approved.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BDP_003F7_CONCEPT_LENS_ARCHIVE_EVIDENCE_POSTURE_SERVICE_CONTRACT.md"
STATE = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER = ROOT / "BUCHANAN_THREAD_HANDOVER.md"

REQUIRED_DOC_MARKERS = [
    "BDP-003F.7 — Concept Lens Archive Evidence Posture Service Contract",
    "service contract only",
    "concept_lens_archive_evidence_posture_service.v1",
    "read_concept_lens_archive_evidence_posture",
    "concepts\n  -> concept_mentions\n  -> passages\n  -> citations\n  -> sources",
    "bdp_003f7_concept_lens_archive_evidence_posture_result_v1",
    "archive_grounded",
    "source_bound_description",
    "system_synthesis",
    "exploratory_unverified",
    "Missing archive evidence is not a failure",
    "BDP-003F.8 — Implement read-only Concept Lens archive evidence posture service behind this contract, if approved.",
]

BLOCKED_FALSE_FIELDS = [
    "implementation_approved",
    "frontend_implementation",
    "concept_lens_ui_dock_added",
    "new_navigation_surface_keys_added",
    "backend_service_implemented",
    "route_handler_added",
    "adapter_endpoint_added",
    "sql_query_implemented",
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
    "external_llm_routing_added",
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
        require(marker in doc_text, f"missing BDP-003F.7 doc marker: {marker}")

    state = json.loads(STATE.read_text(encoding="utf-8"))
    f6 = state.get("bdp_003f6_concept_lens_architecture")
    require(isinstance(f6, dict), "missing BDP-003F.6 architecture anchor")
    require(f6.get("status") == "complete", "BDP-003F.6 anchor is not complete")

    record = state.get("bdp_003f7_concept_lens_archive_evidence_posture_service_contract")
    require(isinstance(record, dict), "missing BDP-003F.7 state record")
    require(record.get("phase") == "BDP-003F.7", "incorrect phase")
    require(record.get("status") == "complete", "BDP-003F.7 not complete")
    require(record.get("controlled_slice") == "service_contract_only", "incorrect controlled slice")
    require(record.get("contract_defined") is True, "contract not marked defined")
    require(record.get("service_role") == "read_only_archive_evidence_posture_readback", "incorrect service role")
    require(record.get("contract_name") == "concept_lens_archive_evidence_posture_service.v1", "incorrect contract name")

    for field in BLOCKED_FALSE_FIELDS:
        require(record.get(field) is False, f"blocked field must be false: {field}")

    required_chain = ["concepts", "concept_mentions", "passages", "citations", "sources"]
    require(record.get("primary_archive_readback_chain") == required_chain, "archive readback chain changed")

    required_postures = [
        "archive_grounded",
        "source_bound_description",
        "secondary_scholarship_supported",
        "system_synthesis",
        "exploratory_unverified",
    ]
    require(record.get("evidence_posture_levels") == required_postures, "evidence posture levels changed")

    required_statuses = [
        "archive_grounded_match",
        "source_bound_match",
        "concept_found_without_reviewed_evidence",
        "no_archive_match",
        "ambiguous_concept_match",
        "rights_restricted_match",
        "optional_layer_required_but_blocked",
    ]
    require(record.get("archive_lookup_statuses") == required_statuses, "archive lookup statuses changed")

    handover = HANDOVER.read_text(encoding="utf-8")
    require("## BDP-003F.7 — Concept Lens Archive Evidence Posture Service Contract" in handover, "missing handover section")
    require("BDP-003F.8 — Implement read-only Concept Lens archive evidence posture service behind this contract, if approved." in handover, "missing next safe step")

    print("[OK] BDP-003F.7 Concept Lens archive evidence posture service contract verified")


if __name__ == "__main__":
    main()
