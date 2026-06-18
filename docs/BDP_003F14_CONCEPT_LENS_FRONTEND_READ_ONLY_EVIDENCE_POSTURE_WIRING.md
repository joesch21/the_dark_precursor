# BDP-003F.14 — Concept Lens Frontend Read-only Evidence Posture Wiring

**Status:** Complete after verifier pass  
**Controlled slice:** Frontend read-only evidence posture display only  
**Frontend target:** `frontend/dark_precursor.py`  
**Service handoff:** `read_concept_lens_archive_evidence_posture_via_existing_archive_bridge`  
**Database mutation:** No  
**SQL migration:** No  
**Evidence promotion:** No  
**Buchanan-specific claim generation:** No

## Purpose

BDP-003F.14 wires the approved BDP-003F.13 Concept Lens UI integration contract into The Dark Precursor frontend as a conservative read-only evidence posture display.

The frontend panel answers only this bounded question:

```text
For this controlled concept example, what does the existing archive bridge and Concept Lens evidence posture service currently report?
```

It does not convert the display into an evidence source, a claim engine, a search system, a database writer, or a Buchanan-specific interpretation layer.

## Contract source

This phase follows the BDP-003F.13 UI integration contract.

Approved source of display data:

```text
scripts/concept_lens_archive_evidence_posture_service.py
scripts/concept_lens_existing_archive_evidence_readback_bridge.py
```

Required service handoff:

```text
read_concept_lens_archive_evidence_posture_via_existing_archive_bridge
```

Preserved archive chain:

```text
concepts -> concept_mentions -> passages -> citations -> sources
```

## Implemented frontend surface

BDP-003F.14 adds a controlled, read-only Concept Lens evidence posture dock inside the existing cinematic frontend.

The surface displays:

1. the controlled requested concept label;
2. the normalized concept label when the service returns one;
3. `archive_lookup_status`;
4. `evidence_posture`;
5. chain completeness / chain summary;
6. rights-safe source metadata when present;
7. rights-safe locator metadata when present;
8. passage display status, conservatively defaulting to `omitted_by_rights_policy`;
9. the service handoff name;
10. an explicit read-only boundary note.

## Controlled smoke examples only

The first frontend implementation does not add a free-text concept search box.

It exposes only the controlled examples already approved for smoke review:

```text
Body without Organs
we repress because we repeat
assemblage
```

Expected posture rules remain:

1. `Body without Organs` may display archive-grounded only if the bridge/service path returns a complete rights-aware row.
2. `we repress because we repeat` remains exploratory / unverified unless an approved archive row exists.
3. `assemblage` must not be marked archive-grounded merely because it is philosophically important.

## Required user-facing boundary note

The frontend includes the boundary note:

```text
This panel displays read-only archive evidence posture. It does not create citations, claims, interpretations, concept relations, or database records.
```

## Approved labels

The frontend uses the approved vocabulary:

```text
Concept Lens
Evidence posture
Archive evidence posture
Archive-grounded match
Source-bound description
Exploratory / unverified
No archive match
Rights-limited display
Read-only archive evidence posture
```

## Blocked paths

BDP-003F.14 does not add:

1. SQL mutation;
2. database writes;
3. archive row creation;
4. citation creation;
5. concept mention creation;
6. concept relation creation;
7. interpretation insertion;
8. evidence promotion;
9. external LLM routing;
10. free-text concept search input;
11. source ingestion;
12. unrestricted passage reproduction;
13. Buchanan-specific interpretive claim generation;
14. backend routes or adapter endpoints;
15. general chat filtering.

## Files changed by this phase

```text
frontend/dark_precursor.py
docs/BDP_003F14_CONCEPT_LENS_FRONTEND_READ_ONLY_EVIDENCE_POSTURE_WIRING.md
scripts/update_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py
scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py
BDP_003F14_PATCH_README.md
BUCHANAN_SYSTEM_STATE.json
BUCHANAN_THREAD_HANDOVER.md
```

## Verification

Run the full F14 chain:

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
git diff --check
```

## Next safe step

```text
BDP-003F.15 — Review the Concept Lens read-only evidence posture display in the running frontend before expanding controls or concept coverage.
```


## Verifier progression repair note

A narrow post-wiring verifier repair updates the historical BDP-003F.10, BDP-003F.11, BDP-003F.12, and BDP-003F.13 verifiers so they remain valid after global state advances to `BDP-003F.14`.

This repair changes verifier progression allowances only. It does not alter frontend behavior or expand Concept Lens functionality.


## Verifier progression repair V2 note

A second narrow verifier repair updates historical F10-F13 progression checks after F14 state advancement. The repair directly edits the named allowlist blocks rather than relying on a broad file-level string check.

This changes verifier progression only. It does not alter frontend behavior or expand Concept Lens functionality.
