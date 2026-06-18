#!/usr/bin/env python3
"""Verify BDP-003F.11 Concept Lens existing archive readback bridge implementation."""

from __future__ import annotations

import importlib.util
import json
import py_compile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BDP_003F11_CONCEPT_LENS_EXISTING_ARCHIVE_READBACK_BRIDGE_IMPLEMENTATION.md"
F10_DOC = ROOT / "docs" / "BDP_003F10_CONCEPT_LENS_READ_ONLY_BRIDGE_CONTRACT.md"
F9_DOC = ROOT / "docs" / "BDP_003F9_CONCEPT_LENS_EVIDENCE_POSTURE_OUTPUT_REVIEW.md"
STATE = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
BRIDGE = ROOT / "scripts" / "concept_lens_existing_archive_evidence_readback_bridge.py"
F8_SERVICE = ROOT / "scripts" / "concept_lens_archive_evidence_posture_service.py"
PHASE_KEY = "bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation"
NEXT_STEP = "BDP-003F.12 — Review live Body without Organs bridge output against the Concept Lens service before UI integration."
WRAPPER = "read_concept_lens_archive_evidence_posture_via_existing_archive_bridge"


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read(path: Path) -> str:
    assert_true(path.exists(), f"Missing required file: {path}")
    return path.read_text(encoding="utf-8")


def import_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert_true(spec is not None and spec.loader is not None, f"Could not load module spec: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def verify_docs() -> None:
    f10 = read(F10_DOC)
    f9 = read(F9_DOC)
    doc = read(DOC)
    assert_true("concept_lens_existing_archive_evidence_readback_bridge.v1" in f10, "F10 contract anchor missing")
    assert_true("Outcome C" in f9, "F9 Outcome C anchor missing")

    required = [
        "BDP-003F.11",
        "read-only bridge implementation only",
        "scripts/concept_lens_existing_archive_evidence_readback_bridge.py",
        "read_existing_archive_evidence_rows_for_concept",
        WRAPPER,
        "Body without Organs",
        "concepts",
        "concept_mentions",
        "passages",
        "citations",
        "sources",
        "omitted_by_rights_policy",
        "UI integration remains blocked",
        NEXT_STEP,
    ]
    for needle in required:
        assert_true(needle in doc, f"F11 doc missing required text: {needle}")

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
    for term in blocked_terms:
        assert_true(term in doc, f"F11 doc missing blocked boundary: {term}")


def verify_state_and_handover() -> None:
    data = json.loads(read(STATE))
    record = data.get(PHASE_KEY)
    assert_true(isinstance(record, dict), "State missing BDP-003F.11 phase record")
    checks = {
        "phase": "BDP-003F.11",
        "status": "complete",
        "contract_source": "BDP-003F.10",
        "bridge_implemented": True,
        "service_wrapper_added": True,
        "frontend_implementation": False,
        "concept_lens_ui_dock_added": False,
        "backend_route_added": False,
        "adapter_endpoint_added": False,
        "database_mutation": False,
        "sql_migration_added": False,
        "citation_creation_added": False,
        "concept_mention_creation_added": False,
        "concept_relation_creation_added": False,
        "interpretation_insertion_added": False,
        "evidence_promotion_added": False,
        "buchanan_claims_created": False,
        "next_step": NEXT_STEP,
    }
    for key, expected in checks.items():
        assert_true(record.get(key) == expected, f"State mismatch for {key}: expected {expected!r}, got {record.get(key)!r}")
    assert_true(data.get("current_phase") == "BDP-003F.11", "Global current_phase should be BDP-003F.11")
    assert_true(data.get("next_step") == NEXT_STEP, "Global next_step mismatch")

    handover = read(HANDOVER)
    for needle in [
        "BDP-003F.11 — Concept Lens Existing Archive Evidence Readback Bridge Implementation",
        "read_existing_archive_evidence_rows_for_concept",
        WRAPPER,
        "No frontend wiring.",
        NEXT_STEP,
    ]:
        assert_true(needle in handover, f"Handover missing required text: {needle}")


def verify_bridge_module_and_service() -> None:
    py_compile.compile(str(BRIDGE), doraise=True)
    py_compile.compile(str(F8_SERVICE), doraise=True)
    service_text = read(F8_SERVICE)
    assert_true("BDP-003F.11 EXISTING ARCHIVE READBACK BRIDGE INTEGRATION START" in service_text, "F8 service missing F11 integration marker")
    assert_true(WRAPPER in service_text, "F8 service missing F11 wrapper function")

    sys.path.insert(0, str(ROOT / "scripts"))
    bridge = import_module("concept_lens_existing_archive_evidence_readback_bridge", BRIDGE)
    service = import_module("concept_lens_archive_evidence_posture_service", F8_SERVICE)

    assert_true(hasattr(bridge, "read_existing_archive_evidence_rows_for_concept"), "Bridge function missing")
    assert_true(hasattr(bridge, "read_existing_archive_evidence_rows_from_readback_text"), "Bridge fixture helper missing")
    assert_true(hasattr(service, WRAPPER), "Service wrapper missing after import")

    fixture_text = """
    Body without Organs evidence readback.
    Evidence chain: concepts -> concept_mentions -> passages -> citations -> sources.
    Source author: Ian Buchanan.
    Source title: The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?
    Citation exists and source exists.
    Concept mention accepted / direct.
    Locator: printed article page 76; PDF page 4.
    Rights status: restricted. Passage text display: omitted_by_rights_policy.
    """
    rows = bridge.read_existing_archive_evidence_rows_from_readback_text("Body without Organs", fixture_text)
    assert_true(len(rows) == 1, "Bridge fixture should produce exactly one BWO row")
    row = rows[0]
    assert_true(row.get("concept") == "Body without Organs", "Bridge row concept mismatch")
    assert_true(row.get("chain_complete") is True, "Bridge row must mark complete chain")
    assert_true(row.get("passage_text_display") == "omitted_by_rights_policy", "Restricted text must be omitted")
    assert_true("Buchanan argues" not in json.dumps(row), "Bridge row must not create Buchanan claim")
    assert_true(
        bridge.read_existing_archive_evidence_rows_from_readback_text("assemblage", fixture_text) == [],
        "Unsupported concept must not fabricate rows",
    )

    wrapper = getattr(service, WRAPPER)
    result = wrapper("Body without Organs", bridge_rows=rows)
    assert_true(isinstance(result, dict), "Service wrapper must return a result dictionary")
    assert_true(result.get("evidence_posture") in {"archive_grounded", "source_bound_description"}, "Wrapper must produce a grounded or conservative source-bound posture from bridge rows")
    assert_true(result.get("passage_text_display") in {"omitted_by_rights_policy", "omitted_until_allowed_by_rights_policy", None}, "Wrapper must preserve rights omission")


def main() -> None:
    verify_docs()
    verify_state_and_handover()
    verify_bridge_module_and_service()
    print("[OK] BDP-003F.11 Concept Lens existing archive readback bridge implementation verified")


if __name__ == "__main__":
    main()
