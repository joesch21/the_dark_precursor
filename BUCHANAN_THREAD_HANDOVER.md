# BDP-003E.5 — Local Reviewed Concept Card Archive Schema Candidate

**Date:** 2026-06-15T17:25:27+00:00  
**Status:** Complete
**Authority:** Schema candidate only; no implementation.

## What changed

BDP-003E.5 defines a local reviewed concept card archive schema candidate only.

It specifies the future record shape for reviewed cinematic concept card drafts, including archive identifiers, source card identifiers, review status, review decision, authority labels, governance flags, and blocked actions.

## Governance

This phase does not add frontend implementation, backend services, database mutation, SQL migration, local file writing, folder persistence, adapter endpoints, image generation, video generation, or evidence promotion.

Generated and reviewed cinematic concept cards remain provisional synthesis unless a later governed evidence-review phase separately promotes a specific citation-backed claim.

## Files updated

- `docs/BDP_003E5_LOCAL_REVIEWED_CONCEPT_CARD_ARCHIVE_SCHEMA_CANDIDATE.md`
- `docs/BDP_003E4_CONCEPT_CARD_PERSISTENCE_READINESS_DECISION.md`
- `scripts/verify_bdp_003e5_local_reviewed_concept_card_archive_schema_candidate.py`
- `scripts/verify_bdp_003e4_concept_card_persistence_readiness_decision.py`
- `BUCHANAN_SYSTEM_STATE.json`
- `BUCHANAN_THREAD_HANDOVER.md`

## Verification

Run:

```bash
python3 -m py_compile frontend/dark_precursor.py
python3 scripts/verify_bdp_003c_cinematic_experience_reset.py
python3 scripts/verify_bdp_003d_cinematic_video_front_page.py
python3 scripts/verify_bdp_003e1_cinematic_concept_card_contract.py
python3 scripts/verify_bdp_003e2_cinematic_concept_card_export_draft.py
python3 scripts/verify_bdp_003e3_cinematic_concept_card_sample_review.py
python3 scripts/verify_bdp_003e4_concept_card_persistence_readiness_decision.py
python3 scripts/verify_bdp_003e5_local_reviewed_concept_card_archive_schema_candidate.py
```

## Next recommended step

BDP-003E.6 — Review local reviewed concept card archive schema candidate against exported samples before implementation.

---

# BDP-003E.4 — Concept Card Persistence Readiness Decision

**Date:** 2026-06-15T17:16:44+00:00  
**Status:** Complete
**Authority:** Review decision only; no persistence implementation.

## Decision

BDP-003E.4 decides that exported cinematic concept cards are **not ready** for database persistence, backend persistence services, adapter endpoints, image/video generation invocation, or evidence promotion.

They are ready only for a future design-only schema candidate concerning local reviewed-card archiving.

## Readiness flags

```text
export_format_reviewed = true
local_download_draft_surface_ready = true
database_persistence_ready = false
adapter_implementation_ready = false
evidence_promotion_ready = false
local_archive_schema_candidate_ready = true
implementation_allowed_in_this_phase = false
```

## Files updated

- `docs/BDP_003E4_CONCEPT_CARD_PERSISTENCE_READINESS_DECISION.md`
- `docs/BDP_003E3_CINEMATIC_CONCEPT_CARD_SAMPLE_REVIEW.md`
- `scripts/verify_bdp_003e4_concept_card_persistence_readiness_decision.py`
- `BUCHANAN_SYSTEM_STATE.json`
- `BUCHANAN_THREAD_HANDOVER.md`

## Verification

Run:

```bash
python3 -m py_compile frontend/dark_precursor.py
python3 scripts/verify_bdp_003c_cinematic_experience_reset.py
python3 scripts/verify_bdp_003d_cinematic_video_front_page.py
python3 scripts/verify_bdp_003e1_cinematic_concept_card_contract.py
python3 scripts/verify_bdp_003e2_cinematic_concept_card_export_draft.py
python3 scripts/verify_bdp_003e3_cinematic_concept_card_sample_review.py
python3 scripts/verify_bdp_003e4_concept_card_persistence_readiness_decision.py
```

