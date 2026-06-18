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


## BDP-003F.5 — Navigation Wiring

**Status:** Complete
**Commit status:** Pending operator commit
**Controlled slice:** minimal frontend navigation wiring only

BDP-003F.5 wires the already-approved BDP-003F.4 navigation architecture into the existing Dark Precursor frontend.

This phase does not add new pages. It does not add a dashboard. It does not add backend services, adapter endpoints, database tables, SQL migrations, archive workflow expansion, evidence promotion, citations, concept relations, interpretations, or Buchanan-specific claims.

Implemented frontend change:

```text
frontend/dark_precursor.py
```

The frontend now defines explicit approved surface keys for the existing concept stage and About page:

```text
SURFACE_STAGE
SURFACE_ABOUT
APPROVED_DARK_PRECURSOR_SURFACES
```

The frontend now routes surface movement through:

```text
get_dark_precursor_surface
set_dark_precursor_surface
```

The verified launch authority is README/docs.

The verified launch method is:

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
. ./venv/bin/activate
python -m streamlit run frontend/dark_precursor.py
```

Verifier:

```text
scripts/verify_bdp_003f5_navigation_wiring.py
```

Next safe step: do not start BDP-003F.6 in this thread.

## BDP-003F.6 — Concept Lens Architecture

**Status:** Complete
**Commit status:** Pending operator commit
**Controlled slice:** architecture definition only

BDP-003F.6 defines the Concept Lens as a future archive-grounded Deleuzian concept exploration dock inside The Dark Precursor concept stage.

The Concept Lens is intended to let students and users ask concept questions while preserving the evidence spine and avoiding conceptual flattening. It is not a new dashboard, not a general chatbot, and not a per-concept page system.

Defined future answer layers:

```text
plain_explanation
technical_deleuzian_explanation
archive_evidence_posture
fidelity_warning
```

Defined future archive readback chain:

```text
concepts -> concept_mentions -> passages -> citations -> sources
```

Defined future evidence posture levels:

```text
archive_grounded
source_bound_description
secondary_scholarship_supported
system_synthesis
exploratory_unverified
```

BDP-003F.6 does not add frontend implementation, Streamlit controls, new navigation surface keys, backend services, adapter endpoints, SQL migrations, database tables, source ingestion, citations, concept mentions, concept relations, interpretations, evidence promotion, Buchanan-specific claims, external LLM routing, automatic chat filtering, hidden personalization, or psychological assessment.

Verifier:

```text
scripts/verify_bdp_003f6_concept_lens_architecture.py
```

Next safe step:

```text
BDP-003F.7 — Define read-only Concept Lens archive evidence posture service contract before implementation.
```

## BDP-003F.7 — Concept Lens Archive Evidence Posture Service Contract

**Status:** Complete
**Commit status:** Pending operator commit
**Controlled slice:** service contract only

BDP-003F.7 defines the contract for a future read-only Concept Lens archive evidence posture service.

The service contract answers one bounded question:

```text
For this requested concept, what does the archive currently support?
```

The contract defines the future service as readback-only. It is not generation, not a philosophical fidelity review, and not a frontend UI dock.

Defined future primary archive readback chain:

```text
concepts -> concept_mentions -> passages -> citations -> sources
```

Defined future evidence posture levels:

```text
archive_grounded
source_bound_description
secondary_scholarship_supported
system_synthesis
exploratory_unverified
```

Defined future archive lookup statuses:

```text
archive_grounded_match
source_bound_match
concept_found_without_reviewed_evidence
no_archive_match
ambiguous_concept_match
rights_restricted_match
optional_layer_required_but_blocked
```

The contract preserves the rule that missing archive evidence is a valid evidence posture, not a failure. It also preserves the rights boundary: restricted text remains reference-only or omitted unless later rights-governed display is approved.

BDP-003F.7 does not add frontend implementation, Streamlit controls, Concept Lens UI dock, new navigation surface keys, backend service code, route handlers, adapter endpoints, SQL queries, SQL migrations, database tables, database mutation, source ingestion, citation creation, concept mention creation, concept relation creation, interpretation insertion, evidence promotion, Buchanan-specific claims, external LLM routing, automatic chat filtering, hidden personalization, or psychological assessment.

Verifier:

```text
scripts/verify_bdp_003f7_concept_lens_archive_evidence_posture_service_contract.py
```

Next safe step:

```text
BDP-003F.8 — Implement read-only Concept Lens archive evidence posture service behind this contract, if approved.
```

## BDP-003F.8 — Concept Lens Archive Evidence Posture Service Implementation

**Status:** Complete
**Controlled slice:** read-only local service implementation
**Commit status:** Pending operator commit

BDP-003F.8 implements the read-only Concept Lens archive evidence posture service behind the BDP-003F.7 contract.

Implemented service module:

```text
scripts/concept_lens_archive_evidence_posture_service.py
```

Implemented function:

```text
read_concept_lens_archive_evidence_posture
```

The service answers one narrow question:

```text
For this requested concept, what does the archive currently support?
```

It classifies supplied or live read-only archive rows into evidence posture results such as:

```text
archive_grounded
source_bound_description
system_synthesis
exploratory_unverified
```

The service preserves the primary archive readback chain:

```text
concepts -> concept_mentions -> passages -> citations -> sources
```

The verifier uses fixture rows and does not require a live database. The service can optionally use a read-only SQLite path or PostgreSQL URL for later local archive readback.

Boundary:

- no frontend wiring
- no Concept Lens UI dock
- no Streamlit controls
- no new navigation surface keys
- no backend route handler
- no adapter endpoint
- no SQL migration
- no database tables
- no database mutation
- no source ingestion
- no citation creation
- no concept mention creation
- no concept relation creation
- no interpretation insertion
- no evidence promotion
- no Buchanan-specific claims
- no automatic chat filtering
- no philosophical fidelity review

Verifier:

```text
scripts/verify_bdp_003f8_concept_lens_archive_evidence_posture_service.py
```

Next safe step:

```text
BDP-003F.9 — Review Concept Lens evidence posture service output against known archive cases before UI integration.
```

## BDP-003F.9 — Concept Lens Evidence Posture Output Review

**Status:** Complete
**Controlled slice:** review-only evidence posture output review

BDP-003F.9 reviews the BDP-003F.8 Concept Lens archive evidence posture service output against known archive cases before UI integration.

Finding: Outcome C.

```text
The archive evidence exists in governed project state, but no approved live readback adapter is currently exposed for the Concept Lens service default path.
```

Review decision:

1. Body without Organs is a known governed archive case in project state.
2. The F8 default service path is safe and intentionally conservative when no live archive adapter is configured.
3. The F8 service must not report `archive_grounded` for Body without Organs from the default no-live-archive invocation.
4. Concept Lens UI integration remains blocked.
5. A read-only bridge from existing archive evidence readback into the Concept Lens service is needed before frontend wiring.

No frontend wiring, Concept Lens UI dock, Streamlit controls, backend route, adapter endpoint, SQL migration, database mutation, citation creation, concept mention creation, concept relation creation, interpretation insertion, evidence promotion, Buchanan-specific claim, automatic chat filtering, or external LLM routing is approved by this phase.

Verifier:

```text
scripts/verify_bdp_003f9_concept_lens_evidence_posture_output_review.py
```

Next safe step:

```text
BDP-003F.10 — Define approved read-only bridge from existing archive evidence readback into the Concept Lens service.
```

<!-- BDP-003F.10-CONCEPT-LENS-READ-ONLY-BRIDGE-CONTRACT-START -->
## BDP-003F.10 — Concept Lens Existing Archive Evidence Readback Bridge Contract

**Status:** Complete
**Controlled slice:** read-only bridge contract definition only

BDP-003F.10 defines the approved read-only bridge contract from existing governed archive evidence readback into the BDP-003F.8 Concept Lens archive evidence posture service.

Decision: the bridge contract is approved as a future implementation boundary, but implementation is not added by BDP-003F.10.

Contract name:

```text
concept_lens_existing_archive_evidence_readback_bridge.v1
```

Future implementation target, if later approved:

```text
scripts/concept_lens_existing_archive_evidence_readback_bridge.py
```

Approved source readback candidates to inspect before implementation:

```text
scripts/read_bdp_001r_bwo_source_bound_description.py
scripts/read_bdp_002b_bwo_evidence_card.py
```

Bridge target:

```text
scripts/concept_lens_archive_evidence_posture_service.py
read_concept_lens_archive_evidence_posture
```

Required primary chain preserved:

```text
concepts -> concept_mentions -> passages -> citations -> sources
```

Boundary:

1. no frontend wiring;
2. no Concept Lens UI dock;
3. no backend route;
4. no adapter endpoint;
5. no SQL migration;
6. no database mutation;
7. no citation, concept mention, concept relation, interpretation, evidence promotion, or Buchanan-specific claim creation;
8. no F8 service implementation change.

UI integration remains blocked.

Verifier:

```text
scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py
```

Next safe step:

```text
BDP-003F.11 — Implement the approved read-only bridge from existing archive evidence readback into the Concept Lens service.
```
<!-- BDP-003F.10-CONCEPT-LENS-READ-ONLY-BRIDGE-CONTRACT-END -->

## BDP-003F.11 — Concept Lens Existing Archive Evidence Readback Bridge Implementation

**Status:** Complete
**Controlled slice:** read-only bridge implementation only

BDP-003F.11 implements the approved BDP-003F.10 read-only bridge from existing governed archive evidence readback into the BDP-003F.8 Concept Lens archive evidence posture service.

Implemented bridge module:

```text
scripts/concept_lens_existing_archive_evidence_readback_bridge.py
```

Implemented bridge function:

```text
read_existing_archive_evidence_rows_for_concept
```

Implemented service wrapper:

```text
read_concept_lens_archive_evidence_posture_via_existing_archive_bridge
```

The bridge supplies F8-compatible in-memory rows only. The F8 service remains the posture classifier.

First supported review case:

```text
Body without Organs
```

Boundary:

1. No frontend wiring.
2. No Concept Lens UI dock.
3. No Streamlit controls.
4. No new navigation surface keys.
5. No backend route.
6. No adapter endpoint.
7. No SQL migration.
8. No database mutation.
9. No citation creation.
10. No concept mention creation.
11. No concept relation creation.
12. No interpretation insertion.
13. No evidence promotion.
14. No Buchanan-specific claims.

Verifier:

```text
scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py
```

Next safe step:

```text
BDP-003F.12 — Review live Body without Organs bridge output against the Concept Lens service before UI integration.
```

## BDP-003F.12 — Concept Lens Bridge Output Smoke Review Before UI Integration

**Status:** Complete
**Controlled slice:** read-only bridge output smoke review only

BDP-003F.12 records the bridge output smoke-review gate after the BDP-003F.11 read-only bridge implementation and before any Concept Lens UI integration.

Review finding:

```text
The BDP-003F.11 bridge may be used for read-only local smoke review, but the Concept Lens UI remains blocked until a separate UI integration contract or frontend wiring phase is approved.
```

Required smoke cases:

```text
Body without Organs
we repress because we repeat
assemblage
```

Preserved archive readback chain:

```text
concepts -> concept_mentions -> passages -> citations -> sources
```

Boundary:

- no Concept Lens UI dock
- no Streamlit controls
- no frontend wiring
- no backend routes
- no adapter endpoints
- no SQL migrations
- no database mutation
- no citation creation
- no concept mention creation
- no concept relation creation
- no interpretation insertion
- no evidence promotion
- no Buchanan-specific claims

Verifier:

```text
scripts/verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py
```

Next safe step:

```text
BDP-003F.13 — Define Concept Lens UI integration contract for read-only evidence posture display before frontend wiring.
```

### BDP-003F.11 verifier-required boundary vocabulary repair

This handover section preserves the required F11 boundary vocabulary for historical verification after BDP-003F.12 advances the global phase pointer.

```text
existing archive readback bridge
```

## BDP-003F.13 — Concept Lens UI Integration Contract for Read-only Evidence Posture Display

**Status:** Complete
**Controlled slice:** UI integration contract only

BDP-003F.13 defines the UI integration contract for displaying read-only Concept Lens evidence posture before frontend wiring.

Approved display model:

```text
Archive evidence posture
Archive-grounded match
Source-bound description
Exploratory / unverified
No archive match
Rights-limited display
Read-only archive evidence
```

Preserved archive chain:

```text
concepts -> concept_mentions -> passages -> citations -> sources
```

Required service handoff boundary:

```text
read_concept_lens_archive_evidence_posture_via_existing_archive_bridge
```

First future UI smoke cases:

```text
Body without Organs
we repress because we repeat
assemblage
```

Boundary:

- no frontend wiring
- no Concept Lens UI dock implementation
- no Streamlit controls
- no backend routes
- no adapter endpoints
- no SQL migrations
- no database mutation
- no citation creation
- no concept mention creation
- no concept relation creation
- no interpretation insertion
- no evidence promotion
- no Buchanan-specific claims
- no automatic chat filtering
- no external LLM routing
- no unrestricted passage reproduction
- no source ingestion

Verifier:

```text
scripts/verify_bdp_003f13_concept_lens_ui_integration_contract.py
```

Next safe step:

```text
BDP-003F.14 — Wire the approved Concept Lens read-only evidence posture display into the frontend after contract verification.
```

## BDP-003F.14 — Concept Lens Frontend Read-only Evidence Posture Wiring

**Status:** Complete
**Controlled slice:** frontend read-only evidence posture display only
**Frontend target:** `frontend/dark_precursor.py`

BDP-003F.14 wires the approved BDP-003F.13 Concept Lens UI integration contract into The Dark Precursor frontend as a conservative read-only evidence posture display.

Implemented frontend surface:

```text
Concept Lens
Evidence posture
Archive evidence posture
Read-only archive evidence posture
```

Required service handoff used:

```text
read_concept_lens_archive_evidence_posture_via_existing_archive_bridge
```

Controlled smoke cases only:

```text
Body without Organs
we repress because we repeat
assemblage
```

Boundary note visible in frontend:

```text
This panel displays read-only archive evidence posture. It does not create citations, claims, interpretations, concept relations, or database records.
```

Boundary:

- no free-text concept search input
- no backend route
- no adapter endpoint
- no SQL migration
- no database mutation
- no archive row creation
- no source ingestion
- no citation creation
- no concept mention creation
- no concept relation creation
- no interpretation insertion
- no evidence promotion
- no Buchanan-specific claims
- no external LLM routing
- no unrestricted passage reproduction
- no general chat filtering

Verifier:

```text
scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py
```

Next safe step:

```text
BDP-003F.15 — Review the Concept Lens read-only evidence posture display in the running frontend before expanding controls or concept coverage.
```


### BDP-003F.14 verifier progression repair

A narrow verifier repair was applied after F14 wiring so the historical F10-F13 verifiers remain valid once global state advances to BDP-003F.14.

The repair updates only verifier progression allowances. It does not change frontend behavior, Concept Lens UI behavior, SQL, database writes, archive row creation, citation creation, concept mention creation, concept relation creation, interpretation insertion, evidence promotion, external LLM routing, free-text concept search input, source ingestion, unrestricted passage reproduction, Buchanan-specific interpretive claim generation, backend routes, adapter endpoints, or general chat filtering.


### BDP-003F.14 verifier progression repair V2

A second narrow verifier repair was applied because the first repair could skip F10-F12 when `BDP-003F.14` appeared elsewhere in those files outside the `ALLOWED_CURRENT_PHASES` block.

This V2 repair directly updates historical verifier allowlist blocks and F13 global next-step progression acceptance. It does not change frontend behavior, Concept Lens UI behavior, SQL, database writes, archive row creation, citation creation, concept mention creation, concept relation creation, interpretation insertion, evidence promotion, external LLM routing, free-text concept search input, source ingestion, unrestricted passage reproduction, Buchanan-specific interpretive claim generation, backend routes, adapter endpoints, or general chat filtering.

<!-- BDP-003F.15 RUNNING FRONTEND REVIEW START -->

## BDP-003F.15 — Concept Lens Running Frontend Review

Status: complete
Review result: pass
Completed at: 2026-06-18T05:59:29+00:00

Summary:
BDP-003F.15 records a manual running-frontend review of the Concept Lens read-only evidence posture display added in BDP-003F.14. The phase is review-only and does not modify frontend, service, or bridge code.

Reviewed controlled examples:
1. Body without Organs
2. we repress because we repeat
3. assemblage

Confirmed boundary:
This panel displays read-only archive evidence posture. It does not create citations, claims, interpretations, concept relations, or database records.

Files added or updated by this phase:
1. docs/BDP_003F15_CONCEPT_LENS_RUNNING_FRONTEND_REVIEW.md
2. scripts/update_bdp_003f15_concept_lens_running_frontend_review.py
3. scripts/verify_bdp_003f15_concept_lens_running_frontend_review.py
4. BDP_003F15_PATCH_README.md
5. BUCHANAN_SYSTEM_STATE.json
6. BUCHANAN_THREAD_HANDOVER.md

Files intentionally not modified:
1. frontend/dark_precursor.py
2. scripts/concept_lens_archive_evidence_posture_service.py
3. scripts/concept_lens_existing_archive_evidence_readback_bridge.py

Review findings:
No repair findings recorded.

Next safe step:
BDP-003F.16 — Decide Concept Lens control and concept coverage expansion readiness after running frontend review.

<!-- BDP-003F.15 RUNNING FRONTEND REVIEW END -->

<!-- BDP-003F.16 HANDOVER START -->

## BDP-003F.16 — Concept Lens expansion readiness decision

**Status:** complete
**Completed at:** 2026-06-18T06:31:28+00:00
**Input:** BDP-003F.15 running frontend review
**Outcome:** Outcome C — Ready for both separate later contract tracks, but implementation remains blocked.

### What changed

1. Added `docs/BDP_003F16_CONCEPT_LENS_EXPANSION_READINESS_DECISION.md`.
2. Added `scripts/verify_bdp_003f16_concept_lens_expansion_readiness_decision.py`.
3. Updated `BUCHANAN_SYSTEM_STATE.json` with the F16 decision record.
4. Recorded this handover block.

### Boundary preserved

1. No frontend changes were made.
2. No Concept Lens service or bridge changes were made.
3. No controls were added.
4. No concept examples were added.
5. No free-text search was added.
6. No citation, claim, interpretation, concept relation, or database record creation path was added.
7. The read-only evidence posture boundary remains intact.

### Next safe step

BDP-003F.17 — Define Concept Lens limited control expansion contract after F16 readiness decision.

Later, separately:

BDP-003F.18 — Define Concept Lens controlled concept coverage expansion contract after control readiness boundary.

<!-- BDP-003F.16 HANDOVER END -->
