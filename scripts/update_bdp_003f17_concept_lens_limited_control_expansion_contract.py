#!/usr/bin/env python3
"""Record BDP-003F.17 Concept Lens limited control expansion contract."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = "BDP-003F.17"
PHASE_KEY = "bdp_003f17_concept_lens_limited_control_expansion_contract"
TITLE = "Define Concept Lens limited control expansion contract after F16 readiness decision"
DOC_PATH = ROOT / "docs" / "BDP_003F17_CONCEPT_LENS_LIMITED_CONTROL_EXPANSION_CONTRACT.md"
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
NEXT_SAFE_STEP = "BDP-003F.18 — Define Concept Lens controlled concept coverage expansion contract after F17 control boundary."

DOC_TEXT = """# BDP-003F.17 — Concept Lens Limited Control Expansion Contract

**Phase:** BDP-003F.17
**Title:** Define Concept Lens limited control expansion contract after F16 readiness decision
**Controlled slice:** limited-control contract only
**Status:** complete

## 1. Purpose

BDP-003F.17 defines the first bounded control expansion contract for the Concept Lens after the BDP-003F.16 readiness decision.

This phase is a contract phase only. It does not implement controls.

The purpose is to define which later user-interface controls may be considered safe for a subsequent implementation phase while preserving the read-only evidence posture boundary established by BDP-003F.14, reviewed by BDP-003F.15, and approved for bounded contract expansion by BDP-003F.16.

## 2. Input authority

The input to this contract is:

```text
BDP-003F.16 — Decide Concept Lens control and concept coverage expansion readiness after running frontend review.
```

BDP-003F.16 selected:

```text
Outcome C — Ready for both separate later contract tracks, but implementation remains blocked.
```

BDP-003F.17 handles only the first of those tracks:

```text
limited control expansion contract
```

It does not handle concept coverage expansion.

## 3. Contract-only boundary

BDP-003F.17 records a contract only.

No frontend changes were made.
No service changes were made.
No bridge changes were made.
No new frontend controls were added.
No concept examples were added.
No free-text search was added.
No database write path was added.
No citation, claim, interpretation, concept relation, concept mention, or archive record creation path was added.
No external LLM routing was added.
No unrestricted passage reproduction was added.

The read-only evidence posture boundary remains intact.

## 4. Existing controlled examples remain unchanged

The existing controlled examples remain the only examples in scope:

```text
Body without Organs
we repress because we repeat
assemblage
```

BDP-003F.17 does not add new examples and does not authorize later concept coverage expansion. Concept coverage expansion requires a separate contract phase.

## 5. Allowed later controls under this contract

A later implementation phase may implement only the following limited, read-only controls, and only if the implementation remains inside the existing Concept Lens display boundary.

### 5.1 Controlled preset selector

A later implementation may expose a selector for the existing controlled examples only:

```text
Body without Organs
we repress because we repeat
assemblage
```

The selector must not accept new options.
The selector must not provide free-text concept search.
The selector must not create concept examples.
The selector must not query unrestricted source text.
The selector must not create database records.

### 5.2 Display density control

A later implementation may expose a display-density control such as:

```text
compact
standard
detailed
```

This control may only change how already-returned read-only evidence posture data is displayed.
It must not change evidence authority, create interpretation, or trigger new backend behaviour.

### 5.3 Evidence detail expander

A later implementation may expose read-only expanders for already-returned metadata such as:

```text
evidence posture label
rights display rule
authority label
source spine summary
controlled concept example status
```

This control must not expose unrestricted passage text and must preserve `omitted_by_rights_policy` where rights require it.

### 5.4 Rights boundary explainer

A later implementation may expose a read-only explanatory toggle for the rights and evidence boundary.

It may explain why passage text is omitted, why evidence posture is not interpretation, and why read-only posture does not authorize Buchanan-specific claims.

### 5.5 Reset to default Concept Lens view

A later implementation may expose a reset control that returns the Concept Lens to the default read-only evidence posture view.

The reset control must not clear database records, session records, archive records, or evidence records because no such records may be created by these controls.