## Next recommended step

BDP-003E.5 — Define local reviewed concept card archive schema candidate only, without implementation.

---

# BDP-003E.3 — Cinematic Concept Card Sample Review

**Date:** 2026-06-15T17:07:39+00:00  
**Status:** Complete
**Authority:** Review-only; no runtime change, no persistence, no adapter implementation.

## What changed

BDP-003E.3 adds a review-only governance gate for the exported cinematic concept card drafts introduced in BDP-003E.2.

The phase records the required sample cases and confirms that exported cards remain local provisional synthesis drafts only.

## Review decision

The BDP-003E.2 export format is acceptable for local human review only.

It is not yet approved for database persistence, server-side persistence, adapter endpoints, image generation, video generation, or evidence promotion.

## Required sample cases

1. Body without Organs / Narrator.
2. Assemblage / Cinematic Treatment.
3. Lines of Flight / Storyboard Film Clip Brief.

## Files updated

- `docs/BDP_003E3_CINEMATIC_CONCEPT_CARD_SAMPLE_REVIEW.md`
- `docs/BDP_003E2_CINEMATIC_CONCEPT_CARD_EXPORT_DRAFT.md`
- `scripts/verify_bdp_003e3_cinematic_concept_card_sample_review.py`
- `BUCHANAN_SYSTEM_STATE.json`
- `BUCHANAN_THREAD_HANDOVER.md`

## Verification

Run:

```bash
python3 -m py_compile frontend/dark_precursor.py
python3 scripts/verify_bdp_003c_cinematic_experience_reset.py
python3 scripts/verify_bdp_003d_cinematic_video_front_page.py
python3 scripts/verify_bdp_003e1_cinematic_concept_card_contract.py
python3 scripts/verify_bdp_003e2_cinematic_concept_card_export_draft.py
python3 scripts/verify_bdp_003e3_cinematic_concept_card_sample_review.py
```

## Next recommended step

BDP-003E.4 — Decide concept card persistence readiness from reviewed samples only.

---

# BDP-003E.2 — Read-only Cinematic Concept Card Export Draft

**Date:** 2026-06-15T17:01:19+00:00  
**Status:** Complete
**Authority:** Frontend download-only draft export; no database mutation.

## What changed

BDP-003E.2 adds a local export dock to The Dark Precursor after a cinematic response has been generated.

The operator can download:

1. A Markdown cinematic concept card draft.
2. A JSON cinematic concept card data object.

The export is generated in memory from the visible response and current interaction controls.

## Governance

Generated cinematic concept cards are not evidence. They are provisional cinematic synthesis drafts only.

This slice does not add database persistence, backend services, adapter endpoints, server-side file persistence, image generation, video generation, citation creation, concept relation creation, or evidence-spine mutation.

## Files updated

- `frontend/dark_precursor.py`
- `frontend/styles/dark_precursor.css`
- `docs/BDP_003E2_CINEMATIC_CONCEPT_CARD_EXPORT_DRAFT.md`
- `docs/BDP_003E_CINEMATIC_CONCEPT_CARD_PERSISTENCE_CONTRACT.md`
- `scripts/verify_bdp_003e2_cinematic_concept_card_export_draft.py`
- `BUCHANAN_SYSTEM_STATE.json`
- `BUCHANAN_THREAD_HANDOVER.md`

## Verification

Run:

```bash
python3 -m py_compile frontend/dark_precursor.py
python3 scripts/verify_bdp_003c_cinematic_experience_reset.py
python3 scripts/verify_bdp_003d_cinematic_video_front_page.py
python3 scripts/verify_bdp_003e1_cinematic_concept_card_contract.py
python3 scripts/verify_bdp_003e2_cinematic_concept_card_export_draft.py
```

## Next recommended step

BDP-003E.3 — Review exported cinematic concept card samples before any persistence or adapter implementation.

---

