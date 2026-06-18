#!/usr/bin/env python3
"""Apply BDP-003F.11 implementation updates."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
F10_DOC_PATH = ROOT / "docs" / "BDP_003F10_CONCEPT_LENS_READ_ONLY_BRIDGE_CONTRACT.md"
F11_DOC_PATH = ROOT / "docs" / "BDP_003F11_CONCEPT_LENS_EXISTING_ARCHIVE_READBACK_BRIDGE_IMPLEMENTATION.md"
F8_SERVICE_PATH = ROOT / "scripts" / "concept_lens_archive_evidence_posture_service.py"
BRIDGE_PATH = ROOT / "scripts" / "concept_lens_existing_archive_evidence_readback_bridge.py"

PHASE_KEY = "bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation"
F10_PHASE_KEY = "bdp_003f10_concept_lens_existing_archive_readback_bridge_contract"
PHASE_TITLE = "Implement the approved read-only bridge from existing archive evidence readback into the Concept Lens service"
NEXT_STEP = "BDP-003F.12 — Review live Body without Organs bridge output against the Concept Lens service before UI integration."
MARKER_START = "# BDP-003F.11 EXISTING ARCHIVE READBACK BRIDGE INTEGRATION START"
MARKER_END = "# BDP-003F.11 EXISTING ARCHIVE READBACK BRIDGE INTEGRATION END"

SERVICE_WRAPPER = f'''

{MARKER_START}
def read_concept_lens_archive_evidence_posture_via_existing_archive_bridge(
    concept: str,
    *,
    repo_root=None,
    require_live_readback: bool = True,
    bridge_rows=None,
):
    """Classify Concept Lens posture through the BDP-003F.11 read-only bridge."""
    import inspect
    from concept_lens_existing_archive_evidence_readback_bridge import (
        read_existing_archive_evidence_rows_for_concept,
    )

    rows = bridge_rows
    if rows is None:
        rows = read_existing_archive_evidence_rows_for_concept(
            concept,
            repo_root=repo_root,
            require_live_readback=require_live_readback,
        )

    classifier = read_concept_lens_archive_evidence_posture
    signature = inspect.signature(classifier)
    params = signature.parameters

    for candidate_name in (
        "archive_rows",
        "supplied_archive_rows",
        "evidence_rows",
        "rows",
    ):
        if candidate_name in params:
            return classifier(concept, **{{candidate_name: rows}})

    positional = [
        param
        for param in params.values()
        if param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD)
    ]
    if len(positional) >= 2:
        return classifier(concept, rows)

    raise TypeError(
        "BDP-003F.11 bridge could not locate a supported supplied-row parameter "
        "on read_concept_lens_archive_evidence_posture."
    )
{MARKER_END}
'''


def load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Missing required state file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def require_f10_anchor(data: dict) -> None:
    if not F10_DOC_PATH.exists():
        raise SystemExit("BDP-003F.11 requires the BDP-003F.10 contract document. Apply and commit F10 first.")
    f10 = data.get(F10_PHASE_KEY)
    if not isinstance(f10, dict) or f10.get("status") != "complete":
        raise SystemExit("BDP-003F.11 requires BDP-003F.10 to be recorded as complete in BUCHANAN_SYSTEM_STATE.json.")


def update_service_wrapper() -> None:
    if not F8_SERVICE_PATH.exists():
        raise SystemExit(f"Missing F8 service file: {F8_SERVICE_PATH}")
    text = F8_SERVICE_PATH.read_text(encoding="utf-8")
    if MARKER_START in text:
        return
    if "def read_concept_lens_archive_evidence_posture" not in text:
        raise SystemExit("F8 service does not contain read_concept_lens_archive_evidence_posture; cannot attach bridge wrapper safely.")
    text = text.rstrip() + SERVICE_WRAPPER + "\n"
    F8_SERVICE_PATH.write_text(text, encoding="utf-8")


def update_state() -> None:
    data = load_json(STATE_PATH)
    require_f10_anchor(data)
    completed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    phase_record = {
        "phase": "BDP-003F.11",
        "title": PHASE_TITLE,
        "status": "complete",
        "completed_at": completed_at,
        "controlled_slice": "read_only_bridge_implementation_only",
        "implementation_type": "existing_archive_readback_bridge_to_f8_service_rows",
        "contract_source": "BDP-003F.10",
        "bridge_contract_name": "concept_lens_existing_archive_evidence_readback_bridge.v1",
        "bridge_implemented": True,
        "bridge_module": "scripts/concept_lens_existing_archive_evidence_readback_bridge.py",
        "bridge_function": "read_existing_archive_evidence_rows_for_concept",
        "bridge_review_helper": "read_existing_archive_evidence_rows_from_readback_text",
        "target_service_module": "scripts/concept_lens_archive_evidence_posture_service.py",
        "target_service_function": "read_concept_lens_archive_evidence_posture",
        "service_wrapper_added": True,
        "service_wrapper_function": "read_concept_lens_archive_evidence_posture_via_existing_archive_bridge",
        "first_supported_review_case": "Body without Organs",
        "approved_source_readback_candidates": [
            "scripts/read_bdp_001r_bwo_source_bound_description.py",
            "scripts/read_bdp_002b_bwo_evidence_card.py",
        ],
        "primary_archive_readback_chain": ["concepts", "concept_mentions", "passages", "citations", "sources"],
        "rights_boundary": "restricted passage text remains omitted_by_rights_policy; metadata and locators only",
        "failure_posture": "return_empty_rows_for_no_confirmed_readback; F8 remains conservative",
        "frontend_implementation": False,
        "concept_lens_ui_dock_added": False,
        "streamlit_controls_added": False,
        "new_navigation_surface_keys_added": False,
        "backend_route_added": False,
        "adapter_endpoint_added": False,
        "database_tables_added": False,
        "sql_migration_added": False,
        "database_mutation": False,
        "source_ingestion_added": False,
        "citation_creation_added": False,
        "concept_mention_creation_added": False,
        "concept_relation_creation_added": False,
        "interpretation_insertion_added": False,
        "evidence_promotion_added": False,
        "buchanan_claims_created": False,
        "automatic_chat_filtering_added": False,
        "external_llm_routing_added": False,
        "philosophical_fidelity_review_added": False,
        "review_output": "docs/BDP_003F11_CONCEPT_LENS_EXISTING_ARCHIVE_READBACK_BRIDGE_IMPLEMENTATION.md",
        "implementation_files": [
            "scripts/concept_lens_existing_archive_evidence_readback_bridge.py",
            "scripts/concept_lens_archive_evidence_posture_service.py",
        ],
        "verifier": "scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py",
        "next_step": NEXT_STEP,
    }

    data[PHASE_KEY] = phase_record
    data.setdefault("phases", {})["BDP-003F.11"] = phase_record
    data["current_phase"] = "BDP-003F.11"
    data["last_updated_phase"] = "BDP-003F.11"
    data["current_next_step"] = NEXT_STEP
    data["next_step"] = NEXT_STEP
    data["recommended_next_step"] = NEXT_STEP
    data["next_safe_step"] = NEXT_STEP
    data["last_updated_utc"] = completed_at
    write_json(STATE_PATH, data)


def update_handover() -> None:
    if not HANDOVER_PATH.exists():
        raise SystemExit(f"Missing handover file: {HANDOVER_PATH}")
    text = HANDOVER_PATH.read_text(encoding="utf-8")
    marker = "## BDP-003F.11 — Concept Lens Existing Archive Evidence Readback Bridge Implementation"
    if marker in text:
        return

    entry = f'''

## BDP-003F.11 — Concept Lens Existing Archive Evidence Readback Bridge Implementation

**Status:** Complete
**Controlled slice:** read-only bridge implementation only

BDP-003F.11 implements the approved BDP-003F.10 read-only bridge from existing governed archive evidence readback into the BDP-003F.8 Concept Lens archive evidence posture service.

Implemented bridge module:

```text
scripts/concept_lens_existing_archive_evidence_readback_bridge.py
```

Implemented bridge function:

```text
read_existing_archive_evidence_rows_for_concept
```

Implemented service wrapper:

```text
read_concept_lens_archive_evidence_posture_via_existing_archive_bridge
```

The bridge supplies F8-compatible in-memory rows only. The F8 service remains the posture classifier.

First supported review case:

```text
Body without Organs
```

Boundary:

1. No frontend wiring.
2. No Concept Lens UI dock.
3. No Streamlit controls.
4. No new navigation surface keys.
5. No backend route.
6. No adapter endpoint.
7. No SQL migration.
8. No database mutation.
9. No citation creation.
10. No concept mention creation.
11. No concept relation creation.
12. No interpretation insertion.
13. No evidence promotion.
14. No Buchanan-specific claims.

Verifier:

```text
scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py
```

Next safe step:

```text
{NEXT_STEP}
```
'''
    HANDOVER_PATH.write_text(text.rstrip() + entry + "\n", encoding="utf-8")


def main() -> None:
    if not F11_DOC_PATH.exists():
        raise SystemExit(f"Missing F11 document: {F11_DOC_PATH}")
    if not BRIDGE_PATH.exists():
        raise SystemExit(f"Missing F11 bridge module: {BRIDGE_PATH}")
    update_service_wrapper()
    update_state()
    update_handover()
    print("[OK] BDP-003F.11 bridge implementation, state, handover, and service wrapper updated")


if __name__ == "__main__":
    main()
