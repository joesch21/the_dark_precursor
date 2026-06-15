# BDP-003E.15 — Local Reviewed Concept Card Archive Controls UI Wiring

**Status:** Complete  
**Phase:** BDP-003E.15  
**Controlled slice:** guarded frontend wiring only  
**Implementation status:** Narrow UI wiring implemented behind safety gates.

## Purpose

BDP-003E.15 wires local reviewed concept card archive controls into The Dark Precursor UI behind safety gates.

This is the first UI wiring slice after:

1. BDP-003E.11 implemented the local reviewed archive writer.
2. BDP-003E.12 reviewed writer output against sample payloads.
3. BDP-003E.13 defined the UI integration contract.
4. BDP-003E.14 decided frontend wiring readiness.

## What Is Implemented

BDP-003E.15 adds a guarded frontend control surface that can call the local reviewed archive writer only when:

1. A locally reviewed concept card payload is present in Streamlit session state.
2. The payload matches the reviewed archive schema expected by the writer.
3. The operator provides an explicit local archive path.
4. The operator checks a confirmation box.
5. The writer safety gates accept the payload.

The UI wiring is deliberately minimal and local.

## Files

- `scripts/ui_reviewed_concept_card_archive_controls.py`
- `frontend/dark_precursor.py`
- `docs/BDP_003E15_ARCHIVE_CONTROLS_UI_WIRING.md`
- `scripts/verify_bdp_003e15_archive_controls_ui_wiring.py`

## Safety Gates

The UI control must preserve these safety gates:

1. Archive action is hidden behind an expander.
2. Archive action is disabled unless an explicit local archive path is provided.
3. Archive action is disabled unless the operator confirms local reviewed archive intent.
4. Archive action only accepts locally reviewed concept card payloads.
5. Archive action does not promote archived cards into the evidence spine.
6. Archive action does not create citations.
7. Archive action does not create concept relations.
8. Archive action does not create interpretations.
9. Archive action does not create Buchanan-specific claims.
10. Archive action does not add backend services, adapter endpoints, database tables, or SQL migrations.

## Explicit Non-Approvals

No backend services.
No adapter endpoints.
No database tables.
No SQL migrations.
No evidence promotion.
No citations.
No concept relations.
No interpretations.
No Buchanan-specific claims.
No generated card evidence promotion.

## Approved Narrow Change

Frontend wiring is approved only for local reviewed archive controls behind safety gates.

This approval does not generalize to backend persistence, database persistence, adapter endpoints, automatic archive-folder creation, or evidence promotion.

## Review Inputs

- BDP-003E.11 local reviewed concept card archive writer.
- BDP-003E.12 archive writer output sample review.
- BDP-003E.13 UI integration contract.
- BDP-003E.14 frontend wiring readiness decision.
- `scripts/local_reviewed_concept_card_archive_writer.py`
- `docs/BDP_003E14_UI_ARCHIVE_CONTROL_FRONTEND_WIRING_READINESS_DECISION.md`

## Next Step

**BDP-003E.16 — Review wired archive controls in The Dark Precursor UI against safety gates before broader archive workflow.**

## BDP-003E.16 Follow-up Safety Gate Review Note

BDP-003E.16 reviewed the wired archive controls against safety gates before any broader archive workflow.

Frontend UX/UI was changed by BDP-003E.15. BDP-003E.16 does not make additional frontend UX/UI changes and does not modify `frontend/dark_precursor.py`.

Broader archive workflow expansion remains blocked.

Next safe step: `BDP-003E.17 — Decide broader archive workflow readiness before expanding beyond local reviewed UI archive controls.`
