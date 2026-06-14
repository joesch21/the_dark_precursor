# BDP-002D — Relational and Adaptive Presentation Governance

**Status:** Doctrine Slice  
**Version:** 1.0  
**Date:** 14 June 2026  
**Related:** `BUCHANAN_SEMANTIC_WORKBENCH.md`, `BUCHANAN_PSYCHOLINGUISTIC_SEMANTIC_ARCHITECTURE.md`, `BUCHANAN_ARCHITECTURE.md`, `BUCHANAN_THREAD_HANDOVER.md`

## 1. Purpose

BDP-002D records a governed rule for relational and adaptive presentation in the Buchanan semantic workbench.

The workbench may adapt its display depth, visual emphasis, metaphor complexity, or exploration paths in response to visible interaction signals, but only when the adaptation is transparent, inspectable, reversible, and under user control.

This is a presentation-governance rule. It is not a new interpretation layer, not a reader-state storage layer, not a psychological assessment layer, and not a schema change.

## 2. Core Rule

The semantic workbench may adapt its presentation in response to observed interaction signals only if the adaptation is accompanied by a visible explanatory layer.

Required explanatory layer wording:

```text
How I am adapting this view
```

The explanatory layer must state:

1. what interaction signals were observed.
2. how those signals influenced the current view.
3. how the user can pause, reset, inspect, or override the adaptation.
4. that no psychological assessment is being made.
5. that no long-term user profile is being created unless explicit informed consent exists.

## 3. Allowed Adaptation Dimensions

Allowed presentation adaptations:

1. depth of explanation.
2. visual emphasis.
3. metaphor complexity.
4. exploration path ordering.
5. concept-card density.
6. relation-map visibility.
7. plain-language versus technical-language balance.

These are display choices only. They do not change citation authority, concept authority, interpretation status, or source status.

## 4. Allowed Interaction Signals

Allowed signals are interaction-only and session-bound unless later governance explicitly permits storage.

Allowed signals:

1. navigation patterns.
2. metaphor selection.
3. time spent on visual versus textual content.
4. question style.
5. depth of follow-up.
6. preference for visual or conceptual framing.

These signals may guide presentation only. They must not be framed as personality diagnosis, cognitive assessment, psychological profiling, or hidden reader-state inference.

## 5. User Control Requirements

Any adaptive presentation must provide user controls for:

1. inspect adaptation.
2. pause adaptation.
3. reset adaptation.
4. manually override the current presentation mode.
5. return to the canonical evidence-first view.

The default fallback must always be the non-adaptive evidence-first readback.

## 6. Storage Boundary

BDP-002D permits no long-term user profile.

Controlled status:

```text
sql_migration = false
database_mutation = false
reader_state_tracking = false
long_term_user_profile = false
psychological_assessment = false
hidden_personalisation = false
frontend_implementation = false
```

Future storage of adaptive preferences requires a separate governed phase with explicit consent, minimisation, inspectability, reset, export, and deletion rules.

## 7. Relation to Psycho-Linguistic Architecture

Adaptive presentation may support the workbench's relational and intuitive use, but it must not collapse psycho-linguistic modelling into user profiling.

Allowed:

```text
The workbench is showing a more visual path because the current session has used visual navigation heavily.
```

Blocked:

```text
The system has inferred the user's psychological type.
```

Allowed:

```text
The workbench is using a simpler metaphor layer because the user selected plain-language framing.
```

Blocked:

```text
The user is being psychologically assessed as needing simplified language.
```

## 8. Authority Boundary

Adaptive presentation does not change authority labels.

An adaptive view may reorder or emphasize already-labelled sections, but it must not upgrade:

1. `metadata` into evidence.
2. `source_bound_description` into interpretation.
3. `secondary_scholarship` into Buchanan direct claim.
4. `experimental_modelling` into objective assessment.
5. `buchanan_pending` into a Buchanan-specific explanation.

## 9. Documentation Integration

BDP-002D updates documentation only.

It should be reflected in:

1. `docs/BUCHANAN_SEMANTIC_WORKBENCH.md`
2. `docs/BUCHANAN_PSYCHOLINGUISTIC_SEMANTIC_ARCHITECTURE.md`
3. `docs/BUCHANAN_ARCHITECTURE.md`
4. `docs/BUCHANAN_THREAD_HANDOVER.md`
5. `ai_boot/BUCHANAN_SYSTEM_STATE.json`

## 10. Success Criteria

BDP-002D is successful when:

1. the adaptive-presentation rule is documented.
2. transparency and user-control requirements are explicit.
3. long-term profiling remains blocked.
4. psychological assessment framing remains blocked.
5. no database, schema, frontend, source, passage, citation, concept mention, relation, interpretation, or generated Buchanan claim is created.

**End of Document**

<!-- BDP-002D.1 INTERACTION ADAPTATION BOUNDARY START -->

## BDP-002D.1 Interaction Adaptation vs Text Psycho-Linguistics

The platform distinguishes two different uses of psycho-linguistic and relational modelling.

### Text Psycho-Linguistics — Layer 3

```text
Focus: how language moves, pressures, and transforms meaning in the texts.
Authority label: experimental_modelling.
Evidence requirement: linked to governed passage locators.
Review requirement: requires human review.
Boundary: never authorizes Buchanan-specific claims without exact source evidence.
```

Examples include metaphor density, conceptual recursion, rhetorical destabilisation, affective pressure, abstraction gradient, and semantic drift in Buchanan / Deleuze and Guattari writing.

### Interaction Adaptation — Relational Layer

```text
Focus: how the interface responds to the user's engagement style during a session.
Allowed signals: navigation choices, time spent on visuals vs text, question style, metaphor preference, depth of exploration.
Boundary: the system observes how the user is using the interface; it does not analyse psychological state or cognitive profile.
```

Interaction adaptation may adjust visual vs textual density, explanation depth, metaphor complexity, or exploration paths.

### Required Explanatory Layer

Any adaptive behaviour must include an always-accessible explanatory layer, such as:

```text
How this view is adapting
```

The explanatory layer must state:

```text
what interaction signals were observed
how those signals are currently influencing the experience
how the user can inspect, pause, reset, or manually adjust the adaptation
```

### Governance Rules

```text
adaptation_must_be_explicit = true
adaptation_must_be_user_controllable = true
session_scoped_by_default = true
long_term_profile_storage_default = false
persistence_requires_explicit_informed_consent = true
psychological_assessment_allowed = false
objective_psychological_insight_claim_allowed = false
psycho_linguistic_analysis_remains_text_focused = true
```

This distinction protects the evidence-first principles while allowing the workbench to become more relational and intuitive.

<!-- BDP-002D.1 INTERACTION ADAPTATION BOUNDARY END -->