# BDP-003E.1 — Cinematic Concept Card Persistence Contract

**Date:** 2026-06-15T16:51:45+00:00  
**Status:** Complete
**Authority:** Contract only; no runtime implementation.

## What changed

BDP-003E.1 defines the persistence contract for future Dark Precursor cinematic concept cards.

The contract specifies:

1. The minimum card shape.
2. Required governance labels.
3. Evidence-spine separation.
4. Human-review requirements.
5. The optional downstream image/video adapter boundary.
6. The next implementation slice.

## Files updated

- `docs/BDP_003E_CINEMATIC_CONCEPT_CARD_PERSISTENCE_CONTRACT.md`
- `scripts/verify_bdp_003e1_cinematic_concept_card_contract.py`
- `BUCHANAN_SYSTEM_STATE.json`
- `BUCHANAN_THREAD_HANDOVER.md`

## Boundary

No frontend, backend, SQL, database, citation, source-ingestion, or adapter implementation was added.

The phase is contract-only. Generated cinematic cards remain `cinematic_synthesis`, `not_evidence`, `not_promoted`, and `human_review_required`.

## Verification

Run:

```bash
python3 scripts/verify_bdp_003e1_cinematic_concept_card_contract.py
```

## Next recommended step

BDP-003E.2 — Implement read-only cinematic concept card export draft without database mutation.

---

# BDP-003D.2 — Cinematic Video Front Page Closeout

**Date:** 2026-06-15T16:43:10+00:00
**Status:** Complete
**Authority:** Frontend display only; no evidence-spine mutation.

## What changed

BDP-003D is now closed out as the completed cinematic video front page slice.

The committed application already contains the BDP-003D behaviours:

1. Local MP4 cinematic background stream.
2. Fallback cinematic background when the video asset is absent.
3. Title gate before the main interface.
4. `Enter the Vault` transition.
5. `Return to title page` sidebar control.
6. Slowed atmospheric playback.
7. Large cinematic typography and softened translucent panels.

## Files updated

- `docs/BDP_003D_CINEMATIC_VIDEO_FRONT_PAGE.md`
- `docs/BDP_003C_CINEMATIC_EXPERIENCE_RESET.md`
- `BUCHANAN_SYSTEM_STATE.json`
- `scripts/verify_bdp_003d_cinematic_video_front_page.py`

## Verification

Run:

```bash
python3 -m py_compile frontend/dark_precursor.py
python3 scripts/verify_bdp_003c_cinematic_experience_reset.py
python3 scripts/verify_bdp_003d_cinematic_video_front_page.py
```

## Boundary

No database mutation, citation insertion, source ingestion, concept relation creation, interpretation insertion, or video generation backend was added.

The video remains atmosphere only. It is not evidence and does not carry conceptual authority.

## Next recommended step

BDP-003E — Define cinematic concept card persistence and optional image/video generation adapter boundary.

---

# Buchanan Thread Handover

<!-- BDP-002G DIFFERENTIAL READING ENGINE -->

## BDP-002G — Add differential reading engine contract

**Status:** Complete
**Updated:** 2026-06-15T03:12:20+00:00  
**Type:** Doctrine and application contract  
**Database mutation:** No  
**SQL migration:** No  
**Frontend auto-wiring:** No  

### What changed

BDP-002G records the core platform thesis:

> The Buchanan / Deleuze Intelligence Platform is not merely a database. It is a differential reading engine.

The patch adds the governed method for tracing:

1. Assemblage
2. Flow
3. Cut / subtraction
4. Capture / extraction
5. Desire
6. Affect / intensity
7. Qualitative difference
8. Line of flight
9. Authority label

### Added files

- `docs/BDP_002G_DIFFERENTIAL_READING_ENGINE.md`
- `prompts/BUCHANAN_DIFFERENTIAL_READING_SYSTEM_PROMPT.md`
- `data/templates/differential_analysis_card.schema.json`
- `data/templates/differential_analysis_card_social_media_feed.example.json`
- `frontend/differential_engine_panel.py`
- `scripts/update_bdp_002g_differential_engine.py`
- `scripts/verify_bdp_002g_differential_engine.py`

