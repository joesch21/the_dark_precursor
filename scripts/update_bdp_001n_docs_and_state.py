#!/usr/bin/env python3
from pathlib import Path
import json
from datetime import datetime, timezone
import textwrap

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "ai_boot" / "BUCHANAN_SYSTEM_STATE.json"

phase_record = {
    "phase": "BDP-001N",
    "status": "complete",
    "title": "Review first Buchanan passage candidate locator and short text, without inserting citation or interpretation",
    "controlled_slice": "passage_candidate_locator_text_review_only",
    "passage_candidate_review": {
        "source_author": "Ian Buchanan",
        "source_title": "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?",
        "source_doi": "10.1177/1357034X97003003004",
        "target_concept": "Body without Organs",
        "candidate_text_status": "reviewed_short_excerpt",
        "candidate_text_stored": True,
        "candidate_excerpt_word_count": 9,
        "locator_status": "reviewed",
        "page_or_timestamp": "printed article page 76; PDF page 4",
        "chapter_or_section": "opening section before Spinoza",
        "review_status": "approved",
        "review_status_detail": "reviewed_for_later_passage_insertion",
        "citation_ready": True,
        "concept_mention_ready": False,
        "interpretation_ready": False,
        "buchanan_claim_ready": False,
        "inserted_as_passage": False,
        "rights_status": "restricted",
        "display_rule": "reference_only",
        "display_rule_detail": "reference_only_short_excerpt_candidate"
    },
    "boundaries": {
        "canonical_passage_insertion": False,
        "citation_insertion": False,
        "concept_mention_insertion": False,
        "concept_relation_insertion": False,
        "interpretation_insertion": False,
        "generated_buchanan_claim": False,
        "long_pdf_quotation": False,
        "article_reproduction_authorized": False,
        "frontend_work": False,
        "psycho_linguistic_modelling_implementation": False
    },
    "verified_invariant": {
        "sources_count": 2,
        "source_candidates_count": 3,
        "passage_candidates_count": 1,
        "passages_count": 1,
        "citations_count": 1,
        "concept_mentions_count": 1,
        "concept_relations_count": 0,
        "interpretations_count": 0,
        "BDP-001M migration_count": 1,
        "BDP-001N migration_count": 1,
        "BDP-002A migration_count": 0
    },
    "next_step": "BDP-001O — Insert reviewed Buchanan passage and citation only, if operator approves.",
    "updated_at": datetime.now(timezone.utc).isoformat()
}

if STATE.exists():
    state = json.loads(STATE.read_text(encoding="utf-8"))
else:
    state = {}

state["bdp_001n_passage_candidate_review"] = phase_record
state["current_phase"] = "BDP-001N"
state["next_recommended_step"] = phase_record["next_step"]
STATE.write_text(json.dumps(state, indent=4, sort_keys=True) + "\n", encoding="utf-8")

