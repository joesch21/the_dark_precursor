# BDP-003F.6 — Concept Lens Architecture

**Status:** Complete  
**Completed:** 2026-06-18T01:50:00+00:00  
**Controlled slice:** architecture definition only  
**Authority:** Application architecture / UX governance only  
**Frontend implementation:** No  
**Backend service:** No  
**Database mutation:** No  
**SQL migration:** No  

## Purpose

BDP-003F.6 defines the **Concept Lens** as a future archive-grounded exploration surface for Deleuzian concepts inside The Dark Precursor.

The Concept Lens answers the application problem surfaced by concept questions such as:

1. What is repetition?
2. What is the Body without Organs?
3. What is assemblage?
4. How does Buchanan frame desire, affect, method, or schizoanalysis?
5. How should a student understand a concept without flattening it into common-sense psychology?

The Concept Lens is not a general chatbot, not a dashboard, and not a per-concept page system. It is a governed concept-answering **dock** that may later be placed inside the existing cinematic concept stage.

## Existing anchors

BDP-003F.6 is anchored in the existing platform shape:

1. The platform is a differential reading engine, not merely a database.
2. The cinematic concept stage remains the primary surface.
3. Navigation architecture must avoid dashboard drift.
4. Generated material remains provisional synthesis unless later promoted through governed evidence review.
5. Buchanan-specific claims require exact evidence.
6. The SQL archive remains the evidence spine.

## Concept Lens thesis

The Concept Lens provides one bounded route from user concept questions to archive-aware explanations:

```text
User asks a concept question
        ↓
Concept Lens identifies the concept and answer mode
        ↓
Future read-only archive lookup checks evidence posture
        ↓
Answer is generated with visible authority labels
        ↓
A future fidelity warning layer flags conceptual flattening risk
        ↓
Output remains exploratory unless archive evidence supports stronger authority
```

## Placement rule

The Concept Lens is a **future dock inside the concept stage**, not a new public page in this phase.

It may later be rendered as a compact panel within the existing Dark Precursor stage, but BDP-003F.6 does not wire frontend controls, Streamlit components, routes, buttons, or page keys.

This preserves the BDP-003F.4 / BDP-003F.5 navigation boundary: the stage remains primary, and supporting explanation surfaces must not become dashboard drift.

## Future answer layers

A future Concept Lens answer should contain four layers:

1. **Plain explanation** — readable introduction for students and general users.
2. **Technical Deleuzian explanation** — more precise conceptual framing.
3. **Archive evidence posture** — what the Buchanan SQL archive currently supports.
4. **Fidelity warning** — risks of flattening, over-psychologising, or making unsupported Buchanan claims.

The four layers should remain visibly separate. The app must not blur provisional synthesis, source-bound description, and citation-backed claim.

## SQL archive leverage

The Concept Lens should later leverage the Buchanan scholarly SQL archive through a read-only evidence posture path:

```text
concepts
  → concept_mentions
  → passages
  → citations
  → sources
```

Optional future layers may include:

```text
concept_relations
interpretations
source_candidates
passage_candidates
```

Those optional layers must only be used when governed evidence exists. They must not be inferred from generated text.

## Evidence posture levels

Future Concept Lens responses should classify concept-answer authority using a visible evidence posture:

1. **archive_grounded** — concept has reviewed linked passage/citation/source evidence.
2. **source_bound_description** — the archive can describe evidence posture, but not yet make an interpretive claim.
3. **secondary_scholarship_supported** — secondary source metadata or reviewed excerpts support a cautious frame.
4. **system_synthesis** — useful generated explanation, but not archive-grounded.
5. **exploratory_unverified** — concept is being explored without sufficient archive evidence.

## Authority labels

The Concept Lens must preserve the platform authority ladder:

```text
primary_text
buchanan_direct
secondary_scholarship
system_synthesis
user_interpretation
```

A future answer must not present `system_synthesis` as `buchanan_direct`.

