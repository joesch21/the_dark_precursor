# BDP-003E.7 — Local Reviewed Concept Card Archive Writer Contract

**Status:** Complete  
**Phase type:** Contract only  
**Decision:** Writer contract is defined as a future boundary; implementation is not approved.

---

## Purpose

BDP-003E.7 defines the contract for a future local reviewed concept card archive writer.

This phase does not implement that writer. It only states what a later writer would be allowed to accept, validate, refuse, and report if a future implementation-bound phase authorizes construction.

The contract exists because BDP-003E.6 found the BDP-003E.5 archive schema candidate suitable for reviewed sample comparison, but explicitly kept implementation blocked.

---

## Review Inputs

1. **BDP-003E.3 exported cinematic concept card sample cases**  
   Generated/exported sample material used for review only.

2. **BDP-003E.5 local reviewed archive schema candidate**  
   Candidate schema for preserving reviewed concept card samples locally in a future phase.

3. **BDP-003E.6 archive schema sample review**  
   Review decision that the schema candidate is suitable for reviewed sample comparison while implementation remains blocked.

---

## Governance Boundary

BDP-003E.7 is a writer contract phase only.

Implementation is not approved.

This phase does **not**:

1. implement a writer,
2. create archive folders,
3. write local files,
4. add frontend archive buttons,
5. add backend services,
6. add adapter endpoints,
7. add database tables,
8. add SQL migrations,
9. persist generated concept cards,
10. promote generated concept cards into evidence,
11. create citations,
12. create concept relations,
13. create interpretations,
14. create Buchanan-specific claims.

The word `writer` in this document means a future contract boundary only. It does not indicate that a writer exists.

---

## Writer Contract Scope

A future local reviewed concept card archive writer, if later approved, must be constrained to local reviewed sample preservation only.

It must not become an evidence-ingestion mechanism, a citation creator, a Buchanan claim generator, or a hidden persistence path for generated content.

The contract has five bounded responsibilities:

1. **Accept a reviewed concept card archive candidate**  
   The future writer may accept a candidate record shaped by the BDP-003E.5 schema candidate and reviewed under the BDP-003E.6 sample review boundary.

2. **Validate required review fields**  
   The future writer must validate that sample identity, concept identity, export context, reviewer decision, reviewer notes, governance flags, and provenance references are present before any future write could be allowed.

3. **Reject authority escalation**  
   The future writer must reject any payload that claims the reviewed card is canonical evidence, a citation-backed claim, a concept relation, an interpretation, or a Buchanan-specific assertion.

4. **Preserve local-only status**  
   The future writer must keep reviewed cinematic concept cards local and separate from the evidence spine unless a later governed evidence-promotion phase explicitly authorizes a different path.

5. **Return an auditable result**  
   The future writer must report whether a future archive operation would be accepted or refused, and explain the governance reason without creating scholarly authority.

---

## Contract Inputs

A future implementation may only be considered if it accepts a bounded candidate record with these conceptual fields:

1. `archive_record_id` — stable local identifier for the reviewed sample record.
2. `source_phase` — phase lineage such as BDP-003E.3, BDP-003E.5, and BDP-003E.6.
3. `concept_id` — local concept identifier from the concept card context.
4. `concept_label` — human-readable concept label.
5. `export_sample_id` — exported cinematic concept card sample identifier.
6. `review_decision` — accepted, rejected, deferred, or changes requested.
7. `reviewer_notes` — local review notes, not evidence claims.
8. `governance_flags` — local reviewed status, generated sample status, evidence promotion blocked status.
9. `provenance` — references to the relevant BDP phase documents and sample review context.
10. `created_at` — local timestamp for future traceability.

These fields define a contract surface only. They do not create a file, folder, table, endpoint, or UI control.

---

## Required Refusals

A future writer must refuse any candidate that attempts to:

1. bypass the evidence spine,
2. convert a cinematic sample into a Buchanan claim,
3. create or imply a citation,
4. create a concept relation,
5. create an interpretation,
6. write to a database,
7. write to a remote service,
8. expose an adapter endpoint,
9. treat generated text as source evidence,
10. hide provenance or review status.

---

## Contract Output Shape

A future writer contract response should distinguish contract evaluation from persistence.

A valid future response shape may contain:

1. `accepted_by_contract` — whether the candidate satisfies the contract.
2. `refusal_reasons` — governance reasons for refusal, if any.
3. `required_fields_present` — validation result for required contract fields.
4. `authority_boundary` — confirmation that the record remains local reviewed sample material only.
5. `evidence_promotion` — always blocked unless a later governed evidence phase changes the rule.
6. `implementation_status` — must not claim that persistence has occurred unless a later implementation phase exists.

This response shape is descriptive only in BDP-003E.7.

---

## Decision

The local reviewed concept card archive writer contract is defined sufficiently for a later boundary review.

Implementation is not approved.

The correct next step is to review this writer contract against the archive schema and implementation boundaries before any code is allowed.

---

## Next Step

**BDP-003E.8 — Review local reviewed concept card archive writer contract against archive boundaries before implementation.**
