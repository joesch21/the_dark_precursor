# Buchanan Concept Ontology

## Purpose

This document defines the first concept ontology for the Buchanan Deleuze Intelligence Platform.

The ontology should remain flexible, but not chaotic.

## Core Concept Object

A concept is not merely a keyword. It is a structured interpretive object.

Each concept may include:

1. preferred name.
2. aliases.
3. source passages.
4. Buchanan explanations.
5. Deleuze and Guattari usages.
6. related concepts.
7. contested interpretations.
8. applied contexts.
9. teaching explanations.

## Initial Concept Cluster

First cluster:

```text
Body without Organs
organism
desire
assemblage
strata
deterritorialisation
reterritorialisation
schizoanalysis
becoming
war machine
capitalism
```

## Relation Types

Recommended relation types:

```text
explains
depends_on
opposes
modifies
intensifies
emerges_from
is_applied_to
is_contested_by
is_translated_as
is_linked_to
is_example_of
```

## Authority Levels

Every concept claim must carry an authority level.

```text
primary_text
buchanan_direct
secondary_scholarship
system_synthesis
user_interpretation
```

## Claim Rule

The system must not say:

```text
Buchanan thinks X
```

unless there is a source-backed passage.

If no direct evidence is available, use:

```text
A Buchanan-informed reading would suggest X.
```

## First Concept Prototype

Concept:

```text
Body without Organs
```

Prototype views:

1. Plain explanation.
2. Buchanan explanation.
3. Deleuze and Guattari primary usage.
4. Concept map.
5. Comparison with other theorists.
6. Applied interpretation.
7. Source trail.

## Ontology Drift Rule

Adding, renaming, merging, or deleting a concept requires:

1. evidence source.
2. relation update.
3. schema/state update if structure changes.
4. review status.

## BDP-001A Canonical Relation Vocabulary

The canonical relation vocabulary is:

```text
explains
depends_on
opposes
modifies
intensifies
emerges_from
is_applied_to
is_contested_by
is_translated_as
is_linked_to
is_example_of
develops
reframes
extends
critiques
operationalises
```

Relation vocabulary changes are ontology changes. They require evidence, review status, state update, and schema-control update.

## BDP-001J.0 Concept Evidence Depth Tiers

Not every concept requires full-source treatment.

Concept detail follows authority:

```text
show term exists
→ light record

show concept is mentioned
→ concept mention + passage

show relation between concepts
→ relation + evidence passage

say Buchanan argues something
→ exact Buchanan source + passage + citation

generate synthesis
→ multiple evidence-backed records + authority label
```

Concept tiers:

```text
Tier 1 — Anchor Concepts: full citation-backed treatment.
Tier 2 — Supporting Concepts: reviewed mention or relation evidence.
Tier 3 — Contextual Terms: proposed lightweight status until promoted.
```

No Buchanan-specific claim may be made without an exact Buchanan source passage.

## BDP-002A Semantic Workbench Authority Contract

The `Body without Organs` semantic workbench may display explanation scaffolds only when they are explicitly labelled.

Allowed BDP-002A authority labels:

```text
citation_backed
primary_text_backed
buchanan_pending
provisional_synthesis
needs_review
user_interpretation
system_synthesis
```

The first workbench card treats `Body without Organs` as an anchor concept with one existing primary-text evidence chain and one Buchanan passage-candidate envelope.

Buchanan-specific explanation remains blocked until a Buchanan passage is reviewed, inserted as a canonical passage, cited, and linked through a concept mention.

The workbench may list related concept candidates such as `organism`, `desire`, `assemblage`, and `strata`, but BDP-002A does not create relation records.


## BDP-002A.2 Psycho-Linguistic Concept Boundary

A concept may later carry psycho-linguistic modelling metadata, but such metadata is not the same as a concept claim.

Examples of future modelling dimensions:

```text
metaphor_density
abstraction_gradient
conceptual_recursion
semantic_elasticity
affective_pressure_point
rhetorical_destabilisation
tonal_transition
interpretive_openness
```

Governance rule:

```text
Psycho-linguistic modelling may describe how language moves.
It may not upgrade authority beyond the available source evidence.
```

No Buchanan-specific psycho-linguistic interpretation may be promoted without an exact Buchanan passage, citation, and reviewed concept link.

## BDP-001N.1 Description Versus Claim Rule

Concept records may contain descriptions of evidence posture without creating concept claims.

Allowed:

```text
This concept has a reviewed Buchanan passage candidate.
```

Blocked until stronger evidence:

```text
Buchanan's interpretation of the concept is X.
```

A description becomes a claim when it attributes a position, argument, intention, conceptual meaning, or theoretical consequence to Buchanan, Deleuze, Guattari, or another author.

Authority ladder:

```text
metadata
→ locator
→ short excerpt
→ source-bound description
→ citation-backed passage
→ concept mention
→ interpretation
→ synthesis
```

## BDP-001O Citation-Backed Passage Boundary

The first Buchanan article passage may now exist as citation-backed passage evidence after BDP-001O.

This upgrades the evidence spine from reviewed candidate to canonical passage plus citation, but it does not yet create a Buchanan concept mention or interpretation.

Allowed after BDP-001O:

```text
The platform has a citation-backed Buchanan passage record available for later Body without Organs concept linking.
```

Blocked until a later governed phase:

```text
Buchanan's interpretation of the Body without Organs is X.
Buchanan argues that the Body without Organs means X.
```

The next ontology step is a reviewed `concept_mentions` row linking the inserted Buchanan passage to `Body without Organs`.