## Buchanan-specific claim boundary

The Concept Lens must never create a Buchanan-specific claim merely because a user asks for a Buchanan-style explanation.

Blocked examples:

```text
Buchanan argues that repetition means X.
Buchanan's reading of Deleuze is X.
Buchanan would say X about this concept.
```

Allowed only with explicit evidence:

```text
The archive contains a reviewed Buchanan source, passage, citation, and concept link that supports a bounded source-grounded description.
```

## Fidelity warning layer

The Concept Lens should later include a philosophical fidelity warning layer for high-risk concepts.

For Deleuze and Guattari concepts, warning checks should flag explanations that reduce concepts to:

1. habit,
2. routine,
3. pattern recognition,
4. self-help psychology,
5. generic identity maintenance,
6. unsupported author-position claims,
7. ordinary metaphor without qualification.

This fidelity layer is not implemented in BDP-003F.6. It is defined only as a future architecture requirement.

## Concept answer output contract candidate

A future Concept Lens answer should use a shape similar to:

```json
{
  "schema_id": "bdp_003f6_concept_lens_answer_candidate_v1",
  "concept": "repetition",
  "normalized_concept": "repetition",
  "question": "What does Deleuze mean by we repress because we repeat?",
  "answer_layers": {
    "plain_explanation": "...",
    "technical_explanation": "...",
    "archive_evidence_posture": "...",
    "fidelity_warning": "..."
  },
  "authority_label": "system_synthesis",
  "evidence_posture": "exploratory_unverified",
  "archive_chain": [],
  "rights_display_rule": "reference_only_when_restricted",
  "human_review_required": true,
  "evidence_promotion": false,
  "buchanan_specific_claim_created": false,
  "blocked_actions": [
    "no citation creation",
    "no concept relation creation",
    "no interpretation insertion",
    "no evidence promotion",
    "no Buchanan-specific claim without exact evidence"
  ]
}
```

This is a candidate contract only. It does not create a data model, file writer, UI renderer, SQL table, or backend service.

## UX principle

The Concept Lens should be small and direct:

```text
Ask a concept
Choose answer mode
Show answer
Show evidence posture
Show fidelity warning when needed
Return to cinematic stage
```

It must not add:

1. per-concept pages,
2. a large dashboard,
3. hidden adaptive personalization,
4. automatic evidence promotion,
5. a second general-purpose chat system,
6. uncontrolled archive writing.

## Explicit non-goals

BDP-003F.6 does not add:

1. frontend implementation,
2. Streamlit controls,
3. new navigation surface keys,
4. backend services,
5. adapter endpoints,
6. SQL migrations,
7. database tables,
8. source ingestion,
9. citation creation,
10. concept mention creation,
11. concept relation creation,
12. interpretation insertion,
13. evidence promotion,
14. Buchanan-specific claims,
15. external LLM routing,
16. automatic chat filtering,
17. hidden personalization,
18. psychological assessment.

## Future safe sequence

Recommended future sequence:

1. **BDP-003F.7** — Define read-only Concept Lens archive evidence posture service contract before implementation.
2. **BDP-003F.8** — Implement read-only concept evidence posture service, if approved.
3. **BDP-003F.9** — Review evidence posture output against known Body without Organs archive chain.
4. **BDP-003F.10** — Define Concept Lens UI dock wiring contract before frontend changes.
5. **BDP-003F.11** — Wire Concept Lens dock into the concept stage behind authority labels, if approved.
6. **BDP-003F.12** — Add philosophical fidelity warning review for generated concept answers, if approved.

## Decision

BDP-003F.6 approves the **architecture definition** of the Concept Lens only.

The Concept Lens is the correct future route for archive-grounded Deleuzian concept exploration because it keeps the application small:

```text
cinematic stage for encounter
Concept Lens for explanation
SQL archive for authority
fidelity warning for conceptual protection
reviewed cards for human-governed learning trails
```

Implementation remains blocked until a later explicitly approved phase.
