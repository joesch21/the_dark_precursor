# Buchanan Deleuze Intelligence Platform Architecture

## Purpose

This platform is an interpretive intelligence system for engaging with Ian Buchanan's scholarship and the wider conceptual field of Deleuze and Guattari studies.

It is not designed as a generic chatbot. It is designed as a structured cognitive research environment that can trace concepts, cite passages, compare interpretations, and support scholarly synthesis.

## Core Principle

The platform does not pretend to speak as Ian Buchanan. It operates as a disciplined interpretive apparatus grounded in Buchanan's published work, lectures, transcripts, interviews, and teaching material.

## Primary Knowledge Layers

1. **Source Layer**  
   Stores books, articles, transcripts, interviews, lectures, URLs, bibliographic metadata, and rights status.

2. **Passage Layer**  
   Stores cited text chunks with page numbers, timestamps, sections, or source references.

3. **Concept Layer**  
   Stores concepts such as Body without Organs, assemblage, desire, schizoanalysis, deterritorialisation, strata, becoming, and war machine.

4. **Relation Layer**  
   Stores relationships between concepts, including dependency, contrast, development, opposition, application, and genealogy.

5. **Interpretation Layer**  
   Separates Buchanan's direct interpretations, Deleuze and Guattari primary usage, secondary scholarship, generated synthesis, and user interpretation.

6. **Usage Layer**  
   Stores user pathways, repeated questions, useful responses, confusion points, and emergent conceptual routes.

## Recommended Technical Shape

Initial system:

```text
PostgreSQL + pgvector
```

Later expansion:

```text
PostgreSQL + pgvector + graph projection + event log
```

The database should begin with relational structure and vector search. Graph functionality can be added after the first concept prototype is stable.

## First Vertical Slice

Initial concept:

```text
Body without Organs
```

Initial functions:

1. Explain through Buchanan.
2. Compare with Deleuze and Guattari.
3. Show related concepts.
4. Trace source passages.
5. Apply the concept to a contemporary problem.

## System Boundary

The system must distinguish between:

1. What Buchanan explicitly says.
2. What Deleuze and Guattari explicitly write.
3. What other scholars argue.
4. What the system synthesizes.
5. What users propose.

No generated synthesis should be treated as canonical without review.

## BDP-002A Semantic Workbench Layer

The semantic workbench is an operator-facing readback layer over the existing source, passage, citation, and concept records.

It does not create evidence. It displays evidence posture.

For `Body without Organs`, BDP-002A introduces a JSON-like concept card that can show provisional explanatory scaffolding while preserving the boundary between:

1. primary-text-backed evidence.
2. Buchanan metadata.
3. Buchanan passage candidates.
4. Buchanan-specific claims that remain blocked.
5. generated system synthesis that remains provisional.

Every explanation in the workbench must carry an authority label.

BDP-002A is intentionally lightweight. It creates a readback script, a verifier, and doctrine before any frontend renderer is added.


## BDP-002A.2 Psycho-Linguistic Semantic Architecture

BDP-002A.2 records the platform's higher architectural direction: philosophical meaning must be modelled not only as retrievable information, but as conceptual movement through language.

The long-term architecture now distinguishes four interpretive layers:

1. citation and provenance.
2. semantic concept modelling.
3. psycho-linguistic modelling.
4. reader / listener transformation modelling.

This direction does not weaken the evidence spine. It strengthens the need for governance: psycho-linguistic observations are modelling claims, not source authority.

Controlled boundary:

```text
No SQL migration.
No database mutation.
No reader-state tracking.
No psycho-linguistic tables yet.
No Buchanan-specific claim.
No generated interpretation.
```

The dedicated doctrine file is:

```text
docs/BUCHANAN_PSYCHOLINGUISTIC_SEMANTIC_ARCHITECTURE.md
```

## BDP-002D Relational Adaptive Presentation Layer

The platform may later include an adaptive presentation layer for the semantic workbench.

This layer may adjust explanation depth, visual emphasis, metaphor complexity, or exploration path order in response to visible interaction-only signals. It remains subordinate to the evidence spine and must include an explanatory layer showing how the view is being adapted.

User control requirements:

```text
inspect adaptation
pause adaptation
reset adaptation
manual override
return to canonical evidence-first view
```

Governance boundary:

```text
No long-term user profile without explicit informed consent.
No psychological assessment framing.
No hidden personalisation.
No change to citation, source, concept, relation, interpretation, or Buchanan-claim authority.
```

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
