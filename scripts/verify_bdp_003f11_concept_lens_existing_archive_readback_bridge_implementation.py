#!/usr/bin/env python3
"""Verify BDP-003F.11 Concept Lens existing archive readback bridge implementation.

Historical-phase safe: later dependent Concept Lens phases may advance global
current_phase/next_step without invalidating the F11 phase record.
"""

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
F11_NEXT_STEP = "BDP-003F.12 — Review live Body without Organs bridge output against the Concept Lens service before UI integration."
WRAPPER = "read_concept_lens_archive_evidence_posture_via_existing_archive_bridge"

ALLOWED_CURRENT_PHASES = {'BDP-003F.11', 'BDP-003F.12', 'BDP-003F.13', 'BDP-003F.14', 'BDP-003F.15', 'BDP-003F.16', 'BDP-003F.17', 'BDP-003F.18'}
ALLOWED_NEXT_PREFIXES = ('BDP-003F.11', 'BDP-003F.12', 'BDP-003F.13', 'BDP-003F.14', 'BDP-003F.15', 'BDP-003F.16', 'BDP-003F.17', 'BDP-003F.18')


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.exists(), f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def import_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"Could not load module spec: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def verify_documents() -> None:
    f10 = read(F10_DOC)
    f9 = read(F9_DOC)
    doc = read(DOC)
    handover = read(HANDOVER)
    require("concept_lens_existing_archive_evidence_readback_bridge.v1" in f10, "F10 bridge contract anchor missing")
    require("Outcome C" in f9, "F9 Outcome C anchor missing")
    for needle in [
        "BDP-003F.11",
        "Body without Organs",
        "scripts/concept_lens_existing_archive_evidence_readback_bridge.py",
        "read_existing_archive_evidence_rows_for_concept",
        WRAPPER,
        "concepts",
        "concept_mentions",
        "passages",
        "citations",
        "sources",
        "omitted_by_rights_policy",
    ]:
        require(needle in doc, f"F11 doc missing required text: {needle}")
    for needle in ["BDP-003F.11", "read_existing_archive_evidence_rows_for_concept", WRAPPER]:
        require(needle in handover, f"Handover missing required text: {needle}")


def verify_state() -> None:
    data = json.loads(read(STATE))
    record = data.get(PHASE_KEY) or data.get("phases", {}).get("BDP-003F.11")
    require(isinstance(record, dict), "State missing BDP-003F.11 phase record")
    expected = {
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
        "next_step": F11_NEXT_STEP,
    }
    for key, value in expected.items():
        require(record.get(key) == value, f"State mismatch for {key}: expected {value!r}, got {record.get(key)!r}")
    require(data.get("current_phase") in ALLOWED_CURRENT_PHASES, "Global current_phase should remain in approved F11-F18 progression")
    require(data.get("next_step", "").startswith(ALLOWED_NEXT_PREFIXES), "Global next_step should remain in approved F11-F18 progression")


def verify_bridge_module_and_service() -> None:
    py_compile.compile(str(BRIDGE), doraise=True)
    py_compile.compile(str(F8_SERVICE), doraise=True)
    service_text = read(F8_SERVICE)
    require("BDP-003F.11 EXISTING ARCHIVE READBACK BRIDGE INTEGRATION START" in service_text, "F8 service missing F11 integration marker")
    require(WRAPPER in service_text, "F8 service missing F11 wrapper function")
    sys.path.insert(0, str(ROOT / "scripts"))
    bridge = import_module("concept_lens_existing_archive_evidence_readback_bridge", BRIDGE)
    service = import_module("concept_lens_archive_evidence_posture_service", F8_SERVICE)
    require(hasattr(bridge, "read_existing_archive_evidence_rows_for_concept"), "Bridge missing read_existing_archive_evidence_rows_for_concept")
    require(hasattr(bridge, "read_existing_archive_evidence_rows_from_readback_text"), "Bridge missing readback text helper")
    require(hasattr(service, WRAPPER), "Service wrapper missing after import")
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
    require(len(rows) == 1, "Bridge fixture should produce exactly one BWO row")
    row = rows[0]
    require(row.get("concept") == "Body without Organs", "Bridge row concept mismatch")
    require(row.get("chain_complete") is True, "Bridge row must mark complete chain")
    require(row.get("passage_text_display") == "omitted_by_rights_policy", "Restricted text must be omitted")
    require("Buchanan argues" not in json.dumps(row), "Bridge row must not create Buchanan claim")
    require(bridge.read_existing_archive_evidence_rows_from_readback_text("assemblage", fixture_text) == [], "Unsupported concept must not fabricate rows")
    result = getattr(service, WRAPPER)("Body without Organs", bridge_rows=rows)
    require(isinstance(result, dict), "Service wrapper must return a result dictionary")
    require(result.get("evidence_posture") in {"archive_grounded", "source_bound_description"}, "Wrapper must produce grounded or conservative posture")
    require(result.get("passage_text_display") in {"omitted_by_rights_policy", "omitted_until_allowed_by_rights_policy", None}, "Wrapper must preserve rights omission")


def main() -> None:
    verify_documents()
    verify_state()
    verify_bridge_module_and_service()
    print("[OK] BDP-003F.11 Concept Lens existing archive readback bridge implementation verified")


if __name__ == "__main__":
    main()
