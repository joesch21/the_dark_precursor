#!/usr/bin/env python3
"""Conservatively update Buchanan docs and state for BDP-001M."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

STATE_PATH = Path("ai_boot/BUCHANAN_SYSTEM_STATE.json")

PHASE_RECORD: dict[str, Any] = {
    "phase": "BDP-001M",
    "status": "complete",
    "title": "Prepare first Buchanan passage candidate from the adopted article, without inserting citation or interpretation yet",
    "controlled_slice": "passage_candidate_preparation_only",
    "database_change": {
        "created_table_when_missing": "passage_candidates",
        "inserted_passage_candidates": 1,
        "inserted_canonical_passages": 0,
        "inserted_citations": 0,
        "inserted_concept_mentions": 0,
        "inserted_concept_relations": 0,
        "inserted_interpretations": 0,
    },
    "passage_candidate": {
        "candidate_label": "BDP-001M first Buchanan passage candidate for Body without Organs",
        "source_title": "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?",
        "source_author": "Ian Buchanan",
        "source_doi": "10.1177/1357034X97003003004",
        "target_concept": "Body without Organs",
        "candidate_status": "candidate",
        "review_status": "prepared",
        "candidate_scope": "passage_candidate_envelope_metadata_only",
        "candidate_text_stored": False,
        "locator_selected": False,
        "display_rule": "reference_only",
        "rights_status": "restricted",
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
    },
    "boundaries": {
        "canonical_passage_insertion": False,
        "citation_insertion": False,
        "concept_mention_insertion": False,
        "concept_relation_insertion": False,
        "interpretation_insertion": False,
        "generated_buchanan_claim": False,
        "long_pdf_quotation": False,
        "candidate_text_storage": False,
    },
    "next_step": "BDP-001N — Review selected Buchanan passage candidate text and locator before any citation or interpretation insertion.",
}

APPENDS: dict[str, tuple[str, str]] = {
    "docs/BUCHANAN_THREAD_HANDOVER.md": (
        "## BDP-001M Handover Update",
        """
## BDP-001M Handover Update

First Buchanan passage candidate preparation completed as a candidate-only governed slice.

Completed:

1. Created `passage_candidates` as a staging table for candidate passages before canonical passage insertion.
2. Prepared one passage-candidate envelope for Ian Buchanan's 1997 article `The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?`.
3. Linked the candidate envelope to the adopted canonical Buchanan source.
4. Linked the candidate envelope to the `Body without Organs` concept as an intended review target.
5. Preserved the candidate as metadata-only and review-pending.
6. Stored no Buchanan article text in the candidate.
7. Selected no page locator yet.
8. Inserted no canonical passage, citation, concept mention, concept relation, interpretation, generated synthesis, or Buchanan claim.
9. Added `sql/013_prepare_bdp_001m_first_buchanan_passage_candidate.sql`.
10. Added `scripts/read_bdp_001m_first_buchanan_passage_candidate.py`.
11. Added `scripts/verify_bdp_001m_first_buchanan_passage_candidate.py`.
12. Added `scripts/verify_bdp_001m_phase_chain_invariant.py`.
13. Added `scripts/update_bdp_001m_docs_and_state.py`.

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
```

Boundary:

```text
No Buchanan article passage inserted.
No Buchanan article citation inserted.
No Buchanan article concept mention inserted.
No concept relation inserted.
No interpretation inserted.
No generated Buchanan claim.
No long quotation from the PDF.
No candidate text stored yet.
```

Next step:

```text
BDP-001N — Review selected Buchanan passage candidate text and locator before any citation or interpretation insertion.
```
""",
    ),
    "docs/BUCHANAN_SOURCE_INTAKE_REGISTRY.md": (
        "## BDP-001M Passage Candidate Preparation Record",
        """
## BDP-001M Passage Candidate Preparation Record

The adopted Buchanan article has now been used to prepare a passage-candidate envelope only.

Candidate metadata:

```text
candidate_label = BDP-001M first Buchanan passage candidate for Body without Organs
source = Ian Buchanan, "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?"
target_concept = Body without Organs
candidate_status = candidate
review_status = prepared
candidate_scope = passage_candidate_envelope_metadata_only
candidate_text_stored = false
locator_selected = false
rights_status = restricted
display_rule = reference_only
```

Boundary:

```text
A passage candidate is not a canonical passage.
A candidate envelope is not article text.
PDF availability is not permission to reproduce the article.
Candidate preparation does not authorize citation insertion.
Candidate preparation does not authorize interpretation.
Candidate preparation does not authorize a Buchanan-specific claim.
```

Next step:

```text
BDP-001N — Review selected Buchanan passage candidate text and locator before any citation or interpretation insertion.
```
""",
    ),
    "docs/BUCHANAN_CITATION_AND_RIGHTS.md": (
        "## BDP-001M Passage Candidate Rights Boundary",
        """
## BDP-001M Passage Candidate Rights Boundary

BDP-001M prepares a passage-candidate envelope from the adopted Buchanan article metadata only.

Rights and display treatment:

```text
rights_status = restricted
display_rule = reference_only
candidate_text_stored = false
long_quotation_stored = false
article_reproduction_authorized = false
```

BDP-001M does not authorize quotation display, article reproduction, citation insertion, interpretation, generated synthesis, or a Buchanan-specific claim.

A later phase must review any proposed short excerpt and locator before the system may insert a canonical passage or citation.
""",
    ),
    "docs/BUCHANAN_SCHEMA_CONTROL.md": (
        "## BDP-001M Passage Candidate Staging Patch",
        """
## BDP-001M Passage Candidate Staging Patch

BDP-001M introduces candidate passage staging so the platform can prepare passage review targets without collapsing them into canonical evidence.

### passage_candidates

Stores passage candidates before canonical passage insertion.

Fields:

```text
id
source_id
concept_id
candidate_label
candidate_status
candidate_scope
candidate_text
candidate_text_status
page_or_timestamp
chapter_or_section
locator_status
rights_status
display_rule
review_status
extraction_status
inserted_as_passage
citation_ready
concept_mention_ready
interpretation_ready
buchanan_claim_ready
created_at
reviewed_at
metadata
```

Purpose:

```text
A passage candidate can identify what should be reviewed next without becoming a passage, citation, concept mention, relation, interpretation, or claim.
```

### Migration Note

BDP-001M creates the `passage_candidates` staging table when missing and inserts one metadata-only candidate envelope for the adopted Buchanan article.

It does not insert a canonical passage into `passages`.

It does not insert a citation into `citations`.

It does not insert a concept mention, concept relation, interpretation, generated synthesis, or Buchanan-specific claim.

### Validation Addition

BDP-001M is valid only if verification proves:

1. `sources_count = 2`.
2. `source_candidates_count = 3`.
3. `passage_candidates_count = 1`.
4. `passages_count = 1`.
5. `citations_count = 1`.
6. `concept_mentions_count = 1`.
7. `concept_relations_count = 0`.
8. `interpretations_count = 0`.
9. the Buchanan article has zero canonical passages attached.
10. the Buchanan article has zero citations attached.
11. the passage candidate stores no Buchanan article text.
12. `BDP-001M migration_count = 1`.
""",
    ),
    "docs/BUCHANAN_INGESTION_WORKFLOW.md": (
        "## BDP-001M Passage Candidate Preparation",
        """
## BDP-001M Passage Candidate Preparation

BDP-001M adds a controlled staging step between canonical source metadata and canonical passage insertion.

Updated controlled sequence:

```text
canonical source metadata
→ passage candidate envelope
→ operator review of exact text and locator
→ approved passage insertion
→ citation insertion
→ concept mention
→ relation or interpretation only after evidence exists
```

Boundary:

```text
candidate envelope is not passage evidence
candidate text absent means no quotation authority
locator pending means no citation authority
prepared candidate does not authorize interpretation
prepared candidate does not authorize Buchanan-specific claims
```

This keeps the adopted Buchanan source available for later passage review without treating bibliographic adoption as textual evidence.
""",
    ),
}


def append_once(path: Path, marker: str, text: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing required docs file: {path}")
    current = path.read_text(encoding="utf-8")
    if marker in current:
        print(f"[SKIP] {path} already contains {marker}")
        return
    suffix = "" if current.endswith("\n") else "\n"
    path.write_text(current + suffix + text.strip() + "\n", encoding="utf-8")
    print(f"[OK] appended {marker} to {path}")


def update_state() -> None:
    if not STATE_PATH.exists():
        raise FileNotFoundError(f"Missing state file: {STATE_PATH}")
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if not isinstance(state, dict):
        raise TypeError(f"{STATE_PATH} must contain a JSON object")

    state["last_completed_phase"] = "BDP-001M"
    state["current_phase"] = "BDP-001M"
    state["next_phase"] = "BDP-001N"
    state["bdp_001m_passage_candidate_preparation"] = PHASE_RECORD

    if isinstance(state.get("phase_records"), dict):
        state["phase_records"]["BDP-001M"] = PHASE_RECORD

    if isinstance(state.get("phases"), dict):
        state["phases"]["BDP-001M"] = PHASE_RECORD

    if isinstance(state.get("phase_history"), list):
        state["phase_history"] = [
            item for item in state["phase_history"]
            if not (isinstance(item, dict) and item.get("phase") == "BDP-001M")
        ]
        state["phase_history"].append(PHASE_RECORD)

    invariant = PHASE_RECORD["verified_invariant"]
    if isinstance(state.get("database_scope"), dict):
        state["database_scope"]["current_verified_invariant"] = invariant
        state["database_scope"]["sources_count"] = 2
        state["database_scope"]["source_candidates_count"] = 3
        state["database_scope"]["passage_candidates_count"] = 1
        state["database_scope"]["passages_count"] = 1
        state["database_scope"]["citations_count"] = 1
        state["database_scope"]["concept_mentions_count"] = 1
        state["database_scope"]["concept_relations_count"] = 0
        state["database_scope"]["interpretations_count"] = 0

    if isinstance(state.get("database"), dict):
        state["database"]["current_verified_invariant"] = invariant

    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[OK] updated {STATE_PATH} for BDP-001M")


def main() -> int:
    for file_name, (marker, text) in APPENDS.items():
        append_once(Path(file_name), marker, text)
    update_state()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
