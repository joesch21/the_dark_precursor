# BDP-003F.8 Patch Bundle — Concept Lens Archive Evidence Posture Service

This patch implements the read-only Concept Lens archive evidence posture service behind the BDP-003F.7 contract.

## Included files

```text
docs/BDP_003F8_CONCEPT_LENS_ARCHIVE_EVIDENCE_POSTURE_SERVICE_IMPLEMENTATION.md
scripts/concept_lens_archive_evidence_posture_service.py
scripts/verify_bdp_003f8_concept_lens_archive_evidence_posture_service.py
BUCHANAN_SYSTEM_STATE.json
BUCHANAN_THREAD_HANDOVER.md
BDP_003F8_PATCH_README.md
```

## Boundary

This patch adds a local read-only service module and verifier only.

It does not add frontend wiring, Streamlit controls, new navigation surfaces, backend routes, adapter endpoints, SQL migrations, database tables, database mutation, source ingestion, citation creation, concept mention creation, concept relation creation, interpretation insertion, evidence promotion, Buchanan-specific claims, automatic chat filtering, external LLM routing, or philosophical fidelity review.

## Apply

Run from the repository root:

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
unzip -o ~/Downloads/BDP_003F8_concept_lens_archive_evidence_posture_service_PATCH_ONLY.zip
```

## Verify

```bash
python3 -m py_compile frontend/dark_precursor.py
python3 scripts/verify_bdp_003f6_concept_lens_architecture.py
python3 scripts/verify_bdp_003f7_concept_lens_archive_evidence_posture_service_contract.py
python3 scripts/verify_bdp_003f8_concept_lens_archive_evidence_posture_service.py
```

## Optional service smoke test

```bash
python3 scripts/concept_lens_archive_evidence_posture_service.py "we repress because we repeat"
```

## Commit

```bash
git add .
git commit -m "Implement BDP-003F.8 Concept Lens evidence posture service"
git push
```

## Next safe step

```text
BDP-003F.9 — Review Concept Lens evidence posture service output against known archive cases before UI integration.
```
