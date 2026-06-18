# BDP-003F.12 — Concept Lens Bridge Output Smoke Review Before UI Integration

**Status:** Complete
**Controlled slice:** read-only bridge output smoke review only
**Authority:** Review gate / no frontend wiring
**Frontend implementation:** No
**Backend route implementation:** No
**Database mutation:** No
**SQL migration:** No

## Purpose

BDP-003F.12 reviews the output posture of the BDP-003F.11 Concept Lens existing archive readback bridge before any Concept Lens UI integration.

The narrow question is:

```text
Can the bridge safely provide read-only archive evidence rows to the F8 Concept Lens evidence posture service without creating new evidence, claims, UI surfaces, routes, or database changes?
```

## Review finding

The BDP-003F.11 bridge is the correct next layer after BDP-003F.10 because it exposes an approved read-only path from existing archive evidence readback into the Concept Lens evidence posture service.

However, BDP-003F.12 does not approve UI wiring.

The safe posture is:

```text
The bridge may be used for read-only local smoke review. The Concept Lens UI remains blocked until the output shape is reviewed and a separate UI contract or wiring phase is approved.
```

## Required smoke cases

The bridge output review must include these cases before UI wiring:

1. `Body without Organs`
2. `we repress because we repeat`
3. `assemblage`

## Expected posture logic

### Body without Organs

When a valid live archive path exposes the governed evidence chain, Body without Organs may truthfully be classified as archive-grounded through the existing chain:

```text
concepts -> concept_mentions -> passages -> citations -> sources
```

If no live archive is configured, the service must not fabricate grounding. It must continue to report a conservative non-live/no-match posture.

### we repress because we repeat

This phrase should not be promoted into archive-grounded evidence unless the bridge returns an approved existing archive row with the required chain.

### assemblage

This concept should not be marked archive-grounded merely because it is philosophically important. It requires existing read-only archive evidence rows.

## What this phase approves

BDP-003F.12 approves only:

1. read-only bridge output smoke review;
2. checking whether F11 can feed safe rows into F8;
3. confirming no fabricated archive grounding occurs when no rows are available;
4. preserving the rights-aware evidence posture boundary;
5. keeping UI integration blocked.

## What this phase blocks

BDP-003F.12 blocks:

1. Concept Lens UI dock;
2. Streamlit controls;
3. frontend wiring;
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
15. external LLM routing.

## Manual smoke commands

Run from the repository root after applying this review patch:

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
git diff --check
```

Optional local output checks may be run against the available local archive configuration, but BDP-003F.12 does not require or create database state.

## UI decision

UI integration remains blocked.

The bridge is not a user-facing Concept Lens dock. It is a read-only evidence row supply layer for later rendering.

## Next safe step

```text
BDP-003F.13 — Define Concept Lens UI integration contract for read-only evidence posture display before frontend wiring.
```

## Explicit UI boundary

BDP-003F.12 is a smoke-output review only. It adds no Concept Lens UI dock, no frontend wiring, no Streamlit controls, no backend route, no adapter endpoint, no SQL migration, no database mutation, no evidence promotion, and no Buchanan-specific claims.
