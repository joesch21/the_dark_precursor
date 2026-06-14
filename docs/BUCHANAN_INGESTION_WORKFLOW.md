# Buchanan Ingestion Workflow

## Purpose

This document defines how material enters the Buchanan Deleuze Intelligence Platform.

The system must grow through disciplined intake rather than uncontrolled scraping.

## Intake Modes

### 1. Manual Upload

Accepted material may include:

1. PDFs.
2. DOCX files.
3. EPUB files.
4. copied text.
5. lecture notes.
6. transcripts.

### 2. Curated Import

Curated imports may include:

1. YouTube transcripts.
2. article URLs.
3. bibliography records.
4. publisher metadata.
5. Zotero exports.

### 3. Assisted Discovery

The system may suggest candidate sources, but it must not automatically adopt them into the canonical knowledge base.

Suggested sources enter `source_candidates` first.

## Ingestion Flow

```text
source discovered
→ source candidate created
→ operator review
→ source accepted or rejected
→ text extracted
→ text cleaned
→ document chunked
→ metadata attached
→ concepts detected
→ embeddings generated
→ passages stored
→ citations generated
→ concept graph updated
→ ingestion event recorded
```

## Source Statuses

```text
candidate
approved
rejected
imported
cleaned
chunked
embedded
concept_tagged
reviewed
canonical
```

## Passage Requirements

Each passage should preserve:

1. source ID.
2. page number or timestamp.
3. chapter, section, or video segment.
4. citation string.
5. rights status.
6. extraction version.

## Concept Detection

Concept detection may be automated, but concept acceptance requires review.

Mention types:

```text
direct
implied
contested
related
metaphorical
```

Review statuses:

```text
proposed
accepted
rejected
needs_review
```

## YouTube Transcript Rule

For video transcripts:

1. Preserve URL.
2. Preserve timestamp ranges.
3. Preserve speaker if available.
4. Clean filler words only if the raw transcript remains recoverable.
5. Do not treat transcript text as canonical if accuracy is uncertain.

## Ingestion Boundary

The system may discover and stage sources.  
The system may not canonize sources without review.

## BDP-001D Candidate Review Gate

Before a source candidate can be considered for canonical adoption, it must carry structured review metadata in `source_candidates.metadata`.

Required review metadata:

```text
title
author
type
candidate status
review notes
bibliographic edition or version note
rights status recommendation
reliability level recommendation
adoption readiness
operator review requirement
```

The title, author, type, status, and review notes may remain normal table fields. Additional review detail should be stored in `metadata JSONB` to avoid over-expanding the schema during early platform formation.

Candidate review does not create source evidence.

The system must preserve this sequence:

```text
source candidate created
→ candidate metadata enriched
→ operator reviews candidate
→ operator adopts or rejects candidate
→ only then may canonical source ingestion begin
```

BDP-001D boundary:

```text
No canonical source records.
No passage records.
No interpretation records.
```

## BDP-001H Source Intake Registry

BDP-001H adds a read-only source intake registry and candidate creation preview layer.

Purpose:

```text
Make future Buchanan / Deleuze source intake inspectable before any source candidate is inserted.
```

Boundary:

```text
Preview is not creation.
Candidate is not canonical source.
Canonical source is not passage evidence.
Passage evidence is not interpretation.
```

BDP-001H does not create source candidates, canonical sources, passages, citations, concept mentions, concept relations, or interpretations.

Next step:

```text
BDP-001I — Select first Buchanan source candidate for Body without Organs.
```

## BDP-001I Buchanan Placeholder Candidate Selection

BDP-001I selects the existing Ian Buchanan Body without Organs placeholder candidate as the next review target.

This is selection-only.

Boundary:

```text
The placeholder candidate remains a candidate.
No canonical Buchanan source is created.
Canonical adoption is hard-blocked until an exact Buchanan publication, lecture, transcript, interview, or teaching source is specified.
```

Preferred repository working method:

```text
make patch bundle
→ download zip
→ unzip locally
→ apply with git apply --check
→ run verifiers
→ commit/push from local repo
```

Next step:

```text
BDP-001J — Specify exact Buchanan source for Body without Organs candidate review.
```

## BDP-001J.0 Concept Evidence Depth Tiers

