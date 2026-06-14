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

