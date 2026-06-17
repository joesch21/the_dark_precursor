# BDP-003F.4 — Dark Precursor Navigation Architecture

**Phase:** BDP-003F.4
**Status:** Complete
**Controlled slice:** navigation architecture definition only
**Authority:** Governance/definition only; no frontend implementation.

## Purpose

BDP-003F.4 defines the navigation architecture for The Dark Precursor before adding further frontend pages.

The application now has a cinematic concept stage and an About page. This phase defines the map before adding more rooms, so the experience does not drift into random page accumulation or become a generic dashboard.

## Current surfaces

The current public-facing surfaces are:

1. **Title gate** — the cinematic entry threshold.
2. **Cinematic concept stage** — the primary working surface where concepts are staged, generated responses appear, and concept-card drafts may be downloaded for local human review.
3. **About page** — a supporting explanation surface that frames The Dark Precursor as a governed cinematic concept laboratory.

## Primary surface

The **cinematic concept stage** remains the primary surface.

It is the centre of the application. Navigation must return users to this stage rather than pulling them into a dashboard-style collection of unrelated pages.

The stage is where the application performs its intended work:

1. entering a concept or scene;
2. staging a cinematic response;
3. preserving slow, readable narrator presentation;
4. maintaining the distinction between generated synthesis and evidence authority.

## Supporting surfaces

The **About page** is a supporting explanation surface.

Its role is to orient the user, not to become a second application centre. It explains the posture of The Dark Precursor and must always provide a clear return path to the cinematic concept stage.

Supporting pages must remain contextual. They may help explain, orient, review, or configure the experience, but they must not displace the stage.

## Future allowed surface candidates

Future navigation may include these architectural candidates:

1. **Concept stage** — primary cinematic working surface.
2. **About** — supporting public explanation.
3. **Archive / reviewed outputs** — future reviewed local outputs only, if separately approved.
4. **Source / evidence posture** — orientation to evidence boundaries, not evidence mutation.
5. **Settings / controls** — explicit visible controls only, not hidden adaptation.
6. **Help / orientation** — lightweight guidance for using the cinematic surface.

These are candidates only. BDP-003F.4 does not implement, wire, route, or authorize any new page.

## Movement contract

Navigation must follow these rules:

1. The cinematic concept stage is the default return point.
2. Supporting pages must have a clear return path to the concept stage.
3. Page movement must be explicit and visible to the user.
4. Navigation must preserve cinematic immersion.
5. Navigation must avoid dashboard drift.
6. Navigation must not introduce hidden personalization, hidden adaptation, or psychological profiling.
7. Navigation must not create or imply scholarly authority.

## Authority boundary

Moving between surfaces does not create:

1. citation authority;
2. source ingestion;
3. evidence promotion;
4. concept relations;
5. interpretations;
6. Buchanan-specific claims;
7. database records;
8. backend services;
9. adapter invocations;
10. image or video generation.

Navigation is an experiential structure only. It is not an evidence operation.

## Philosophical and experiential protection

Navigation must protect the application’s central distinction:

> atmosphere is not authority.

The Dark Precursor may be cinematic, immersive, and conceptually suggestive, but its movement between surfaces must not make generated synthesis appear to have scholarly authority.

The concept stage should feel like a room with a few governed doors, not a dashboard with uncontrolled tabs.

## Implementation boundary

BDP-003F.4 authorizes no implementation.

Specifically, this phase does not add:

1. new frontend page routing;
2. new Streamlit controls;
3. backend services;
4. adapter endpoints;
5. database tables;
6. SQL migrations;
7. archive workflow expansion;
8. evidence promotion;
9. citations;
10. concept relations;
11. interpretations;
12. Buchanan-specific claims;
13. image generation backend;
14. video generation backend;
15. user profile memory;
16. adaptive navigation behaviour.

## Decision

The Dark Precursor navigation architecture is defined as a governed cinematic surface model:

1. the cinematic concept stage is primary;
2. the About page is supporting;
3. future pages are only architectural candidates;
4. every supporting surface must return clearly to the stage;
5. navigation must preserve immersion and prevent dashboard drift;
6. navigation must not create evidence or scholarly authority.

## Next safe step

BDP-003F.5 — Wire navigation architecture only after BDP-003F.4 is committed and pushed.
