# BDP-003F.11 — Concept Lens Existing Archive Evidence Readback Bridge Implementation

**Status:** Complete
**Controlled slice:** read-only bridge implementation only
**Authority:** Read-only archive readback bridge implementation; no UI wiring; no database mutation
**Contract source:** `docs/BDP_003F10_CONCEPT_LENS_READ_ONLY_BRIDGE_CONTRACT.md`
**Target service:** `scripts/concept_lens_archive_evidence_posture_service.py`
**Bridge module:** `scripts/concept_lens_existing_archive_evidence_readback_bridge.py`

## Purpose

BDP-003F.11 implements the approved read-only bridge defined by BDP-003F.10.

BDP-003F.9 recorded Outcome C: the governed archive evidence exists in project state, but no approved live readback adapter was exposed for the Concept Lens service default path. BDP-003F.10 defined the bridge contract. BDP-003F.11 now implements the first bounded bridge layer that can translate existing governed archive readback into F8-compatible in-memory evidence rows.

The implementation answers one narrow question:

```text
Can existing approved archive evidence readback be transformed into rows that the BDP-003F.8 service can classify, without creating new evidence or claims?
```

## Implementation

BDP-003F.11 adds:

```text
scripts/concept_lens_existing_archive_evidence_readback_bridge.py
```

Primary bridge function:

```text
read_existing_archive_evidence_rows_for_concept
```

Review/test helper:

```text
read_existing_archive_evidence_rows_from_readback_text
```

The bridge is intentionally narrow. The first supported governed review case is:

```text
Body without Organs
```

The bridge can inspect approved local readback scripts if they are present:

```text
scripts/read_bdp_001r_bwo_source_bound_description.py
scripts/read_bdp_002b_bwo_evidence_card.py
```

It does not assume those scripts are always present or always successful. If a script is missing, fails, or emits insufficient evidence signals, the bridge returns an empty row list rather than fabricating archive support.

## Target service integration

BDP-003F.11 adds a small integration wrapper to the BDP-003F.8 service:

```text
read_concept_lens_archive_evidence_posture_via_existing_archive_bridge
```

The existing F8 service remains the posture classifier. The bridge supplies rows; the service classifies those rows.

The wrapper does not replace or bypass:

```text
read_concept_lens_archive_evidence_posture
```

## Required bridge output shape

For a valid Body without Organs readback, the bridge returns F8-compatible rows with the primary evidence chain fields:

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

The bridge also includes conservative provenance fields such as:

```text
bridge_contract
bridge_source
bridge_review_case
bridge_source_script
```

## Rights boundary

Restricted passage text is not reproduced.

For restricted material, the bridge emits:

```text
passage_text_display: omitted_by_rights_policy
rights_display_rule: reference_only
```

The bridge may pass metadata, source identifiers, locators, rights status, source title, source author, and DOI. It must not pass long restricted quotation text.

## Buchanan-specific claim boundary

BDP-003F.11 does not create or authorize Buchanan-specific claims.

The bridge does not say:

```text
Buchanan argues X.
Buchanan's position is X.
The meaning of Body without Organs in Buchanan is X.
```

It only presents a read-only archive evidence posture row for classification by the F8 service.

## Failure posture

When the bridge cannot confirm the governed readback case, it returns an empty row list. The F8 service can then continue to produce a conservative posture such as:

```text
archive_lookup_status: no_archive_match
evidence_posture: exploratory_unverified
```

Failure to bridge is not evidence absence. It means the approved bridge could not confirm an accessible local readback path.

## Review result

BDP-003F.11 implements the approved bridge boundary and connects it to the F8 service through a wrapper only.

The implementation does not add UI, does not mutate the archive, does not add a backend route, and does not promote evidence.

## Explicit non-goals

BDP-003F.11 does not add:

1. frontend wiring;
2. Concept Lens UI dock;
3. Streamlit controls;
4. new navigation surface keys;
5. backend routes;
6. adapter endpoints;
7. SQL migrations;
8. database tables;
9. database mutation;
10. source ingestion;
11. citation creation;
12. concept mention creation;
13. concept relation creation;
14. interpretation insertion;
15. evidence promotion;
16. Buchanan-specific claims;
17. automatic chat filtering;
18. external LLM routing;
19. philosophical fidelity review.

## Verification

Verifier:

```text
scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py
```

The verifier checks:

1. BDP-003F.10 contract exists;
2. BDP-003F.11 document exists;
3. bridge module exists and compiles;
4. F8 service has the BDP-003F.11 wrapper;
5. fixture readback text for Body without Organs produces a complete rights-aware archive row;
6. non-supported concepts return no fabricated rows;
7. the wrapper can pass bridge rows into the F8 service classifier;
8. restricted passage text remains omitted;
9. state and handover record implementation boundaries;
10. no UI, database mutation, SQL migration, evidence promotion, interpretation, relation, or Buchanan-specific claim is approved.

## Next safe step

```text
BDP-003F.12 — Review live Body without Organs bridge output against the Concept Lens service before UI integration.
```

UI integration remains blocked.

## Preserved archive readback chain

The implemented bridge preserves the approved existing archive evidence readback chain:

```text
concepts -> concept_mentions -> passages -> citations -> sources
```

The bridge reads existing archive evidence only. It does not create concepts, concept_mentions, passages, citations, sources, concept relations, interpretations, evidence promotion, database mutations, SQL migrations, frontend UI, backend routes, or Buchanan-specific claims.
