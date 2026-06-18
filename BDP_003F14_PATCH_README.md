# BDP-003F.14 Patch Bundle — Concept Lens Frontend Read-only Evidence Posture Wiring

This bundle wires the approved Concept Lens read-only evidence posture display into `frontend/dark_precursor.py` after the BDP-003F.13 contract.

Required service handoff:

```text
read_concept_lens_archive_evidence_posture_via_existing_archive_bridge
```

Required frontend boundary note:

```text
This panel displays read-only archive evidence posture. It does not create citations, claims, interpretations, concept relations, or database records.
```

Controlled smoke examples:

```text
Body without Organs
we repress because we repeat
assemblage
```

It is intentionally conservative:

1. controlled smoke examples only;
2. no free-text concept search input;
3. no SQL mutation;
4. no database writes;
5. no citation, claim, interpretation, concept relation, or evidence promotion path;
6. no backend route or adapter endpoint;
7. no external LLM routing.

## Apply from repo root

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
set +e

unzip -o ~/Downloads/BDP_003F14_concept_lens_frontend_read_only_evidence_posture_wiring_PATCH_ONLY.zip
python3 scripts/update_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py
```

## Verify

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
set +e

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
git diff --check
```

## Inspect before commit

```bash
git status -sb
git status --short
git diff -- frontend/dark_precursor.py
git diff -- BUCHANAN_SYSTEM_STATE.json BUCHANAN_THREAD_HANDOVER.md
git diff -- docs/BDP_003F14_CONCEPT_LENS_FRONTEND_READ_ONLY_EVIDENCE_POSTURE_WIRING.md scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py
```

## Commit only after successful verification

```bash
git add frontend/dark_precursor.py docs/BDP_003F14_CONCEPT_LENS_FRONTEND_READ_ONLY_EVIDENCE_POSTURE_WIRING.md scripts/update_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py BDP_003F14_PATCH_README.md BUCHANAN_SYSTEM_STATE.json BUCHANAN_THREAD_HANDOVER.md

git commit -m "Wire BDP-003F.14 Concept Lens read-only evidence posture display"
git push
```

## Next safe step

Do not expand Concept Lens controls in this phase.

Next phase:

```text
BDP-003F.15 — Review the Concept Lens read-only evidence posture display in the running frontend before expanding controls or concept coverage.
```
