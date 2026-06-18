#!/usr/bin/env python3
"""Update state, handover, and progression-safe verifiers for BDP-003F.13."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
PHASE = "BDP-003F.13"
PHASE_KEY = "bdp_003f13_concept_lens_ui_integration_contract"
TITLE = "Define Concept Lens UI integration contract for read-only evidence posture display before frontend wiring"
DOC = "docs/BDP_003F13_CONCEPT_LENS_UI_INTEGRATION_CONTRACT.md"
VERIFIER = "scripts/verify_bdp_003f13_concept_lens_ui_integration_contract.py"
NEXT_STEP = "BDP-003F.14 — Wire the approved Concept Lens read-only evidence posture display into the frontend after contract verification."

F10_VERIFIER = "scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py"
F11_VERIFIER = "scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py"
F12_VERIFIER = "scripts/verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py"

F10_VERIFIER_TEXT = '#!/usr/bin/env python3\n"""Verify BDP-003F.10 Concept Lens read-only bridge contract.\n\nHistorical-phase safe: later dependent Concept Lens phases may advance global\ncurrent_phase/next_step without invalidating the F10 phase record.\n"""\n\nfrom __future__ import annotations\n\nimport json\nimport py_compile\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "BDP_003F10_CONCEPT_LENS_READ_ONLY_BRIDGE_CONTRACT.md"\nSTATE = ROOT / "BUCHANAN_SYSTEM_STATE.json"\nHANDOVER = ROOT / "BUCHANAN_THREAD_HANDOVER.md"\nF8_SERVICE = ROOT / "scripts" / "concept_lens_archive_evidence_posture_service.py"\nF9_DOC = ROOT / "docs" / "BDP_003F9_CONCEPT_LENS_EVIDENCE_POSTURE_OUTPUT_REVIEW.md"\nPHASE_KEY = "bdp_003f10_concept_lens_existing_archive_readback_bridge_contract"\nF10_NEXT_STEP = "BDP-003F.11 — Implement the approved read-only bridge from existing archive evidence readback into the Concept Lens service."\nALLOWED_CURRENT_PHASES = {"BDP-003F.10", "BDP-003F.11", "BDP-003F.12", "BDP-003F.13"}\nALLOWED_NEXT_PREFIXES = ("BDP-003F.11", "BDP-003F.12", "BDP-003F.13", "BDP-003F.14")\n\n\ndef require(condition: bool, message: str) -> None:\n    if not condition:\n        raise AssertionError(message)\n\n\ndef read(path: Path) -> str:\n    require(path.exists(), f"Missing required file: {path.relative_to(ROOT)}")\n    return path.read_text(encoding="utf-8")\n\n\ndef verify_python_compile(path: Path) -> None:\n    require(path.exists(), f"Missing Python file: {path.relative_to(ROOT)}")\n    py_compile.compile(str(path), doraise=True)\n\n\ndef verify_doc() -> None:\n    text = read(DOC)\n    for needle in [\n        "BDP-003F.10",\n        "read-only bridge contract definition only",\n        "BDP-003F.9 recorded Outcome C",\n        "concept_lens_existing_archive_evidence_readback_bridge.v1",\n        "scripts/concept_lens_existing_archive_evidence_readback_bridge.py",\n        "read_existing_archive_evidence_rows_for_concept",\n        "scripts/concept_lens_archive_evidence_posture_service.py",\n        "read_concept_lens_archive_evidence_posture",\n        "concepts -> concept_mentions -> passages -> citations -> sources",\n        "archive_lookup_status: archive_grounded_match",\n        "evidence_posture: archive_grounded",\n        "omitted_by_rights_policy",\n        "UI integration remains blocked",\n        F10_NEXT_STEP,\n    ]:\n        require(needle in text, f"F10 doc missing required text: {needle}")\n\n\ndef verify_state() -> None:\n    data = json.loads(read(STATE))\n    record = data.get(PHASE_KEY) or data.get("phases", {}).get("BDP-003F.10")\n    require(isinstance(record, dict), "State missing BDP-003F.10 record")\n    require(record.get("phase") == "BDP-003F.10", "State phase mismatch")\n    require(record.get("status") == "complete", "State status must be complete")\n    require(record.get("contract_only") is True, "F10 must be contract-only")\n    require(record.get("definition_only") is True, "F10 must be definition-only")\n    require(record.get("bridge_contract_defined") is True, "Bridge contract must be defined")\n    require(record.get("bridge_implemented") is False, "F10 must not implement bridge")\n    for blocked in [\n        "frontend_implementation",\n        "database_mutation",\n        "sql_migration_added",\n        "adapter_endpoint_added",\n        "evidence_promotion_added",\n        "buchanan_claims_created",\n    ]:\n        require(record.get(blocked) is False, f"F10 must keep {blocked}=false")\n    require(record.get("next_step") == F10_NEXT_STEP, "F10 record next step mismatch")\n    require(data.get("current_phase") in ALLOWED_CURRENT_PHASES, "Global current_phase should remain in approved F10-F13 progression")\n    global_next = data.get("next_step", "")\n    require(global_next.startswith(ALLOWED_NEXT_PREFIXES), "Global next_step should remain in approved F10-F13 progression")\n\n\ndef verify_handover() -> None:\n    text = read(HANDOVER)\n    for needle in [\n        "BDP-003F.10 — Concept Lens Existing Archive Evidence Readback Bridge Contract",\n        "read-only bridge contract definition only",\n        "concept_lens_existing_archive_evidence_readback_bridge.v1",\n        "concepts -> concept_mentions -> passages -> citations -> sources",\n        "UI integration remains blocked",\n    ]:\n        require(needle in text, f"Handover missing required text: {needle}")\n\n\ndef verify_existing_phase_anchors() -> None:\n    f9_text = read(F9_DOC)\n    require("Outcome C" in f9_text, "F9 Outcome C anchor missing")\n    verify_python_compile(F8_SERVICE)\n\n\ndef main() -> None:\n    verify_doc()\n    verify_state()\n    verify_handover()\n    verify_existing_phase_anchors()\n    print("[OK] BDP-003F.10 Concept Lens read-only bridge contract verified")\n\n\nif __name__ == "__main__":\n    main()\n'
F11_VERIFIER_TEXT = '#!/usr/bin/env python3\n"""Verify BDP-003F.11 Concept Lens existing archive readback bridge implementation.\n\nHistorical-phase safe: later dependent Concept Lens phases may advance global\ncurrent_phase/next_step without invalidating the F11 phase record.\n"""\n\nfrom __future__ import annotations\n\nimport importlib.util\nimport json\nimport py_compile\nimport sys\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "BDP_003F11_CONCEPT_LENS_EXISTING_ARCHIVE_READBACK_BRIDGE_IMPLEMENTATION.md"\nF10_DOC = ROOT / "docs" / "BDP_003F10_CONCEPT_LENS_READ_ONLY_BRIDGE_CONTRACT.md"\nF9_DOC = ROOT / "docs" / "BDP_003F9_CONCEPT_LENS_EVIDENCE_POSTURE_OUTPUT_REVIEW.md"\nSTATE = ROOT / "BUCHANAN_SYSTEM_STATE.json"\nHANDOVER = ROOT / "BUCHANAN_THREAD_HANDOVER.md"\nBRIDGE = ROOT / "scripts" / "concept_lens_existing_archive_evidence_readback_bridge.py"\nF8_SERVICE = ROOT / "scripts" / "concept_lens_archive_evidence_posture_service.py"\nPHASE_KEY = "bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation"\nF11_NEXT_STEP = "BDP-003F.12 — Review live Body without Organs bridge output against the Concept Lens service before UI integration."\nWRAPPER = "read_concept_lens_archive_evidence_posture_via_existing_archive_bridge"\nALLOWED_CURRENT_PHASES = {"BDP-003F.11", "BDP-003F.12", "BDP-003F.13"}\nALLOWED_NEXT_PREFIXES = ("BDP-003F.12", "BDP-003F.13", "BDP-003F.14")\n\n\ndef require(condition: bool, message: str) -> None:\n    if not condition:\n        raise AssertionError(message)\n\n\ndef read(path: Path) -> str:\n    require(path.exists(), f"Missing required file: {path.relative_to(ROOT)}")\n    return path.read_text(encoding="utf-8")\n\n\ndef import_module(name: str, path: Path):\n    spec = importlib.util.spec_from_file_location(name, path)\n    require(spec is not None and spec.loader is not None, f"Could not load module spec: {path}")\n    module = importlib.util.module_from_spec(spec)\n    sys.modules[name] = module\n    spec.loader.exec_module(module)\n    return module\n\n\ndef verify_documents() -> None:\n    f10 = read(F10_DOC)\n    f9 = read(F9_DOC)\n    doc = read(DOC)\n    handover = read(HANDOVER)\n    require("concept_lens_existing_archive_evidence_readback_bridge.v1" in f10, "F10 bridge contract anchor missing")\n    require("Outcome C" in f9, "F9 Outcome C anchor missing")\n    for needle in [\n        "BDP-003F.11",\n        "Body without Organs",\n        "scripts/concept_lens_existing_archive_evidence_readback_bridge.py",\n        "read_existing_archive_evidence_rows_for_concept",\n        WRAPPER,\n        "concepts",\n        "concept_mentions",\n        "passages",\n        "citations",\n        "sources",\n        "omitted_by_rights_policy",\n    ]:\n        require(needle in doc, f"F11 doc missing required text: {needle}")\n    for needle in ["BDP-003F.11", "read_existing_archive_evidence_rows_for_concept", WRAPPER]:\n        require(needle in handover, f"Handover missing required text: {needle}")\n\n\ndef verify_state() -> None:\n    data = json.loads(read(STATE))\n    record = data.get(PHASE_KEY) or data.get("phases", {}).get("BDP-003F.11")\n    require(isinstance(record, dict), "State missing BDP-003F.11 phase record")\n    expected = {\n        "phase": "BDP-003F.11",\n        "status": "complete",\n        "contract_source": "BDP-003F.10",\n        "bridge_implemented": True,\n        "service_wrapper_added": True,\n        "frontend_implementation": False,\n        "concept_lens_ui_dock_added": False,\n        "backend_route_added": False,\n        "adapter_endpoint_added": False,\n        "database_mutation": False,\n        "sql_migration_added": False,\n        "citation_creation_added": False,\n        "concept_mention_creation_added": False,\n        "concept_relation_creation_added": False,\n        "interpretation_insertion_added": False,\n        "evidence_promotion_added": False,\n        "buchanan_claims_created": False,\n        "next_step": F11_NEXT_STEP,\n    }\n    for key, value in expected.items():\n        require(record.get(key) == value, f"State mismatch for {key}: expected {value!r}, got {record.get(key)!r}")\n    require(data.get("current_phase") in ALLOWED_CURRENT_PHASES, "Global current_phase should remain in approved F11-F13 progression")\n    require(data.get("next_step", "").startswith(ALLOWED_NEXT_PREFIXES), "Global next_step should remain in approved F11-F13 progression")\n\n\ndef verify_bridge_module_and_service() -> None:\n    py_compile.compile(str(BRIDGE), doraise=True)\n    py_compile.compile(str(F8_SERVICE), doraise=True)\n    service_text = read(F8_SERVICE)\n    require("BDP-003F.11 EXISTING ARCHIVE READBACK BRIDGE INTEGRATION START" in service_text, "F8 service missing F11 integration marker")\n    require(WRAPPER in service_text, "F8 service missing F11 wrapper function")\n    sys.path.insert(0, str(ROOT / "scripts"))\n    bridge = import_module("concept_lens_existing_archive_evidence_readback_bridge", BRIDGE)\n    service = import_module("concept_lens_archive_evidence_posture_service", F8_SERVICE)\n    require(hasattr(bridge, "read_existing_archive_evidence_rows_for_concept"), "Bridge missing read_existing_archive_evidence_rows_for_concept")\n    require(hasattr(bridge, "read_existing_archive_evidence_rows_from_readback_text"), "Bridge missing readback text helper")\n    require(hasattr(service, WRAPPER), "Service wrapper missing after import")\n    fixture_text = """\n    Body without Organs evidence readback.\n    Evidence chain: concepts -> concept_mentions -> passages -> citations -> sources.\n    Source author: Ian Buchanan.\n    Source title: The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?\n    Citation exists and source exists.\n    Concept mention accepted / direct.\n    Locator: printed article page 76; PDF page 4.\n    Rights status: restricted. Passage text display: omitted_by_rights_policy.\n    """\n    rows = bridge.read_existing_archive_evidence_rows_from_readback_text("Body without Organs", fixture_text)\n    require(len(rows) == 1, "Bridge fixture should produce exactly one BWO row")\n    row = rows[0]\n    require(row.get("concept") == "Body without Organs", "Bridge row concept mismatch")\n    require(row.get("chain_complete") is True, "Bridge row must mark complete chain")\n    require(row.get("passage_text_display") == "omitted_by_rights_policy", "Restricted text must be omitted")\n    require("Buchanan argues" not in json.dumps(row), "Bridge row must not create Buchanan claim")\n    require(bridge.read_existing_archive_evidence_rows_from_readback_text("assemblage", fixture_text) == [], "Unsupported concept must not fabricate rows")\n    result = getattr(service, WRAPPER)("Body without Organs", bridge_rows=rows)\n    require(isinstance(result, dict), "Service wrapper must return a result dictionary")\n    require(result.get("evidence_posture") in {"archive_grounded", "source_bound_description"}, "Wrapper must produce grounded or conservative posture")\n    require(result.get("passage_text_display") in {"omitted_by_rights_policy", "omitted_until_allowed_by_rights_policy", None}, "Wrapper must preserve rights omission")\n\n\ndef main() -> None:\n    verify_documents()\n    verify_state()\n    verify_bridge_module_and_service()\n    print("[OK] BDP-003F.11 Concept Lens existing archive readback bridge implementation verified")\n\n\nif __name__ == "__main__":\n    main()\n'
F12_VERIFIER_TEXT = '#!/usr/bin/env python3\n"""Verify BDP-003F.12 Concept Lens bridge output smoke review.\n\nHistorical-phase safe: BDP-003F.13 may advance global current_phase/next_step\nwithout invalidating the F12 phase record.\n"""\n\nfrom __future__ import annotations\n\nimport json\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nPHASE = "BDP-003F.12"\nPHASE_KEY = "bdp_003f12_concept_lens_bridge_output_smoke_review"\nDOC = ROOT / "docs/BDP_003F12_CONCEPT_LENS_BRIDGE_OUTPUT_SMOKE_REVIEW.md"\nSTATE = ROOT / "BUCHANAN_SYSTEM_STATE.json"\nHANDOVER = ROOT / "BUCHANAN_THREAD_HANDOVER.md"\nF11_BRIDGE = ROOT / "scripts/concept_lens_existing_archive_evidence_readback_bridge.py"\nF8_SERVICE = ROOT / "scripts/concept_lens_archive_evidence_posture_service.py"\nF12_NEXT_STEP = "BDP-003F.13 — Define Concept Lens UI integration contract for read-only evidence posture display before frontend wiring."\nALLOWED_CURRENT_PHASES = {"BDP-003F.12", "BDP-003F.13"}\nALLOWED_NEXT_PREFIXES = ("BDP-003F.13", "BDP-003F.14")\n\n\ndef require(condition: bool, message: str) -> None:\n    if not condition:\n        raise AssertionError(message)\n\n\ndef read(path: Path) -> str:\n    require(path.exists(), f"Missing required file: {path.relative_to(ROOT)}")\n    return path.read_text(encoding="utf-8")\n\n\ndef verify_doc() -> None:\n    doc = read(DOC)\n    for needle in [\n        "BDP-003F.12",\n        "read-only bridge output smoke review only",\n        "Body without Organs",\n        "we repress because we repeat",\n        "assemblage",\n        "concepts -> concept_mentions -> passages -> citations -> sources",\n        "UI integration remains blocked",\n        "no Concept Lens UI dock",\n        "no database mutation",\n        "no SQL migration",\n        F12_NEXT_STEP,\n    ]:\n        require(needle in doc, f"F12 doc missing required text: {needle}")\n\n\ndef verify_existing_bridge_boundary() -> None:\n    bridge = read(F11_BRIDGE)\n    service = read(F8_SERVICE)\n    require("concept_lens" in bridge.lower(), "F11 bridge should remain Concept Lens scoped")\n    require("read" in bridge.lower(), "F11 bridge should expose read-oriented logic")\n    require("concept_lens" in service.lower(), "F8 service should remain Concept Lens scoped")\n    combined = bridge + "\\n" + service\n    for needle in [\n        "st.button(\\"Concept Lens",\n        "st.text_input(\\"Concept Lens",\n        "CREATE TABLE concept_lens",\n        "INSERT INTO concept_mentions",\n        "INSERT INTO citations",\n        "INSERT INTO concept_relations",\n        "INSERT INTO interpretations",\n    ]:\n        require(needle not in combined, f"Forbidden implementation expansion found: {needle}")\n\n\ndef verify_state() -> None:\n    data = json.loads(read(STATE))\n    record = data.get(PHASE_KEY) or data.get("phases", {}).get(PHASE)\n    require(isinstance(record, dict), "State missing BDP-003F.12 record")\n    require(record.get("phase") == PHASE, "State phase mismatch")\n    require(record.get("status") == "complete", "F12 status should be complete")\n    require(record.get("controlled_slice") == "read_only_bridge_output_smoke_review_only", "F12 controlled slice mismatch")\n    require(record.get("read_only_bridge_reviewed") is True, "F12 should record read_only_bridge_reviewed=true")\n    for blocked in [\n        "frontend_wiring_approved",\n        "concept_lens_ui_dock_added",\n        "streamlit_controls_added",\n        "backend_routes_added",\n        "adapter_endpoints_added",\n        "sql_migrations_added",\n        "database_mutation",\n        "citation_creation_added",\n        "concept_mention_creation_added",\n        "concept_relation_creation_added",\n        "interpretation_insertion_added",\n        "evidence_promotion_added",\n        "buchanan_claims_created",\n    ]:\n        require(record.get(blocked) is False, f"F12 must keep {blocked}=false")\n    require(record.get("next_step") == F12_NEXT_STEP, "F12 record next_step mismatch")\n    require(data.get("current_phase") in ALLOWED_CURRENT_PHASES, "Global current_phase should remain in approved F12-F13 progression")\n    require(data.get("next_step", "").startswith(ALLOWED_NEXT_PREFIXES), "Global next_step should remain in approved F12-F13 progression")\n\n\ndef verify_handover() -> None:\n    handover = read(HANDOVER)\n    for needle in [\n        "BDP-003F.12 — Concept Lens Bridge Output Smoke Review Before UI Integration",\n        "Body without Organs",\n        "we repress because we repeat",\n        "assemblage",\n        "concepts -> concept_mentions -> passages -> citations -> sources",\n        "no Concept Lens UI dock",\n        F12_NEXT_STEP,\n    ]:\n        require(needle in handover, f"Handover missing required text: {needle}")\n\n\ndef main() -> None:\n    verify_doc()\n    verify_existing_bridge_boundary()\n    verify_state()\n    verify_handover()\n    print("[OK] BDP-003F.12 Concept Lens bridge output smoke review verified")\n\n\nif __name__ == "__main__":\n    main()\n'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"[FAIL] {message}")


def load_state() -> dict:
    require(STATE_PATH.exists(), "BUCHANAN_SYSTEM_STATE.json not found")
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(data: dict) -> None:
    STATE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def normalize(path: Path) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip(" \t") for line in text.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_progression_safe_verifiers() -> None:
    targets = {
        F10_VERIFIER: F10_VERIFIER_TEXT,
        F11_VERIFIER: F11_VERIFIER_TEXT,
        F12_VERIFIER: F12_VERIFIER_TEXT,
    }
    for rel, text in targets.items():
        path = ROOT / rel
        require(path.exists(), f"Required verifier not found: {rel}")
        path.write_text(text, encoding="utf-8")
        path.chmod(0o755)
        normalize(path)


def update_state() -> None:
    data = load_state()
    require(
        "bdp_003f12_concept_lens_bridge_output_smoke_review" in data
        or "BDP-003F.12" in data.get("phases", {}),
        "BDP-003F.12 state record is required before F13",
    )
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    record = {
        "phase": PHASE,
        "title": TITLE,
        "status": "complete",
        "completed_at": now,
        "controlled_slice": "ui_integration_contract_only",
        "contract_only": True,
        "frontend_contract_defined": True,
        "frontend_implementation": False,
        "frontend_wiring_approved": False,
        "concept_lens_ui_dock_added": False,
        "streamlit_controls_added": False,
        "backend_routes_added": False,
        "adapter_endpoints_added": False,
        "sql_migrations_added": False,
        "database_mutation": False,
        "citation_creation_added": False,
        "concept_mention_creation_added": False,
        "concept_relation_creation_added": False,
        "interpretation_insertion_added": False,
        "evidence_promotion_added": False,
        "buchanan_claims_created": False,
        "automatic_chat_filtering_added": False,
        "external_llm_routing_added": False,
        "source_ingestion_added": False,
        "approved_display_model": [
            "requested concept label",
            "normalized concept label",
            "archive_lookup_status",
            "evidence_posture",
            "chain completeness summary",
            "rights-safe source metadata",
            "rights-safe locator metadata",
            "rights-safe passage display status",
            "conservative no-match or exploratory status",
        ],
        "approved_labels": [
            "Archive evidence posture",
            "Archive-grounded match",
            "Source-bound description",
            "Exploratory / unverified",
            "No archive match",
            "Rights-limited display",
            "Read-only archive evidence",
        ],
        "blocked_labels": [
            "Buchanan says",
            "Deleuze means",
            "definitive interpretation",
            "validated philosophical truth",
            "automatic concept proof",
        ],
        "first_ui_smoke_cases": [
            "Body without Organs",
            "we repress because we repeat",
            "assemblage",
        ],
        "preserved_archive_chain": [
            "concepts",
            "concept_mentions",
            "passages",
            "citations",
            "sources",
        ],
        "required_service_handoff": "read_concept_lens_archive_evidence_posture_via_existing_archive_bridge",
        "documentation": DOC,
        "verifier": VERIFIER,
        "progression_safe_verifiers_updated": [F10_VERIFIER, F11_VERIFIER, F12_VERIFIER],
        "next_step": NEXT_STEP,
    }
    data[PHASE_KEY] = record
    data.setdefault("phases", {})[PHASE] = record
    data["current_phase"] = PHASE
    data["last_updated_phase"] = PHASE
    data["last_updated_utc"] = now
    for key in ["next_step", "current_next_step", "recommended_next_step", "next_safe_step", "next_recommended_step"]:
        data[key] = NEXT_STEP
    save_state(data)


def update_handover() -> None:
    require(HANDOVER_PATH.exists(), "BUCHANAN_THREAD_HANDOVER.md not found")
    text = HANDOVER_PATH.read_text(encoding="utf-8")
    marker = "## BDP-003F.13 — Concept Lens UI Integration Contract for Read-only Evidence Posture Display"
    block = f"""

