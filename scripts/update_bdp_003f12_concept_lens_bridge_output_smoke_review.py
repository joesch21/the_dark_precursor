#!/usr/bin/env python3
"""Update state and handover for BDP-003F.12 Concept Lens bridge output smoke review."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

PHASE = "BDP-003F.12"
PHASE_KEY = "bdp_003f12_concept_lens_bridge_output_smoke_review"
TITLE = "Review Concept Lens bridge output smoke posture before UI integration"
DOC = "docs/BDP_003F12_CONCEPT_LENS_BRIDGE_OUTPUT_SMOKE_REVIEW.md"
VERIFIER = "scripts/verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py"
NEXT_STEP = "BDP-003F.13 — Define Concept Lens UI integration contract for read-only evidence posture display before frontend wiring."

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"[FAIL] {message}")


def load_state() -> dict:
    require(STATE_PATH.exists(), "BUCHANAN_SYSTEM_STATE.json not found")
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(data: dict) -> None:
    STATE_PATH.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def update_state() -> None:
    data = load_state()
    require(
        "bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation" in data
        or "BDP-003F.11" in data.get("phases", {}),
        "BDP-003F.11 state record is required before F12",
    )

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    record = {
        "phase": PHASE,
        "title": TITLE,
        "status": "complete",
        "completed_at": now,
        "controlled_slice": "read_only_bridge_output_smoke_review_only",
        "review_type": "bridge_output_smoke_review_before_ui_integration",
        "decision": "The BDP-003F.11 bridge may be used for read-only local smoke review, but Concept Lens UI integration remains blocked until a separate UI integration contract or wiring phase is approved.",
        "smoke_cases_required": [
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
        "read_only_bridge_reviewed": True,
        "frontend_wiring_approved": False,
        "concept_lens_ui_dock_added": False,
        "streamlit_controls_added": False,
        "backend_routes_added": False,
        "adapter_endpoints_added": False,
        "sql_migrations_added": False,
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
        "documentation": DOC,
        "verifier": VERIFIER,
        "review_inputs": [
            "BDP-003F.10 Concept Lens read-only bridge contract",
            "BDP-003F.11 Concept Lens existing archive readback bridge implementation",
            "scripts/concept_lens_existing_archive_evidence_readback_bridge.py",
            "scripts/concept_lens_archive_evidence_posture_service.py",
        ],
        "next_step": NEXT_STEP,
    }

    data[PHASE_KEY] = record
    data.setdefault("phases", {})[PHASE] = record
    data["current_phase"] = PHASE
    data["last_updated_phase"] = PHASE
    data["last_updated_utc"] = now
    for key in [
        "next_step",
        "current_next_step",
        "recommended_next_step",
        "next_safe_step",
        "next_recommended_step",
    ]:
        data[key] = NEXT_STEP

    save_state(data)


def update_handover() -> None:
    require(HANDOVER_PATH.exists(), "BUCHANAN_THREAD_HANDOVER.md not found")
    text = HANDOVER_PATH.read_text(encoding="utf-8")
    marker = "## BDP-003F.12 — Concept Lens Bridge Output Smoke Review Before UI Integration"
    block = f"""

{marker}

**Status:** Complete
**Controlled slice:** read-only bridge output smoke review only

BDP-003F.12 records the bridge output smoke-review gate after the BDP-003F.11 read-only bridge implementation and before any Concept Lens UI integration.

Review finding:

```text
The BDP-003F.11 bridge may be used for read-only local smoke review, but the Concept Lens UI remains blocked until a separate UI integration contract or frontend wiring phase is approved.
```

Required smoke cases:

```text
Body without Organs
we repress because we repeat
assemblage
```

Preserved archive readback chain:

```text
concepts -> concept_mentions -> passages -> citations -> sources
```

Boundary:

- no Concept Lens UI dock
- no Streamlit controls
- no frontend wiring
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
    update_state()
    update_handover()
    print("[OK] BDP-003F.12 state and handover updated")


if __name__ == "__main__":
    main()
