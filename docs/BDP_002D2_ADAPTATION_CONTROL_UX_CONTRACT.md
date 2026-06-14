# BDP-002D.2 — Adaptation Control UX Contract

**Status:** Doctrine and UX Contract Phase  
**Version:** 1.0  
**Date:** 14 June 2026  
**Type:** Doctrine-only (no implementation)

## 1. Purpose

This phase defines the required user control contract for any future adaptive presentation layer in the Buchanan Deleuze Intelligence Platform.

The goal is to ensure that any interface adaptation remains transparent, inspectable, and fully under user control before any adaptive frontend behaviour is implemented.

## 2. Core Distinction

- **Text Psycho-Linguistics**: Analyses how language moves and produces meaning in governed texts. Remains experimental and evidence-linked.
- **Interaction Adaptation**: Adjusts interface presentation (visual density, explanation depth, metaphor emphasis, etc.) during a session based on observed interaction signals only.

Interaction adaptation must **never** be framed as analysis of the user’s psychological state, cognitive profile, personality, or mental condition.

## 3. Required Explanatory Layer

Any future adaptive interface must include a visible and accessible **Explanatory Layer** (recommended label: “How this view is adapting”).

This layer must clearly communicate:

- Observed interaction signals (session-scoped)
- How those signals are influencing the current presentation
- Whether adaptation is currently active or paused
- How to pause adaptation
- How to reset adaptation
- How to manually override adaptation
- Whether adaptation state is session-only or has become persistent (and whether persistence was explicitly consented to)

## 4. Allowed Interaction Signals

The following signals may be observed for adaptation purposes. All signals are **session-scoped by default**:

- Navigation choices and selected metaphors
- Time spent on visual versus textual content
- Question style and depth of follow-up questions
- Metaphor or conceptual framing preferences
- Depth of exploration and selected conceptual routes
- Manual view preferences

**Prohibited**: Any inference framed as psychological assessment, cognitive profiling, or long-term user modelling without explicit informed consent.

## 5. Required User Controls

The platform must provide four core controls:

### 5.1 Inspect
- User can view the current adaptation explanation.
- User can see the specific interaction signals currently being used.
- User can see the effect of those signals on the current presentation.

### 5.2 Pause
- User can temporarily disable adaptive presentation.
- While paused, the system must use a neutral/default presentation mode.
- Pausing must not delete session history unless the user chooses to reset.

### 5.3 Reset
- User can clear all session-scoped adaptation state.
- Reset must return the presentation to the platform default.
- Reset must not alter canonical evidence, sources, concepts, citations, or interpretations.

### 5.4 Override
- User can manually select a preferred presentation mode at any time.
- Manual override must take precedence over any system-inferred adaptation.
- Recommended override options include:
  - More visual / More textual
  - Simpler explanation / Deeper technical explanation
  - Less metaphor / More metaphor
  - Evidence-first mode
  - Concept-map mode

## 6. Persistence and Consent

- Adaptation state is **session-scoped by default**.
- Any persistence of adaptation preferences beyond the current session requires **explicit informed consent**.
- The user must be able to revoke consent and clear persistent state at any time.

## 7. Governance Boundaries

BDP-002D.2 establishes the following non-negotiable boundaries:

- No frontend implementation or UI components may be added in this phase.
- No database mutation, SQL migration, or schema changes are permitted.
- No user tracking, reader-state storage, or long-term profiles may be introduced.
- No psychological assessment language or framing is authorised.
- No Buchanan-specific interpretations or claims may be generated.
- No concept relations or new evidence records may be created.

This UX contract applies **only** to interface presentation adaptation. It does not extend to the Reader / Listener Transformation Layer, which remains future-governed and separate.

## 8. Success Criteria

BDP-002D.2 is successful when:

- A clear, documented UX contract exists defining Inspect, Pause, Reset, and Override.
- An Explanatory Layer is mandated for any future adaptive presentation.
- The distinction between text psycho-linguistics and interaction adaptation is preserved.
- All adaptation remains transparent, session-scoped by default, and under explicit user control.
- The platform is ready for future implementation planning without having implemented any adaptive behaviour.

**End of Document**