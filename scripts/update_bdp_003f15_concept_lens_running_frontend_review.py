#!/usr/bin/env python3
"""Record BDP-003F.15 as a running-frontend review-only phase.

This script is intentionally documentation/state only. It does not import or modify
frontend, service, bridge, adapter, or database code.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PHASE = "BDP-003F.15"
PHASE_KEY = "bdp_003f15_concept_lens_running_frontend_review"
TITLE = "Review the Concept Lens read-only evidence posture display in the running frontend before expanding controls or concept coverage"
DOC_PATH = Path("docs/BDP_003F15_CONCEPT_LENS_RUNNING_FRONTEND_REVIEW.md")
STATE_PATH = Path("BUCHANAN_SYSTEM_STATE.json")
HANDOVER_PATH = Path("BUCHANAN_THREAD_HANDOVER.md")
README_PATH = Path("BDP_003F15_PATCH_README.md")

BOUNDARY_NOTE = (
    "This panel displays read-only archive evidence posture. It does not create "
    "citations, claims, interpretations, concept relations, or database records."
)

CONTROLLED_EXAMPLES = [
    "Body without Organs",
    "we repress because we repeat",
    "assemblage",
]

POSTURE_LABELS = [
    "Archive grounded",
    "Source-bound description",
    "Exploratory / unverified",
    "No archive match",
    "Rights-limited display",
    "Read-only archive evidence posture",
]

BLOCKED_PATHS = [
    "frontend/dark_precursor.py",
    "scripts/concept_lens_archive_evidence_posture_service.py",
    "scripts/concept_lens_existing_archive_evidence_readback_bridge.py",
]

BASE_BLOCKED_FLAGS = {
    "frontend_modified_by_bdp_003f15": False,
    "service_modified_by_bdp_003f15": False,
    "bridge_modified_by_bdp_003f15": False,
    "new_frontend_controls_added": False,
    "free_text_search_input_added": False,
    "concept_search_box_added": False,
    "expanded_concept_coverage": False,
    "backend_route_added": False,
    "adapter_endpoint_added": False,
    "sql_migration_added": False,
    "database_mutation": False,
    "database_writes_added": False,
    "archive_row_creation_added": False,
    "source_ingestion_added": False,
    "citation_creation_added": False,
    "claim_creation_added": False,
    "concept_mention_creation_added": False,
    "concept_relation_creation_added": False,
    "interpretation_insertion_added": False,
    "evidence_promotion_added": False,
    "buchanan_claims_created": False,
    "external_llm_routing_added": False,
    "automatic_chat_filtering_added": False,
    "unrestricted_passage_reproduction_added": False,
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "+00:00")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Required state file is missing: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def next_step_for_result(result: str) -> str:
    if result == "pass":
        return "BDP-003F.16 — Decide Concept Lens control and concept coverage expansion readiness after running frontend review."
    return "BDP-003F.16 — Repair the Concept Lens read-only evidence posture display based on running frontend review findings."


def decision_for_result(result: str, findings: list[str]) -> str:
    if result == "pass":
        return (
            "The Concept Lens read-only evidence posture display passed manual running-frontend review. "
            "No expansion of controls or concept coverage is approved by BDP-003F.15."
        )
    joined = "; ".join(findings) if findings else "bounded running-frontend issue recorded"
    return (
        "The Concept Lens read-only evidence posture display requires a later bounded repair phase before controls or "
        f"concept coverage may expand. Findings: {joined}."
    )


def phase_record(result: str, findings: list[str], reviewer_note: str, timestamp: str) -> dict[str, Any]:
    passed = result == "pass"
    next_step = next_step_for_result(result)
    return {
        "phase": PHASE,
        "title": TITLE,
        "status": "complete",
        "completed_at": timestamp,
        "controlled_slice": "running_frontend_review_only",
        "review_type": "manual_running_frontend_review_before_expansion",
        "review_only": True,
        "manual_frontend_inspection_recorded": True,
        "running_frontend_review_passed": passed,
        "running_frontend_review_result": result,
        "decision": decision_for_result(result, findings),
        "running_frontend_review_findings": [] if passed else findings,
        "operator_reviewer_note": reviewer_note,
        "frontend_target_reviewed": "frontend/dark_precursor.py",
        "service_target_reviewed": "scripts/concept_lens_archive_evidence_posture_service.py",
        "bridge_target_reviewed": "scripts/concept_lens_existing_archive_evidence_readback_bridge.py",
        "controlled_concept_examples_reviewed": CONTROLLED_EXAMPLES,
        "approved_posture_labels_reviewed": POSTURE_LABELS,
        "boundary_note_visible": passed,
        "boundary_note": BOUNDARY_NOTE,
        "read_only_boundary_confirmed": passed,
        "no_free_text_concept_search_input_confirmed": passed,
        "no_create_save_promote_cite_interpret_controls_confirmed": passed,
        "restricted_passage_text_omitted_or_rights_limited_confirmed": passed,
        "readable_cinematic_style_confirmed": passed,
        "existing_concept_stage_available": passed,
        "existing_about_page_available": passed,
        "existing_narrator_stage_available": passed,
        "existing_archive_controls_available": passed,
        "next_safe_step": next_step,
        "next_step": next_step,
        "review_output": str(DOC_PATH),
        "verifier": "scripts/verify_bdp_003f15_concept_lens_running_frontend_review.py",
        "review_inputs": [
            "docs/HOW_WE_WORK.md",
            "docs/NEW_THREAD_ONBOARDING.md",
            "docs/DOCS_UPDATE_POLICY.md",
            "BUCHANAN_THREAD_HANDOVER.md",
            "BUCHANAN_SYSTEM_STATE.json",
            "BDP_003F14_PATCH_README.md",
            "docs/BDP_003F14_CONCEPT_LENS_FRONTEND_READ_ONLY_EVIDENCE_POSTURE_WIRING.md",
            "docs/BDP_003F13_CONCEPT_LENS_UI_INTEGRATION_CONTRACT.md",
            "docs/BDP_003F12_CONCEPT_LENS_BRIDGE_OUTPUT_SMOKE_REVIEW.md",
            "docs/BDP_003F11_CONCEPT_LENS_EXISTING_ARCHIVE_READBACK_BRIDGE_IMPLEMENTATION.md",
            "docs/BDP_003F10_CONCEPT_LENS_READ_ONLY_BRIDGE_CONTRACT.md",
            "frontend/dark_precursor.py",
            "scripts/concept_lens_archive_evidence_posture_service.py",
            "scripts/concept_lens_existing_archive_evidence_readback_bridge.py",
            "scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py",
        ],
        **BASE_BLOCKED_FLAGS,
    }


def render_doc(record: dict[str, Any]) -> str:
    findings = record["running_frontend_review_findings"]
    findings_text = "No repair findings recorded." if not findings else "\n".join(f"- {item}" for item in findings)
    result_label = "PASS" if record["running_frontend_review_passed"] else "REPAIR NEEDED"
    examples_text = "\n".join(f"{idx}. {item}" for idx, item in enumerate(CONTROLLED_EXAMPLES, 1))
    labels_text = "\n".join(f"{idx}. {item}" for idx, item in enumerate(POSTURE_LABELS, 1))
    blocked_files_text = "\n".join(f"{idx}. `{item}`" for idx, item in enumerate(BLOCKED_PATHS, 1))
    checklist = [
        ("Concept Lens panel appears inside the existing cinematic frontend", record["running_frontend_review_result"]),
        ("The panel displays read-only evidence posture only", record["running_frontend_review_result"]),
        ("Controlled examples only are visible", record["running_frontend_review_result"]),
        ("The explicit boundary note is visible", "pass" if record["boundary_note_visible"] else "bounded finding"),
        ("No free-text concept search input is present", "pass" if record["no_free_text_concept_search_input_confirmed"] else "bounded finding"),
        ("No create / save / promote / cite / interpret controls are present", "pass" if record["no_create_save_promote_cite_interpret_controls_confirmed"] else "bounded finding"),
        ("Restricted passage text remains omitted or rights-limited", "pass" if record["restricted_passage_text_omitted_or_rights_limited_confirmed"] else "bounded finding"),
        ("The display is readable, cinematic, slow, and visually consistent", "pass" if record["readable_cinematic_style_confirmed"] else "bounded finding"),
        ("Existing concept stage, About page, narrator stage, and archive controls remain available", "pass" if record["existing_concept_stage_available"] else "bounded finding"),
    ]
    checklist_rows = "\n".join(f"| {item} | {status} |" for item, status in checklist)
    return f"""# BDP-003F.15 — Concept Lens Running Frontend Review

