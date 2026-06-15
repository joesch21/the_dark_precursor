# BDP-003F.2 — About Page for The Dark Precursor

**Status:** Complete  
**Phase:** BDP-003F.2  
**Controlled slice:** frontend explanatory UX only  
**Implementation status:** About page added to The Dark Precursor UI.

## Purpose

BDP-003F.2 adds an About page to The Dark Precursor so that a new reader, teacher, scholar, or invited reviewer can understand what the application is before using it.

The page explains that The Dark Precursor is a governed cinematic research interface for Deleuze, Guattari, and Ian Buchanan’s conceptual field.

## Core Explanation

The About page must make the following boundary clear:

The Dark Precursor does not claim to think like Ian Buchanan, impersonate Ian Buchanan, replace scholarship, or produce authoritative Deleuzian interpretation.

It stages concepts cinematically while preserving a strict separation between generated synthesis, human review, and evidence authority.

## What Changes

1. `frontend/dark_precursor.py`
   - Adds `render_about_page`.
   - Adds an About navigation control in the sidebar.
   - Adds a route guard that displays the About page instead of the main concept stage when selected.

2. `frontend/styles/dark_precursor.css`
   - Adds cinematic About page styles.

## User Experience

The sidebar now includes an About control. When selected, the user sees a full explanatory page that describes:

1. What the application is.
2. What it is not.
3. How it separates atmosphere from authority.
4. Why the cinematic interface exists.
5. How generated synthesis remains distinct from evidence.
6. What the archive and governance posture protects.

## Boundaries

This is a frontend explanatory UX change only.

No backend services.
No adapter endpoints.
No database tables.
No SQL migrations.
No archive workflow expansion.
No evidence promotion.
No citations.
No concept relations.
No interpretations.
No Buchanan-specific claims.

## Review Inputs

- `frontend/dark_precursor.py`
- `frontend/styles/dark_precursor.css`
- BDP-003F.1 teleprompter narrator stage
- BDP-003E.16 archive control safety review

## Next Step

**BDP-003F.3 — Review The Dark Precursor About page in the running frontend before further public-facing explanation changes.**
