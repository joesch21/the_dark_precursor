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

## BDP-001H Handover Update

Source intake registry and candidate creation readback prepared as a read-only slice.

Completed:

1. Added `docs/BUCHANAN_SOURCE_INTAKE_REGISTRY.md`.
2. Added `scripts/read_bdp_001h_source_intake_registry.py`.
3. Added `scripts/preview_bdp_001h_candidate_creation.py`.
4. Added `scripts/verify_bdp_001h_source_intake_registry.py`.
5. Updated `ai_boot/BUCHANAN_SYSTEM_STATE.json` for BDP-001H.
6. Updated ingestion workflow with the source intake registry boundary.
7. Preserved the existing database invariant.
8. Confirmed no source candidate, canonical source, passage, citation, concept mention, concept relation, or interpretation was inserted.

Current invariant:

```text
sources_count = 1
passages_count = 1
citations_count = 1
concept_mentions_count = 1
concept_relations_count = 0
interpretations_count = 0
BDP-001F migration_count = 1
BDP-001H migration_count = 0
```

Boundary:

```text
No SQL migration was added.
No database mutation was performed.
No source candidate was inserted.
No canonical source was inserted.
No passage was inserted.
No citation was inserted.
No concept mention was inserted.
No concept relation was inserted.
No interpretation was inserted.
No generated Buchanan claim was created.
```

Next step:

```text
BDP-001I — Select first Buchanan source candidate for Body without Organs.
```

## BDP-001I Handover Update

First Buchanan source candidate selection completed as a selection-only governed slice.

Completed:

1. Selected the existing `Ian Buchanan Body without Organs source candidate` as the next Buchanan review target.
2. Preserved the candidate as `status = candidate`.
3. Recorded an explicit hard block against canonical Buchanan source adoption until the exact Buchanan source is specified.
4. Added `docs/BUCHANAN_PATCH_BUNDLE_WORKFLOW.md` as the preferred repository working method.
5. Added `sql/009_select_bdp_001i_buchanan_placeholder_candidate_only.sql`.
6. Added `scripts/read_bdp_001i_buchanan_candidate_selection.py`.
7. Added `scripts/verify_bdp_001i_buchanan_candidate_selection.py`.
8. Updated `ai_boot/BUCHANAN_SYSTEM_STATE.json` for BDP-001I.
9. Updated ingestion workflow with the BDP-001I selection-only boundary.

Preferred working method:

```text
make patch bundle
→ download zip
→ unzip locally
→ apply with git apply --check
→ run verifiers
→ commit/push from local repo
```

Current invariant:

```text
sources_count = 1
source_candidates_count = 3
passages_count = 1
citations_count = 1
concept_mentions_count = 1
concept_relations_count = 0
interpretations_count = 0
BDP-001F migration_count = 1
BDP-001H migration_count = 0
BDP-001I migration_count = 1
```

Boundary:

```text
No new source candidate was inserted.
No canonical Buchanan source was inserted.
No passage was inserted.
No citation was inserted.
No concept mention was inserted.
No concept relation was inserted.
No interpretation was inserted.
No generated Buchanan claim was created.
Canonical adoption is blocked until the exact Buchanan source is specified.
```

Next step:

```text
BDP-001J — Specify exact Buchanan source for Body without Organs candidate review.
```

## BDP-001J.0 Handover Update

Concept evidence depth tiers recorded as a doctrine-only slice.

Completed:

1. Added `docs/BUCHANAN_CONCEPT_EVIDENCE_DEPTH_TIERS.md`.
2. Added `scripts/verify_bdp_001j0_concept_evidence_depth_tiers.py`.
3. Updated `ai_boot/BUCHANAN_SYSTEM_STATE.json` for BDP-001J.0.
4. Updated concept ontology and ingestion workflow with tiered evidence depth.
5. Preserved the patch-bundle workflow as the preferred application method.
6. Confirmed no database mutation was performed.
7. Confirmed no new source, passage, citation, concept mention, concept relation, interpretation, or Buchanan claim was created.

Doctrine:

```text
Not every concept requires full-source treatment.
Concept detail follows authority.
Anchor concepts require full citation-backed treatment.
Supporting concepts require reviewed mention or relation evidence.
Contextual terms may remain proposed until promoted.
No Buchanan-specific claim may be made without an exact Buchanan source passage.
```

Current invariant:

```text
sources_count = 1
passages_count = 1
citations_count = 1
concept_mentions_count = 1
concept_relations_count = 0
interpretations_count = 0
BDP-001I migration_count = 1
BDP-001J.0 migration_count = 0
```

Next step:

```text
BDP-001J — Specify exact Buchanan source for Body without Organs candidate review.
```

## BDP-001J Handover Update

Exact Buchanan source specified for Body without Organs candidate review.

Completed:

