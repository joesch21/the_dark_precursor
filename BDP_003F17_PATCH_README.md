# BDP-003F.17 Patch README

## Phase

```text
BDP-003F.17 — Define Concept Lens limited control expansion contract after F16 readiness decision.
```

## Patch type

This is a contract-only patch bundle.

It defines the limited control expansion contract for the Concept Lens after the BDP-003F.16 readiness decision.

## Boundary

This patch records a contract only.

It makes:

```text
no frontend changes
no service or bridge changes
no new frontend controls are implemented
no concept examples are added
no free-text concept search
no backend route
no adapter endpoint
no SQL migration
no database writes
no citation creation
no claim creation
no concept mention creation
no concept relation creation
no interpretation insertion
no evidence promotion
no external LLM routing
no unrestricted passage reproduction
```

## Allowed later controls defined by the contract

The contract defines only the following as possible later read-only controls:

```text
controlled preset selector over existing examples only
display density control
read-only evidence detail expander
rights boundary explainer toggle
reset to default Concept Lens view
```

These are not implemented in BDP-003F.17.

## Existing controlled examples remain unchanged

```text
Body without Organs
we repress because we repeat
assemblage
```

## Next safe step

```text
BDP-003F.18 — Define Concept Lens controlled concept coverage expansion contract after F17 control boundary.
```

This next step must remain contract-only unless explicitly re-scoped by the operator.

## Apply

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
set +e

unzip -o ~/Downloads/BDP_003F17_concept_lens_limited_control_expansion_contract_PATCH_ONLY.zip
python3 scripts/update_bdp_003f17_concept_lens_limited_control_expansion_contract.py
python3 scripts/repair_bdp_003f17_verifier_progression.py
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
python3 scripts/verify_bdp_003f17_concept_lens_limited_control_expansion_contract.py
python3 scripts/verify_bdp_003f17_verifier_progression_repair.py

git diff --check
```

Do not commit automatically. Commit only after the full verifier chain passes.
