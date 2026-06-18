#!/usr/bin/env python3
"""Verify BDP-003F.8 Concept Lens archive evidence posture service.

This verifier confirms that BDP-003F.8 implements only the read-only local
archive evidence posture service behind the BDP-003F.7 contract. It uses fixture
rows and does not require or mutate a live database.
"""
from __future__ import annotations

import importlib.util
import json
import py_compile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC_F7 = ROOT / "docs" / "BDP_003F7_CONCEPT_LENS_ARCHIVE_EVIDENCE_POSTURE_SERVICE_CONTRACT.md"
DOC_F8 = ROOT / "docs" / "BDP_003F8_CONCEPT_LENS_ARCHIVE_EVIDENCE_POSTURE_SERVICE_IMPLEMENTATION.md"
SERVICE = ROOT / "scripts" / "concept_lens_archive_evidence_posture_service.py"
STATE = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER = ROOT / "BUCHANAN_THREAD_HANDOVER.md"

REQUIRED_DOC_MARKERS = [
    "BDP-003F.8 — Concept Lens Archive Evidence Posture Service Implementation",
    "read-only local service implementation",
    "scripts/concept_lens_archive_evidence_posture_service.py",
    "read_concept_lens_archive_evidence_posture",
    "bdp_003f8_concept_lens_archive_evidence_posture_result_v1",
    "concepts\n  -> concept_mentions\n  -> passages\n  -> citations\n  -> sources",
    "archive_grounded",
    "source_bound_description",
    "exploratory_unverified",
    "Restricted passage text is never reproduced by this service",
    "BDP-003F.9 — Review Concept Lens evidence posture service output against known archive cases before UI integration.",
]

