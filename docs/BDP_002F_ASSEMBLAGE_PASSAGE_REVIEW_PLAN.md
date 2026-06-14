# BDP-002F — Assemblage Passage Review Plan

**Status:** Active Phase  
**Phase Type:** Passage Review & Preparation (Read-only)  
**Predecessor:** BDP-002E  
**Date:** 14 June 2026

## 1. Purpose

BDP-002F prepares a high-quality set of reviewed, rights-aware passage candidates from Ian Buchanan’s book *Assemblage Theory and Method* (2021). These passages will form the foundation of the **Assemblage** evidence spine as a Tier 1 Anchor Concept.

This phase focuses on **targeted review and preparation** rather than exhaustive coverage of the book. It maintains strict governance boundaries: no database insertion, no citations, and no interpretive claims.

## 2. Scope and Boundaries

### In Scope
- Identify and review the most important passages that articulate Buchanan’s distinctive reading of assemblage.
- Prioritise passages covering:
  - Assemblage as **process**
  - The **two axes** (Content/Expression + Territorialisation/Deterritorialisation)
  - Relation to **strata** and **desire**
  - Buchanan’s critique of DeLanda, ANT, and New Materialism
  - Connection to the **Body without Organs**
- Record short excerpts and precise page locators.
- Mark passages as reviewed and ready for later governed phases.

### Out of Scope
- Inserting passages into the canonical `passages` table.
- Creating citations or concept mentions.
- Generating interpretive claims about Buchanan’s position.
- Full book coverage (targeted selection only).

## 3. Priority Passage Categories

| Priority | Category                        | Focus Areas                                      |
|----------|----------------------------------|--------------------------------------------------|
| 1        | Core Definition & Method        | Process vs thing/network, return to Deleuze & Guattari |
| 2        | Two Axes                        | Content/Expression + Territorialisation/Deterritorialisation |
| 3        | Critique of Existing Theory     | DeLanda, Actor-Network Theory, New Materialism   |
| 4        | Strata, Desire & BwO            | Consistency, coding, relation to Body without Organs |
| 5        | Analytical & Political Use      | How Buchanan applies assemblage in analysis      |

## 4. Deliverables

- `docs/BDP_002F_ASSEMBLAGE_PASSAGE_REVIEW_PLAN.md` (this document)
- `docs/BDP_002F_KEY_PASSAGES_REVIEWED.md`
- State update in `ai_boot/BUCHANAN_SYSTEM_STATE.json`
- `scripts/update_bdp_002f_assemblage_passages.py`
- `scripts/verify_bdp_002f_assemblage_passages.py`

## 5. Authority Labels

- `passage_candidate_review`
- `metadata`
- `record_description`
- `buchanan_pending`
- `blocked_until_governed_citation_phase`

## 6. Verifier Requirements

The verifier must confirm:
- Only review and preparation activities occurred.
- No canonical passages, citations, or concept mentions were created.
- Reviewed passages are clearly linked to Buchanan’s key arguments.
- All records carry appropriate authority labels.
- No interpretive claims were generated.

## 7. Next Recommended Phases

- **BDP-002G** — Insert reviewed passages and citations.
- **BDP-002H** — Link passages to the **Assemblage** concept via reviewed concept mentions.
- **BDP-002I** — Develop Visual Exploration Mode based on Buchanan’s two-axis model.

**End of Document**