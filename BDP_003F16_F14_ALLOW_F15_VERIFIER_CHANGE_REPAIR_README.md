# BDP-003F.16 — F14 Allow F15 Verifier Change Repair

This is a narrow verifier-boundary repair.

It updates the BDP-003F.14 verifier allow-list so the verifier does not reject the intentional BDP-003F.16 repair to:

```text
scripts/verify_bdp_003f15_concept_lens_running_frontend_review.py
```

No frontend, Concept Lens service, Concept Lens bridge, database, citation, claim, concept relation, or interpretation behavior is changed.

Apply:

```bash
unzip -o ~/Downloads/BDP_003F16_F14_ALLOW_F15_VERIFIER_CHANGE_REPAIR_PATCH_ONLY.zip
python3 scripts/repair_bdp_003f16_f14_allow_f15_verifier_change.py
python3 scripts/verify_bdp_003f16_f14_allow_f15_verifier_change_repair.py
```
