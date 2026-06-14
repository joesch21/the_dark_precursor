# Buchanan Semantic Workbench Doctrine

## Purpose

BDP-002A creates the first operator-facing semantic workbench slice for `Body without Organs`.

The semantic workbench is not a new evidence layer. It is a readback and explanation surface over already-governed evidence.

It exists so the operator can see what the platform can already do without waiting for every Buchanan source, passage, citation, relation, and interpretation to be complete.

## Working Rule

```text
Do not build the entire library first, then understand concepts.
Build one clean evidence spine.
Build one semantic concept workbench.
Repeat only where needed.
```

## Authority Label Contract

Every semantic explanation must carry one of the controlled authority labels below:

```text
citation_backed
primary_text_backed
buchanan_pending
provisional_synthesis
needs_review
user_interpretation
system_synthesis
```

The workbench may contain provisional teaching scaffolding, but provisional text must never be presented as Buchanan's position.

## Body without Organs BDP-002A Card

The first readback card must separate:

1. concept identity.
2. plain-language explanation placeholder.
3. technical Deleuzian explanation placeholder.
4. Buchanan-specific explanation status.
5. current evidence chain.
6. related concept candidates.
7. authority labels.
8. confirmed knowledge.
9. provisional knowledge.
10. open evidence gaps.
11. next recommended action.

## Evidence Boundary

The BDP-002A workbench may read:

```text
concepts
sources
source_candidates
passage_candidates
passages
citations
concept_mentions
concept_relations
interpretations
schema_migrations
```

It may not write to any of them.

## Buchanan Boundary

BDP-002A may say:

```text
Buchanan-specific explanation is pending.
Buchanan article metadata exists.
A Buchanan passage candidate envelope exists.
The next evidence task is to review the passage candidate locator and short text.
```

BDP-002A must not say:

```text
Buchanan argues X.
Buchanan claims X.
Buchanan's view is X.
```

That authority remains blocked until a Buchanan passage is reviewed, inserted, cited, and linked.

## Read-Only Verifier Requirements

The verifier must prove that BDP-002A preserves the current invariant:

```text
sources_count = 2
source_candidates_count = 3
passage_candidates_count = 1
passages_count = 1
citations_count = 1
concept_mentions_count = 1
concept_relations_count = 0
interpretations_count = 0
BDP-002A migration_count = 0
```

The verifier must also prove:

```text
BDP-002A is read-only.
Buchanan-specific explanation is marked pending and blocked.
All semantic explanations carry authority labels.
No Buchanan claim is generated.
No SQL migration is added.
```

## BDP-002A.1 Workbench Tooling Boundary

The semantic workbench is read-only.

Implementation boundary:

```text
No psycopg dependency.
No psycopg2 dependency.
Use existing psql subprocess readback style.
No SQL migration.
No database mutation.
```

Verifier boundary:

```text
Check database counts before and after readback.
Check Buchanan explanation remains pending and blocked.
Check all explanation sections carry authority labels.
Check SQL strings passed to psql helpers for mutation keywords.
Do not scan explanatory prose as if it were SQL.
```


## BDP-002A.2 Psycho-Linguistic Workbench Direction

The semantic workbench may later expose psycho-linguistic observations, but only as labelled modelling surfaces over governed evidence.

Allowed future observation types include:

1. conceptual recursion.
2. metaphor density.
3. abstraction gradient.
4. rhetorical destabilisation.
5. affective pressure point.
6. tonal transition.
7. ambiguity structure.
8. semantic drift.

BDP-002A.2 does not implement these fields yet.

Boundary:

```text
Psycho-linguistic observation is not citation authority.
Reader transformation modelling is not hidden psychological profiling.
LLM inference is not mind-reading or psychological certainty.
```

All future psycho-linguistic workbench fields must carry authority labels and evidence posture.

## BDP-001N.1 Description Authority Rule

The semantic workbench may show source-bound descriptions when they describe governed records rather than authorial positions.

Allowed workbench description:

```text
A Buchanan passage candidate has a reviewed short excerpt and locator for the Body without Organs concept.
```

Blocked author-position claim:

```text
Buchanan argues that the Body without Organs means X.
```

All descriptions must carry authority labels.

Recommended authority labels for descriptions:

```text
record_description
source_bound_description
citation_backed
buchanan_pending
needs_review
```

A description does not become an interpretation unless it attributes conceptual meaning or theoretical consequence to an author.

## BDP-001O Workbench Evidence Posture

After BDP-001O, the semantic workbench may report a stronger evidence posture for the Buchanan article:

```text
Buchanan passage status = citation_backed_passage_available
Buchanan concept mention status = pending
Buchanan interpretation status = blocked
Buchanan claim status = blocked
```

Allowed workbench description:

```text
A short citation-backed Buchanan passage is available for later Body without Organs concept linking.
```

Blocked author-position claim:

```text
Buchanan argues that the Body without Organs means X.
```

The workbench must keep Buchanan-specific explanation marked pending until a reviewed concept mention and later interpretation layer exist.


## BDP-001P Workbench Evidence Posture

After BDP-001P, the semantic workbench may report a stronger Buchanan evidence posture:

```text
Buchanan passage status = citation_backed_passage_available
Buchanan concept mention status = reviewed_direct_concept_mention_available
Buchanan relation status = blocked
Buchanan interpretation status = blocked
Buchanan claim status = blocked
```

