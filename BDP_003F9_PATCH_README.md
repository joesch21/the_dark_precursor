# BDP-003F.9 Patch Bundle — Concept Lens Evidence Posture Output Review

This patch adds a review-only BDP-003F.9 finding before any Concept Lens UI integration.

## Finding

Outcome C:

```text
The archive evidence exists in governed project state, but no approved live readback adapter is currently exposed for the Concept Lens service default path.
```

Body without Organs is a known governed archive case in the broader project state, but the BDP-003F.8 default service invocation must not claim `archive_grounded` unless a live read-only archive bridge is configured and approved.

## Included files

```text
docs/BDP_003F9_CONCEPT_LENS_EVIDENCE_POSTURE_OUTPUT_REVIEW.md
scripts/update_bdp_003f9_concept_lens_evidence_posture_output_review.py
scripts/verify_bdp_003f9_concept_lens_evidence_posture_output_review.py
BDP_003F9_PATCH_README.md
```

## Boundary

This patch is review-only.

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

It does not create citations, concept mentions, concept relations, interpretations, evidence promotion, Buchanan-specific claims, automatic chat filtering, or external LLM routing.

## Apply

Run from the repository root:

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
unzip -o ~/Downloads/BDP_003F9_concept_lens_evidence_posture_output_review_PATCH_ONLY.zip
python3 scripts/update_bdp_003f9_concept_lens_evidence_posture_output_review.py
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
git diff --check
```

## Optional smoke review

```bash
python3 scripts/concept_lens_archive_evidence_posture_service.py "Body without Organs"
python3 scripts/concept_lens_archive_evidence_posture_service.py "we repress because we repeat"
python3 scripts/concept_lens_archive_evidence_posture_service.py "assemblage"
```

The default no-live-archive posture should remain safe and conservative:

```text
archive_lookup_status: no_archive_match
evidence_posture: exploratory_unverified
notes: No live archive adapter was configured
```

## Commit after operator verification

```bash
git add .
git commit -m "Review BDP-003F.9 Concept Lens evidence posture output"
git push
```

## Next safe step

```text
BDP-003F.10 — Define approved read-only bridge from existing archive evidence readback into the Concept Lens service.
```
