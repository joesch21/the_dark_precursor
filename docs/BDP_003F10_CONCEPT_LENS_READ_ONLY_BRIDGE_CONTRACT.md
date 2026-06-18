# BDP-003F.10 — Concept Lens Existing Archive Evidence Readback Bridge Contract

**Status:** Complete
**Controlled slice:** read-only bridge contract definition only
**Authority:** Contract only; no implementation, no frontend wiring, no database mutation
**Prior phase:** BDP-003F.9 — Concept Lens Evidence Posture Output Review
**Target service:** `scripts/concept_lens_archive_evidence_posture_service.py`

## Purpose

BDP-003F.10 defines the approved read-only bridge contract from existing governed archive evidence readback into the BDP-003F.8 Concept Lens archive evidence posture service.

BDP-003F.9 recorded Outcome C:

```text
The archive evidence exists in governed project state, but no approved live readback adapter is currently exposed for the Concept Lens service default path.
```

BDP-003F.10 answers the next narrow question:

```text
What read-only bridge is allowed to translate existing archive evidence readback into F8-compatible Concept Lens evidence posture rows?
```

This phase defines the bridge contract only. It does not implement the bridge.

## Boundary

BDP-003F.10 does not add, approve, or modify:

1. frontend wiring;
2. Concept Lens UI dock;
3. Streamlit controls;
4. new navigation surface keys;
5. backend routes;
6. adapter endpoints;
7. SQL migrations;
8. database tables;
9. database mutation;
10. citation creation;
11. concept mention creation;
12. concept relation creation;
13. interpretation insertion;
14. evidence promotion;
15. Buchanan-specific claims;
16. automatic chat filtering;
17. external LLM routing;
18. philosophical fidelity review;
19. the F8 service implementation.

## Approved bridge contract name

```text
concept_lens_existing_archive_evidence_readback_bridge.v1
```

Future implementation target, if later approved:

```text
scripts/concept_lens_existing_archive_evidence_readback_bridge.py
```

Future function name, if later approved:

```text
read_existing_archive_evidence_rows_for_concept
```

BDP-003F.10 does not create that module or function. It defines the contract for a later implementation slice.

## Bridge role

The bridge has one role:

```text
Translate approved existing read-only archive evidence readback into supplied archive rows that the BDP-003F.8 service can classify.
```

The bridge is not a second concept engine. It is not a UI feature. It is not an interpretation service. It must not make a Buchanan-specific claim. It only prepares read-only evidence rows for the existing F8 posture classifier.

## Approved source readback candidates

The bridge may use existing governed readback paths only after inspecting them in the local repository.

Known candidate readback scripts from earlier Body without Organs phases include:

```text
scripts/read_bdp_001r_bwo_source_bound_description.py
scripts/read_bdp_002b_bwo_evidence_card.py
```

These are candidates because earlier project state records Body without Organs evidence posture through the chain:

```text
concepts -> concept_mentions -> passages -> citations -> sources
```

A later implementation phase must inspect the current repository before binding to either script. If a script is missing, renamed, or no longer safe, the implementation must stop and report the mismatch rather than inventing evidence.

## Target service handoff

The bridge must feed rows into the existing F8 service function:

```text
read_concept_lens_archive_evidence_posture
```

Target module:

```text
scripts/concept_lens_archive_evidence_posture_service.py
```

The F8 service remains the posture classifier. The bridge must not duplicate or bypass the F8 posture decision rules.

## Allowed bridge inputs

A later bridge implementation may accept only:

1. a requested concept string;
2. an explicit local readback mode or local archive source configuration;
3. bounded read-only process or file output from approved existing readback scripts;
4. optional operator-supplied local database connection details already accepted by the F8 service boundary.

The bridge must reject or ignore:

1. generated concept-card drafts;
2. unreviewed cinematic synthesis;
3. chat responses;
4. arbitrary external LLM output;
5. unknown scripts;
6. write-capable database handles;
7. source-candidate or passage-candidate material unless a later phase explicitly approves those optional layers.

## Required bridge output shape

The bridge output must be an in-memory list of F8-compatible archive evidence rows. Rows must preserve the primary chain fields needed to establish posture:

```text
concept
normalized_concept
concept_review_status
concept_mention_review_status
mention_type
passage_id
citation_id
source_id
source_author
source_title
source_type
source_year
source_doi
locator
rights_status
rights_display_rule
authority_label
passage_text_display
chain_complete
```

The bridge may include additional metadata when available, but it must not add interpretive claims or unsupported concept relations.

## Required classification handoff

For a known complete Body without Organs chain, the bridge may allow the F8 service to classify the result as:

```text
archive_lookup_status: archive_grounded_match
evidence_posture: archive_grounded
```

only if the current repository readback confirms a complete primary chain:

```text
concept -> reviewed concept mention -> passage -> citation -> source
```

If any part of the chain is missing, inaccessible, restricted beyond metadata display, or not reviewed, the bridge must pass rows that cause the F8 service to classify more conservatively.

## Rights boundary

The bridge must preserve the existing rights boundary.

Restricted passage text must not be reproduced. The bridge may pass metadata, locators, source identifiers, rights status, and source-bound evidence posture. For restricted material, the bridge must keep passage text display as:

```text
omitted_by_rights_policy
```

or an equivalent F8-recognized omission marker.

## Failure posture

Failure to find or parse existing archive evidence is not a runtime failure of the Concept Lens.

The bridge must return an empty row list or an explicit safe no-match structure that allows F8 to produce:

```text
archive_lookup_status: no_archive_match
evidence_posture: exploratory_unverified
```

The bridge must never fabricate archive evidence to make a concept appear grounded.

## Body without Organs expected review case

Body without Organs is the required first implementation review case for the later bridge implementation.

Expected implementation review question:

```text
When the approved bridge is configured, does Body without Organs return archive_grounded through the F8 service without reproducing restricted passage text or creating new claims?
```

If the answer is yes, that only authorizes evidence posture readback. It does not authorize a Buchanan-specific explanation, interpretation, relation graph, or frontend UI.

## UI integration status

UI integration remains blocked.

BDP-003F.10 does not approve:

1. Concept Lens frontend dock;
2. sidebar controls;
3. page navigation changes;
4. live UI archive calls;
5. automatic chat filtering;
6. any visible claim that the Concept Lens is archive-grounded for a concept.

Frontend work must wait until the bridge is implemented, verified against Body without Organs, and then separately reviewed before UI integration.

## Verification requirement

F10 verification must confirm:

1. BDP-003F.9 review output exists;
2. the F8 service still exists and compiles;
3. this document defines a bridge contract only;
4. the contract names the existing readback candidates;
5. the contract preserves the primary archive chain;
6. UI integration remains blocked;
7. the next safe step is implementation of the bridge, not frontend wiring.

## Next safe step

```text
BDP-003F.11 — Implement the approved read-only bridge from existing archive evidence readback into the Concept Lens service.
```
