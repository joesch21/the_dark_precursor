# Buchanan Schema Control

## Purpose

This document defines schema drift protection for the Buchanan Deleuze Intelligence Platform.

The goal is to prevent the knowledge system from becoming an uncontrolled pile of transcripts, embeddings, and generated interpretations.

## Schema Rule

No schema change is valid unless it updates:

1. The schema definition.
2. The migration note.
3. `ai_boot/BUCHANAN_SYSTEM_STATE.json`.
4. Any affected workflow document.
5. The validation checklist.

## Initial Tables

### sources

Stores canonical source records.

Fields:

```text
id
title
author
type
year
publisher
url_or_reference
rights_status
reliability_level
status
created_at
updated_at
```

### source_candidates

Stores discovered but unapproved sources.

Fields:

```text
id
title
author
url
type
discovered_by
status
review_notes
created_at
```

### raw_documents

Stores extracted raw text or file references.

Fields:

```text
id
source_id
raw_text
file_path
imported_at
extractor_version
```

### clean_documents

Stores cleaned document text.

Fields:

```text
id
source_id
cleaned_text
cleaning_version
created_at
```

### passages

Stores cited chunks of text.

Fields:

```text
id
source_id
text
page_or_timestamp
chapter_or_section
citation
embedding
created_at
```

### concepts

Stores concept records.

Fields:

```text
id
name
aliases
short_description
status
created_at
updated_at
```

### concept_mentions

Links concepts to passages.

Fields:

```text
id
concept_id
passage_id
confidence
mention_type
reviewed_status
created_at
```

### concept_relations

Stores relationships between concepts.

Fields:

```text
id
source_concept_id
target_concept_id
relation_type
evidence_passage_id
confidence
reviewed_status
created_at
```

### interpretations

Stores interpretive claims.

Fields:

```text
id
concept_id
interpreter
claim
authority_level
evidence_passage_id
confidence
reviewed_status
created_at
```

### ingestion_events

Stores the intake audit trail.

Fields:

```text
id
source_id
action
result
notes
timestamp
```

### user_interactions

Stores usage traces without altering canonical sources.

Fields:

```text
id
session_id
query
selected_concepts
response_mode
useful_response
followup_path
created_at
```

## Drift Protection Checklist

Before accepting a schema change:

1. Does the change alter canonical source storage?
2. Does it alter concept identity?
3. Does it alter citation behaviour?
4. Does it change authority-level logic?
5. Does it affect ingestion review?
6. Does it require a migration?
7. Has the repo-state JSON been updated?

If any answer is yes, a migration note is required.

## BDP-001A Schema-Control Patch

This patch aligns the initial SQL migration with the control-plane state before database implementation.

### schema_migrations

Stores migration identity and phase history.

Fields:

```text
id
phase
description
applied_at
```

### citations

Stores explicit citation trails for passages and interpretations.

Fields:

```text
id
source_id
passage_id
interpretation_id
citation_text
citation_format
locator
page_or_timestamp
chapter_or_section
url_or_reference
rights_status
display_rule
created_at
metadata
```

### Controlled Values

The initial migration enforces controlled values for source types, source statuses, rights statuses, authority levels, mention types, review statuses, and concept relation types.

### Migration Note

BDP-001A introduces the first executable schema contract. Future schema changes must update this document, `ai_boot/BUCHANAN_SYSTEM_STATE.json`, and the validation script.

## BDP-001D Source Candidate Review Metadata Patch

BDP-001D adds structured review metadata to `source_candidates` before any canonical source adoption.

### source_candidates extension

Added field:

```text
metadata JSONB
```

Purpose:

```text
Store structured candidate-review metadata without promoting a candidate into the canonical sources table.
```

Minimum BDP-001D metadata keys:

```text
candidate_status
review_notes
bibliographic_edition_or_version_note
rights_status_recommendation
reliability_level_recommendation
adoption_readiness
operator_review_requirement
canonical_adoption_boundary
bdp_phase
```

### Migration Note

BDP-001D changes candidate staging only.

It does not alter canonical source storage, passage storage, concept identity, citation behaviour, authority-level logic, or interpretation storage.

It does alter ingestion review by adding a structured metadata gate before source adoption.

### Boundary Rule

```text
source candidate ≠ canonical source
bibliographic metadata ≠ source evidence
review readiness ≠ adoption
source adoption ≠ interpretive authority
```

### Validation Addition

BDP-001D is valid only if verification proves:

