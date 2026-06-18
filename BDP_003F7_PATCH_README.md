# BDP-003F.7 Patch — Concept Lens Archive Evidence Posture Service Contract

## Purpose

This patch defines BDP-003F.7 as a contract-only governance slice for a future read-only Concept Lens archive evidence posture service.

It does not implement the service.

## Files included

- `docs/BDP_003F7_CONCEPT_LENS_ARCHIVE_EVIDENCE_POSTURE_SERVICE_CONTRACT.md`
- `scripts/verify_bdp_003f7_concept_lens_archive_evidence_posture_service_contract.py`
- `BUCHANAN_SYSTEM_STATE.json`
- `BUCHANAN_THREAD_HANDOVER.md`

## Boundary

No frontend controls, Concept Lens dock, backend service, route handler, adapter endpoint, SQL query, SQL migration, database table, database mutation, source ingestion, citation creation, concept mention creation, concept relation creation, interpretation insertion, evidence promotion, Buchanan-specific claim, external LLM routing, automatic chat filtering, hidden personalization, or psychological assessment is added.

## Apply

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
unzip -o ~/Downloads/BDP_003F7_concept_lens_archive_evidence_posture_service_contract_PATCH_ONLY.zip
python3 scripts/verify_bdp_003f7_concept_lens_archive_evidence_posture_service_contract.py
```

## Suggested verification chain

```bash
python3 -m py_compile frontend/dark_precursor.py
python3 scripts/verify_bdp_003f5_navigation_wiring.py
python3 scripts/verify_bdp_003f6_concept_lens_architecture.py
python3 scripts/verify_bdp_003f7_concept_lens_archive_evidence_posture_service_contract.py
```

## Commit

```bash
git add .
git commit -m "Define BDP-003F.7 Concept Lens evidence posture contract"
git push
```

## Next safe step

`BDP-003F.8 — Implement read-only Concept Lens archive evidence posture service behind this contract, if approved.`
