#!/usr/bin/env python3
"""Record BDP-003F.16 Concept Lens expansion readiness decision.

This updater is intentionally documentation/state only. It writes the F16
readiness decision document, updates BUCHANAN_SYSTEM_STATE.json, and appends a
bounded handover block. It does not edit frontend or Concept Lens service files.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "BDP_003F16_CONCEPT_LENS_EXPANSION_READINESS_DECISION.md"
PATCH_README_PATH = ROOT / "BDP_003F16_PATCH_README.md"
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"

PHASE = "BDP-003F.16"
TITLE = "Decide Concept Lens control and concept coverage expansion readiness after running frontend review"
OUTCOME = "Outcome C — Ready for both separate later contract tracks, but implementation remains blocked."
NEXT_STEP = "BDP-003F.17 — Define Concept Lens limited control expansion contract after F16 readiness decision."
FOLLOW_ON_STEP = "BDP-003F.18 — Define Concept Lens controlled concept coverage expansion contract after control readiness boundary."

DECISION_DOC = '''# BDP-003F.16 — Concept Lens Expansion Readiness Decision

**Phase:** BDP-003F.16
**Title:** Decide Concept Lens control and concept coverage expansion readiness after running frontend review
**Controlled slice:** decision-only readiness record
**Status:** complete
**Input phase:** BDP-003F.15 — Concept Lens running frontend review
**Readiness outcome:** Outcome C — Ready for both separate later contract tracks, but implementation remains blocked.

## Decision

BDP-003F.16 records a decision only.

After the BDP-003F.15 running-frontend review, the Concept Lens read-only evidence posture display is stable enough to define later bounded expansion contracts for both:

1. limited control expansion; and
2. controlled concept coverage expansion.

This decision does not authorize implementation in BDP-003F.16.

The next safe move is a later bounded contract phase, not direct expansion.

## Review input

The decision input is BDP-003F.15, which reviewed the Concept Lens read-only evidence posture display in the running frontend after the BDP-003F.14 wiring phase.

The F15 review input means this decision is based on the running frontend posture display, not on a new service, new route, new adapter endpoint, new concept search feature, or new archive-writing capability.

## Readiness finding

The F15 running frontend review is sufficient to move to separate contract-definition phases because the current surface can be treated as a stable read-only posture display.

The display is ready for bounded contract planning only. It is not ready for direct control implementation, direct concept coverage expansion, or any generative claim layer.

## Control expansion readiness

Limited controls may proceed to a later contract phase.

Any future control expansion contract must remain bounded and must define the exact allowed operator controls before implementation. It must not smuggle in free-text concept search, backend routes, adapter endpoints, SQL mutation, unrestricted archive browsing, citation creation, concept mention creation, relation creation, interpretation insertion, evidence promotion, or external LLM routing.

## Concept coverage expansion readiness

Controlled concept coverage may proceed to a later contract phase.

Additional concept examples must be defined in a separate contract before any examples are added. Future concept coverage must stay controlled, finite, evidence-posture oriented, and rights-aware. It must not become a general concept search surface or a Buchanan-specific interpretive claim generator.

## Controlled examples sufficiency

The current controlled examples are sufficient for defining later bounded expansion contracts.

They are not sufficient to authorize implementation directly.

## F15 risks carried forward

1. A readable evidence posture display can be mistaken for interpretive authority unless authority labels and boundary language remain visible.
2. Control expansion can drift into free-text search unless the contract explicitly limits allowed controls.
3. Concept coverage expansion can drift into new claims, citations, relations, or interpretations unless each concept remains governed by the evidence spine.
4. Running-frontend stability is not the same as authorization to mutate archive records.
5. Rights boundaries must continue to prevent unrestricted passage reproduction.

## Boundaries preserved

F16 is decision-only.

F15 running frontend review is the input.

No frontend changes were made.

No service or bridge changes were made.

No controls were added.

No concept examples were added.

No free-text search was added.

No citation, claim, interpretation, concept relation, or database record creation path was added.

No SQL mutation was added.

No archive row creation was added.

No evidence promotion was added.

No external LLM routing was added.

No source ingestion was added.

No unrestricted passage reproduction was added.

No Buchanan-specific interpretive claim generation was added.

No general chat filtering was added.

The read-only evidence posture boundary remains intact.

## Decision outcome

Outcome C — Ready for both contract tracks, but implementation remains blocked.

This means:

1. the Concept Lens may proceed to a later limited control expansion contract;
2. the Concept Lens may proceed to a later controlled concept coverage expansion contract; and
3. neither track may be implemented until its own contract phase is written and verified.

## Next safe step

BDP-003F.17 — Define Concept Lens limited control expansion contract after F16 readiness decision.

A later separate phase may then define:

BDP-003F.18 — Define Concept Lens controlled concept coverage expansion contract after control readiness boundary.

## Verification expectations

The BDP-003F.16 verifier must prove that:

1. this phase is recorded as decision-only;
2. F15 is recorded as the review input;
3. the readiness outcome is recorded;
4. no controls were added;
5. no concept examples were added;
6. no free-text search input was added;
7. no citation, claim, interpretation, concept relation, or database record creation path was added;
8. frontend, service, and bridge files were not modified by the F16 patch; and
9. the next safe step is recorded.
'''

PATCH_README = '''# BDP-003F.16 Patch README

## Phase

BDP-003F.16 — Decide Concept Lens control and concept coverage expansion readiness after running frontend review.

## Current verified anchor expected

```text
b63e227 Review BDP-003F.15 Concept Lens running frontend posture
```

A direct clean descendant is acceptable if `main` is aligned with `origin/main` and the working tree is clean before applying this bundle.

## Scope

This is a decision-only patch bundle.

It records Outcome C:

```text
Ready for both separate later contract tracks, but implementation remains blocked.
```

## Files delivered

```text
docs/BDP_003F16_CONCEPT_LENS_EXPANSION_READINESS_DECISION.md
scripts/update_bdp_003f16_concept_lens_expansion_readiness_decision.py
scripts/verify_bdp_003f16_concept_lens_expansion_readiness_decision.py
BDP_003F16_PATCH_README.md
```

The updater also records BDP-003F.16 in:

```text
BUCHANAN_SYSTEM_STATE.json
BUCHANAN_THREAD_HANDOVER.md
```

## Blocked in this phase

```text
no frontend changes
no new frontend controls
no new concept search box
no new concept examples
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

## Apply

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
set +e

unzip -o ~/Downloads/BDP_003F16_concept_lens_expansion_readiness_decision_PATCH_ONLY.zip
python3 scripts/update_bdp_003f16_concept_lens_expansion_readiness_decision.py
```

## Verify

```bash
python3 -m py_compile frontend/dark_precursor.py
python3 -m py_compile scripts/concept_lens_archive_evidence_posture_service.py
python3 -m py_compile scripts/concept_lens_existing_archive_evidence_readback_bridge.py
python3 scripts/verify_bdp_003f6_concept_lens_architecture.py
python3 scripts/verify_bdp_003f7_concept_lens_archive_evidence_posture_service_contract.py
python3 scripts/verify_bdp_003f8_concept_lens_archive_evidence_posture_service.py
python3 scripts/verify_bdp_003f9_concept_lens_evidence_posture_output_review.py
python3 scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py
python3 scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py
python3 scripts/verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py
python3 scripts/verify_bdp_003f13_concept_lens_ui_integration_contract.py
python3 scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py
python3 scripts/verify_bdp_003f15_concept_lens_running_frontend_review.py
python3 scripts/verify_bdp_003f16_concept_lens_expansion_readiness_decision.py
git diff --check
```

## Commit only after successful verification

```bash
git status -sb
git diff -- docs/BDP_003F16_CONCEPT_LENS_EXPANSION_READINESS_DECISION.md \
  scripts/update_bdp_003f16_concept_lens_expansion_readiness_decision.py \
  scripts/verify_bdp_003f16_concept_lens_expansion_readiness_decision.py \
  BDP_003F16_PATCH_README.md \
  BUCHANAN_SYSTEM_STATE.json \
  BUCHANAN_THREAD_HANDOVER.md

git add docs/BDP_003F16_CONCEPT_LENS_EXPANSION_READINESS_DECISION.md \
  scripts/update_bdp_003f16_concept_lens_expansion_readiness_decision.py \
  scripts/verify_bdp_003f16_concept_lens_expansion_readiness_decision.py \
  BDP_003F16_PATCH_README.md \
  BUCHANAN_SYSTEM_STATE.json \
  BUCHANAN_THREAD_HANDOVER.md

git diff --cached --check
git commit -m "Decide BDP-003F.16 Concept Lens expansion readiness"
git push
```

## Next safe step

```text
BDP-003F.17 — Define Concept Lens limited control expansion contract after F16 readiness decision.
```

Then later, separately:

```text
BDP-003F.18 — Define Concept Lens controlled concept coverage expansion contract after control readiness boundary.
```
'''


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        raise FileNotFoundError(f"Missing required state file: {STATE_PATH}")
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def update_phase_notes(data: dict[str, Any], note: dict[str, Any]) -> None:
    notes = data.setdefault("recent_phase_notes", [])
    if not isinstance(notes, list):
        data["recent_phase_notes"] = []
        notes = data["recent_phase_notes"]
    notes[:] = [item for item in notes if not isinstance(item, dict) or item.get("phase") != PHASE]
    notes.append(note)


def update_state(completed_at: str) -> None:
    data = load_state()
    record = {
        "phase": PHASE,
        "title": TITLE,
        "status": "complete",
        "type": "decision_only_readiness_record",
        "controlled_slice": "decision_only_no_implementation",
        "input_phase": "BDP-003F.15 — Concept Lens running frontend review",
        "readiness_outcome": OUTCOME,
        "completed_at": completed_at,
        "decision": {
            "controls_ready_for_later_contract": True,
            "concept_coverage_ready_for_later_contract": True,
            "implementation_authorized_in_f16": False,
            "next_safe_move": "later_bounded_contract_phase_not_implementation",
        },
        "boundaries": {
            "frontend_changes": False,
            "service_changes": False,
            "bridge_changes": False,
            "new_frontend_controls": False,
            "new_concept_search_box": False,
            "new_concept_examples": False,
            "backend_route": False,
            "adapter_endpoint": False,
            "sql_mutation": False,
            "database_writes": False,
            "archive_row_creation": False,
            "citation_creation": False,
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
        "risk_record": [
            "Evidence posture display must not be mistaken for interpretive authority.",
            "Control expansion must not drift into free-text search or backend mutation.",
            "Concept coverage expansion must not create claims, citations, relations, or interpretations.",
            "Running-frontend stability is not archive mutation authorization.",
            "Rights boundaries must continue to block unrestricted passage reproduction.",
        ],
        "docs": [
            "docs/BDP_003F16_CONCEPT_LENS_EXPANSION_READINESS_DECISION.md",
            "BDP_003F16_PATCH_README.md",
        ],
        "scripts": [
            "scripts/update_bdp_003f16_concept_lens_expansion_readiness_decision.py",
            "scripts/verify_bdp_003f16_concept_lens_expansion_readiness_decision.py",
        ],
        "next_safe_step": NEXT_STEP,
        "later_separate_step": FOLLOW_ON_STEP,
    }

    data["bdp_003f16_concept_lens_expansion_readiness_decision"] = record
    phases = data.setdefault("phases", {})
    if not isinstance(phases, dict):
        data["phases"] = {}
        phases = data["phases"]
    phases[PHASE] = record

    data["last_updated_phase"] = PHASE
    data["last_updated_utc"] = completed_at
    data["current_phase"] = PHASE
    data["next_recommended_step"] = NEXT_STEP
    data["next_phase"] = "BDP-003F.17"
    data["last_completed_phase"] = PHASE

    data["bdp_003f_concept_lens_next_tracks"] = {
        "status": "contract_ready_no_implementation",
        "readiness_outcome": OUTCOME,
        "control_expansion_contract_next": NEXT_STEP,
        "concept_coverage_contract_later": FOLLOW_ON_STEP,
        "implementation_blocked_until_contracts_verified": True,
    }

    update_phase_notes(
        data,
        {
            "phase": PHASE,
            "recorded_at": completed_at,
            "summary": "Recorded Outcome C: Concept Lens is ready for separate later control and concept coverage contract tracks, while implementation remains blocked.",
        },
    )

    STATE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_handover(completed_at: str) -> None:
    if not HANDOVER_PATH.exists():
        raise FileNotFoundError(f"Missing required handover file: {HANDOVER_PATH}")
    existing = HANDOVER_PATH.read_text(encoding="utf-8")
    start = "<!-- BDP-003F.16 HANDOVER START -->"
    end = "<!-- BDP-003F.16 HANDOVER END -->"
    block = f'''{start}

## BDP-003F.16 — Concept Lens expansion readiness decision

**Status:** complete
**Completed at:** {completed_at}
**Input:** BDP-003F.15 running frontend review
**Outcome:** {OUTCOME}

### What changed

1. Added `docs/BDP_003F16_CONCEPT_LENS_EXPANSION_READINESS_DECISION.md`.
2. Added `scripts/verify_bdp_003f16_concept_lens_expansion_readiness_decision.py`.
3. Updated `BUCHANAN_SYSTEM_STATE.json` with the F16 decision record.
4. Recorded this handover block.

### Boundary preserved

1. No frontend changes were made.
2. No Concept Lens service or bridge changes were made.
3. No controls were added.
4. No concept examples were added.
5. No free-text search was added.
6. No citation, claim, interpretation, concept relation, or database record creation path was added.
7. The read-only evidence posture boundary remains intact.

### Next safe step

{NEXT_STEP}

Later, separately:

{FOLLOW_ON_STEP}

{end}
'''
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        updated = before + "\n\n" + block.rstrip() + "\n\n" + after
    else:
        updated = existing.rstrip() + "\n\n" + block.rstrip() + "\n"
    HANDOVER_PATH.write_text(updated, encoding="utf-8")


def main() -> None:
    completed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    write_text(DOC_PATH, DECISION_DOC)
    write_text(PATCH_README_PATH, PATCH_README)
    update_state(completed_at)
    update_handover(completed_at)
    print("[OK] BDP-003F.16 readiness decision recorded")
    print(f"[OK] Wrote {DOC_PATH.relative_to(ROOT)}")
    print(f"[OK] Updated {STATE_PATH.relative_to(ROOT)}")
    print(f"[OK] Updated {HANDOVER_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
