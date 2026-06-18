# BDP-003F.7 — Concept Lens Archive Evidence Posture Service Contract

**Status:** Complete  
**Completed:** 2026-06-18T02:20:00+00:00  
**Controlled slice:** service contract only  
**Authority:** Application contract / archive readback governance only  
**Frontend implementation:** No  
**Backend service implementation:** No  
**Database mutation:** No  
**SQL migration:** No  

## Purpose

BDP-003F.7 defines the contract for a future **read-only Concept Lens archive evidence posture service**.

BDP-003F.6 defined the Concept Lens as a future archive-grounded Deleuzian concept exploration dock inside The Dark Precursor concept stage. BDP-003F.7 now defines how a later service may report what the Buchanan SQL archive currently supports for a requested concept.

This phase does not implement the service. It defines the service boundary, input shape, output shape, evidence posture rules, authority labels, rights boundaries, and blocked actions before any code is written.

## Service contract name

Future implementation candidate:

```text
concept_lens_archive_evidence_posture_service.v1
```

Potential future function name:

```text
read_concept_lens_archive_evidence_posture
```

This is a contract name only. BDP-003F.7 does not add the service module, route, frontend call, SQL query, database table, or adapter endpoint.

## Contract role

The future service should answer one narrow question:

```text
For this requested concept, what does the archive currently support?
```

It must not answer the whole philosophical question by itself. It must provide evidence posture for a later Concept Lens answer.

The service is a **readback contract**, not a generation contract.

## Input contract candidate

A future implementation should accept a bounded input shape similar to:

```json
{
  "schema_id": "bdp_003f7_concept_lens_archive_evidence_posture_request_v1",
  "raw_concept_query": "we repress because we repeat",
  "normalized_concept": "repetition",
  "requested_answer_mode": "student",
  "include_optional_layers": false,
  "rights_display_policy": "reference_only_when_restricted"
}
```

### Input field meanings

1. `raw_concept_query` — the user's phrase or concept question fragment.
2. `normalized_concept` — the resolved concept key used for archive lookup.
3. `requested_answer_mode` — optional future hint such as `student`, `technical`, `archive`, or `cinematic`.
4. `include_optional_layers` — defaults to false; optional layers must not be used silently.
5. `rights_display_policy` — controls excerpt display and restricted text handling.

The future service must tolerate missing archive matches without fabricating evidence.

## Primary read-only archive chain

The future service may read the existing evidence spine only through the primary chain:

```text
concepts
  -> concept_mentions
  -> passages
  -> citations
  -> sources
```

This chain is the contract center.

The service must not create or update any row in these tables.

## Optional future layers

The following layers are optional and blocked unless later explicitly approved:

```text
concept_relations
interpretations
source_candidates
passage_candidates
```

If a later phase permits optional layers, the output must visibly separate primary evidence from optional contextual material.

## Output contract candidate

A future implementation should return a bounded evidence posture object similar to:

```json
{
  "schema_id": "bdp_003f7_concept_lens_archive_evidence_posture_result_v1",
  "concept": "repetition",
  "normalized_concept": "repetition",
  "archive_lookup_status": "no_archive_match",
  "evidence_posture": "exploratory_unverified",
  "authority_label": "system_synthesis",
  "buchanan_specific_claim_allowed": false,
  "archive_chain": [],
  "matched_records": {
    "concepts": 0,
    "concept_mentions": 0,
    "passages": 0,
    "citations": 0,
    "sources": 0
  },
  "rights_display_rule": "reference_only_when_restricted",
  "passage_text_display": "omitted_until_allowed_by_rights_policy",
  "interpretation_available": false,
  "concept_relation_available": false,
  "human_review_required": true,
  "blocked_actions": [
    "no database mutation",
    "no citation creation",
    "no concept mention creation",
    "no concept relation creation",
    "no interpretation insertion",
    "no evidence promotion",
    "no Buchanan-specific claim without exact governed evidence"
  ]
}
```

## Archive chain item candidate

When the archive contains evidence, each chain item should remain compact and rights-aware:

```json
{
  "concept_id": "...",
  "concept_name": "Body without Organs",
  "concept_mention_id": "...",
  "mention_type": "direct",
  "review_status": "accepted",
  "passage_id": "...",
  "passage_locator": "printed article page 76; PDF page 4",
  "passage_text_display": "omitted_by_rights_policy",
  "citation_id": "...",
  "source_id": "...",
  "source_author": "Ian Buchanan",
  "source_title": "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?",
  "rights_status": "restricted",
  "authority_label": "buchanan_direct"
}
```

