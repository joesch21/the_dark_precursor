# BDP-003F.1 — Teleprompter Narrator Stage

**Status:** Complete  
**Phase:** BDP-003F.1  
**Controlled slice:** frontend cinematic narrator UX only  
**Implementation status:** Full-screen teleprompter narrator stage implemented.

## Purpose

BDP-003F.1 changes the narrator reading experience so the generated narrator text scrolls upward through a large screen-height stage, like a teleprompter.

This replaces the previous chunk-by-chunk narrator reveal loop with a browser-side scrolling text track.

## What Changes

1. `frontend/dark_precursor.py`
   - Adds `teleprompter_duration_seconds`.
   - Reworks `reveal_text` so it renders the full narrator text as one scrolling teleprompter stage.
   - Preserves the existing `reveal_text(full_response, reveal_speed)` call path.
   - Keeps instant display behavior when reveal speed is set to `0`.

2. `frontend/styles/dark_precursor.css`
   - Adds teleprompter stage classes.
   - Uses a large viewport-height reading surface.
   - Animates the narrator text upward.
   - Preserves reduced-motion accessibility.

## User Experience

When the narrator speaks, the response now appears as a large cinematic teleprompter:

- text enters low on the screen,
- scrolls upward across the full stage,
- remains large and readable,
- keeps the existing Dark Precursor visual language,
- does not require manual scrolling during the animated reading.

## Boundaries

This is a frontend UX change only.

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
- BDP-003D cinematic video front page styling
- BDP-003E.16 archive control safety review

## Next Step

**BDP-003F.2 — Review teleprompter narrator stage in the running frontend before further cinematic UX changes.**
