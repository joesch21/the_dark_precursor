# BDP-003F.16 — F15 Global Next-Step Loop Repair

This patch repairs the BDP-003F.15 verifier so it remains valid after BDP-003F.16 advances global next-step fields to the F17 contract phase.

## Boundary

This repair only modifies verifier logic. It does not modify:

- `frontend/dark_precursor.py`
- `scripts/concept_lens_archive_evidence_posture_service.py`
- `scripts/concept_lens_existing_archive_evidence_readback_bridge.py`
- database/schema/SQL files
- Concept Lens runtime functionality

## Apply

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
set +e

unzip -o ~/Downloads/BDP_003F16_F15_GLOBAL_NEXT_STEP_LOOP_REPAIR_PATCH_ONLY.zip
python3 scripts/repair_bdp_003f16_f15_global_next_step_loop.py
python3 scripts/verify_bdp_003f16_f15_global_next_step_loop_repair.py
```
