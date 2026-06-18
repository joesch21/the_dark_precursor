# BDP-003F.15 Patch Bundle — Concept Lens Running Frontend Review

This patch bundle adds the BDP-003F.15 review record, updater, and verifier for reviewing the Concept Lens read-only evidence posture display in the running Streamlit frontend.

It is a review-only bundle. It must not modify Concept Lens functionality.

## Files in this bundle

```text
docs/BDP_003F15_CONCEPT_LENS_RUNNING_FRONTEND_REVIEW.md
scripts/update_bdp_003f15_concept_lens_running_frontend_review.py
scripts/verify_bdp_003f15_concept_lens_running_frontend_review.py
BDP_003F15_PATCH_README.md
```

The updater modifies these existing repo files only after you run it:

```text
BUCHANAN_SYSTEM_STATE.json
BUCHANAN_THREAD_HANDOVER.md
```

## Files intentionally not included

```text
frontend/dark_precursor.py
scripts/concept_lens_archive_evidence_posture_service.py
scripts/concept_lens_existing_archive_evidence_readback_bridge.py
```

## Required manual review before completion

Launch the frontend using the repo venv:

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
. ./venv/bin/activate
python -m streamlit run frontend/dark_precursor.py
```

Inspect the Concept Lens display and confirm:

1. Controlled examples only are visible:
   - Body without Organs
   - we repress because we repeat
   - assemblage
2. The panel is read-only archive evidence posture only.
3. The boundary note is visible:

```text
This panel displays read-only archive evidence posture. It does not create citations, claims, interpretations, concept relations, or database records.
```

4. No free-text concept search input is present.
5. No create / save / promote / cite / interpret controls are present.
6. Restricted passage text remains omitted or rights-limited.
7. The display is readable, cinematic, and consistent with The Dark Precursor style.
8. The existing concept stage, About page, narrator stage, and archive controls still remain available.

## Record a passed review

After the manual running-frontend review passes:

```bash
python3 scripts/update_bdp_003f15_concept_lens_running_frontend_review.py --result pass
```

## Record a bounded finding instead of a pass

If a problem is found, do not repair it in F15. Record it:

```bash
python3 scripts/update_bdp_003f15_concept_lens_running_frontend_review.py \
  --result repair_needed \
  --finding "Describe the bounded visual or functional issue."
```

## Verification

Run the verifier chain after running the update script. The F15 verifier checks that:

1. BDP-003F.15 is recorded as a running-frontend review phase.
2. F15 does not modify `frontend/dark_precursor.py`.
3. F15 does not modify the Concept Lens service or bridge code.
4. Controlled examples are recorded.
5. The read-only boundary is recorded.
6. No free-text concept search input was added.
7. No citation, claim, interpretation, concept relation, or database record creation path was added.
8. The review result and next safe step are recorded.

Do not commit automatically. Commit only after successful verification and operator review.
