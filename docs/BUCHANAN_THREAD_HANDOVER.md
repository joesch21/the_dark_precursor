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
