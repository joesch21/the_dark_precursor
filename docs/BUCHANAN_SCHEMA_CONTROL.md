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

