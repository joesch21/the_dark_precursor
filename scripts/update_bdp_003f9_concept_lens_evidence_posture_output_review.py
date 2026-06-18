#!/usr/bin/env python3
"""Apply BDP-003F.9 review-only state and handover updates.

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
DOC_PATH = ROOT / "docs" / "BDP_003F9_CONCEPT_LENS_EVIDENCE_POSTURE_OUTPUT_REVIEW.md"

PHASE_KEY = "bdp_003f9_concept_lens_evidence_posture_output_review"
PHASE_TITLE = "Review Concept Lens evidence posture service output against known archive cases before UI integration"
NEXT_STEP = "BDP-003F.10 — Define approved read-only bridge from existing archive evidence readback into the Concept Lens service."


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
        "phase": "BDP-003F.9",
        "title": PHASE_TITLE,
        "status": "complete",
        "completed_at": completed_at,
        "controlled_slice": "review_only_evidence_posture_output_review",
        "review_only": True,
        "review_target": "scripts/concept_lens_archive_evidence_posture_service.py",
        "review_output": "docs/BDP_003F9_CONCEPT_LENS_EVIDENCE_POSTURE_OUTPUT_REVIEW.md",
        "verifier": "scripts/verify_bdp_003f9_concept_lens_evidence_posture_output_review.py",
        "finding": "outcome_c_existing_archive_evidence_not_currently_reachable_by_default_service_path",
        "decision": "The archive evidence exists in governed project state, but no approved live readback adapter is currently exposed for the Concept Lens service default path.",
        "body_without_organs_project_archive_status": "known_governed_archive_case",
        "body_without_organs_default_f8_service_status": "must_not_report_archive_grounded_without_configured_live_bridge",
        "f8_service_intentionally_non_live_by_default": True,
        "f8_default_no_live_archive_output_safe": True,
        "default_archive_lookup_status": "no_archive_match",
        "default_evidence_posture": "exploratory_unverified",
        "known_archive_readback_chain": [
            "concepts",
            "concept_mentions",
            "passages",
            "citations",
            "sources",
        ],
        "known_archive_case": "Body without Organs",
        "known_prior_readback_scripts_to_inspect": [
            "scripts/read_bdp_001r_bwo_source_bound_description.py",
            "scripts/read_bdp_002b_bwo_evidence_card.py",
        ],
        "live_sql_archive_adapter_contract_needed_next": True,
        "ui_integration_blocked": True,
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
        "next_step": NEXT_STEP,
    }

    data[PHASE_KEY] = phase_record
    for key in [
        "last_updated_phase",
        "current_phase",
    ]:
        data[key] = "BDP-003F.9"
    data["last_updated_utc"] = completed_at
    for key in [
        "current_next_step",
        "next_step",
        "recommended_next_step",
        "next_safe_step",
        "next_recommended_step",
    ]:
        data[key] = NEXT_STEP

    phases = data.setdefault("phases", {})
    phases["BDP-003F.9"] = {
        "phase": "BDP-003F.9",
        "title": PHASE_TITLE,
        "status": "complete",
        "type": "review_only_evidence_posture_output_review",
        "updated_at": completed_at,
        "summary": phase_record["decision"],
        "deliverables": [
            "docs/BDP_003F9_CONCEPT_LENS_EVIDENCE_POSTURE_OUTPUT_REVIEW.md",
            "scripts/verify_bdp_003f9_concept_lens_evidence_posture_output_review.py",
            "scripts/update_bdp_003f9_concept_lens_evidence_posture_output_review.py",
            "BDP_003F9_PATCH_README.md",
        ],
        "boundaries": {
            "frontend_implementation": False,
            "backend_route_added": False,
            "adapter_endpoint_added": False,
            "sql_migration_added": False,
            "database_mutation": False,
            "citation_creation_added": False,
            "concept_mention_creation_added": False,
            "concept_relation_creation_added": False,
            "interpretation_insertion_added": False,
            "evidence_promotion_added": False,
            "buchanan_claims_created": False,
        },
        "next_step": NEXT_STEP,
    }

    write_json(STATE_PATH, data)


def update_handover() -> None:
    if not HANDOVER_PATH.exists():
        raise SystemExit(f"Missing required handover file: {HANDOVER_PATH}")

    text = HANDOVER_PATH.read_text(encoding="utf-8")
    marker = "## BDP-003F.9 — Concept Lens Evidence Posture Output Review"
    if marker in text:
        return

    section = f"""

## BDP-003F.9 — Concept Lens Evidence Posture Output Review

**Status:** Complete  
**Controlled slice:** review-only evidence posture output review

BDP-003F.9 reviews the BDP-003F.8 Concept Lens archive evidence posture service output against known archive cases before UI integration.

Finding: Outcome C.

```text
The archive evidence exists in governed project state, but no approved live readback adapter is currently exposed for the Concept Lens service default path.
```

Review decision:

1. Body without Organs is a known governed archive case in project state.
2. The F8 default service path is safe and intentionally conservative when no live archive adapter is configured.
3. The F8 service must not report `archive_grounded` for Body without Organs from the default no-live-archive invocation.
4. Concept Lens UI integration remains blocked.
5. A read-only bridge from existing archive evidence readback into the Concept Lens service is needed before frontend wiring.

No frontend wiring, Concept Lens UI dock, Streamlit controls, backend route, adapter endpoint, SQL migration, database mutation, citation creation, concept mention creation, concept relation creation, interpretation insertion, evidence promotion, Buchanan-specific claim, automatic chat filtering, or external LLM routing is approved by this phase.

Verifier:

```text
scripts/verify_bdp_003f9_concept_lens_evidence_posture_output_review.py
```

Next safe step:

```text
{NEXT_STEP}
```
"""
    HANDOVER_PATH.write_text(text.rstrip() + section + "\n", encoding="utf-8")


def main() -> None:
    if not DOC_PATH.exists():
        raise SystemExit(f"Missing BDP-003F.9 review doc: {DOC_PATH}")
    update_state()
    update_handover()
    print("[OK] BDP-003F.9 state and handover updated")


if __name__ == "__main__":
    main()