### Boundary

This phase does not create Buchanan-specific claims, insert citations, insert interpretations, mutate the database, or change the schema.

### Next recommended action

BDP-002G.1 — Wire the optional Differential Engine panel into The Dark Precursor after operator review, or test the template on one reviewed example.

## BDP-002H — Dark Precursor Style Split

**Status:** complete  
**Type:** frontend refactor  
**Updated:** 2026-06-15T03:18:11+00:00  

### What changed

- Moved the cinematic Streamlit CSS from `frontend/dark_precursor.py` into `frontend/styles/dark_precursor.css`.
- Added a local CSS loader in `frontend/dark_precursor.py`.
- Moved `render_differential_engine_panel()` so it executes after `st.set_page_config()`.

### Boundaries

- No database mutation.
- No SQL migration.
- No evidence spine change.
- No Buchanan claim or interpretation created.
- No generative prompt change.

### Next recommended step

BDP-002I — Decide where the Differential Reading Engine panel belongs inside the main Dark Precursor flow.


<!-- BDP-003C CINEMATIC EXPERIENCE RESET -->

## BDP-003C — Dark Precursor Cinematic Experience Reset

**Status:** Prepared  
**Updated:** 2026-06-15T03:26:40+00:00  
**Type:** Frontend / generative surface reset

### Summary

BDP-003C resets The Dark Precursor toward the intended cinematic experience:

- large readable narrator text.
- slower chunked reveal.
- simplified concept-first stage.
- cinematic treatment and storyboard / film clip brief modes.
- differential method mechanics embedded in the prompt.
- CSS isolated in `frontend/styles/dark_precursor.css`.
- no impersonation claim that the app is Ian Buchanan.
- no database mutation, SQL migration, evidence-spine change, interpretation insertion, or Buchanan-specific claim creation.

### Boundary

Film/video backend generation is not implemented in this slice. The patch creates the governed cinematic brief pathway only.

### Next Recommended Step

BDP-003D — Add cinematic concept card output persistence and optional image/video generation adapter boundary.

<!-- BDP-003E.6-ARCHIVE-SCHEMA-SAMPLE-REVIEW-START -->
## BDP-003E.6 — Archive Schema Sample Review

**Status:** Complete
**Type:** review-only governance phase

BDP-003E.6 reviewed the BDP-003E.5 local reviewed concept card archive schema candidate against the BDP-003E.3 exported cinematic concept card sample cases.

Decision: the schema candidate is suitable for reviewed sample comparison, but implementation remains blocked.

No persistence was implemented. No frontend archive controls were added. No backend services, SQL migrations, local file writers, archive folders, adapter endpoints, citations, concept relations, interpretations, evidence promotions, or Buchanan-specific claims were created.

Verifier added:

```bash
python3 scripts/verify_bdp_003e6_archive_schema_sample_review.py
```

Current next step:

`BDP-003E.7 — Define local reviewed concept card archive writer contract only, without implementation.`
<!-- BDP-003E.6-ARCHIVE-SCHEMA-SAMPLE-REVIEW-END -->

<!-- BDP-003E.7-WRITER-CONTRACT-START -->
## BDP-003E.7 — Local Reviewed Concept Card Archive Writer Contract

**Status:** Complete
**Type:** contract-only governance phase

BDP-003E.7 defines the contract for a future local reviewed concept card archive writer.

Decision: the writer contract is defined as a future boundary only; implementation remains blocked.

No writer was implemented. No archive folders were created. No local files were written. No frontend archive controls, backend services, adapter endpoints, database tables, SQL migrations, persistence path, evidence promotion, citations, concept relations, interpretations, or Buchanan-specific claims were created.

Verifier added:

```bash
python3 scripts/verify_bdp_003e7_local_reviewed_concept_card_archive_writer_contract.py
```

Current next step:

`BDP-003E.8 — Review local reviewed concept card archive writer contract against archive boundaries before implementation.`
<!-- BDP-003E.7-WRITER-CONTRACT-END -->

## BDP-003E.8 — Local Reviewed Concept Card Archive Writer Contract Boundary Review

**Status:** Complete
**Controlled slice:** review_only_writer_contract_boundary
**Commit:** pending local commit after verifier pass
**Verifier:** `scripts/verify_bdp_003e8_archive_writer_contract_boundary_review.py`

BDP-003E.8 reviewed the BDP-003E.7 local reviewed concept card archive writer contract against the archive boundaries established by BDP-003E.5 and BDP-003E.6.

Decision: the writer contract is suitable as a future implementation boundary, but Implementation is not approved.

Boundary findings:

1. The writer contract may carry forward as a contract-only specification.
2. Future writer behavior must remain limited to reviewed concept card archive records.
3. Future writer behavior must preserve generated/exported/reviewed separation.
4. Future writer behavior must not promote cinematic concept cards into the evidence spine.
5. Future writer behavior must not create citations, concept relations, interpretations, or Buchanan-specific claims.
6. No implementation was added in this phase.

Blocked by this phase:

1. No persistence implementation.
2. No frontend archive controls.
3. No backend services.
4. No adapter endpoints.
5. No database tables or SQL migrations.
6. No archive folders.
7. No local files written.

Next safe step:

`BDP-003E.9 — Decide local reviewed concept card archive writer implementation readiness, without implementation.`

## BDP-003E.9 — Local Reviewed Concept Card Archive Writer Implementation Readiness Decision

**Status:** Complete
**Controlled slice:** readiness-decision only
**Commit status:** pending local commit after verification

### Decision

The local reviewed concept card archive writer is ready for a future implementation-boundary phase, but Implementation is not approved by BDP-003E.9.

### Boundary

BDP-003E.9 does not add a writer, archive folder, local file persistence, frontend archive controls, backend service, adapter endpoint, database table, SQL migration, evidence promotion, citation, concept relation, interpretation, or Buchanan-specific claim.

### Files

- `docs/BDP_003E9_ARCHIVE_WRITER_IMPLEMENTATION_READINESS_DECISION.md`
- `scripts/verify_bdp_003e9_archive_writer_implementation_readiness_decision.py`

### Next safe step

`BDP-003E.10 — Define local reviewed concept card archive implementation boundary and safety gates before writing code.`



## BDP-003E.10 — Local Reviewed Concept Card Archive Implementation Boundary and Safety Gates

**Status:** Complete

BDP-003E.10 defines the implementation boundary and safety gates before any local reviewed concept card archive writer code is written.

Decision: The writer may proceed only into a later explicitly approved implementation phase guarded by safety gates. Implementation is not approved by BDP-003E.10.

Boundary remains blocked for:

- writer implementation
- archive folders
- local files written
- frontend archive controls
- backend services
- adapter endpoints
- database tables
- SQL migrations
- evidence promotion
- citations
- concept relations
- interpretations
- Buchanan-specific claims

Verifier: `scripts/verify_bdp_003e10_archive_implementation_boundary_and_safety_gates.py`

Next safe step: `BDP-003E.11 — Implement local reviewed concept card archive writer behind safety gates, if approved.`



## BDP-003E.11 — Local Reviewed Concept Card Archive Writer Implementation

**Status:** Complete

BDP-003E.11 implements the local reviewed concept card archive writer behind the BDP-003E.10 safety gates.

Implemented file: `scripts/local_reviewed_concept_card_archive_writer.py`

Verifier: `scripts/verify_bdp_003e11_local_reviewed_concept_card_archive_writer.py`

Boundary:

- local writer implementation only
- no frontend archive controls
- no backend services
- no adapter endpoints
- no database tables
- no SQL migrations
- no evidence promotion
- no citations
- no concept relations
- no interpretations
- no Buchanan-specific claims
- no repository archive folder or archived concept card payload is created by this phase

The verifier writes only to a temporary directory to prove validation, idempotency, path-safety, and rejection behavior.