**Phase:** {PHASE}
**Title:** {TITLE}
**Controlled slice:** running-frontend review only
**Status:** complete
**Completed at:** {record['completed_at']}
**Manual review result:** {result_label}

## Decision

{record['decision']}

This phase records the running-frontend inspection only. It does not expand Concept Lens functionality and does not approve new controls, broader concept coverage, backend routes, adapter endpoints, database writes, citation creation, concept relation creation, interpretation insertion, or evidence promotion.

## Launch method used

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
. ./venv/bin/activate
python -m streamlit run frontend/dark_precursor.py
```

Do not use PowerShell for this repo. Do not grep recursively through `./venv/`.

## Reviewed controlled concept examples

{examples_text}

No new controlled examples are added by BDP-003F.15.

## Evidence posture labels reviewed

{labels_text}

## Boundary note reviewed

```text
{BOUNDARY_NOTE}
```

## Running-frontend checklist record

| Check | Recorded result |
|---|---|
{checklist_rows}

## Review findings

{findings_text}

## Code modification boundary

BDP-003F.15 does not modify:

{blocked_files_text}

## Confirmed blocked paths

```text
no new frontend controls
no new concept search box
no expansion beyond controlled examples
no backend route
no adapter endpoint
no SQL mutation
no database writes
no archive row creation
no citation creation
no concept mention creation
no concept relation creation
no interpretation insertion
no evidence promotion
no external LLM routing
no source ingestion
no unrestricted passage reproduction
no Buchanan-specific interpretive claim generation
no general chat filtering
```

## Next safe step

```text
{record['next_safe_step']}
```
"""


def update_state(record: dict[str, Any]) -> None:
    state = load_json(STATE_PATH)
    phases = state.setdefault("phases", {})
    phases[PHASE] = record
    state[PHASE_KEY] = record
    state["current_phase"] = PHASE
    state["current_status"] = "complete"
    state["last_updated_phase"] = PHASE
    state["last_updated_utc"] = record["completed_at"]
    state["next_recommended_step"] = record["next_safe_step"]
    state["current_next_step"] = record["next_safe_step"]
    state["next_step"] = record["next_safe_step"]
    state["recommended_next_step"] = record["next_safe_step"]
    state["next_safe_step"] = record["next_safe_step"]
    write_json(STATE_PATH, state)


def update_handover(record: dict[str, Any]) -> None:
    existing = HANDOVER_PATH.read_text(encoding="utf-8") if HANDOVER_PATH.exists() else "# Buchanan Thread Handover\n"
    start = "<!-- BDP-003F.15 RUNNING FRONTEND REVIEW START -->"
    end = "<!-- BDP-003F.15 RUNNING FRONTEND REVIEW END -->"
    findings = record["running_frontend_review_findings"]
    finding_text = "No repair findings recorded." if not findings else "\n".join(f"- {item}" for item in findings)
    block = f"""{start}

## BDP-003F.15 — Concept Lens Running Frontend Review

Status: complete
Review result: {record['running_frontend_review_result']}
Completed at: {record['completed_at']}

Summary:
BDP-003F.15 records a manual running-frontend review of the Concept Lens read-only evidence posture display added in BDP-003F.14. The phase is review-only and does not modify frontend, service, or bridge code.

Reviewed controlled examples:
1. Body without Organs
2. we repress because we repeat
3. assemblage

Confirmed boundary:
{BOUNDARY_NOTE}

Files added or updated by this phase:
1. docs/BDP_003F15_CONCEPT_LENS_RUNNING_FRONTEND_REVIEW.md
2. scripts/update_bdp_003f15_concept_lens_running_frontend_review.py
3. scripts/verify_bdp_003f15_concept_lens_running_frontend_review.py
4. BDP_003F15_PATCH_README.md
5. BUCHANAN_SYSTEM_STATE.json
6. BUCHANAN_THREAD_HANDOVER.md

Files intentionally not modified:
1. frontend/dark_precursor.py
2. scripts/concept_lens_archive_evidence_posture_service.py
3. scripts/concept_lens_existing_archive_evidence_readback_bridge.py

Review findings:
{finding_text}

Next safe step:
{record['next_safe_step']}

{end}
"""
    if start in existing and end in existing:
        before = existing.split(start, 1)[0]
        after = existing.split(end, 1)[1]
        updated = before.rstrip() + "\n\n" + block + after
    else:
        updated = existing.rstrip() + "\n\n" + block
    HANDOVER_PATH.write_text(updated, encoding="utf-8")


def ensure_readme_exists() -> None:
    if README_PATH.exists():
        return
    README_PATH.write_text(
        "# BDP-003F.15 Patch Bundle — Concept Lens Running Frontend Review\n\n"
        "Run `python3 scripts/update_bdp_003f15_concept_lens_running_frontend_review.py --result pass` "
        "after completing the manual running-frontend review.\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Record BDP-003F.15 running-frontend review.")
    parser.add_argument(
        "--result",
        choices=["pass", "repair_needed"],
        default="pass",
        help="Manual review result to record after inspecting the running frontend.",
    )
    parser.add_argument(
        "--finding",
        action="append",
        default=[],
        help="Bounded finding to record when --result repair_needed is used. May be repeated.",
    )
    parser.add_argument(
        "--reviewer-note",
        default="Manual running-frontend review recorded by operator after launching Streamlit via the repo venv.",
        help="Optional operator note stored in state.",
    )
    args = parser.parse_args()

    findings = [item.strip() for item in args.finding if item.strip()]
    if args.result == "repair_needed" and not findings:
        raise SystemExit("--result repair_needed requires at least one --finding entry")

    timestamp = utc_now_iso()
    record = phase_record(args.result, findings, args.reviewer_note, timestamp)

    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.write_text(render_doc(record), encoding="utf-8")
    ensure_readme_exists()
    update_state(record)
    update_handover(record)

    print(f"[OK] {PHASE} running frontend review recorded: {args.result}")
    print(f"[OK] Review doc: {DOC_PATH}")
    print(f"[OK] Next safe step: {record['next_safe_step']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
