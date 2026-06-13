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