Next safe step: `BDP-003E.12 — Review local reviewed concept card archive writer output against sample payloads before UI integration.`

## BDP-003E.12 — Local Reviewed Concept Card Archive Writer Output Sample Review

**Status:** Complete

BDP-003E.12 reviews the BDP-003E.11 local reviewed concept card archive writer output against controlled sample payloads before UI integration.

The verifier exercises the writer in a temporary directory only and checks deterministic output shape, boundary flags, payload preservation, idempotency, and rejection behavior.

Boundary:

- writer output sample review only
- no frontend archive controls
- no backend services
- no adapter endpoints
- no database tables
- no SQL migrations
- no evidence promotion
- no citations
- no concept relations
- no interpretations
- no Buchanan-specific claims
- no repository archive records written

Next safe step: `BDP-003E.13 — Define UI integration contract for local reviewed concept card archive controls before wiring frontend.`

## BDP-003E.13 — UI Integration Contract for Local Reviewed Concept Card Archive Controls

**Status:** Complete
**Controlled slice:** UI integration contract only

BDP-003E.13 defines the future UI integration contract for local reviewed concept card archive controls before frontend wiring.

Boundary:
- No frontend wiring
- No archive control implementation
- No Streamlit archive button
- No backend services
- No adapter endpoints
- No database tables or SQL migrations
- No evidence promotion, citations, concept relations, interpretations, or Buchanan-specific claims

Decision: the UI integration contract is suitable for a later readiness phase, but frontend wiring is not approved by BDP-003E.13.

Next safe step: `BDP-003E.14 — Decide UI archive control frontend wiring readiness, without wiring frontend.`

## BDP-003E.14 — UI Archive Control Frontend Wiring Readiness Decision

**Status:** Complete
**Commit status:** Pending operator commit
**Controlled slice:** frontend wiring readiness decision only

BDP-003E.14 decides that UI archive control frontend wiring is ready for a later explicitly approved wiring phase, but frontend wiring is not approved by this phase.

No frontend wiring, frontend archive controls, archive buttons, Streamlit writer calls, backend services, adapter endpoints, database tables, SQL migrations, archive folders created by default, evidence promotion, citations, concept relations, interpretations, or Buchanan-specific claims are approved by BDP-003E.14.

Verifier:
`scripts/verify_bdp_003e14_ui_archive_control_frontend_wiring_readiness_decision.py`

Next safe step: `BDP-003E.15 — Wire local reviewed concept card archive controls into The Dark Precursor UI behind safety gates.`

## BDP-003E.15 — Archive Controls UI Wiring

**Status:** Complete
**Commit status:** Pending operator commit
**Controlled slice:** guarded frontend wiring only

BDP-003E.15 wires local reviewed concept card archive controls into The Dark Precursor UI behind safety gates.

The UI wiring requires a locally reviewed payload, an explicit local archive path, and operator confirmation before calling the local archive writer.

No backend services, adapter endpoints, database tables, SQL migrations, evidence promotion, citations, concept relations, interpretations, or Buchanan-specific claims are added by this phase.

Verifier:
`scripts/verify_bdp_003e15_archive_controls_ui_wiring.py`

Next safe step: `BDP-003E.16 — Review wired archive controls in The Dark Precursor UI against safety gates before broader archive workflow.`

## BDP-003E.16 — Wired Archive Controls Safety Gate Review

**Status:** Complete
**Commit status:** Pending operator commit
**Controlled slice:** safety review only

BDP-003E.16 reviews the BDP-003E.15 wired local reviewed archive controls against the safety gates.

Frontend UX/UI was changed by BDP-003E.15. BDP-003E.16 does not make additional frontend UX/UI changes and does not modify `frontend/dark_precursor.py`.

The review confirms local reviewed payload gating, explicit archive path gating, operator confirmation, local writer only, and continued blocking of broader archive workflow expansion.

No backend services, adapter endpoints, database tables, SQL migrations, evidence promotion, citations, concept relations, interpretations, or Buchanan-specific claims are approved by BDP-003E.16.

