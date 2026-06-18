# BDP-003F.11 Patch Bundle — Concept Lens Existing Archive Readback Bridge Implementation

This patch implements the approved BDP-003F.10 read-only bridge from existing governed archive evidence readback into the BDP-003F.8 Concept Lens archive evidence posture service.

## Dependency

Apply and verify BDP-003F.10 first.

BDP-003F.11 will stop if the F10 contract document and F10 state record are missing.

## Included files

```text
docs/BDP_003F11_CONCEPT_LENS_EXISTING_ARCHIVE_READBACK_BRIDGE_IMPLEMENTATION.md
scripts/concept_lens_existing_archive_evidence_readback_bridge.py
scripts/update_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py
scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py
BDP_003F11_PATCH_README.md
```

The update script also appends a guarded BDP-003F.11 wrapper to:

```text
scripts/concept_lens_archive_evidence_posture_service.py
```

Wrapper:

```text
read_concept_lens_archive_evidence_posture_via_existing_archive_bridge
```

## Boundary

This patch implements only the read-only bridge and service wrapper.

It does not add:

```text
frontend wiring
Concept Lens UI dock
Streamlit controls
new navigation surface keys
backend route
adapter endpoint
SQL migration
database table
database mutation
source ingestion
citation creation
concept mention creation
concept relation creation
interpretation insertion
evidence promotion
Buchanan-specific claims
automatic chat filtering
external LLM routing
philosophical fidelity review
```

## Apply

Run from the repository root:

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
unzip -o ~/Downloads/BDP_003F11_concept_lens_existing_archive_readback_bridge_implementation_PATCH_ONLY.zip
python3 scripts/update_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py
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
git diff --check
```

## Optional bridge smoke test

```bash
python3 scripts/concept_lens_existing_archive_evidence_readback_bridge.py "Body without Organs" --allow-empty
```

This may return an empty row list if the local readback scripts cannot run in the current environment. Empty rows are a safe failure posture, not evidence fabrication.

## Inspect before commit

```bash
git status -sb
git status --short
git diff --name-only
git diff --stat
grep -RIn "BDP-003F.11\|read_existing_archive_evidence_rows_for_concept\|read_concept_lens_archive_evidence_posture_via_existing_archive_bridge\|UI integration remains blocked" \
  docs/BDP_003F11_CONCEPT_LENS_EXISTING_ARCHIVE_READBACK_BRIDGE_IMPLEMENTATION.md \
  scripts/concept_lens_existing_archive_evidence_readback_bridge.py \
  scripts/concept_lens_archive_evidence_posture_service.py \
  BUCHANAN_THREAD_HANDOVER.md \
  BUCHANAN_SYSTEM_STATE.json \
  BDP_003F11_PATCH_README.md \
  | sed -n '1,260p'
```

Expected changed or added files after running the updater:

```text
BUCHANAN_SYSTEM_STATE.json
BUCHANAN_THREAD_HANDOVER.md
BDP_003F11_PATCH_README.md
docs/BDP_003F11_CONCEPT_LENS_EXISTING_ARCHIVE_READBACK_BRIDGE_IMPLEMENTATION.md
scripts/concept_lens_existing_archive_evidence_readback_bridge.py
scripts/concept_lens_archive_evidence_posture_service.py
scripts/update_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py
scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py
```

## Commit

```bash
git add .
git commit -m "Implement BDP-003F.11 Concept Lens read-only bridge"
git push
```

## Next safe step

```text
BDP-003F.12 — Review live Body without Organs bridge output against the Concept Lens service before UI integration.
```

Still no UI wiring.
