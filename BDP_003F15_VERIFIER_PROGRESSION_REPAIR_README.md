# BDP-003F.15 Verifier Progression Repair

This repair fixes a progression-compatibility issue found after recording BDP-003F.15.

## Problem

BDP-003F.15 correctly advances the global state to `current_phase = BDP-003F.15`, but older Concept Lens verifier scripts for BDP-003F.10 through BDP-003F.14 still cap their allowed progression at BDP-003F.14. That causes the historical verifier chain to fail even though F15 itself verifies.

The F15 handover updater also wrote two markdown lines with trailing spaces, causing `git diff --check` to fail.

## Repair boundary

This repair only updates verifier compatibility and whitespace hygiene. It does not modify frontend, service, bridge, adapter, route, SQL, database, archive, citation, claim, interpretation, or concept relation logic.

## Apply

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
. ./venv/bin/activate
python3 scripts/repair_bdp_003f15_verifier_progression_and_whitespace.py
```

Then rerun the BDP-003F.6 through BDP-003F.15 verifier chain and `git diff --check`.