## 6. Explicitly blocked controls

The following remain blocked:

```text
free-text concept search input
new concept search box
new concept examples
accept-new-options selector behaviour
create / save / promote / cite / interpret controls
citation creation controls
claim creation controls
interpretation insertion controls
concept mention creation controls
concept relation creation controls
source ingestion controls
archive row creation controls
database write controls
backend route controls
adapter endpoint controls
external LLM routing controls
general chat filtering controls
unrestricted passage reproduction controls
Buchanan-specific interpretive claim generation controls
```

## 7. Later implementation acceptance criteria

A later control implementation phase must prove all of the following before it can be marked complete:

```text
The implementation touches only the approved frontend Concept Lens block.
The implementation uses only the existing read-only service handoff.
The implementation does not modify the Concept Lens evidence posture service.
The implementation does not modify the existing archive readback bridge.
The implementation does not add a backend route.
The implementation does not add an adapter endpoint.
The implementation does not add SQL migration or database writes.
The implementation does not add free-text concept search.
The implementation does not add concept examples.
The implementation does not create citations, claims, interpretations, concept mentions, concept relations, archive rows, passages, or sources.
The implementation preserves rights-limited display behaviour.
The implementation preserves the read-only evidence posture boundary note.
```

## 8. Concept coverage remains separate

Concept coverage expansion is not authorized by BDP-003F.17.

A separate later contract must define any controlled concept coverage expansion before any new concept examples are added.

## 9. Decision

BDP-003F.17 decides that limited read-only controls may proceed to a later implementation contract or implementation phase only under the boundaries recorded here.

Implementation remains blocked in BDP-003F.17.

## 10. Next safe step

The next safe step is:

```text
BDP-003F.18 — Define Concept Lens controlled concept coverage expansion contract after F17 control boundary.
```

This next step must remain contract-only unless explicitly re-scoped by the operator.
"""

HANDOVER_START = "<!-- BDP-003F.17 START -->"
HANDOVER_END = "<!-- BDP-003F.17 END -->"
HANDOVER_SECTION = f"""{HANDOVER_START}

## BDP-003F.17 — Concept Lens limited control expansion contract

**Status:** complete
**Commit target:** pending operator commit
**Controlled slice:** limited-control contract only

### What changed

- Added `docs/BDP_003F17_CONCEPT_LENS_LIMITED_CONTROL_EXPANSION_CONTRACT.md`.
- Added `scripts/update_bdp_003f17_concept_lens_limited_control_expansion_contract.py`.
- Added `scripts/verify_bdp_003f17_concept_lens_limited_control_expansion_contract.py`.
- Recorded that F17 is a contract-only phase after the F16 readiness decision.
- Defined the only later controls that may be considered under this contract:
  - controlled preset selector over existing examples only
  - display density control
  - read-only evidence detail expander
  - rights boundary explainer toggle
  - reset to default Concept Lens view

### Boundary preserved

- No frontend changes were made.
- No service or bridge changes were made.
- No new frontend controls were added.
- No concept examples were added.
- No free-text search was added.
- No database writes were added.
- No citation, claim, interpretation, concept mention, concept relation, or archive record creation path was added.
- No external LLM routing was added.
- No unrestricted passage reproduction was added.

### Next safe step

```text
{NEXT_SAFE_STEP}
```

This next step must remain contract-only unless explicitly re-scoped by the operator.

