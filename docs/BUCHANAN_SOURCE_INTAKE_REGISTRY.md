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