The future service should return enough structure for the Concept Lens to explain authority posture, but not enough to reproduce restricted source text improperly.

## Evidence posture decision rules

A future implementation should classify evidence posture conservatively.

### `archive_grounded`

Use only when the archive has a resolved concept linked through reviewed concept mention, passage, citation, and source records.

This means the archive can support a bounded evidence posture. It still does not automatically authorize a broad Buchanan interpretation.

### `source_bound_description`

Use when the archive can describe a reviewed record, locator, source, or concept link, but cannot support an interpretive claim.

This is the default posture for many early archive-backed records.

### `secondary_scholarship_supported`

Use only when reviewed secondary scholarship evidence has been explicitly permitted for the concept posture.

Metadata alone is not enough to create author-position claims.

### `system_synthesis`

Use when the answer may be useful as a generated concept explanation, but the archive does not currently ground the requested claim.

The Concept Lens may still explain the concept, but it must label the answer as synthesis.

### `exploratory_unverified`

Use when the concept is not found or when archive support is too thin to support even source-bound description.

The future Concept Lens should make this visible to students and users.

## Archive lookup statuses

The future service should use explicit lookup statuses:

```text
archive_grounded_match
source_bound_match
concept_found_without_reviewed_evidence
no_archive_match
ambiguous_concept_match
rights_restricted_match
optional_layer_required_but_blocked
```

The status must make absence visible. Missing archive evidence is not a failure; it is a valid evidence posture.

## Authority labels

The future service must preserve the authority ladder:

```text
primary_text
buchanan_direct
secondary_scholarship
system_synthesis
user_interpretation
```

It must not upgrade `system_synthesis` into `buchanan_direct`.

It must not treat a source candidate, metadata record, or generated answer as citation-backed interpretation.

## Buchanan-specific claim boundary

The future service must never authorize claims such as:

```text
Buchanan argues X.
Buchanan's reading is X.
Buchanan would say X.
```

unless a later governed path confirms exact evidence capable of supporting that claim.

The service may only report evidence posture:

```text
The archive currently contains / does not contain reviewed evidence for this concept chain.
```

## Rights and excerpt boundary

The future service must respect rights display policy.

Restricted source text must remain omitted or reference-only unless a later rights-governed phase permits display.

Allowed output:

```text
source metadata
locator
short governed excerpt only when allowed
rights status
citation metadata
evidence posture
```

Blocked output:

```text
long restricted quotation
ungoverned passage reproduction
automatic citation insertion
automatic interpretation insertion
```

## Relationship to the Concept Lens answer

The service returns evidence posture only. A later Concept Lens answer may combine:

1. plain explanation,
2. technical Deleuzian explanation,
3. archive evidence posture,
4. fidelity warning.

BDP-003F.7 defines only layer 3.

## Relationship to philosophical fidelity review

The service does not perform philosophical fidelity review.

It may provide archive posture to a later fidelity layer, but it does not judge whether an explanation flattens Deleuze, Guattari, or Buchanan.

A later phase may define the fidelity review contract separately.

## Explicit non-goals

BDP-003F.7 does not add:

1. frontend implementation,
2. Streamlit controls,
3. Concept Lens UI dock,
4. new navigation surface keys,
5. backend service code,
6. route handlers,
7. adapter endpoints,
8. SQL queries,
9. SQL migrations,
10. database tables,
11. database mutation,
12. source ingestion,
13. citation creation,
14. concept mention creation,
15. concept relation creation,
16. interpretation insertion,
17. evidence promotion,
18. Buchanan-specific claims,
19. external LLM routing,
20. automatic chat filtering,
21. hidden personalization,
22. psychological assessment.

## Future safe sequence

Recommended future sequence:

1. **BDP-003F.8** — Implement read-only Concept Lens archive evidence posture service behind this contract, if approved.

Plain next safe step:

```text
BDP-003F.8 — Implement read-only Concept Lens archive evidence posture service behind this contract, if approved.
```
2. **BDP-003F.9** — Review service output against known archive cases before UI integration.
3. **BDP-003F.10** — Define Concept Lens frontend dock integration contract before wiring.
