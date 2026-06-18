# BDP-003F.6 Concept Lens Architecture Patch Bundle

This patch bundle defines BDP-003F.6 as an architecture-only phase.

Files included:

- `docs/BDP_003F6_CONCEPT_LENS_ARCHITECTURE.md`
- `scripts/verify_bdp_003f6_concept_lens_architecture.py`
- `BUCHANAN_SYSTEM_STATE.json`
- `BUCHANAN_THREAD_HANDOVER.md`

No frontend implementation, backend services, SQL migration, database mutation, evidence promotion, citations, concept relations, interpretations, or Buchanan-specific claims are included.

Apply from repo root:

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
unzip -o ~/Downloads/BDP_003F6_concept_lens_architecture_PATCH_ONLY.zip
python3 scripts/verify_bdp_003f6_concept_lens_architecture.py
```

Suggested verification chain:

```bash
python3 -m py_compile frontend/dark_precursor.py
python3 scripts/verify_bdp_003f4_navigation_architecture.py
python3 scripts/verify_bdp_003f5_navigation_wiring.py
python3 scripts/verify_bdp_003f6_concept_lens_architecture.py
```

Commit message suggestion:

```text
Define BDP-003F.6 Concept Lens architecture
```
