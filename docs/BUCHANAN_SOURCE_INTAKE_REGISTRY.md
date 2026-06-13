# Buchanan Source Intake Registry

## Purpose

This document defines the controlled front door for new Buchanan / Deleuze source material.

BDP-001H is a read-only registry and candidate-creation preview slice. It does not create source candidates. It defines how future candidate creation should be inspected before any database write.

## Intake Principle

The platform must not ingest material directly into canonical knowledge.

All new material must pass through the staged sequence:

```text
external material
→ intake description
→ source candidate preview
→ operator review
→ candidate creation
→ candidate enrichment
→ canonical adoption decision
→ passage extraction
→ citation
→ concept mention
→ relation or interpretation only after evidence exists
```

## Intake Modes

Allowed intake modes:

1. manual_upload
2. curated_import
3. assisted_discovery
4. operator_note
5. bibliography_seed
6. transcript_seed

## Candidate Preview Fields

A candidate creation preview must show:

```text
title
author
source_type
url_or_reference
discovered_by
rights_status_recommendation
reliability_level_recommendation
bibliographic_note
operator_review_requirement
canonical_adoption_boundary
intended_concept_link
```

## Candidate Creation Boundary

A preview is not a candidate.

A candidate is not a canonical source.

A canonical source is not passage evidence.

A passage is not an interpretation.

A citation is not a concept claim.

A concept mention is not a synthesis.

## BDP-001H Boundary

```text
No SQL migration.
No database mutation.
No source candidate insertion.
No canonical source insertion.
No passage insertion.
No citation insertion.
No concept mention insertion.
No concept relation insertion.
No interpretation insertion.
No generated Buchanan claim.
```

## Current Data Source Position

The current database already contains:

```text
one canonical source
one cited passage
one citation
one accepted direct concept mention
zero concept relations
zero interpretations
```

BDP-001H prepares the intake readback layer for future sources, especially Buchanan-authored material connected to Body without Organs.

## Next Intended Step

```text
BDP-001I — Select first Buchanan source candidate for Body without Organs.
```

## BDP-001J Exact Buchanan Source Specification

The selected Buchanan placeholder candidate has been refined with an exact source for candidate review.

Exact source:

```text
Ian Buchanan, "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?", Body & Society 3(3), September 1997, pp. 73-91. DOI: 10.1177/1357034X97003003004.
```

Review status:

```text
specified_not_reviewed_for_canonical_adoption
```

Boundary:

```text
Exact source specified does not mean canonical source adopted.
Exact source specified does not authorize passage insertion.
Exact source specified does not authorize citation insertion.
Exact source specified does not authorize Buchanan interpretation.
```

Next step:

```text
BDP-001K — Review exact Buchanan source candidate for canonical adoption readiness.
```

## BDP-001K PDF Availability and Canonical Metadata Adoption Readiness

The exact Buchanan source candidate has been reviewed against the uploaded PDF availability.

Observed uploaded PDF:

```text
7daa2f5c56c085aba493f7cdc309cddb.pdf
```

Review result:

```text
pdf_access_status = user_provided_pdf_available
source_text_available_for_review = true
canonical_metadata_adoption_readiness = ready_for_metadata_adoption_only
```

Boundary:

```text
BDP-001K does not adopt a canonical source.
BDP-001K does not insert a passage.
BDP-001K does not insert a citation.
BDP-001K does not create a concept mention or relation.
BDP-001K does not create an interpretation or Buchanan claim.
```

Next step:

```text
BDP-001L — Adopt reviewed Buchanan source metadata into canonical sources only.
```

## BDP-001L Canonical Metadata Adoption Record

The exact Buchanan source candidate reviewed in BDP-001J and BDP-001K has been adopted as canonical source metadata only.

Adopted canonical metadata:

```text
title = The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?
author = Ian Buchanan
type = article
publication_year = 1997
journal = Body & Society
volume = 3
issue = 3
pages = 73-91
doi = 10.1177/1357034X97003003004
url_or_reference = https://doi.org/10.1177/1357034X97003003004
publisher = SAGE Publications
rights_status = restricted
reliability_level = high
status = canonical
```

Candidate-history treatment:

```text
source_candidates_count remains 3
reviewed candidate is preserved as approved/adopted review history
adopted_from = BDP-001J + BDP-001K
pdf_access_status = user_provided_pdf_available
display_rule = reference_only
```

Boundary:

```text
BDP-001L adopts metadata only.
BDP-001L does not insert source text.
BDP-001L does not insert a passage.
BDP-001L does not insert a citation.
BDP-001L does not create a concept mention or relation.
BDP-001L does not create an interpretation or Buchanan claim.
```

Next step:

```text
BDP-001M — Prepare first Buchanan passage candidate from the adopted article, without inserting citation or interpretation yet.
```

## BDP-001M Passage Candidate Preparation Record

The adopted Buchanan article has now been used to prepare a passage-candidate envelope only.

Candidate metadata:

```text
candidate_label = BDP-001M first Buchanan passage candidate for Body without Organs
source = Ian Buchanan, "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?"
target_concept = Body without Organs
candidate_status = candidate
review_status = prepared
candidate_scope = passage_candidate_envelope_metadata_only
candidate_text_stored = false
locator_selected = false
rights_status = restricted
display_rule = reference_only
```

Boundary:

```text
A passage candidate is not a canonical passage.
A candidate envelope is not article text.
PDF availability is not permission to reproduce the article.
Candidate preparation does not authorize citation insertion.
Candidate preparation does not authorize interpretation.
Candidate preparation does not authorize a Buchanan-specific claim.
```

Next step:

```text
BDP-001N — Review selected Buchanan passage candidate text and locator before any citation or interpretation insertion.
```

## BDP-001N Passage Candidate Review Record

The adopted Buchanan article now has one reviewed passage-candidate locator and short excerpt for `Body without Organs`.

Candidate review metadata:

```text
candidate_text_status = reviewed_short_excerpt
locator_status = reviewed
page_or_timestamp = printed article page 76; PDF page 4
chapter_or_section = opening section before Spinoza
review_status = approved
review_status_detail = reviewed_for_later_passage_insertion
citation_ready = true
concept_mention_ready = false
interpretation_ready = false
buchanan_claim_ready = false
inserted_as_passage = false
```

Boundary:

```text
The candidate is still not a canonical passage.
Citation insertion is not performed in BDP-001N.
No Buchanan-specific claim is authorized yet.
```

Next step:

```text
BDP-001O — Insert reviewed Buchanan passage and citation only, if operator approves.
```