BLOCKED_FALSE_FIELDS = [
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
    "philosophical_fidelity_review_added",
    "hidden_personalization_added",
    "psychological_assessment_added",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_service_module():
    spec = importlib.util.spec_from_file_location("concept_lens_archive_evidence_posture_service", SERVICE)
    require(spec is not None and spec.loader is not None, "could not load service module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def main() -> None:
    require(DOC_F7.exists(), f"missing BDP-003F.7 contract anchor: {DOC_F7}")
    require(DOC_F8.exists(), f"missing BDP-003F.8 implementation document: {DOC_F8}")
    require(SERVICE.exists(), f"missing service module: {SERVICE}")
    require(STATE.exists(), f"missing state file: {STATE}")
    require(HANDOVER.exists(), f"missing handover file: {HANDOVER}")

    doc_text = DOC_F8.read_text(encoding="utf-8")
    for marker in REQUIRED_DOC_MARKERS:
        require(marker in doc_text, f"missing BDP-003F.8 doc marker: {marker}")

    py_compile.compile(str(SERVICE), doraise=True)
    module = load_service_module()

    normalize = module.normalize_concept_query
    read = module.read_concept_lens_archive_evidence_posture
    build_sql = module.build_postgres_readonly_query

    require(normalize("we repress because we repeat") == "repetition", "Deleuze/Freud phrase should normalize to repetition")

    no_match = read("repetition", archive_rows=[])
    require(no_match["schema_id"] == "bdp_003f8_concept_lens_archive_evidence_posture_result_v1", "wrong schema id")
    require(no_match["archive_lookup_status"] == "no_archive_match", "no rows should be no_archive_match")
    require(no_match["evidence_posture"] == "exploratory_unverified", "no rows should be exploratory_unverified")
    require(no_match["buchanan_specific_claim_allowed"] is False, "Buchanan claim must remain blocked")

    grounded_fixture = [
        {
            "concept_id": "concept-bwo",
            "concept_name": "Body without Organs",
            "concept_mention_id": "mention-bwo-1",
            "mention_type": "direct",
            "mention_review_status": "accepted",
            "passage_id": "passage-bwo-1",
            "passage_locator": "printed article page 76; PDF page 4",
            "citation_id": "citation-bwo-1",
            "source_id": "source-buchanan-body",
            "source_author": "Ian Buchanan",
            "source_title": "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?",
            "rights_status": "restricted",
            "passage_text": "THIS TEXT MUST NOT BE DISPLAYED BY THE SERVICE",
        }
    ]
    grounded = read("Body without Organs", archive_rows=grounded_fixture)
    require(grounded["evidence_posture"] == "archive_grounded", "complete fixture should be archive_grounded")
    require(grounded["archive_lookup_status"] == "rights_restricted_match", "restricted fixture should be rights_restricted_match")
    require(grounded["authority_label"] == "buchanan_direct", "Buchanan fixture should be buchanan_direct")
    require(grounded["matched_records"]["concepts"] == 1, "concept count should be 1")
    require(grounded["matched_records"]["concept_mentions"] == 1, "mention count should be 1")
    require(grounded["archive_chain"][0]["passage_text_display"] == "omitted_by_rights_policy", "restricted passage display must be omitted")
    grounded_json = json.dumps(grounded, ensure_ascii=False)
    require("THIS TEXT MUST NOT BE DISPLAYED" not in grounded_json, "service leaked fixture passage text")
    require(grounded["buchanan_specific_claim_allowed"] is False, "archive posture must not authorize Buchanan claims")

    incomplete_fixture = [
        {
            "concept_id": "concept-assemblage",
            "concept_name": "assemblage",
            "concept_mention_id": "",
            "mention_type": "",
            "mention_review_status": "",
            "passage_id": "passage-assemblage-1",
            "passage_locator": "reviewed locator only",
            "citation_id": "",
            "source_id": "source-buchanan-assemblage-method",
            "source_author": "Ian Buchanan",
            "source_title": "Assemblage Theory and Method",
            "rights_status": "restricted",
        }
    ]
    source_bound = read("assemblage", archive_rows=incomplete_fixture)
    require(source_bound["archive_lookup_status"] == "source_bound_match", "incomplete source fixture should be source_bound_match")
    require(source_bound["evidence_posture"] == "source_bound_description", "incomplete source fixture should be source_bound_description")

    sql = build_sql("body without organs")
    lowered = sql.lower()
    for forbidden in [" insert ", " update ", " delete ", " drop ", " alter ", " create ", " truncate "]:
        require(forbidden not in lowered, f"SQL contains forbidden mutation token: {forbidden.strip()}")
    require("select" in lowered and "from concepts" in lowered, "SQL should read from concepts")

    state = json.loads(STATE.read_text(encoding="utf-8"))
    f7 = state.get("bdp_003f7_concept_lens_archive_evidence_posture_service_contract")
    require(isinstance(f7, dict), "missing BDP-003F.7 contract anchor")
    require(f7.get("status") == "complete", "BDP-003F.7 anchor is not complete")

    record = state.get("bdp_003f8_concept_lens_archive_evidence_posture_service")
    require(isinstance(record, dict), "missing BDP-003F.8 state record")
    require(record.get("phase") == "BDP-003F.8", "incorrect phase")
    require(record.get("status") == "complete", "BDP-003F.8 not complete")
    require(record.get("controlled_slice") == "read_only_local_service_implementation", "incorrect controlled slice")
    require(record.get("contract_source") == "BDP-003F.7", "incorrect contract source")
    require(record.get("service_implemented") is True, "service not marked implemented")
    require(record.get("service_module") == "scripts/concept_lens_archive_evidence_posture_service.py", "incorrect service module")
    require(record.get("service_role") == "read_only_archive_evidence_posture_readback", "incorrect service role")

    for field in BLOCKED_FALSE_FIELDS:
        require(record.get(field) is False, f"blocked field must be false: {field}")

    required_chain = ["concepts", "concept_mentions", "passages", "citations", "sources"]
    require(record.get("primary_archive_readback_chain") == required_chain, "archive readback chain changed")
    require(record.get("next_step") == "BDP-003F.9 — Review Concept Lens evidence posture service output against known archive cases before UI integration.", "incorrect next step")

    handover = HANDOVER.read_text(encoding="utf-8")
    require("## BDP-003F.8 — Concept Lens Archive Evidence Posture Service Implementation" in handover, "missing handover section")
    require("BDP-003F.9 — Review Concept Lens evidence posture service output against known archive cases before UI integration." in handover, "missing handover next step")

    print("[OK] BDP-003F.8 Concept Lens archive evidence posture service verified")


if __name__ == "__main__":
    main()
