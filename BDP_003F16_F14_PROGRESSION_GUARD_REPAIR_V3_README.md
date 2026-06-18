# BDP-003F.16 — F14 Progression Guard Repair V3

This is a verifier-only repair for the BDP-003F.14 verifier after BDP-003F.16.

## Problem

BDP-003F.16 correctly records the Concept Lens expansion readiness decision and recommends:

```text
BDP-003F.17 — Define Concept Lens limited control expansion contract after F16 readiness decision.
```

The F14 verifier still contained a historical progression guard that allowed F14/F15 state and F15/F16 next-step descendants, but did not allow F16 `last_updated_phase` or the F17 next safe step produced by the F16 decision.

## Boundary

This repair only modifies:

```text
scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py
```

It does not modify:

```text
frontend/dark_precursor.py
scripts/concept_lens_archive_evidence_posture_service.py
scripts/concept_lens_existing_archive_evidence_readback_bridge.py
```

## Apply

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
set +e

unzip -o ~/Downloads/BDP_003F16_F14_PROGRESSION_GUARD_REPAIR_V3_PATCH_ONLY.zip
python3 scripts/repair_bdp_003f16_f14_progression_guard_v3.py
python3 scripts/verify_bdp_003f16_f14_progression_guard_repair_v3.py
python3 scripts/verify_bdp_003f16_verifier_progression_repair.py
```

Then rerun the full BDP-003F.6–F16 verifier chain.