{marker}

**Status:** Complete
**Controlled slice:** UI integration contract only

BDP-003F.13 defines the UI integration contract for displaying read-only Concept Lens evidence posture before frontend wiring.

Approved display model:

```text
Archive evidence posture
Archive-grounded match
Source-bound description
Exploratory / unverified
No archive match
Rights-limited display
Read-only archive evidence
```

Preserved archive chain:

```text
concepts -> concept_mentions -> passages -> citations -> sources
```

Required service handoff boundary:

```text
read_concept_lens_archive_evidence_posture_via_existing_archive_bridge
```

First future UI smoke cases:

```text
Body without Organs
we repress because we repeat
assemblage
```

Boundary:

- no frontend wiring
- no Concept Lens UI dock implementation
- no Streamlit controls
- no backend routes
- no adapter endpoints
- no SQL migrations
- no database mutation
- no citation creation
- no concept mention creation
- no concept relation creation
- no interpretation insertion
- no evidence promotion
- no Buchanan-specific claims
- no automatic chat filtering
- no external LLM routing
- no unrestricted passage reproduction
- no source ingestion

Verifier:

```text
{VERIFIER}
```

Next safe step:

```text
{NEXT_STEP}
```
"""
    if marker not in text:
        text = text.rstrip() + block + "\n"
    text = "\n".join(line.rstrip() for line in text.splitlines()).rstrip() + "\n"
    HANDOVER_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    write_progression_safe_verifiers()
    update_state()
    update_handover()
    for rel in [
        DOC,
        VERIFIER,
        F10_VERIFIER,
        F11_VERIFIER,
        F12_VERIFIER,
        "BUCHANAN_THREAD_HANDOVER.md",
    ]:
        normalize(ROOT / rel)
    print("[OK] BDP-003F.13 state, handover, and progression-safe verifiers updated")


if __name__ == "__main__":
    main()
