# Buchanan Vault Resources Integration

**Status:** Initial Integration Documentation (Experimental Layer Addition)  
**Version:** 0.1  
**Date:** June 15, 2026  
**Related Blueprints:** `BUCHANAN_PSYCHOLINGUISTIC_MODELLING_BLUEPRINT.md`, `BUCHANAN_METAPHOR_DENSITY_APPROACH.md`  
**Governance:** Follows `NEW_THREAD_ONBOARDING.md` mandatory reading; patch-bundle preferred for future changes; documentation update mandatory.

## 1. Purpose

This document records the addition of selected links, structured data, and image resources from the external **Ian Buchanan Vault** repository (https://github.com/joesch21/Ian_Buchanan_Vault) into the Buchanan Deleuze Intelligence Platform project workspace.

The Vault serves as a public-facing archive of resources tied to Ian Buchanan's scholarship, including ORCID data, scholar networks, book visuals, and cartography tooling. Integration strengthens the **citation/provenance** and **semantic concept** layers while providing raw material for future psycho-linguistic and visual extensions — without compromising the evidence spine or authority hierarchy.

## 2. What Was Added

### 2.1 Structured Data (now in `/artifacts/data/`)
- **scholars.json**: Curated list of 19 core Deleuzian and critical theory scholars, including Ian Buchanan. Each entry contains:
  - `name`, `orcid` (where available), `aliases`, `sources` (ORCID pages or institutional links).
  - Directly enriches the `sources` and scholar attribution layer for passage/concept grounding.
- **groups.json**: Defines the "Deleuzian Scholars" group with members and defaultConcepts (assemblage, affect, deterritorialization, becoming, war machine).
  - Provides a ready-made semantic cluster for concept mapping and future reader-transformation analysis.

These files were extracted verbatim from the Vault and persisted locally to avoid external dependency while preserving provenance.

### 2.2 Image Resources (documented in `/artifacts/images/IMAGE_MANIFEST.md`)
- 20+ image assets from Vault `/images/`, primarily **book covers** of key texts in Deleuze & Guattari studies (e.g., *Anti-Oedipus*, schizoanalysis volumes, assemblage theory, Deleuze and Literature/Space/Cinema).
- Additional: portraits/collages (`dg.jpeg`, `collage_animation.gif`, `collage_output.png`).
- Full manifest with direct raw GitHub URLs provided for reference/download.
- **Conceptual fit**: These visuals align with zones of conceptual intensity. Book covers can anchor source metadata; collages may illustrate metaphorical transformation or semantic drift for Level 2+ metaphor density experiments.

**Note on binaries**: Only manifest and URLs added at this stage. Local mirroring of image files requires controlled patch and licensing review (many appear standard academic book covers).

### 2.3 Key Links Incorporated
- Vault repository: https://github.com/joesch21/Ian_Buchanan_Vault
- Deployed interface: https://buchanan-vault.vercel.app (Cartography / concept graph viewer)
- ORCID Verification Guide: https://github.com/joesch21/Ian_Buchanan_Vault/blob/main/docs/ORCID_Verification_Guide.md
- Wikipedia Update Guide: https://github.com/joesch21/Ian_Buchanan_Vault/blob/main/docs/Wikipedia_Update_Guide.md
- Cartography API notes (from README): Points to backend for dynamic concept graphs (`VITE_CARTO_API_BASE`, `VITE_DEFAULT_SITE_ID=buchanan-vault`).
- Individual scholar sources: ORCID and institutional links already embedded in scholars.json.

These links expand the external evidence spine and may inform future automated ingestion or cross-platform queries (under strict human review).

## 3. Relation to Existing Layers & Blueprints

| Layer | Impact of Addition | Authority Level |
|-------|--------------------|-----------------|
| Citation & Provenance | Adds verifiable scholar records and source links; book covers as optional visual metadata | Primary (strengthens) |
| Semantic Concept | Groups and defaultConcepts provide seed clusters (e.g., "assemblage") for concept_mentions expansion | Structural |
| Psycho-Linguistic (Experimental) | Book covers and schizoanalysis-themed images offer visual correlates for affective pressure, metaphorical density zones in related texts | Secondary / Observational |
| Reader Transformation | Potential future: visual "entry points" into dense passages | Tertiary (future) |

All additions remain **read-only** with respect to canonical tables. No existing passage or concept records were modified.

## 4. Risks, Limitations & Safeguards (per Blueprint §7)

- **Over-interpretation**: Images/filenames are indicative only; exact edition-to-passage mapping requires citation verification.
- **Scope creep**: This is documentation-level integration only. No code changes, no automatic flagging in Dark Precursor or Evidence Cards.
- **Reproducibility**: Data extracted at a point in time; Vault may evolve. Record commit or date in future patches.
- **Safeguard**: All outputs labelled experimental where appropriate. Human review gate before any surface integration.

## 5. Compliance with Governance

- **Patch workflow**: This addition is recorded via documentation (this file + data/manifest). Future binary or architectural changes should be delivered as patch bundles per `WORKFLOW_PATCH_APPLICATION.md` (once read).
- **Documentation update**: This file itself satisfies the mandatory update rule for resource layer expansion.
- **Invariants**: Does not contradict `BUCHANAN_SYSTEM_STATE.json` (assumed current phase allows experimental resource enrichment). If invariants block, flag for review.
- **Buchanan voice**: Integration remains conceptually faithful — focused on how these resources support observation of meaning-production (metaphor, recursion, affective force) in the texts, without reductive claims about authorial intent.

## 6. Next Steps (Recommended, Subject to Review)

1. Read/confirm mandatory onboarding docs if not already completed (especially `BUCHANAN_THREAD_HANDOVER.md`, `docs/HOW_WE_WORK.md`, `BUCHANAN_SYSTEM_STATE.json`).
2. Human review of scholars.json against existing citation spine for duplicates/aliases.
3. Curate high-value images (e.g., *The Incomplete Project of Schizoanalysis*, Anti-Oedipus cover) for potential attachment to relevant source records.
4. If approved, prepare patch bundle to:
   - Merge scholars/groups into core data layer.
   - Extend source schema with optional `visual_assets` array.
   - Update Evidence Card template to support image previews (labelled experimental).
5. Explore Vault's Cartography API for possible future concept-graph enrichment of the Dark Precursor.
6. Test Level 2 embedding deviation on passages from newly linked texts (once full texts available).

## 7. Questions for Clarification

Per onboarding: If the current phase invariants, patch process details, or how these resources map to specific Buchanan 1997 (or other) passages are unclear, provide guidance before deeper implementation.

**This integration expands the observable texture of the philosophical corpus available to the platform while preserving strict separation between descriptive resources and interpretive claims.**

---

**End of Integration Record**  
*Persisted to project artifacts as part of governed addition of Vault resources.*