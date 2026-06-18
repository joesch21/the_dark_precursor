# BDP-003F.13 — Concept Lens UI Integration Contract for Read-only Evidence Posture Display

**Status:** Complete
**Controlled slice:** UI integration contract only
**Authority:** Contract definition before frontend wiring
**Frontend implementation:** No
**Streamlit wiring:** No
**Backend route implementation:** No
**Database mutation:** No
**SQL migration:** No

## Purpose

BDP-003F.13 defines the approved UI integration contract for displaying Concept Lens read-only evidence posture in the Dark Precursor frontend.

This phase answers one narrow question:

```text
How may the frontend display read-only Concept Lens archive evidence posture without turning that display into a new evidence source, claim engine, database writer, or Buchanan-specific interpretation layer?
```

BDP-003F.13 does not wire the UI. It defines the display contract that a later frontend phase must obey.

## Prior chain

The contract sits after this verified chain:

```text
BDP-003F.6  — Concept Lens architecture
BDP-003F.7  — archive evidence posture service contract
BDP-003F.8  — archive evidence posture service
BDP-003F.9  — evidence posture output review
BDP-003F.10 — read-only bridge contract
BDP-003F.11 — existing archive readback bridge implementation
BDP-003F.12 — bridge output smoke review
```

The read-only evidence posture path remains:

```text
existing archive readback bridge -> Concept Lens evidence posture service -> rights-aware display model
```

The preserved archive chain remains:

```text
concepts -> concept_mentions -> passages -> citations -> sources
```

## Approved UI display model

A later frontend phase may display only a read-only evidence posture panel or dock using values already returned by the Concept Lens evidence posture service and approved bridge.

The UI display model may show:

1. requested concept label;
2. normalized concept label when available;
3. `archive_lookup_status`;
4. `evidence_posture`;
5. chain completeness summary;
6. source metadata already allowed for display;
7. rights-safe locator metadata;
8. rights-safe passage display status such as `omitted_by_rights_policy`;
9. conservative no-match or exploratory status when no archive row exists;
10. a clear boundary note that the display is read-only archive posture, not interpretation.

## Approved user-facing labels

The frontend must avoid presenting evidence posture as philosophical truth or as a Buchanan claim.

Approved label language:

```text
Archive evidence posture
Archive-grounded match
Source-bound description
Exploratory / unverified
No archive match
Rights-limited display
Read-only archive evidence
```

Blocked label language:

```text
Buchanan says
Deleuze means
definitive interpretation
validated philosophical truth
automatic concept proof
```

## Required display states

The future UI must support these states without fabricating evidence:

### archive_grounded

Display as archive-grounded only when the service returns a complete reviewed chain through:

```text
concepts -> concept_mentions -> passages -> citations -> sources
```

### source_bound_description

Display as source-bound only when the service has enough rights-safe source metadata to support a source-bound description but not a full archive-grounded posture.

### exploratory_unverified

Display as exploratory / unverified when no approved archive evidence row exists, when the bridge returns no rows, or when chain completeness is not established.

### rights_limited

Display passage text as omitted whenever rights policy requires omission.

Required omission phrase:

```text
omitted_by_rights_policy
```

## Approved first UI smoke cases

The future frontend wiring phase must inspect the display contract against these cases before committing UI expansion:

```text
Body without Organs
we repress because we repeat
assemblage
```

Expected posture rules:

1. `Body without Organs` may display archive-grounded only if the bridge/service path returns a complete rights-aware row.
2. `we repress because we repeat` must remain exploratory / unverified unless an approved archive row exists.
3. `assemblage` must not be marked archive-grounded merely because it is philosophically important.

## Required future UI boundary note

A later UI implementation should include a short boundary note equivalent to:

```text
This panel displays read-only archive evidence posture. It does not create citations, claims, interpretations, concept relations, or database records.
```

## What this phase approves

BDP-003F.13 approves only:

1. the UI integration contract;
2. the read-only display model;
3. rights-aware evidence posture labels;
4. first UI smoke cases;
5. frontend implementation boundaries for a later phase.

## What this phase blocks

BDP-003F.13 blocks:

1. frontend wiring;
2. Concept Lens UI dock implementation;
3. Streamlit controls;
4. backend routes;
5. adapter endpoints;
6. SQL migrations;
7. database mutation;
8. citation creation;
9. concept mention creation;
10. concept relation creation;
11. interpretation insertion;
12. evidence promotion;
13. Buchanan-specific claims;
14. automatic chat filtering;
15. external LLM routing;
16. unrestricted passage reproduction;
17. free-text concept search input;
18. source ingestion.

## Implementation constraints for the next phase

A later frontend phase must not bypass the service layer.

Allowed source of display data:

```text
scripts/concept_lens_archive_evidence_posture_service.py
scripts/concept_lens_existing_archive_evidence_readback_bridge.py
```

Required service handoff boundary:

```text
read_concept_lens_archive_evidence_posture_via_existing_archive_bridge
```

The UI must treat the service result as display data only.

## Verification boundary

BDP-003F.13 is contract-only.

It does not change:

```text
frontend/dark_precursor.py
frontend styles
navigation state
runtime routes
database files
SQL files
archive rows
```

## Next safe step

```text
BDP-003F.14 — Wire the approved Concept Lens read-only evidence posture display into the frontend after contract verification.
```

## Verifier literal boundary

Frontend implementation: No


## Verifier literal boundary phrases

Streamlit wiring: No
Database mutation: No
SQL migration: No