{HANDOVER_END}
"""


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"Missing required file: {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        fail(f"Expected JSON object in {path.relative_to(ROOT)}")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def upsert_marked_section(path: Path, section: str, start: str, end: str) -> None:
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    if start in original and end in original:
        before = original.split(start, 1)[0]
        after = original.split(end, 1)[1]
        updated = before.rstrip() + "\n\n" + section.strip() + "\n" + after.lstrip()
    else:
        updated = section.strip() + "\n\n" + original.lstrip()
    path.write_text(updated, encoding="utf-8")


def build_record() -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "phase": PHASE,
        "title": TITLE,
        "status": "complete",
        "controlled_slice": "limited_control_expansion_contract_only",
        "contract_only": True,
        "input_phase": "BDP-003F.16 — Concept Lens expansion readiness decision",
        "input_outcome": "Outcome C — Ready for both separate later contract tracks, but implementation remains blocked.",
        "completed_at": now,
        "updated_at": now,
        "implementation_added": False,
        "frontend_modified_by_bdp_003f17": False,
        "service_modified_by_bdp_003f17": False,
        "bridge_modified_by_bdp_003f17": False,
        "new_frontend_controls_added": False,
        "concept_coverage_expanded": False,
        "free_text_search_input_added": False,
        "concept_search_box_added": False,
        "new_concept_examples_added": False,
        "controlled_concept_examples_unchanged": [
            "Body without Organs",
            "we repress because we repeat",
            "assemblage",
        ],
        "allowed_later_controls_defined": True,
        "allowed_later_controls": [
            "controlled_preset_selector_existing_examples_only",
            "display_density_control",
            "read_only_evidence_detail_expander",
            "rights_boundary_explainer_toggle",
            "reset_to_default_concept_lens_view",
        ],
        "blocked_controls": [
            "free_text_concept_search_input",
            "new_concept_search_box",
            "new_concept_examples",
            "accept_new_options_selector_behaviour",
            "create_save_promote_cite_interpret_controls",
            "citation_creation_controls",
            "claim_creation_controls",
            "interpretation_insertion_controls",
            "concept_mention_creation_controls",
            "concept_relation_creation_controls",
            "source_ingestion_controls",
            "archive_row_creation_controls",
            "database_write_controls",
            "backend_route_controls",
            "adapter_endpoint_controls",
            "external_llm_routing_controls",
            "general_chat_filtering_controls",
            "unrestricted_passage_reproduction_controls",
            "buchanan_specific_interpretive_claim_generation_controls",
        ],
        "boundaries": {
            "frontend_changes": False,
            "service_changes": False,
            "bridge_changes": False,
            "new_frontend_controls": False,
            "new_concept_search_box": False,
            "new_concept_examples": False,
            "concept_coverage_expansion": False,
            "backend_route": False,
            "adapter_endpoint": False,
            "sql_migration": False,
            "sql_mutation": False,
            "database_writes": False,
            "archive_row_creation": False,
            "citation_creation": False,
            "claim_creation": False,
            "concept_mention_creation": False,
            "concept_relation_creation": False,
            "interpretation_insertion": False,
            "evidence_promotion": False,
            "external_llm_routing": False,
            "source_ingestion": False,
            "unrestricted_passage_reproduction": False,
            "buchanan_specific_interpretive_claim_generation": False,
            "general_chat_filtering": False,
        },
        "next_safe_step": NEXT_SAFE_STEP,
    }


def update_state() -> None:
    data = load_json(STATE_PATH)
    phases = data.setdefault("phases", {})
    if not isinstance(phases, dict):
        fail("BUCHANAN_SYSTEM_STATE.json phases field must be an object")

    record = build_record()
    phases[PHASE] = record
    data[PHASE_KEY] = record
    data["current_phase"] = PHASE
    data["last_updated_phase"] = PHASE
    data["last_updated_utc"] = record["updated_at"]
    data["next_recommended_step"] = NEXT_SAFE_STEP
    data["next_step"] = NEXT_SAFE_STEP
    data["current_next_step"] = NEXT_SAFE_STEP
    data["recommended_next_step"] = NEXT_SAFE_STEP
    data["next_safe_step"] = NEXT_SAFE_STEP

    write_json(STATE_PATH, data)


def main() -> None:
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.write_text(DOC_TEXT, encoding="utf-8")
    update_state()
    upsert_marked_section(HANDOVER_PATH, HANDOVER_SECTION, HANDOVER_START, HANDOVER_END)

    print("[OK] BDP-003F.17 limited control expansion contract recorded")
    print(f"[OK] Wrote {DOC_PATH.relative_to(ROOT)}")
    print(f"[OK] Updated {STATE_PATH.relative_to(ROOT)}")
    print(f"[OK] Updated {HANDOVER_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
