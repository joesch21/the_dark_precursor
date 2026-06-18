# BDP-003F.16 Patch README

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
git diff -- docs/BDP_003F16_CONCEPT_LENS_EXPANSION_READINESS_DECISION.md   scripts/update_bdp_003f16_concept_lens_expansion_readiness_decision.py   scripts/verify_bdp_003f16_concept_lens_expansion_readiness_decision.py   BDP_003F16_PATCH_README.md   BUCHANAN_SYSTEM_STATE.json   BUCHANAN_THREAD_HANDOVER.md

git add docs/BDP_003F16_CONCEPT_LENS_EXPANSION_READINESS_DECISION.md   scripts/update_bdp_003f16_concept_lens_expansion_readiness_decision.py   scripts/verify_bdp_003f16_concept_lens_expansion_readiness_decision.py   BDP_003F16_PATCH_README.md   BUCHANAN_SYSTEM_STATE.json   BUCHANAN_THREAD_HANDOVER.md

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