append_blocks = {
    "docs/BUCHANAN_THREAD_HANDOVER.md": """
## BDP-001N Handover Update

First Buchanan passage candidate locator and short text review completed.

Completed:

1. Reviewed the existing `passage_candidates` row for Ian Buchanan's 1997 article.
2. Recorded one short rights-aware candidate excerpt.
3. Recorded locator as printed article page 76 / PDF page 4.
4. Marked the candidate as reviewed for later passage insertion.
5. Marked citation readiness as true for a later governed citation phase.
6. Preserved concept mention, interpretation, and Buchanan-claim readiness as false.
7. Confirmed the candidate is still not a canonical passage.
8. Confirmed no citation, concept mention, concept relation, interpretation, or Buchanan claim was inserted.
9. Added `sql/014_review_bdp_001n_buchanan_passage_candidate_locator_text.sql`.
10. Added `scripts/read_bdp_001n_buchanan_passage_candidate_review.py`.
11. Added `scripts/verify_bdp_001n_buchanan_passage_candidate_review.py`.
12. Added `scripts/update_bdp_001n_docs_and_state.py`.

Current invariant:

```text
sources_count = 2
source_candidates_count = 3
passage_candidates_count = 1
passages_count = 1
citations_count = 1
concept_mentions_count = 1
concept_relations_count = 0
interpretations_count = 0
BDP-001M migration_count = 1
BDP-001N migration_count = 1
BDP-002A migration_count = 0
```

Boundary:

```text
No canonical Buchanan article passage inserted.
No Buchanan article citation inserted.
No Buchanan article concept mention inserted.
No concept relation inserted.
No interpretation inserted.
No generated Buchanan claim.
No long quotation from the PDF.
The reviewed candidate excerpt is short and rights-aware.
```

Next step:

```text
BDP-001O — Insert reviewed Buchanan passage and citation only, if operator approves.
```
""",
    "docs/BUCHANAN_SCHEMA_CONTROL.md": """
## BDP-001N Passage Candidate Locator and Short Text Review Patch

BDP-001N updates the existing `passage_candidates` row for the adopted Buchanan article.

It records:

```text
candidate_text_status = reviewed_short_excerpt
locator_status = reviewed
review_status = approved
review_status_detail = reviewed_for_later_passage_insertion
citation_ready = true
concept_mention_ready = false
interpretation_ready = false
buchanan_claim_ready = false
inserted_as_passage = false
```

Migration note:

```text
BDP-001N updates candidate review metadata only.
It does not create a canonical passage.
It does not create a citation.
It does not create a concept mention, concept relation, interpretation, synthesis, or Buchanan-specific claim.
```

Validation addition:

BDP-001N is valid only if verification proves:

1. exactly one Buchanan article passage candidate exists.
2. the candidate stores only a short reviewed excerpt.
3. the candidate locator is reviewed.
4. `citation_ready = true`.
5. `inserted_as_passage = false`.
6. `concept_mention_ready = false`.
7. `interpretation_ready = false`.
8. `buchanan_claim_ready = false`.
9. canonical table counts are preserved.
10. `BDP-001N migration_count = 1`.
""",
    "docs/BUCHANAN_CITATION_AND_RIGHTS.md": """
## BDP-001N Passage Candidate Short Excerpt Rights Boundary

BDP-001N reviews one short candidate excerpt and locator from the user-provided Buchanan PDF.

Rights and display treatment:

```text
rights_status = restricted
display_rule = reference_only
display_rule_detail = reference_only_short_excerpt_candidate
candidate_text_status = reviewed_short_excerpt
long_quotation_stored = false
article_reproduction_authorized = false
```

BDP-001N does not authorize article reproduction.

It does not insert a canonical passage or citation.

The reviewed short excerpt may support a later governed passage-and-citation insertion phase, but it is not yet canonical evidence.
""",
    "docs/BUCHANAN_INGESTION_WORKFLOW.md": """
## BDP-001N Passage Candidate Review

BDP-001N completes the controlled review step between passage-candidate preparation and canonical passage insertion.

Updated controlled sequence:

```text
canonical source metadata
→ passage candidate envelope
→ operator review of exact short text and locator
→ reviewed passage candidate
→ approved passage insertion later
→ citation insertion later
→ concept mention later
→ relation or interpretation only after evidence exists
```

Boundary:

```text
reviewed candidate text is not canonical passage evidence
reviewed locator is not citation insertion
citation_ready means ready for later governed insertion
concept mention remains blocked
interpretation remains blocked
Buchanan-specific claims remain blocked
```
""",
    "docs/BUCHANAN_SOURCE_INTAKE_REGISTRY.md": """
## BDP-001N Passage Candidate Review Record

The adopted Buchanan article now has one reviewed passage-candidate locator and short excerpt for `Body without Organs`.

Candidate review metadata:

```text
candidate_text_status = reviewed_short_excerpt
locator_status = reviewed
page_or_timestamp = printed article page 76; PDF page 4
chapter_or_section = opening section before Spinoza
review_status = approved
review_status_detail = reviewed_for_later_passage_insertion
citation_ready = true
concept_mention_ready = false
interpretation_ready = false
buchanan_claim_ready = false
inserted_as_passage = false
```

Boundary:

```text
The candidate is still not a canonical passage.
Citation insertion is not performed in BDP-001N.
No Buchanan-specific claim is authorized yet.
```

Next step:

```text
BDP-001O — Insert reviewed Buchanan passage and citation only, if operator approves.
```
"""
}

for rel, block in append_blocks.items():
    path = ROOT / rel
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    marker = block.strip().splitlines()[0]
    if marker not in text:
        path.write_text(text.rstrip() + "\n\n" + textwrap.dedent(block).strip() + "\n", encoding="utf-8")

print("BDP-001N docs and state updated.")