Verifier:
`scripts/verify_bdp_003e16_wired_archive_controls_safety_review.py`

Next safe step: `BDP-003E.17 — Decide broader archive workflow readiness before expanding beyond local reviewed UI archive controls.`

## BDP-003F.1 — Teleprompter Narrator Stage

**Status:** Complete
**Commit status:** Pending operator commit
**Controlled slice:** frontend cinematic narrator UX only

BDP-003F.1 changes narrator display from chunk-by-chunk reveal to a fullscreen-style upward scrolling teleprompter stage.

The change affects `frontend/dark_precursor.py` and `frontend/styles/dark_precursor.css` only.

No backend services, adapter endpoints, database tables, SQL migrations, archive workflow expansion, evidence promotion, citations, concept relations, interpretations, or Buchanan-specific claims are added.

Verifier:
`scripts/verify_bdp_003f1_teleprompter_narrator_stage.py`

Next safe step: `BDP-003F.2 — Review teleprompter narrator stage in the running frontend before further cinematic UX changes.`

## BDP-003F.2 — About Page

**Status:** Complete
**Commit status:** Pending operator commit
**Controlled slice:** frontend explanatory UX only

BDP-003F.2 adds an About page to The Dark Precursor. The page explains the application as a governed cinematic concept laboratory and makes clear that it does not claim to think like Ian Buchanan, impersonate Ian Buchanan, replace scholarship, or produce authoritative Deleuzian interpretation.

The page foregrounds the governing distinction: it separates atmosphere from authority.

No backend services, adapter endpoints, database tables, SQL migrations, archive workflow expansion, evidence promotion, citations, concept relations, interpretations, or Buchanan-specific claims are added.

Verifier:
`scripts/verify_bdp_003f2_about_page.py`

Next safe step: `BDP-003F.3 — Review The Dark Precursor About page in the running frontend before further public-facing explanation changes.`
## BDP-003F.3 — About Page Running Frontend Review

**Status:** Complete
**Commit status:** Pending operator commit
**Controlled slice:** running-frontend review only

BDP-003F.3 records the manual running-frontend inspection of the BDP-003F.2 About page before further public-facing explanation changes.

Manual inspection result:

```text
The About page works in the running frontend.
The application launches.
The About page opens.
The Return to concept stage control works.
The core cinematic interface remains available.
```

No new frontend UX, controls, backend services, adapter endpoints, database work, archive workflow expansion, evidence promotion, citations, concept relations, interpretations, or Buchanan-specific claims are added.

Verifier:

```text
scripts/verify_bdp_003f3_about_page_running_frontend_review.py
```

Next safe step:

```text
BDP-003F.4 — Define The Dark Precursor navigation architecture before adding further frontend pages.
```


## BDP-003F.4 — Navigation Architecture Definition

**Status:** Complete
**Commit status:** Pending operator commit
**Controlled slice:** navigation architecture definition only

BDP-003F.4 defines The Dark Precursor navigation architecture before adding further frontend pages.

The cinematic concept stage remains the primary surface. The About page is a supporting explanation surface.

Future surface candidates may include the concept stage, About, archive/reviewed outputs, source/evidence posture, settings/controls, and help/orientation, but these are architectural candidates only. BDP-003F.4 does not implement them.

Navigation must preserve cinematic immersion, avoid dashboard drift, make page movement explicit, and ensure supporting pages return clearly to the concept stage.

Navigation does not create citation authority, evidence promotion, interpretation, concept relation, source ingestion, database mutation, adapter invocation, or Buchanan-specific claim.

No frontend implementation, backend services, adapter endpoints, database tables, SQL migrations, evidence promotion, citations, concept relations, interpretations, or Buchanan-specific claims are added.

Verifier:

```text
scripts/verify_bdp_003f4_navigation_architecture.py
```

Next safe step:

```text
BDP-003F.5 — Wire navigation architecture only after BDP-003F.4 is committed and pushed.
```