1. the three expected source candidates exist.
2. each candidate has enriched review metadata.
3. each candidate remains in `source_candidates` with `status = candidate`.
4. the `sources` table remains empty.
5. the `passages` table remains empty.
6. the `interpretations` table remains empty.

## BDP-001L Canonical Source Metadata Adoption Patch

BDP-001L adopts the reviewed Buchanan article into the canonical `sources` table as metadata only.

### sources extension

Added field when missing:

```text
metadata JSONB
```

Purpose:

```text
Preserve article-specific bibliographic metadata without treating bibliographic existence as passage evidence or interpretive authority.
```

BDP-001L metadata keys include:

```text
doi
journal
volume
issue
pages
publication_date
publisher
display_rule
pdf_access_status
source_text_available_for_review
canonical_metadata_adoption_readiness
adopted_from_phases
passage_ingestion_ready
citation_insertion_ready
concept_mention_ready
concept_relation_ready
interpretation_ready
buchanan_claim_ready
bdp_phase
```

### Migration Note

BDP-001L changes canonical source metadata storage only.

It does not alter passage storage, concept identity, citation behaviour, authority-level logic, or interpretation storage.

It does not create a passage, citation, concept mention, concept relation, interpretation, synthesis, or Buchanan-specific claim.

### Validation Addition

BDP-001L is valid only if verification proves:

1. `sources_count = 2`.
2. `source_candidates_count = 3`.
3. one canonical Buchanan article source exists with the reviewed metadata.
4. the reviewed Buchanan source candidate is preserved as approved/adopted review history.
5. `passages_count = 1`.
6. `citations_count = 1`.
7. `concept_mentions_count = 1`.
8. `concept_relations_count = 0`.
9. `interpretations_count = 0`.
10. no passage or citation is attached to the newly adopted Buchanan article source.
11. `BDP-001L migration_count = 1`.

## BDP-001M Passage Candidate Staging Patch

BDP-001M introduces candidate passage staging so the platform can prepare passage review targets without collapsing them into canonical evidence.

### passage_candidates

Stores passage candidates before canonical passage insertion.

Fields:

```text
id
source_id
concept_id
candidate_label
candidate_status
candidate_scope
candidate_text
candidate_text_status
page_or_timestamp
chapter_or_section
locator_status
rights_status
display_rule
review_status
extraction_status
inserted_as_passage
citation_ready
concept_mention_ready
interpretation_ready
buchanan_claim_ready
created_at
reviewed_at
metadata
```

Purpose:

```text
A passage candidate can identify what should be reviewed next without becoming a passage, citation, concept mention, relation, interpretation, or claim.
```

### Migration Note

BDP-001M creates the `passage_candidates` staging table when missing and inserts one metadata-only candidate envelope for the adopted Buchanan article.

It does not insert a canonical passage into `passages`.

It does not insert a citation into `citations`.

It does not insert a concept mention, concept relation, interpretation, generated synthesis, or Buchanan-specific claim.

### Validation Addition

BDP-001M is valid only if verification proves:

1. `sources_count = 2`.
2. `source_candidates_count = 3`.
3. `passage_candidates_count = 1`.
4. `passages_count = 1`.
5. `citations_count = 1`.
6. `concept_mentions_count = 1`.
7. `concept_relations_count = 0`.
8. `interpretations_count = 0`.
9. the Buchanan article has zero canonical passages attached.
10. the Buchanan article has zero citations attached.
11. the passage candidate stores no Buchanan article text.
12. `BDP-001M migration_count = 1`.

## BDP-002A.1 Tooling Drift Repair

BDP-002A exposed a tooling drift risk.

The semantic workbench readback initially introduced a Python PostgreSQL driver dependency even though the existing Buchanan verifier/readback convention uses:

```text
Python subprocess
→ psql CLI
→ JSON or scalar readback
```

Repair rule:

```text
New Buchanan readback and verifier scripts should follow the existing psql subprocess pattern unless a phase explicitly records and justifies a dependency change.
```

Verifier rule:

```text
Read-only verification must inspect SQL execution boundaries, not arbitrary operator-facing prose.
```

A verifier must not treat a future-action phrase such as `Insert Buchanan cited passage in later phase` as a database mutation unless that phrase is part of SQL executed against the database.


## BDP-002A.2 Psycho-Linguistic Architecture Doctrine

BDP-002A.2 records architecture doctrine only.

It does not introduce a schema change.

Controlled status:

```text
sql_migration = false
database_mutation = false
new_tables = false
new_columns = false
reader_state_tracking = false
psycho_linguistic_tables = false
```

Future psycho-linguistic modelling or reader/listener transformation storage will require a separate schema proposal, explicit governance rules, state update, workflow update, and verifier.

## BDP-001N Passage Candidate Locator and Short Text Review Patch

BDP-001N updates the existing `passage_candidates` row for the adopted Buchanan article.

It records:

```text
candidate_text_status = reviewed_short_excerpt
locator_status = reviewed
review_status = approved
review_status_detail = reviewed_for_later_passage_insertion
citation_ready = true
concept_mention_ready = false
interpretation_ready = false
buchanan_claim_ready = false
inserted_as_passage = false
```

Migration note:

```text
BDP-001N updates candidate review metadata only.
It does not create a canonical passage.
It does not create a citation.
It does not create a concept mention, concept relation, interpretation, synthesis, or Buchanan-specific claim.
```

Validation addition:

BDP-001N is valid only if verification proves:

1. exactly one Buchanan article passage candidate exists.
2. the candidate stores only a short reviewed excerpt.
3. the candidate locator is reviewed.
4. `citation_ready = true`.
5. `inserted_as_passage = false`.
6. `concept_mention_ready = false`.
7. `interpretation_ready = false`.
8. `buchanan_claim_ready = false`.
9. canonical table counts are preserved.
10. `BDP-001N migration_count = 1`.

## BDP-001N.1 Description Versus Claim Authority Rule

BDP-001N.1 records a doctrine-only rule. It does not introduce a schema change.

The platform now distinguishes:

```text
description ≠ claim
```

A description may report the state of reviewed records, locators, excerpts, and evidence posture.

A description becomes a claim when it attributes any of the following to Buchanan, Deleuze, Guattari, or another author:

```text
position
argument
intention
conceptual meaning
theoretical consequence
```

Descriptions must carry authority labels.

Claims require stronger governed evidence.

Authority ladder:

```text
metadata
→ locator
→ short excerpt
→ source-bound description
→ citation-backed passage
→ concept mention
→ interpretation
→ synthesis
```

Controlled status:

```text
sql_migration = false
database_mutation = false
new_tables = false
new_columns = false
authority_rule_update = true
```

## BDP-001O Reviewed Passage and Citation Insertion Patch

BDP-001O promotes the already-reviewed Buchanan passage candidate into canonical evidence.

It inserts:

```text
one passages row
one citations row linked to that passage
```

It updates the existing `passage_candidates` row only to record that the reviewed candidate has been inserted as a canonical passage.

Migration note:

```text
BDP-001O changes canonical passage and citation storage.
It does not change schema shape.
It does not create a concept mention.
It does not create a concept relation.
It does not create an interpretation, synthesis, or Buchanan-specific claim.
```

Validation addition:

BDP-001O is valid only if verification proves:

1. `sources_count = 2`.
2. `source_candidates_count = 3`.
3. `passage_candidates_count = 1`.
4. `passages_count = 2`.
5. `citations_count = 2`.
6. exactly one canonical passage is attached to the Buchanan article source.
7. exactly one citation is attached to the inserted Buchanan passage.
8. the reviewed passage candidate is marked `inserted_as_passage = true`.
9. `concept_mentions_count = 1`.
10. `concept_relations_count = 0`.
11. `interpretations_count = 0`.
12. `BDP-001O migration_count = 1`.


## BDP-001P Reviewed Concept Mention Link Patch

BDP-001P links the inserted citation-backed Buchanan article passage to `Body without Organs` through one reviewed `concept_mentions` row.

It inserts:

```text
one concept_mentions row
one schema_migrations ledger row
```

Migration note:

```text
BDP-001P changes concept mention storage only.
It does not change schema shape.
It does not create a source, passage, citation, concept relation, interpretation, synthesis, or Buchanan-specific claim.
```

Validation addition:

BDP-001P is valid only if verification proves:

1. `sources_count = 2`.
2. `source_candidates_count = 3`.
3. `passage_candidates_count = 1`.
4. `passages_count = 2`.
5. `citations_count = 2`.
6. `concept_mentions_count = 2`.
7. exactly one reviewed direct `Body without Organs` concept mention is attached to the Buchanan article passage.
8. `concept_relations_count = 0`.
9. `interpretations_count = 0`.
10. `BDP-001P migration_count = 1`.
