# Integration of Methodological and Resource Documents into the Application

**Status:** Practical Integration Guidance (Governed)  
**Version:** 0.1  
**Date:** June 15, 2026  
**Applies to:** The Dark Precursor (frontend/dark_precursor.py) and supporting layers of the Buchanan Deleuze Intelligence Platform.  
**Related:** All persisted methodological documents in /artifacts/docs/, `NEW_THREAD_ONBOARDING.md`, `BUCHANAN_PSYCHOLINGUISTIC_MODELLING_BLUEPRINT.md`.

## 1. Nature of These Documents

The documents created in this thread (Vault resource integration, usable elements assessment, Deleuzian concept mapping investigation, differential method exploration, and this guide) are **governed reference and methodological records**. They are not:

- Raw passage data for the citation spine.
- Training data or direct RAG corpus for the generative model.
- Automatic inputs to Evidence Cards or concept graphs.

They are:

- Documentation updates triggered by resource and methodological exploration (mandatory per governance).
- Records of how external resources (Vault) and Buchanan’s own methods (differential, rhizomatic) can inform platform development.
- Operator and developer reference material.

## 2. How to Use Them in the Application

### 2.1 Operator-Facing Reference (Immediate, Low-Risk)
- **Location**: Move or copy the key MD files into the project’s official `docs/` directory (alongside `HOW_WE_WORK.md`, `DOCS_UPDATE_POLICY.md`, etc.).
- **In The Dark Precursor (Streamlit)**: Add a collapsible “Governed References” or “Methodological Resources” panel/sidebar section. Use Streamlit’s `st.expander` or `st.tabs` to load and display selected documents (or summaries) for human operators during sessions.
  - Purpose: Supports informed use of differential reading, rhizomatic mapping perspectives, and Vault resources without bypassing human governance or the evidence spine.
  - Labelling: Clearly mark as “Reference — Human Review Required for Application”.
- **Benefit**: Operators can consult Buchanan’s differential method or rhizomatic principles while exploring passages or concepts, maintaining conceptual fidelity.

### 2.2 Semantic Concept Layer Enrichment (Experimental, Patch-Required)
- Curate a small set of high-value concepts from these documents (e.g., “differential method”, “specific causality”, “flows via interruption/subtraction”, “rhizomatic cartography”, “qualitative differentiation”) .
- Add them to the semantic concept store or `concept_mentions` with:
  - Full provenance (e.g., “Buchanan, I. (2022). Deleuze and Guattari’s Differential Method. Lecture at Institute of Philosophy, Czech Academy of Sciences.” + link to persisted doc).
  - Experimental label: `experimental_methodological_annotation`.
  - Read-only status: Never auto-link to passages or promote to canonical concepts.
- These enrich the layer for future differential/rhizomatic graph features without altering the evidence spine.

### 2.3 Psycho-Linguistic Modelling Support (Experimental)
- Use excerpts from Buchanan’s lecture (or the differential method exploration) as test material for Level 2 embedding deviation or higher-level metaphor density work.
- Example: Identify passages in the lecture where differential distinctions (weapons/tools, addition/subtraction) are performed linguistically — these are zones of conceptual intensity and movement.
- Outputs must carry full authority labels and remain subject to human review before influencing any surface.

### 2.4 Interface and Architectural Influence (Future Patch)
- The Dark Precursor can incorporate differential tracing tools or rhizomatic map overlays informed by these documents (e.g., UI elements for marking flows, interruptions, qualitative distinctions, lines of flight).
- Any such feature must be developed as a patch bundle, with this document (and related ones) referenced in the patch notes.
- Update `BUCHANAN_SYSTEM_STATE.json` if invariants around experimental modules or control surfaces are affected.

### 2.5 Developer / Governance Use
- These documents serve as the living record for thread handovers, patch proposals, and compliance checks.
- Before any code change that touches architecture or control surfaces, re-read the relevant methodological document(s) to ensure fidelity to differential/rhizomatic principles and governance.

## 3. Recommended Immediate Actions

1. Create or confirm the project `docs/` directory and move the methodological MD files there (or create symlinks/references from artifacts).
2. In `frontend/dark_precursor.py`, implement a simple governed references panel (using `st.markdown` or file loaders with caching disabled for freshness).
3. Document the panel addition itself as a minor patch or note in the next bundle.
4. For any RAG or LLM context loading: Implement strict allow-list + human approval workflow; these methodological docs should be in a separate “governed references” namespace, never mixed with citation/provenance data.

## 4. Risks and Safeguards

- **Direct LLM Ingestion without Review**: These docs contain interpretive and methodological claims. Auto-feeding them into generative responses risks bypassing the evidence spine and producing reductive readings. Mitigation: Human-curated excerpts only; clear labelling.
- **Confusion with Canonical Data**: Distinguish clearly between “reference methodology” and “citation/provenance evidence”.
- **Scope Creep**: Integration must remain experimental until reviewed. No automatic promotion of concepts or features.

## 5. Conceptual Fidelity

These documents enlarge the observable field of Buchanan’s own methods and the resources that support Deleuzian studies. They do not replace close reading of primary texts or the citation spine. Their proper use in the application is to support attentive, differential, human-governed exploration of how meaning moves through philosophical language — exactly the purpose of the psycho-linguistic layer and The Dark Precursor.

---

**Persisted as integration guidance.**  
**Any implementation of the recommendations above must be accompanied by a patch bundle and further documentation update.**  
**End of Guidance.**