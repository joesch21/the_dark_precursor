#!/usr/bin/env python3
"""Apply BDP-003F.10 state and handover updates.

This updater is intentionally merge-safe: it edits the repository's current
BUCHANAN_SYSTEM_STATE.json and BUCHANAN_THREAD_HANDOVER.md instead of replacing
those files from a generated bundle.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
DOC_PATH = ROOT / "docs" / "BDP_003F10_CONCEPT_LENS_READ_ONLY_BRIDGE_CONTRACT.md"

PHASE_KEY = "bdp_003f10_concept_lens_existing_archive_readback_bridge_contract"
PHASE_TITLE = "Define approved read-only bridge from existing archive evidence readback into the Concept Lens service"
NEXT_STEP = "BDP-003F.11 — Implement the approved read-only bridge from existing archive evidence readback into the Concept Lens service."


def load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Missing required state file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_state() -> None:
    data = load_json(STATE_PATH)
    completed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    phase_record = {
        "phase": "BDP-003F.10",
        "title": PHASE_TITLE,
        "status": "complete",
        "completed_at": completed_at,
        "controlled_slice": "read_only_bridge_contract_definition_only",
        "definition_only": True,
        "contract_only": True,
        "bridge_contract_defined": True,
        "bridge_contract_name": "concept_lens_existing_archive_evidence_readback_bridge.v1",
        "bridge_implemented": False,
        "future_bridge_module": "scripts/concept_lens_existing_archive_evidence_readback_bridge.py",
        "future_bridge_function": "read_existing_archive_evidence_rows_for_concept",
        "target_service_module": "scripts/concept_lens_archive_evidence_posture_service.py",
        "target_service_function": "read_concept_lens_archive_evidence_posture",
        "prior_review_finding": "BDP-003F.9 Outcome C: governed archive evidence exists, but no approved live readback adapter is currently exposed for the Concept Lens service default path.",
        "approved_source_readback_candidates": [
            "scripts/read_bdp_001r_bwo_source_bound_description.py",
            "scripts/read_bdp_002b_bwo_evidence_card.py",
        ],
        "primary_archive_readback_chain": [
            "concepts",
            "concept_mentions",
            "passages",
            "citations",
            "sources",
        ],
        "required_first_review_case": "Body without Organs",
        "bridge_output_scope": "in_memory_f8_compatible_archive_evidence_rows_only",
        "rights_boundary": "restricted passage text remains omitted_by_rights_policy; metadata and locators only",
        "failure_posture": "missing or inaccessible readback returns safe empty/no-match rows; no archive evidence is fabricated",
        "frontend_implementation": False,
        "concept_lens_ui_dock_added": False,
        "streamlit_controls_added": False,
        "new_navigation_surface_keys_added": False,
        "backend_route_added": False,
        "adapter_endpoint_added": False,
        "sql_migration_added": False,
        "database_tables_added": False,
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
        "service_modified": False,
        "review_output": "docs/BDP_003F10_CONCEPT_LENS_READ_ONLY_BRIDGE_CONTRACT.md",
        "verifier": "scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py",
        "review_inputs": [
            "BDP-003F.8 Concept Lens archive evidence posture service",
            "BDP-003F.9 Concept Lens evidence posture output review",
            "scripts/read_bdp_001r_bwo_source_bound_description.py",
            "scripts/read_bdp_002b_bwo_evidence_card.py",
        ],
        "next_step": NEXT_STEP,
    }

    data.setdefault("phases", {})["BDP-003F.10"] = phase_record
    data[PHASE_KEY] = phase_record
    data["last_updated_phase"] = "BDP-003F.10"
    data["current_phase"] = "BDP-003F.10"
    data["current_status"] = "complete"
    data["last_updated_utc"] = completed_at
    data["current_next_step"] = NEXT_STEP
    data["next_step"] = NEXT_STEP
    data["recommended_next_step"] = NEXT_STEP
    data["next_recommended_step"] = NEXT_STEP
    data["next_safe_step"] = NEXT_STEP

    write_json(STATE_PATH, data)


def update_handover() -> None:
    if not HANDOVER_PATH.exists():
        raise SystemExit(f"Missing required handover file: {HANDOVER_PATH}")
    if not DOC_PATH.exists():
        raise SystemExit(f"Missing required F10 doc: {DOC_PATH}")

    text = HANDOVER_PATH.read_text(encoding="utf-8")
    start = "<!-- BDP-003F.10-CONCEPT-LENS-READ-ONLY-BRIDGE-CONTRACT-START -->"
    end = "<!-- BDP-003F.10-CONCEPT-LENS-READ-ONLY-BRIDGE-CONTRACT-END -->"

    block = f"""{start}
## BDP-003F.10 — Concept Lens Existing Archive Evidence Readback Bridge Contract

**Status:** Complete
**Controlled slice:** read-only bridge contract definition only

BDP-003F.10 defines the approved read-only bridge contract from existing governed archive evidence readback into the BDP-003F.8 Concept Lens archive evidence posture service.

Decision: the bridge contract is approved as a future implementation boundary, but implementation is not added by BDP-003F.10.

Contract name:

```text
concept_lens_existing_archive_evidence_readback_bridge.v1
```

Future implementation target, if later approved:

```text
scripts/concept_lens_existing_archive_evidence_readback_bridge.py
```

Approved source readback candidates to inspect before implementation:

```text
scripts/read_bdp_001r_bwo_source_bound_description.py
scripts/read_bdp_002b_bwo_evidence_card.py
```

Bridge target:

```text
scripts/concept_lens_archive_evidence_posture_service.py
read_concept_lens_archive_evidence_posture
```

Required primary chain preserved:

```text
concepts -> concept_mentions -> passages -> citations -> sources
```

Boundary:

1. no frontend wiring;
2. no Concept Lens UI dock;
3. no backend route;
4. no adapter endpoint;
5. no SQL migration;
6. no database mutation;
7. no citation, concept mention, concept relation, interpretation, evidence promotion, or Buchanan-specific claim creation;
8. no F8 service implementation change.

UI integration remains blocked.

Verifier:

```text
scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py
```

Next safe step:

```text
{NEXT_STEP}
```
{end}"""

    if start in text and end in text:
        before = text.split(start, 1)[0].rstrip()
        after = text.split(end, 1)[1].lstrip()
        text = before + "\n\n" + block + "\n\n" + after
    else:
        text = text.rstrip() + "\n\n" + block + "\n"

    lines = [line.rstrip() for line in text.splitlines()]
    while lines and lines[-1] == "":
        lines.pop()
    HANDOVER_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    update_state()
    update_handover()
    print("[OK] BDP-003F.10 state and handover updated")


if __name__ == "__main__":
    main()
