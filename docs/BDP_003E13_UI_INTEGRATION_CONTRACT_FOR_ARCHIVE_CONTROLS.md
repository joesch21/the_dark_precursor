# BDP-003E.13 — UI Integration Contract for Local Reviewed Concept Card Archive Controls

**Status:** Complete
**Phase:** BDP-003E.13
**Controlled slice:** UI integration contract only

## Decision

BDP-003E.13 defines a UI integration contract only for future local reviewed concept card archive controls.

The contract may be used in a later phase to wire frontend controls to the existing local reviewed concept card archive writer, but BDP-003E.13 does not wire the frontend, does not add archive buttons, does not call the writer from the UI, and does not create any new runtime control surface.

Implementation is not approved beyond the already-complete local writer from BDP-003E.11.

## Review Inputs

This contract is based on:

1. BDP-003E.5 local reviewed archive schema candidate.
2. BDP-003E.6 archive schema sample review.
3. BDP-003E.7 local reviewed concept card archive writer contract.
4. BDP-003E.8 archive writer contract boundary review.
5. BDP-003E.9 implementation readiness decision.
6. BDP-003E.10 implementation boundary and safety gates.
7. BDP-003E.11 local reviewed archive writer implementation.
8. BDP-003E.12 archive writer output sample review.

## Contract Purpose

The future UI control must support a deliberate operator action to archive a locally reviewed cinematic concept card.

The control must not convert generated cards into evidence. It must not produce Buchanan-specific claims. It must not create citations, concept relations, interpretations, database records, adapter calls, backend service calls, or automatic side effects.

The UI contract exists to define the shape of a later frontend integration before any frontend code is changed.

## Contract Boundary

BDP-003E.13 is a contract-only phase.

No frontend wiring.
No archive control implementation.
No Streamlit button implementation.
No automatic archive action.
No backend services.
No adapter endpoints.
No database tables.
No SQL migrations.
No evidence promotion.
No citations.
No concept relations.
No interpretations.
No Buchanan-specific claims.

## Future UI Control Contract

A later approved frontend wiring phase may expose a local archive control only if it satisfies all of the following requirements.

### 1. Operator-controlled action only

The archive action must be triggered by an explicit operator action.

The UI must not archive on generation, page load, session reset, card preview, export preview, or sample review.

### 2. Reviewed payload only

The UI must pass only a locally reviewed concept card payload that matches the BDP-003E.5 archive schema candidate and has passed the E11/E12 writer-output expectations.

The UI must reject or disable archive action for:

1. unreviewed generated drafts,
2. malformed payloads,
3. partial concept cards,
4. missing review metadata,
5. payloads that attempt to add evidence or citations.

### 3. Preview before write

The UI should expose a preview/readback of the archive payload before the operator commits the local archive write.

The preview must make clear that the archive is a local reviewed-card archive only, not evidence insertion.

### 4. Local writer boundary

The UI may call only the local writer from `scripts/local_reviewed_concept_card_archive_writer.py` in a later approved phase.

It must not call a backend route, adapter endpoint, database service, evidence ingestion function, citation service, relation service, or interpretation writer.

### 5. Output readback

After a later approved archive write, the UI should report:

1. archive write status,
2. output file path or relative archive location,
3. reviewed concept card identifier,
4. timestamp or metadata preserved from the reviewed payload,
5. warning that the archived card is not evidence.

### 6. No hidden persistence

The UI must not create hidden files, hidden archive folders, background writes, session-state persistence, database rows, or adapter calls.

Any later archive path must be explicitly approved in a later phase before frontend wiring.

## Safety Gates for Later UI Wiring

A later frontend wiring phase must verify:

1. the E11 local writer still passes,
2. the E12 output sample review still passes,
3. the UI only enables archive controls for reviewed payloads,
4. the UI displays a pre-write review boundary,
5. the UI displays a post-write local archive readback,
6. the UI does not promote archive output into evidence,
7. the UI does not create Buchanan-specific claims,
8. the UI does not introduce backend, adapter, or database persistence.

## Required UI Language

Any later UI archive control should use language that preserves the governance boundary:

- `Archive reviewed local concept card`
- `Local archive only — not evidence`
- `Review payload before local write`
- `Archived card remains separate from citations, relations, interpretations, and Buchanan claims`

The UI must avoid language such as:

- `Save as evidence`
- `Commit to Buchanan archive`
- `Create citation`
- `Add interpretation`
- `Publish claim`

## Decision Outcome

The UI integration contract is suitable for a future frontend-wiring readiness phase.

BDP-003E.13 does not approve frontend wiring. It only defines the future UI integration contract for local reviewed concept card archive controls.

## Next Step

**BDP-003E.14 — Decide UI archive control frontend wiring readiness, without wiring frontend.**

## BDP-003E.14 Follow-up Frontend Wiring Readiness Note

BDP-003E.14 reviewed the BDP-003E.13 UI integration contract and decided that UI archive control frontend wiring is ready for a later explicitly approved wiring phase.

Frontend wiring is not approved by BDP-003E.14. This follow-up does not add frontend archive controls, archive buttons, Streamlit writer calls, backend services, adapter endpoints, database tables, SQL migrations, archive folders created by default, evidence promotion, citations, concept relations, interpretations, or Buchanan-specific claims.

Next safe step: `BDP-003E.15 — Wire local reviewed concept card archive controls into The Dark Precursor UI behind safety gates.`

## BDP-003E.14/E15 Verifier Phrase Repair Note

frontend wiring is not approved by BDP-003E.13. The UI integration contract remains a contract-only phase; later wiring requires explicit approval and must preserve the archive safety gates.

## BDP-003E.15 Exact Boundary Phrase Repair

No frontend archive controls are approved by BDP-003E.13. The phase remains a UI integration contract only; frontend wiring requires later explicit approval.

