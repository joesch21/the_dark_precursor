# BDP-001R — Source-Bound Description Candidate

**Status:** Implementation Slice  
**Version:** 1.0  
**Date:** 14 June 2026  
**Related:** `BUCHANAN_SEMANTIC_WORKBENCH.md`, `BUCHANAN_CONCEPT_ONTOLOGY.md`, `BUCHANAN_CITATION_AND_RIGHTS.md`, `BDP_002C_RICHER_SEMANTIC_READBACK_SURFACE.md`, `BDP-001N.1 Description vs Claim Rule`

## 1. Purpose

BDP-001R prepares the **first source-bound description** of the Buchanan `Body without Organs` evidence posture.

This phase operates **strictly in description mode**. It describes the current governed records and evidence chain without attributing conceptual meaning, theoretical consequence, position, or argument to Ian Buchanan.

It follows directly after BDP-002C (richer semantic readback surface) and prepares the ground for any future interpretation layer.

## 2. Core Rule (Description vs Claim)

From BDP-001N.1:

> A description may report the state of reviewed records, locators, excerpts, and evidence posture.  
> A description becomes a claim when it attributes any of the following to Buchanan, Deleuze, Guattari, or another author: position, argument, intention, conceptual meaning, or theoretical consequence.

**BDP-001R produces descriptions only.**

## 3. Scope of BDP-001R

BDP-001R shall produce:

- A **source-bound description** of the existing evidence chain for `Body without Organs` from the 1997 Buchanan article.
- A **secondary_scholarship posture** description for the three new Buchanan PDFs added in BDP-002C (metadata-only).
- Clear statements of what is **blocked** (interpretation, relation, Buchanan-specific claim).
- Updated evidence posture suitable for display in the richer readback surface or future Evidence Cards.

BDP-001R does **not**:
- Create new database records (passages, citations, concept mentions, etc.)
- Generate interpretive content
- Upgrade any Buchanan explanation status beyond `buchanan_pending`

## 4. Required Output Structure

The phase shall produce a **Source-Bound Description Document** containing at minimum:

1. **Evidence Chain Summary** (with authority labels)
2. **Buchanan Article Posture** (1997 source)
3. **Secondary Scholarship Posture** (the three new PDFs)
4. **Blocked Layers** (relation, interpretation, Buchanan claim)
5. **Rights & Display Status**
6. **Next Recommended Governed Action**
7. **Authority Label Summary**

Every section must carry an explicit authority label from the controlled set (especially `source_bound_description`, `record_description`, `secondary_scholarship`, `buchanan_pending`).

## 5. Authority Labels for This Phase

Approved labels for BDP-001R outputs:

- `source_bound_description`
- `record_description`
- `secondary_scholarship`
- `buchanan_pending`
- `blocked_until_governed_interpretation_phase`
- `blocked_until_reviewed_relation_evidence`
- `rights_display_boundary`
- `metadata`

## 6. Integration with BDP-002C Richer Card

The description produced in BDP-001R should be suitable for insertion into the richer semantic readback surface (section 10 or 11) as an authoritative `source_bound_description`.

It must not contradict or override any existing labels or blocked statuses shown in the BDP-002C card.

## 7. Rights Boundary

- All PDFs remain `restricted` / `reference_only`
- No long excerpts or article reproduction
- Secondary PDFs (VtUTk, XJVks, Tl9xR) are described at **metadata level only**

## 8. Verifier Requirements

Any script or output for BDP-001R must be verified against:

- No database mutation performed
- No author-position or interpretive language generated
- All sections carry correct authority labels
- Current DB invariant preserved
- Buchanan explanation status remains `buchanan_pending` / blocked

## 9. Success Criteria

BDP-001R is successful when:

- A clean, labelled source-bound description exists for the current `Body without Organs` evidence posture.
- The description stays strictly within the “description of records” boundary.
- It can be safely referenced by the richer readback surface without creating interpretive claims.
- The platform remains ready for a later governed interpretation phase.

**End of Document**

## 10. Implementation Deliverables

BDP-001R deliverables:

```text
docs/BDP_001R_Source_Bound_Description.md
docs/BDP_001R_BWO_SOURCE_BOUND_DESCRIPTION.md
scripts/read_bdp_001r_bwo_source_bound_description.py
scripts/verify_bdp_001r_source_bound_description.py
scripts/update_bdp_001r_docs_and_state.py
```

No SQL migration is added.
No database mutation is performed.
No frontend renderer is added.

## 11. SQL Boundary

The readback script may pass only `SELECT` SQL to `psql`.
The verifier must inspect SQL strings actually passed to the psql helper.
It must not treat governance prose or future-action descriptions as database mutation.

## 12. Controlled Source-Bound Statement

The following description is allowed for BDP-001R:

```text
The database records a restricted citation-backed Buchanan passage from the 1997 article and a reviewed direct concept mention linking that passage record to Body without Organs.
```

This statement describes governed records only. It does not attribute a position, argument, intention, conceptual meaning, or theoretical consequence to Ian Buchanan, Deleuze, or Guattari.
