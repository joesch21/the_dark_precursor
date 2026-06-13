# Buchanan Platform Thread Handover

## Current Direction

The project has shifted from Tower workbench mechanics into a Buchanan-grounded Deleuze and Guattari intelligence platform.

The system is intended to be a cognitive research environment rather than a generic chatbot.

## Core Idea

Build a platform that can ingest, structure, cite, compare, and synthesize Ian Buchanan's published work, lectures, transcripts, interviews, and related Deleuzian scholarship.

## First Build Slice

Phase:

```text
BDP-001 — Buchanan Platform Control Plane Foundation
```

Primary task:

```text
Create documentation and state files before database implementation.
```

Initial concept:

```text
Body without Organs
```

## Created Control Plane Files

```text
ai_boot/BUCHANAN_SYSTEM_STATE.json
docs/BUCHANAN_ARCHITECTURE.md
docs/BUCHANAN_SCHEMA_CONTROL.md
docs/BUCHANAN_INGESTION_WORKFLOW.md
docs/BUCHANAN_CONCEPT_ONTOLOGY.md
docs/BUCHANAN_CITATION_AND_RIGHTS.md
docs/BUCHANAN_THREAD_HANDOVER.md
```

## Key Design Rules

1. Do not build a chatbot-first system.
2. Build a concept and citation-first system.
3. Do not auto-ingest discovered sources into canon.
4. Keep candidate source staging separate from accepted sources.
5. Keep generated synthesis separate from source-backed claims.
6. Require citation trails for interpretive claims.
7. Record schema drift through state and workflow docs.

## Next Recommended Step

Create the first database prototype using PostgreSQL with pgvector.

Minimum tables:

```text
sources
source_candidates
raw_documents
clean_documents
passages
concepts
concept_mentions
concept_relations
interpretations
ingestion_events
user_interactions
```

## Current Open Question

Whether the first prototype should be:

1. a standalone local database and CLI ingestion tool, or
2. a small web interface for uploading and reviewing sources.

## BDP-001A Handover Update

Schema-control alignment completed for the first database prototype.

Key changes:

1. Added explicit `citations` table contract.
2. Added `schema_migrations` ledger.
3. Aligned state database scope with SQL migration tables.
4. Consolidated concept relation vocabulary.
5. Added stronger initialization verifier.

Next step:

```text
Run scripts/verify_init.py, then apply sql/001_buchanan_control_plane.sql to local PostgreSQL.
```

## BDP-001C Handover Update

Initial seed records have been applied to the live local PostgreSQL database.

Completed:

1. Seeded canonical concept target: `Body without Organs`.
2. Seeded related proposed concepts: `organism`, `desire`, `assemblage`, `strata`.
3. Seeded source candidates only.
4. Confirmed source candidates remain non-canonical.
5. Confirmed no passages or interpretations were inserted.
6. Added and pushed `sql/002_seed_bdp_001c.sql`.
7. Added and pushed `scripts/verify_bdp_001c_seed.py`.

Next step:

```text
BDP-001D — Review and enrich source candidates before canonical source adoption.


```

## BDP-001D Handover Update

Source candidates have been reviewed and enriched before canonical source adoption.

Completed:

1. Added structured `metadata JSONB` support to `source_candidates`.
2. Enriched the three existing source candidates with review-ready metadata.
3. Preserved all three records as non-canonical candidates.
4. Confirmed no canonical `sources` records are created by this phase.
5. Confirmed no `passages` are inserted by this phase.
6. Confirmed no `interpretations` are inserted by this phase.
7. Added `sql/003_enrich_bdp_001d_source_candidates.sql`.
8. Added `scripts/verify_bdp_001d_candidates.py`.
9. Updated `ai_boot/BUCHANAN_SYSTEM_STATE.json` for BDP-001D.
10. Updated schema and ingestion workflow notes for the candidate review metadata gate.

Governance boundary:

```text
source candidate ≠ canonical source
bibliographic metadata ≠ source evidence
review readiness ≠ adoption
source adoption ≠ interpretive authority
```

Required verification:

```bash
export BUCHANAN_DB_NAME=buchanan_platform_dev

python3 ./scripts/verify_init.py
python3 ./scripts/verify_db_schema.py
python3 ./scripts/verify_bdp_001c_seed.py
python3 ./scripts/verify_bdp_001d_candidates.py
```

Expected final verifier output:

```text
BDP-001D source candidate review verification passed.
```

Next step:

```text
BDP-001E — Adopt first reviewed source and insert first cited passage.
```


## BDP-001D Repair Closeout

BDP-001D required a repair after the first pushed commit because the live `schema_migrations.id` column requires an explicit text ID and the original migration attempted to insert only phase and description.

Repair completed:

1. Removed accidental nested patch folder from the repository.
2. Corrected `sql/003_enrich_bdp_001d_source_candidates.sql` to insert explicit schema migration ID.
3. Confirmed `source_candidates.metadata` is JSONB.
4. Enriched all three initial source candidates with review-ready metadata.
5. Confirmed all enriched records remain candidate-only.
6. Confirmed no canonical sources were created.
7. Confirmed no passages were inserted.
8. Confirmed no interpretations were inserted.
9. Verified BDP-001D with `scripts/verify_bdp_001d_candidates.py`.

Next step:

```text
BDP-001E — Adopt first reviewed source and insert first cited passage.


## BDP-001E.1 Handover Update

First adoption candidate selection completed as a metadata-only governed slice.

Completed:

1. Selected `A Thousand Plateaus: Capitalism and Schizophrenia` as the first candidate for canonical adoption review.
2. Locked the selection in `source_candidates.metadata`.
3. Preserved candidate status as `candidate`.
4. Confirmed no canonical source was created.
5. Confirmed no passage was inserted.
6. Confirmed no interpretation was inserted.
7. Added `sql/004_select_bdp_001e1_first_adoption_candidate.sql`.
8. Added `scripts/verify_bdp_001e1_candidate_selection.py`.

Current invariant:

```text
sources_count = 0
passages_count = 0
interpretations_count = 0
Next step:

BDP-001E.2 — Adopt selected candidate into canonical sources only.


## BDP-001E.1 Cleanup Closeout

BDP-001E.1 completed as a selection-only governed slice.

Completed:

1. Selected `A Thousand Plateaus: Capitalism and Schizophrenia` as the first candidate for canonical adoption review.
2. Locked the selection in `source_candidates.metadata`.
3. Preserved candidate status as `candidate`.
4. Removed premature full-adoption and passage files from the repository.
5. Restored `BUCHANAN_SYSTEM_STATE.json` database scope expected by `verify_init.py`.
6. Confirmed no canonical source was created.
7. Confirmed no passage was inserted.
8. Confirmed no interpretation was inserted.

Current invariant:

```text
sources_count = 0
passages_count = 0
interpretations_count = 0
BDP-001E.1 migration_count = 1

Next step:

BDP-001E.2 — Adopt selected candidate into canonical sources only.


## BDP-001E.2 Handover Update

Selected source adoption completed as a source-only governed slice.

Completed:

1. Adopted `A Thousand Plateaus: Capitalism and Schizophrenia` into `sources`.
2. Marked the adopted source as canonical.
3. Preserved the original source candidate as review history.
4. Confirmed no passage was inserted.
5. Confirmed no citation was inserted.
6. Confirmed no interpretation was inserted.
7. Added `sql/005_adopt_bdp_001e2_selected_candidate_source_only.sql`.
8. Added `scripts/verify_bdp_001e2_source_only.py`.

Current invariant:

```text
sources_count = 1
passages_count = 0
citations_count = 0
interpretations_count = 0

Next step:

BDP-001E.3 — Insert first cited passage only.



## BDP-001E.5 Closeout

BDP-001E is now closed through E.5.

Completed:

1. Recorded BDP-001E.5 in `ai_boot/BUCHANAN_SYSTEM_STATE.json`.
2. Confirmed the first canonical source has been adopted: `A Thousand Plateaus: Capitalism and Schizophrenia`.
3. Confirmed the first short cited passage has been inserted.
4. Confirmed the first citation record has been inserted and linked to the canonical source and first passage.
5. Confirmed no interpretations have been inserted.
6. Preserved the source/passage/citation chain as ready for concept-linking.
7. Preserved the database scope and current verified invariant.

Current invariant:

```text
sources_count = 1
passages_count = 1
citations_count = 1
interpretations_count = 0
BDP-001E.4 migration_count = 1
```

Boundary:

```text
No SQL migration was added.
No database mutation was performed.
No source was inserted.
No passage was inserted.
No citation was inserted.
No interpretation was inserted.
No concept mention was inserted.
No concept relation was inserted.
No interpretive claim was created.
```

Next step:

```text
BDP-001F — Link first cited passage to Body without Organs concept mention
```


## BDP-001F Handover Update

The first cited passage has been linked to the `Body without Organs` concept through a reviewed concept mention.

Completed:

1. Added one `concept_mentions` row linking the first cited passage to `Body without Organs`.
2. Preserved the canonical source count at one.
3. Preserved the passage count at one.
4. Preserved the citation count at one.
5. Confirmed no interpretations were inserted.
6. Confirmed no concept relations were inserted.
7. Added `sql/008_link_bdp_001f_first_passage_to_bwo_concept.sql`.
8. Added `scripts/verify_bdp_001f_concept_mention.py`.
9. Updated `ai_boot/BUCHANAN_SYSTEM_STATE.json` for BDP-001F.

Current invariant:

```text
sources_count = 1
passages_count = 1
citations_count = 1
concept_mentions_count = 1
concept_relations_count = 0
interpretations_count = 0
BDP-001F migration_count = 1
```

Boundary:

```text
No source was inserted.
No passage was inserted.
No citation was inserted.
No interpretation was inserted.
No concept relation was inserted.
No interpretive claim was created.
```

Next step:

```text
BDP-001G — Prepare first citation-backed Body without Organs concept readback
```


## BDP-001G Handover Update

First citation-backed concept readback prepared for `Body without Organs`.

Completed:

1. Added `scripts/read_bdp_001g_bwo_concept_readback.py`.
2. Added `scripts/verify_bdp_001g_concept_readback.py`.
3. Prepared a read-only evidence card over the chain `concepts → concept_mentions → passages → citations → sources`.
4. Confirmed the readback resolves the accepted direct `Body without Organs` concept mention.
5. Confirmed the readback is linked to the first cited passage from `A Thousand Plateaus: Capitalism and Schizophrenia`.
6. Confirmed the citation chain remains reference-only and interpretation-free.
7. Confirmed no sources, passages, citations, concept mentions, concept relations, or interpretations were inserted by this phase.

Current invariant:

```text
sources_count = 1
passages_count = 1
citations_count = 1
concept_mentions_count = 1
concept_relations_count = 0
interpretations_count = 0
BDP-001F migration_count = 1
```

Boundary:

```text
No SQL migration was added.
No database mutation was performed.
No source was inserted.
No passage was inserted.
No citation was inserted.
No concept mention was inserted.
No concept relation was inserted.
No interpretation was inserted.
No Buchanan interpretation was generated.
No system synthesis was generated.
```

Next step:

```text
BDP-001H — Define source intake and candidate staging workflow
```