Allowed workbench description:

```text
A citation-backed Buchanan passage is linked to Body without Organs through a reviewed concept mention.
```

Blocked author-position claim:

```text
Buchanan argues that the Body without Organs means X.
```

The workbench must keep Buchanan-specific interpretation marked blocked until a later governed interpretation layer exists.

## BDP-001Q Buchanan Evidence Card Readback

BDP-001Q prepares the first Buchanan-specific `Body without Organs` evidence card as a read-only workbench surface.

The card may show:

```text
concept identity
Buchanan source metadata
citation locator
citation-backed passage status
reviewed concept mention status
rights display rule
blocked relation status
blocked interpretation status
blocked Buchanan claim status
```

Allowed workbench description:

```text
A citation-backed Buchanan passage is linked to Body without Organs through a reviewed concept mention.
```

Blocked workbench claim:

```text
Buchanan argues that the Body without Organs means X.
```

The evidence card must display `passage_text_display = omitted_by_rights_policy` for restricted passage text.

## BDP-002B Operator-Facing Evidence Card

BDP-002B consolidates the existing Buchanan `Body without Organs` evidence spine into one operator-facing card generated by a read-only script.

The card may show:

```text
concept identity
canonical Buchanan source metadata
citation-backed passage record status
reviewed concept mention status
source-bound description with authority label
blocked relation status
blocked interpretation status
blocked Buchanan-specific claim status
rights/display rules
```

Required authority labels include:

```text
concept_record
metadata
citation_backed_passage
reviewed_concept_mention
source_bound_description
record_description
rights_display_boundary
blocked_until_reviewed_relation_evidence
blocked_until_governed_interpretation_phase
blocked_until_interpretive_authority_exists
```

Allowed card description:

```text
The database records a restricted, citation-backed Buchanan passage linked to Body without Organs through a reviewed direct concept mention.
```

Blocked card upgrade:

```text
No authorial position, conceptual meaning, relation, interpretation, synthesis, or Buchanan-specific claim may be generated by this card.
```

Rights rule:

```text
passage_text_display = omitted_by_rights_policy
long_quotation_displayed = false
article_reproduction_authorized = false
```

Implementation boundary:

```text
Read script only.
Verifier only.
No SQL migration.
No database mutation.
No frontend work.
No new source, passage, citation, concept mention, relation, interpretation, or generated Buchanan claim.
```

## BDP-002C Richer Semantic Readback Surface

BDP-002C expands the Buchanan `Body without Organs` evidence card into a 15-section read-only semantic readback surface.

The surface remains an evidence-posture card only. It does not create sources, passages, citations, concept mentions, concept relations, interpretations, generated synthesis, or Buchanan-specific claims.

Every section, field, item, and psycho-linguistic observation must carry a controlled authority label.

BDP-002C preserves the BDP-002A.1 tooling repair boundary:

```text
No psycopg dependency.
No psycopg2 dependency.
Use existing psql subprocess readback style.
No SQL migration.
No database mutation.
```

Required authority labels are defined in `docs/BDP_002C_RICHER_SEMANTIC_READBACK_SURFACE.md`.

Buchanan-specific explanation remains `buchanan_pending` and blocked until a governed interpretation phase.

Psycho-linguistic placeholders remain `experimental_modelling`, locator-linked, and human-review gated. Level 2 Embedding Deviation is the current ceiling.

## BDP-002D Relational and Adaptive Presentation Governance

The semantic workbench may adapt presentation depth, visual emphasis, metaphor complexity, or exploration paths in response to observed interaction signals, provided the adaptation is visible, inspectable, reversible, and under user control.

Required visible explanatory layer:

```text
How I am adapting this view
```

The explanatory layer must state:

1. what interaction signals were observed.
2. how those signals influenced the current view.
3. how the user can inspect, pause, reset, or manually override the adaptation.
4. that no psychological assessment is being made.
5. that no long-term user profile is being created unless explicit informed consent exists.

Allowed interaction-only signals:

```text
navigation patterns
metaphor selection
time spent on visual versus textual content
question style
depth of follow-up
preference for visual or conceptual framing
```

Boundary:

```text
Adaptive presentation changes display only.
It does not change citation authority.
It does not change interpretation status.
It does not create a Buchanan-specific claim.
It does not create a long-term user profile.
It does not perform psychological assessment.
The default fallback remains the non-adaptive evidence-first readback.
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

## BDP-002D.2 — Adaptation Control UX Contract

BDP-002D.2 defines the required user controls for any future adaptive presentation layer in the platform.

The semantic workbench must provide a visible and accessible **Explanatory Layer** (for example: “How this view is adapting”) that allows the user to:

- **Inspect**: View the current adaptation signals being used and how they are affecting the presentation.
- **Pause**: Temporarily disable adaptive presentation and receive a neutral/default view.
- **Reset**: Clear all session-scoped adaptation state and return to the platform default.
- **Override**: Manually select a preferred presentation mode at any time.

**Key Rules:**
- Adaptation is **session-scoped by default**.
- Any persistence of adaptation preferences beyond the current session requires **explicit informed consent**.
- Manual override always takes precedence over system-inferred adaptation.
- This contract applies only to interface presentation adaptation. It does not authorise psychological profiling or reader-state modelling.
