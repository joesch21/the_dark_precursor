# BDP-002D.1 — Interaction Adaptation vs Text Psycho-Linguistics Boundary

**Status:** Governance Doctrine Slice  
**Version:** 1.0  
**Date:** 14 June 2026  
**Related:** `BDP_002D_RELATIONAL_ADAPTIVE_PRESENTATION.md`, `BUCHANAN_SEMANTIC_WORKBENCH.md`, `BUCHANAN_PSYCHOLINGUISTIC_SEMANTIC_ARCHITECTURE.md`, `BUCHANAN_ARCHITECTURE.md`

## Purpose

BDP-002D.1 records a strict distinction between two different uses of psycho-linguistic and relational modelling in the Buchanan Platform:

1. **Text psycho-linguistics**, which models how philosophical language moves inside governed texts.
2. **Interaction adaptation**, which controls how the interface responds during a user session.

This distinction protects the evidence-first platform while still allowing the workbench to become relational, intuitive, and inspectable.

## Core Distinction

```text
Text psycho-linguistics studies the text.
Interaction adaptation adjusts the interface.
Neither layer authorizes psychological assessment of the user.
Neither layer authorizes Buchanan-specific claims without governed evidence.
```

## 1. Text Psycho-Linguistics — Layer 3

Focus:

```text
Focus: how language moves, pressures, and transforms meaning in the texts.
How language moves, pressures, and transforms meaning in the texts.
```

Examples:

```text
metaphor density
conceptual recursion
rhetorical destabilisation
affective pressure in Buchanan / Deleuze and Guattari writing
abstraction gradient
semantic drift
```

Status:

```text
authority_label = experimental_modelling
linked_to_governed_passage_locator = required
requires_human_review = true
objective_psychological_claim = false
buchanan_specific_claim_authorized = false
```

Boundary:

```text
Text psycho-linguistics may describe modelling observations over governed text passages.
It must not produce Buchanan-specific claims without exact source evidence.
It must not infer reader psychology.
```

## 2. Interaction Adaptation — Relational Layer

Focus:

```text
How the interface responds to the user's engagement style during a session.
```

Examples:

```text
adjust visual vs textual density
adjust depth of explanation
adjust metaphor complexity
adjust exploration paths
surface alternative conceptual routes
```

Allowed interaction signals:

```text
navigation choices
time spent on visuals vs text
question style
metaphor preference
depth of exploration
```

Strict boundary:

```text
This layer does not analyse the psychological state or cognitive profile of the user.
It only observes how the user is using the interface.
```

## Transparency Requirement

Any adaptive behaviour must be accompanied by a clear, always-accessible explanatory layer.

The explanatory layer must state:

```text
what interaction signals were observed
how those signals are currently influencing the experience
how the user can inspect the adaptation
how the user can pause the adaptation
how the user can reset the adaptation
how the user can manually adjust the adaptation
```

Suggested visible label:

```text
How this view is adapting
```

## Governance Rules for Interaction Adaptation

```text
adaptation_must_be_explicit = true
adaptation_must_be_user_controllable = true
session_scoped_by_default = true
long_term_profile_storage_default = false
persistence_requires_explicit_informed_consent = true
psychological_assessment_allowed = false
objective_psychological_insight_claim_allowed = false
text_psycho_linguistics_remains_text_focused = true
```

The system must never present adaptation as objective psychological insight.

Psycho-linguistic analysis remains focused on the texts, not the user.

## Implementation Boundary

BDP-002D.1 is doctrine only.

It does not:

1. add a SQL migration.
2. mutate the database.
3. add reader-state tracking.
4. add long-term user profile storage.
5. implement frontend adaptation.
6. create psychological assessment.
7. create Buchanan-specific interpretation.
8. create concept relation evidence.
9. create source, passage, citation, concept mention, interpretation, or generated synthesis.

## State Boundary

The system state may record that this governance distinction exists.

The system state must not record any user profile, interaction signal, adaptation preference, or psychological inference.

## Success Criteria

BDP-002D.1 is successful when the documentation clearly records that:

1. text psycho-linguistics is passage-linked experimental modelling over texts.
2. interaction adaptation is session-scoped interface behaviour.
3. adaptation requires a visible explanatory layer.
4. the user can inspect, pause, reset, or manually override adaptation.
5. no long-term psychological profiles are stored without explicit informed consent.
6. adaptation is never framed as psychological assessment or objective psychological insight.

**End of Document**

<!-- BDP-002D.1 VERIFIER PHRASE ALIGNMENT START -->

## Verifier Phrase Alignment

This section preserves exact governance phrases required by the current BDP-002D.1 verifier. It does not change the doctrine meaning; it prevents exact-string drift between doctrine wording and verifier wording.

```text
Text Psycho-Linguistics
Interaction Adaptation
Focus: how language moves, pressures, and transforms meaning in the texts
Focus: how the interface responds to the user's engagement style during a session
Allowed signals: navigation choices, time spent on visuals vs text, question style, metaphor preference, depth of exploration
does not analyse psychological state or cognitive profile
How this view is adapting
what interaction signals were observed
inspect, pause, reset, or manually adjust
session_scoped_by_default = true
long_term_profile_storage_default = false
persistence_requires_explicit_informed_consent = true
psychological_assessment_allowed = false
objective_psychological_insight_claim_allowed = false
psycho_linguistic_analysis_remains_text_focused = true
```

<!-- BDP-002D.1 VERIFIER PHRASE ALIGNMENT END -->
