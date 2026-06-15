# BDP-003E.14 — UI Archive Control Frontend Wiring Readiness Decision

**Status:** Complete  
**Phase:** BDP-003E.14  
**Controlled slice:** readiness decision only  
**Decision type:** UI archive control frontend wiring readiness decision  
**Implementation status:** Frontend wiring is not approved by this phase.

## Purpose

BDP-003E.14 decides whether the local reviewed concept card archive controls are ready to move into a later explicitly approved frontend wiring phase.

This phase follows:

1. BDP-003E.11 — local reviewed archive writer implemented behind safety gates.
2. BDP-003E.12 — writer output reviewed against sample payloads.
3. BDP-003E.13 — UI integration contract defined before frontend wiring.

## Decision

The UI archive control frontend wiring is ready for a later explicitly approved wiring phase, but frontend wiring is not approved by BDP-003E.14.

This is a readiness decision only.

## Approval Boundary

BDP-003E.14 approves readiness to consider a later frontend wiring phase.

BDP-003E.14 does not approve frontend wiring.

## Explicit Non-Approvals

No frontend wiring.
No frontend archive controls.
No archive buttons.
No Streamlit writer call.
No backend services.
No adapter endpoints.
No database tables.
No SQL migrations.
No archive folders created by default.
No evidence promotion.
No citations.
No concept relations.
No interpretations.
No Buchanan-specific claims.

## Required Safety Conditions for a Later Wiring Phase

A later frontend wiring phase must preserve the following conditions:

1. The UI may only expose archive controls for locally reviewed concept card payloads.
2. The UI must not archive unreviewed generated drafts.
3. The UI must not promote archived cards into the evidence spine.
4. The UI must not create citations, concept relations, interpretations, or Buchanan-specific claims.
5. The UI must keep archive writing visibly separate from Buchanan evidence claims.
6. The UI must present archive action as a local reviewed storage action, not as scholarly validation.
7. The UI must surface rejection/failure states clearly if the payload fails writer safety gates.
8. The UI wiring must remain separate from backend services, adapter endpoints, and database migrations unless later approved.

## Review Inputs

- BDP-003E.11 local reviewed concept card archive writer implementation.
- BDP-003E.12 archive writer output sample review.
- BDP-003E.13 UI integration contract for archive controls.
- `scripts/local_reviewed_concept_card_archive_writer.py`
- `docs/BDP_003E11_LOCAL_REVIEWED_CONCEPT_CARD_ARCHIVE_WRITER_IMPLEMENTATION.md`
- `docs/BDP_003E12_ARCHIVE_WRITER_OUTPUT_SAMPLE_REVIEW.md`
- `docs/BDP_003E13_UI_INTEGRATION_CONTRACT_FOR_ARCHIVE_CONTROLS.md`

## Frontend Wiring Readiness

The frontend wiring is ready to be considered in a later implementation phase because:

1. A local writer exists and is verified behind safety gates.
2. Writer output has been reviewed against sample payloads.
3. A UI integration contract exists.
4. The governance boundary is explicit.
5. Evidence promotion remains blocked.

## Still Blocked

The following remain blocked until a later explicitly approved phase:

1. Editing `frontend/dark_precursor.py`.
2. Adding archive buttons.
3. Calling the writer from Streamlit.
4. Creating archive folders by default from UI actions.
5. Adding backend services.
6. Adding adapter endpoints.
7. Adding database tables or migrations.
8. Promoting generated concept cards into evidence.

## Next Step

**BDP-003E.15 — Wire local reviewed concept card archive controls into The Dark Precursor UI behind safety gates.**

## BDP-003E.15 Follow-up UI Wiring Note

BDP-003E.15 wires local reviewed concept card archive controls into The Dark Precursor UI behind safety gates.

This follow-up does not add backend services, adapter endpoints, database tables, SQL migrations, evidence promotion, citations, concept relations, interpretations, or Buchanan-specific claims.
