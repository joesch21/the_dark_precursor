# BDP-003F.15 Verifier Progression Repair V2 Patch

This is a patch-only repair bundle for a second narrow verifier progression issue.

## Apply

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
. ./venv/bin/activate

unzip -o ~/Downloads/BDP_003F15_verifier_progression_repair_V2_PATCH_ONLY.zip
python3 scripts/repair_bdp_003f15_verifier_progression_v2.py
```

## Then rerun

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
git diff --check
```

## Do not commit until all checks pass.