BDP-001J.0 records that concepts do not all require the same evidence depth.

The ingestion workflow should scale evidence requirements by intended authority:

```text
contextual term
→ proposed record only

supporting concept
→ reviewed mention evidence

anchor concept
→ citation-backed source, passage, concept mention, and later relation or interpretation evidence
```

Buchanan-specific claims remain blocked until an exact Buchanan source passage is specified, reviewed, cited, and linked.

## BDP-001L Metadata-Only Canonical Source Adoption

BDP-001L promotes the reviewed Buchanan article candidate into canonical `sources` as metadata only.

Controlled sequence:

```text
BDP-001J exact source specified
→ BDP-001K PDF availability and adoption readiness reviewed
→ BDP-001L canonical source metadata adopted
→ BDP-001M passage candidate preparation may begin later
```

Boundary:

```text
canonical source metadata is not source text
source text availability is not passage evidence
passage preparation is not passage insertion
citation insertion remains blocked until a passage is approved
interpretation remains blocked until evidence exists
Buchanan-specific claims remain blocked until an exact passage and citation are linked
```

The original source candidate remains review history and is not deleted.

## BDP-001M Passage Candidate Preparation

BDP-001M adds a controlled staging step between canonical source metadata and canonical passage insertion.

Updated controlled sequence:

```text
canonical source metadata
→ passage candidate envelope
→ operator review of exact text and locator
→ approved passage insertion
→ citation insertion
→ concept mention
→ relation or interpretation only after evidence exists
```

Boundary:

```text
candidate envelope is not passage evidence
candidate text absent means no quotation authority
locator pending means no citation authority
prepared candidate does not authorize interpretation
prepared candidate does not authorize Buchanan-specific claims
```

This keeps the adopted Buchanan source available for later passage review without treating bibliographic adoption as textual evidence.

## BDP-001N Passage Candidate Review

BDP-001N completes the controlled review step between passage-candidate preparation and canonical passage insertion.

Updated controlled sequence:

```text
canonical source metadata
→ passage candidate envelope
→ operator review of exact short text and locator
→ reviewed passage candidate
→ approved passage insertion later
→ citation insertion later
→ concept mention later
→ relation or interpretation only after evidence exists
```

Boundary:

```text
reviewed candidate text is not canonical passage evidence
reviewed locator is not citation insertion
citation_ready means ready for later governed insertion
concept mention remains blocked
interpretation remains blocked
Buchanan-specific claims remain blocked
```

## BDP-001N.1 Description Layer

BDP-001N.1 adds a missing layer between short excerpt review and canonical interpretation.

Updated ladder:

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

A source-bound description may describe the reviewed record and evidence posture.

It must not attribute a position, argument, intention, conceptual meaning, or theoretical consequence to an author unless the stronger governed evidence layer exists.

This prevents the system from jumping directly from excerpt review to interpretation.

## BDP-001O Reviewed Passage and Citation Insertion

BDP-001O completes the first canonical Buchanan passage-and-citation insertion after BDP-001N review.

Updated controlled sequence:

```text
canonical source metadata
→ passage candidate envelope
→ operator review of exact short text and locator
→ reviewed passage candidate
→ canonical passage insertion
→ citation insertion
→ concept mention later
→ relation or interpretation only after evidence exists
```

Boundary:

```text
citation-backed passage is not yet a concept mention
citation-backed passage is not yet a Buchanan interpretation
citation-backed passage does not authorize a generated Buchanan claim
concept mention remains blocked until the next governed phase
interpretation remains blocked
Buchanan-specific claims remain blocked
```


## BDP-001P Reviewed Concept Mention Link

BDP-001P completes the next controlled step after canonical Buchanan passage and citation insertion.

Updated controlled sequence:

```text
canonical source metadata
→ passage candidate envelope
→ operator review of exact short text and locator
→ reviewed passage candidate
→ canonical passage insertion
→ citation insertion
→ reviewed concept mention
→ relation or interpretation only after later evidence review
```

Boundary:

```text
The Buchanan passage is now linked to Body without Organs through a reviewed concept mention.
The concept mention is not a concept relation.
The concept mention is not an interpretation.
The concept mention does not authorize a generated Buchanan claim.
Interpretation remains blocked.
```
