# BDP-003F.13 Patch Bundle — Concept Lens UI Integration Contract

This patch defines the contract for a later frontend display of read-only Concept Lens evidence posture.

It also makes the BDP-003F.10, BDP-003F.11, and BDP-003F.12 verifiers historical-phase safe for F13 progression so the full verification chain does not fail merely because `current_phase` advances.

## Included files

```text
docs/BDP_003F13_CONCEPT_LENS_UI_INTEGRATION_CONTRACT.md
scripts/update_bdp_003f13_concept_lens_ui_integration_contract.py
scripts/verify_bdp_003f13_concept_lens_ui_integration_contract.py
BDP_003F13_PATCH_README.md
```

The updater also rewrites these existing verifier files as progression-safe historical verifiers:

```text
scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py
scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py
scripts/verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py
```

## Boundary

This patch is contract-only.

It does not add frontend wiring, a Concept Lens UI dock implementation, Streamlit controls, backend routes, adapter endpoints, SQL migrations, database mutation, citation creation, concept mention creation, concept relation creation, interpretation insertion, evidence promotion, Buchanan-specific claims, automatic chat filtering, external LLM routing, unrestricted passage reproduction, or source ingestion.

## Apply

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
unzip -o ~/Downloads/BDP_003F13_concept_lens_ui_integration_contract_PATCH_ONLY.zip
python3 scripts/update_bdp_003f13_concept_lens_ui_integration_contract.py
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
git diff --check
```

## Inspect before commit

```bash
git status -sb
git status --short
git diff --name-only
git diff --stat
grep -RIn "BDP-003F.13\|Archive evidence posture\|read_concept_lens_archive_evidence_posture_via_existing_archive_bridge\|BDP-003F.14"   BUCHANAN_SYSTEM_STATE.json   BUCHANAN_THREAD_HANDOVER.md   docs/BDP_003F13_CONCEPT_LENS_UI_INTEGRATION_CONTRACT.md   BDP_003F13_PATCH_README.md   scripts/verify_bdp_003f13_concept_lens_ui_integration_contract.py   | sed -n '1,240p'
```

Expected changed or added files:

```text
BUCHANAN_SYSTEM_STATE.json
BUCHANAN_THREAD_HANDOVER.md
BDP_003F13_PATCH_README.md
docs/BDP_003F13_CONCEPT_LENS_UI_INTEGRATION_CONTRACT.md
scripts/update_bdp_003f13_concept_lens_ui_integration_contract.py
scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py
scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py
scripts/verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py
scripts/verify_bdp_003f13_concept_lens_ui_integration_contract.py
```

## Commit

```bash
git add .
git commit -m "Define BDP-003F.13 Concept Lens UI integration contract"
git push
```

## Next safe step

```text
BDP-003F.14 — Wire the approved Concept Lens read-only evidence posture display into the frontend after contract verification.
```

Still no UI wiring until the F13 contract is verified and committed.