1. Refined the existing `Ian Buchanan Body without Organs source candidate`.
2. Recorded the exact source as Ian Buchanan's 1997 article `The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?`.
3. Preserved the candidate as non-canonical.
4. Recorded canonical adoption as blocked pending operator review.
5. Added `sql/010_specify_bdp_001j_exact_buchanan_source_candidate_review.sql`.
6. Added `scripts/read_bdp_001j_exact_buchanan_source.py`.
7. Added `scripts/verify_bdp_001j_exact_buchanan_source.py`.
8. Updated system state, source intake registry, and citation/rights policy.
9. Confirmed no new source, passage, citation, concept mention, relation, interpretation, or Buchanan claim was created.

Current invariant:

```text
sources_count = 1
source_candidates_count = 3
passages_count = 1
citations_count = 1
concept_mentions_count = 1
concept_relations_count = 0
interpretations_count = 0
BDP-001I migration_count = 1
BDP-001J migration_count = 1
```

Next step:

```text
BDP-001K — Review exact Buchanan source candidate for canonical adoption readiness.
```

## BDP-001K Handover Update

Exact Buchanan source candidate reviewed for canonical metadata adoption readiness.

Completed:

1. Recorded uploaded PDF availability for the exact Buchanan article.
2. Confirmed the candidate remains non-canonical.
3. Recorded readiness for metadata-only canonical source adoption.
4. Kept passage ingestion blocked.
5. Kept citation insertion blocked.
6. Kept concept relation and interpretation blocked.
7. Added `sql/011_review_bdp_001k_buchanan_pdf_adoption_readiness.sql`.
8. Added `scripts/read_bdp_001k_buchanan_pdf_readiness.py`.
9. Added `scripts/verify_bdp_001k_buchanan_pdf_readiness.py`.

Current invariant:

```text
sources_count = 1
source_candidates_count = 3
passages_count = 1
citations_count = 1
concept_mentions_count = 1
concept_relations_count = 0
interpretations_count = 0
BDP-001J migration_count = 1
BDP-001K migration_count = 1
```

Next step:

```text
BDP-001L — Adopt reviewed Buchanan source metadata into canonical sources only.
```

## BDP-001L Handover Update

Reviewed Buchanan source metadata has been adopted into canonical `sources` as a metadata-only governed slice.

Completed:

1. Inserted one canonical `sources` record for Ian Buchanan's 1997 article `The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?`.
2. Preserved the existing Buchanan source candidate as review history.
3. Marked the reviewed Buchanan source candidate as approved/adopted metadata history.
4. Recorded adoption from BDP-001J exact-source specification and BDP-001K PDF availability review.
5. Preserved uploaded PDF availability as metadata only.
6. Confirmed no Buchanan article passage was inserted.
7. Confirmed no citation record was inserted for the Buchanan article.
8. Confirmed no concept mention, concept relation, interpretation, generated synthesis, or Buchanan claim was created.
9. Added `sql/012_adopt_bdp_001l_buchanan_source_metadata_only.sql`.
10. Added `scripts/read_bdp_001l_buchanan_source_metadata.py`.
11. Added `scripts/verify_bdp_001l_buchanan_source_metadata_only.py`.
12. Added `scripts/update_bdp_001l_system_state.py`.

Current invariant:

```text
sources_count = 2
source_candidates_count = 3
passages_count = 1
citations_count = 1
concept_mentions_count = 1
concept_relations_count = 0
interpretations_count = 0
BDP-001L migration_count = 1
```

Boundary:

```text
No passage insertion.
No citation insertion.
No concept mention insertion.
No concept relation insertion.
No interpretation insertion.
No generated Buchanan claim.
No long quotation from the PDF.
No claim that Buchanan argues anything yet.
```

Next step:

```text
BDP-001M — Prepare first Buchanan passage candidate from the adopted article, without inserting citation or interpretation yet.
```

## BDP-001M Handover Update

First Buchanan passage candidate preparation completed as a candidate-only governed slice.

Completed:

1. Created `passage_candidates` as a staging table for candidate passages before canonical passage insertion.
2. Prepared one passage-candidate envelope for Ian Buchanan's 1997 article `The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?`.
3. Linked the candidate envelope to the adopted canonical Buchanan source.
4. Linked the candidate envelope to the `Body without Organs` concept as an intended review target.
5. Preserved the candidate as metadata-only and review-pending.
6. Stored no Buchanan article text in the candidate.
7. Selected no page locator yet.
8. Inserted no canonical passage, citation, concept mention, concept relation, interpretation, generated synthesis, or Buchanan claim.
9. Added `sql/013_prepare_bdp_001m_first_buchanan_passage_candidate.sql`.
10. Added `scripts/read_bdp_001m_first_buchanan_passage_candidate.py`.
11. Added `scripts/verify_bdp_001m_first_buchanan_passage_candidate.py`.
12. Added `scripts/verify_bdp_001m_phase_chain_invariant.py`.
13. Added `scripts/update_bdp_001m_docs_and_state.py`.

