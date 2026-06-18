# BDP-003F.16 Verifier Progression Repair README

## Purpose

This repair is for the verifier progression failure observed after applying BDP-003F.16.

BDP-003F.16 itself verifies successfully, but older Concept Lens verifiers still contain hard-coded phase progression windows that stop at BDP-003F.14 or BDP-003F.15. Once `BUCHANAN_SYSTEM_STATE.json` records `current_phase` / `last_updated_phase` as `BDP-003F.16`, those earlier verifiers reject the valid later state.

This is a verifier progression repair only.

## What this repair changes

The repair updater widens completed Concept Lens verifier guards so F10-F15 checks tolerate a clean F16 descendant state.

Expected touched files:

```text
scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py
scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py
scripts/verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py
scripts/verify_bdp_003f13_concept_lens_ui_integration_contract.py
scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py
scripts/verify_bdp_003f15_concept_lens_running_frontend_review.py
```

The repair does not modify:

```text
frontend/dark_precursor.py
scripts/concept_lens_archive_evidence_posture_service.py
scripts/concept_lens_existing_archive_evidence_readback_bridge.py
```

## Apply

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
set +e

unzip -o ~/Downloads/BDP_003F16_VERIFIER_PROGRESSION_REPAIR_PATCH_ONLY.zip
python3 scripts/repair_bdp_003f16_verifier_progression.py
python3 scripts/verify_bdp_003f16_verifier_progression_repair.py
```

## Verify full chain

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
python3 scripts/verify_bdp_003f16_verifier_progression_repair.py
git diff --check
```

## Commit only after successful verification

```bash
git status -sb
git diff --stat

git add scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py \
  scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py \
  scripts/verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py \
  scripts/verify_bdp_003f13_concept_lens_ui_integration_contract.py \
  scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py \
  scripts/verify_bdp_003f15_concept_lens_running_frontend_review.py \
  scripts/repair_bdp_003f16_verifier_progression.py \
  scripts/verify_bdp_003f16_verifier_progression_repair.py \
  BDP_003F16_VERIFIER_PROGRESSION_REPAIR_README.md

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
