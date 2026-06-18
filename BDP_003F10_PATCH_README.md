# BDP-003F.10 Patch Bundle — Concept Lens Read-only Bridge Contract

This patch defines the approved read-only bridge contract from existing archive evidence readback into the BDP-003F.8 Concept Lens archive evidence posture service.

## Decision

BDP-003F.10 approves a future implementation boundary for:

```text
concept_lens_existing_archive_evidence_readback_bridge.v1
```

It does not implement the bridge.

## Included files

```text
docs/BDP_003F10_CONCEPT_LENS_READ_ONLY_BRIDGE_CONTRACT.md
scripts/update_bdp_003f10_concept_lens_read_only_bridge_contract.py
scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py
BDP_003F10_PATCH_README.md
```

## Boundary

This patch is contract-only.

It does not modify:

```text
frontend/dark_precursor.py
frontend/styles/dark_precursor.css
scripts/concept_lens_archive_evidence_posture_service.py
database files
SQL migrations
backend routes
adapter endpoints
```

It does not create citations, concept mentions, concept relations, interpretations, evidence promotion, Buchanan-specific claims, automatic chat filtering, external LLM routing, or a Concept Lens UI dock.

## Apply

Run from the repository root:

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
unzip -o ~/Downloads/BDP_003F10_concept_lens_read_only_bridge_contract_PATCH_ONLY.zip
python3 scripts/update_bdp_003f10_concept_lens_read_only_bridge_contract.py
```

The updater modifies the current local `BUCHANAN_SYSTEM_STATE.json` and `BUCHANAN_THREAD_HANDOVER.md` in place. This avoids replacing those files with a stale generated copy.

## Verify

```bash
python3 -m py_compile frontend/dark_precursor.py
python3 -m py_compile scripts/concept_lens_archive_evidence_posture_service.py
python3 scripts/verify_bdp_003f6_concept_lens_architecture.py
python3 scripts/verify_bdp_003f7_concept_lens_archive_evidence_posture_service_contract.py
python3 scripts/verify_bdp_003f8_concept_lens_archive_evidence_posture_service.py
python3 scripts/verify_bdp_003f9_concept_lens_evidence_posture_output_review.py
python3 scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py
git diff --check
```

## Inspect before commit

```bash
git status -sb
git status --short
git diff --name-only
git diff --stat
grep -RIn "BDP-003F.10\|concept_lens_existing_archive_evidence_readback_bridge.v1\|UI integration remains blocked" \
  docs/BDP_003F10_CONCEPT_LENS_READ_ONLY_BRIDGE_CONTRACT.md \
  BUCHANAN_THREAD_HANDOVER.md \
  BUCHANAN_SYSTEM_STATE.json \
  BDP_003F10_PATCH_README.md \
  | sed -n '1,220p'
```

Expected changed or added files:

```text
BUCHANAN_SYSTEM_STATE.json
BUCHANAN_THREAD_HANDOVER.md
BDP_003F10_PATCH_README.md
docs/BDP_003F10_CONCEPT_LENS_READ_ONLY_BRIDGE_CONTRACT.md
scripts/update_bdp_003f10_concept_lens_read_only_bridge_contract.py
scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py
```

## Commit

```bash
git add .
git commit -m "Define BDP-003F.10 Concept Lens read-only bridge contract"
git push
```

## Next safe step

```text
BDP-003F.11 — Implement the approved read-only bridge from existing archive evidence readback into the Concept Lens service.
```

Still no UI wiring.
