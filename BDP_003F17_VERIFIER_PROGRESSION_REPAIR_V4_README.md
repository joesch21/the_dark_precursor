# BDP-003F.17 Verifier Progression Repair V4

This repair widens the existing BDP-003F.10-F15 Concept Lens verifier progression guards so completed historical verifiers tolerate the valid F17/F18 state introduced by BDP-003F.17.

It does not modify:

- `frontend/dark_precursor.py`
- `scripts/concept_lens_archive_evidence_posture_service.py`
- `scripts/concept_lens_existing_archive_evidence_readback_bridge.py`
- database, archive, citation, claim, concept, relation, interpretation, route, endpoint, or source-ingestion code

Use this after restoring any malformed F17 V1/V2/V3 verifier progression repair attempts.