Current invariant:

```text
sources_count = 2
source_candidates_count = 3
passage_candidates_count = 1
passages_count = 1
citations_count = 1
concept_mentions_count = 1
concept_relations_count = 0
interpretations_count = 0
BDP-001M migration_count = 1
```

Boundary:

```text
No Buchanan article passage inserted.
No Buchanan article citation inserted.
No Buchanan article concept mention inserted.
No concept relation inserted.
No interpretation inserted.
No generated Buchanan claim.
No long quotation from the PDF.
No candidate text stored yet.
```

Next step:

```text
BDP-001N — Review selected Buchanan passage candidate text and locator before any citation or interpretation insertion.
```

## BDP-002A Handover Update

Body without Organs semantic workbench prepared as a read-only demo slice.

Completed:

1. Added `docs/BUCHANAN_SEMANTIC_WORKBENCH.md`.
2. Added `scripts/read_bdp_002a_bwo_semantic_workbench.py`.
3. Added `scripts/verify_bdp_002a_semantic_workbench.py`.
4. Added `scripts/update_bdp_002a_system_state.py`.
5. Updated architecture and concept ontology docs with the semantic workbench authority boundary.
6. Preserved the current database invariant.
7. Confirmed the workbench generates no Buchanan-specific interpretation or claim.
8. Confirmed all explanation fields carry explicit authority labels.
9. Confirmed no SQL migration is added for BDP-002A.

Current invariant:

```text
sources_count = 2
source_candidates_count = 3
passage_candidates_count = 1
passages_count = 1
citations_count = 1
concept_mentions_count = 1
concept_relations_count = 0
interpretations_count = 0
BDP-001L migration_count = 1
BDP-001M migration_count = 1
BDP-002A migration_count = 0
```

Boundary:

```text
No SQL migration was added.
No database mutation was performed.
No canonical passage was inserted.
No citation was inserted.
No concept mention was inserted.
No concept relation was inserted.
No interpretation was inserted.
No generated Buchanan claim was created.
Buchanan-specific explanation remains pending and blocked.
```

Next step:

```text
BDP-001N — Review first Buchanan passage candidate locator and short text, without inserting citation or interpretation.
```

Alternative next step:

```text
BDP-002B — Add semantic workbench card renderer / frontend preview.
```

## BDP-002A.1 Repair Note

BDP-002A was committed and pushed, but the first verifier failed after the readback preview.

Observed drift:

1. The initial readback used `psycopg/psycopg2`, while existing Buchanan scripts use `psql` through Python `subprocess`.
2. The verifier falsely detected the word `Insert` inside operator-facing prose as mutating SQL.
3. The phase was pushed before verifier success.

Repair action:

```text
BDP-002A.1 — Repair semantic workbench verifier drift.
```

Required correction:

```text
Keep BDP-002A read-only.
Use the existing psql subprocess pattern.
Inspect SQL passed to psql helpers rather than all explanatory text.
Record this tooling boundary in schema/workbench docs.
Run verifier before the corrective commit.
```


## BDP-002A.2 Handover Update

Psycho-linguistic semantic architecture doctrine has been recorded as a doctrine-only slice.

Completed:

1. Added `docs/BUCHANAN_PSYCHOLINGUISTIC_SEMANTIC_ARCHITECTURE.md`.
2. Updated architecture doctrine with the four-layer interpretive stack.
3. Updated semantic workbench doctrine with psycho-linguistic observation boundaries.
4. Updated concept ontology with the distinction between psycho-linguistic modelling metadata and concept claims.
5. Updated schema control with an explicit no-schema-change boundary.
6. Added `scripts/update_bdp_002a2_system_state.py`.
7. Added `scripts/verify_bdp_002a2_psycholinguistic_architecture.py`.
8. Preserved the patch-bundle workflow as the preferred application method.
9. Confirmed no SQL migration is added for BDP-002A.2.

Core doctrine:

```text
The platform does not only ask what an author says.
It also preserves the architectural question of how philosophical language moves, pressures, destabilises, and transforms interpretation.
```

Current boundary:

```text
No SQL migration.
No database mutation.
No psycho-linguistic tables.
No reader-state tracking.
No canonical passage insertion.
No citation insertion.
No concept mention insertion.
No concept relation insertion.
No interpretation insertion.
No Buchanan-specific claim.
No frontend renderer.
```

Next step:

```text
BDP-001N — Review first Buchanan passage candidate locator and short text, without inserting citation or interpretation.
```

Alternative next step:

```text
BDP-002B — Add semantic workbench card renderer / frontend preview.
```
