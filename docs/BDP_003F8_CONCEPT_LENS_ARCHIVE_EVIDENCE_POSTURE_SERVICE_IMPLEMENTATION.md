# BDP-003F.8 — Concept Lens Archive Evidence Posture Service Implementation

**Status:** Complete  
**Completed:** 2026-06-18T02:45:00+00:00  
**Controlled slice:** read-only local service implementation  
**Authority:** Application readback implementation / archive evidence posture only  
**Contract source:** `docs/BDP_003F7_CONCEPT_LENS_ARCHIVE_EVIDENCE_POSTURE_SERVICE_CONTRACT.md`  
**Frontend implementation:** No  
**Backend route implementation:** No  
**Database mutation:** No  
**SQL migration:** No  

## Purpose

BDP-003F.8 implements the first read-only **Concept Lens archive evidence posture service** behind the BDP-003F.7 contract.

BDP-003F.6 defined the Concept Lens as a future dock inside The Dark Precursor concept stage. BDP-003F.7 defined the service contract for reporting what the Buchanan SQL archive currently supports for a requested concept. BDP-003F.8 now adds a local read-only service module that can classify archive evidence posture without creating citations, interpretations, concept relations, evidence promotion, Buchanan-specific claims, database tables, SQL migrations, backend routes, or frontend UI.

The service answers one narrow question:

```text
For this requested concept, what does the archive currently support?
```

It does not answer the whole philosophical question. It only produces evidence posture for later Concept Lens rendering.

## Implemented service

Implemented module:

```text
scripts/concept_lens_archive_evidence_posture_service.py
```

Implemented function:

```text
read_concept_lens_archive_evidence_posture
```

Result schema marker:

```text
bdp_003f8_concept_lens_archive_evidence_posture_result_v1
```

The service can be used in three ways:

1. with explicit archive rows supplied by tests or later adapters;
2. with an optional read-only SQLite archive path;
3. with an optional read-only PostgreSQL URL through `psql`.

The verifier uses supplied fixture rows only. It does not require a live database.

## Primary read-only archive chain

The service preserves the BDP-003F.7 primary chain:

```text
concepts
  -> concept_mentions
  -> passages
  -> citations
  -> sources
```

It does not read optional layers by default.

Blocked unless later approved:

```text
concept_relations
interpretations
source_candidates
passage_candidates
```

## Evidence posture output

The service returns a bounded object with:

1. `schema_id`,
2. `concept`,
3. `normalized_concept`,
4. `archive_lookup_status`,
5. `evidence_posture`,
6. `authority_label`,
7. `buchanan_specific_claim_allowed`,
8. `archive_chain`,
9. `matched_records`,
10. `rights_display_rule`,
11. `passage_text_display`,
12. `interpretation_available`,
13. `concept_relation_available`,
14. `human_review_required`,
15. `blocked_actions`.

## Evidence posture decision rules implemented

### `archive_grounded`

Returned only when a concept has at least one complete primary evidence chain:

```text
concept -> reviewed concept mention -> passage -> citation -> source
```

This is still evidence posture only. It does not automatically authorize broad Buchanan interpretation.

### `source_bound_description`

Returned when the archive contains source/passage-linked material, but the primary chain is incomplete or not fully reviewed.

### `system_synthesis`

Returned when the concept exists or is useful as a normalized query, but the archive does not ground the requested explanation.

### `exploratory_unverified`

Returned when the concept is not found or supplied evidence rows are empty.

## Archive lookup statuses implemented

```text
archive_grounded_match
source_bound_match
concept_found_without_reviewed_evidence
no_archive_match
rights_restricted_match
```

The following BDP-003F.7 statuses remain contract-reserved for later expansion:

```text
ambiguous_concept_match
optional_layer_required_but_blocked
```

## Rights boundary

The service is rights-aware by default.

Restricted passage text is never reproduced by this service. Returned archive chain items use:

```text
passage_text_display = omitted_by_rights_policy
```

or:

```text
passage_text_display = omitted_until_allowed_by_rights_policy
```

The service may return source metadata, locators, rights status, and authority labels.

## Buchanan-specific claim boundary

The service never authorizes claims such as:

```text
Buchanan argues X.
Buchanan's reading is X.
Buchanan would say X.
```

The service only reports evidence posture. A later Concept Lens answer must still respect authority labels and human review boundaries.

## CLI use

Basic no-live-archive run:

```bash
python3 scripts/concept_lens_archive_evidence_posture_service.py "repetition"
```

Optional SQLite read-only run:

```bash
python3 scripts/concept_lens_archive_evidence_posture_service.py "Body without Organs" --sqlite-db path/to/archive.sqlite
```

Optional PostgreSQL read-only run:

```bash
python3 scripts/concept_lens_archive_evidence_posture_service.py "Body without Organs" --postgres-url "$DATABASE_URL"
```

If no live archive is configured, the service returns a visible no-archive-match posture rather than fabricating evidence.

## Verification

Verifier:

```text
scripts/verify_bdp_003f8_concept_lens_archive_evidence_posture_service.py
```

The verifier checks:

1. BDP-003F.7 contract anchor exists;
2. BDP-003F.8 document exists;
3. service module exists and compiles;
4. service returns `exploratory_unverified` for no archive rows;
5. service returns `archive_grounded` for a complete fixture chain;
6. service omits restricted passage text;
7. service returns `source_bound_description` for incomplete source-bound fixture rows;
8. state and handover record implementation boundaries;
9. no frontend wiring, route handler, SQL migration, evidence promotion, interpretation, concept relation, or Buchanan-specific claim is approved.

## Explicit non-goals

BDP-003F.8 does not add:

1. Concept Lens frontend dock,
2. Streamlit controls,
3. new navigation surface keys,
4. backend route handlers,
5. adapter endpoints,
6. SQL migrations,
7. database tables,
8. database mutation,
9. source ingestion,
10. citation creation,
11. concept mention creation,
12. concept relation creation,
13. interpretation insertion,
14. evidence promotion,
15. Buchanan-specific claims,
16. automatic chat filtering,
17. external LLM routing,
18. philosophical fidelity review.

## Future safe sequence

Recommended next safe step:

```text
BDP-003F.9 — Review Concept Lens evidence posture service output against known archive cases before UI integration.
```

Later, after output review, the application may proceed toward a UI contract and then a small Concept Lens dock inside the existing Dark Precursor concept stage.
