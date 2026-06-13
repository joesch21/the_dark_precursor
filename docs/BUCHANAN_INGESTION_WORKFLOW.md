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
