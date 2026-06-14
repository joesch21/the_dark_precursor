#!/usr/bin/env python3
"""
Update Buchanan docs and state for BDP-001P.

This script intentionally appends compact phase records instead of rewriting the
whole documentation set. It does not mutate the database.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


PHASE = "BDP-001P"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def append_once(path: Path, marker: str, block: str) -> None:
    if not path.exists():
        raise SystemExit(f"Required document missing: {path}")

    text = path.read_text()
    if marker in text:
        print(f"[OK] {path} already contains {marker}")
        return

    if text and not text.endswith("\n"):
        text += "\n"

    path.write_text(text + "\n" + block.strip() + "\n")
    print(f"[OK] appended {marker} to {path}")


def update_state(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Required state file missing: {path}")

    state = json.loads(path.read_text())

    invariant = {
        "sources_count": 2,
        "source_candidates_count": 3,
        "passage_candidates_count": 1,
        "passages_count": 2,
        "citations_count": 2,
        "concept_mentions_count": 2,
        "concept_relations_count": 0,
        "interpretations_count": 0,
        "bdp_001o_migration_count": 1,
        "bdp_001p_migration_count": 1,
        "buchanan_article_passage_count": 1,
        "buchanan_article_citation_count": 1,
        "buchanan_article_concept_mention_count": 1,
    }

    state["bdp_001p_buchanan_concept_mention_only"] = {
        "phase": PHASE,
        "title": "Link inserted Buchanan passage to Body without Organs concept mention only",
        "status": "complete",
        "completed_at": NOW,
        "controlled_slice": "concept_mention_only",
        "database_mutation": True,
        "sql_migration": True,
        "inserted_rows": {
            "concept_mentions": 1,
            "schema_migrations": 1,
            "sources": 0,
            "passages": 0,
            "citations": 0,
            "concept_relations": 0,
            "interpretations": 0,
        },
        "target": {
            "source_author": "Ian Buchanan",
            "source_title": "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?",
            "concept": "Body without Organs",
            "mention_type": "direct",
            "reviewed_status": "accepted",
            "confidence": 1.0,
        },
        "verified_invariant": invariant,
        "boundary": {
            "new_source": False,
            "new_passage": False,
            "new_citation": False,
            "concept_relation": False,
            "interpretation": False,
            "generated_buchanan_claim": False,
            "frontend_work": False,
        },
        "next_step": "BDP-001Q — Prepare Buchanan Body without Organs concept readback after reviewed concept mention, without interpretation.",
    }

    state["current_verified_invariant"] = invariant
    state["next_step"] = "BDP-001Q — Prepare Buchanan Body without Organs concept readback after reviewed concept mention, without interpretation."

    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    print(f"[OK] updated {path}")


def main() -> None:
    update_state(Path("ai_boot/BUCHANAN_SYSTEM_STATE.json"))

    append_once(
        Path("docs/BUCHANAN_SCHEMA_CONTROL.md"),
        "## BDP-001P Reviewed Concept Mention Link Patch",
        """
## BDP-001P Reviewed Concept Mention Link Patch

BDP-001P links the inserted citation-backed Buchanan article passage to `Body without Organs` through one reviewed `concept_mentions` row.

It inserts:

```text
one concept_mentions row
one schema_migrations ledger row
```

Migration note:

```text
BDP-001P changes concept mention storage only.
It does not change schema shape.
It does not create a source, passage, citation, concept relation, interpretation, synthesis, or Buchanan-specific claim.
```

Validation addition:

BDP-001P is valid only if verification proves:

1. `sources_count = 2`.
2. `source_candidates_count = 3`.
3. `passage_candidates_count = 1`.
4. `passages_count = 2`.
5. `citations_count = 2`.
6. `concept_mentions_count = 2`.
7. exactly one reviewed direct `Body without Organs` concept mention is attached to the Buchanan article passage.
8. `concept_relations_count = 0`.
9. `interpretations_count = 0`.
10. `BDP-001P migration_count = 1`.
""",
    )

    append_once(
        Path("docs/BUCHANAN_INGESTION_WORKFLOW.md"),
        "## BDP-001P Reviewed Concept Mention Link",
        """
## BDP-001P Reviewed Concept Mention Link

BDP-001P completes the next controlled step after canonical Buchanan passage and citation insertion.

Updated controlled sequence:

```text
canonical source metadata
→ passage candidate envelope
→ operator review of exact short text and locator
→ reviewed passage candidate
→ canonical passage insertion
→ citation insertion
→ reviewed concept mention
→ relation or interpretation only after later evidence review
```

Boundary:

```text
The Buchanan passage is now linked to Body without Organs through a reviewed concept mention.
The concept mention is not a concept relation.
The concept mention is not an interpretation.
The concept mention does not authorize a generated Buchanan claim.
Interpretation remains blocked.
```
""",
    )

    append_once(
        Path("docs/BUCHANAN_CONCEPT_ONTOLOGY.md"),
        "## BDP-001P Buchanan Concept Mention Boundary",
        """
## BDP-001P Buchanan Concept Mention Boundary

The inserted citation-backed Buchanan passage is now linked to `Body without Organs` through one reviewed direct `concept_mentions` row.

Allowed after BDP-001P:

```text
The platform has a reviewed Buchanan concept mention linking the citation-backed Buchanan passage to Body without Organs.
```

Still blocked after BDP-001P:

```text
Buchanan's interpretation of the Body without Organs is X.
Buchanan argues that the Body without Organs means X.
```

The next ontology step is readback, not interpretation.
""",
    )

    append_once(
        Path("docs/BUCHANAN_SEMANTIC_WORKBENCH.md"),
        "## BDP-001P Workbench Evidence Posture",
        """
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
""",
    )

    append_once(
        Path("docs/BUCHANAN_SOURCE_INTAKE_REGISTRY.md"),
        "## BDP-001P Concept Mention Link Record",
        """
## BDP-001P Concept Mention Link Record

The canonical Buchanan passage inserted in BDP-001O is now linked to `Body without Organs`.

Successful BDP-001P result:

```text
canonical Buchanan passage inserted = already true from BDP-001O
citation inserted = already true from BDP-001O
concept mention inserted = true
concept relation inserted = false
interpretation inserted = false
buchanan claim inserted = false
```

Boundary:

```text
The concept mention confirms a reviewed concept link.
The concept mention is not a relation.
The concept mention is not an interpretation.
The concept mention is not a Buchanan-specific claim.
```

Next step:

```text
BDP-001Q — Prepare Buchanan Body without Organs concept readback after reviewed concept mention, without interpretation.
```
""",
    )

    append_once(
        Path("docs/BUCHANAN_CITATION_AND_RIGHTS.md"),
        "## BDP-001P Concept Mention Rights Boundary",
        """
## BDP-001P Concept Mention Rights Boundary

BDP-001P links the existing short citation-backed Buchanan passage to `Body without Organs` through one reviewed concept mention.

Rights and display treatment:

```text
rights_status = restricted
display_rule = reference_only
display_rule_detail = concept_mention_over_restricted_short_excerpt
long_quotation_stored = false
article_reproduction_authorized = false
concept_mention_backed_by_citation = true
```

BDP-001P authorizes only the controlled concept mention link over the existing citation-backed passage.

It does not authorize article reproduction, long quotation display, concept relation insertion, interpretation, synthesis, or a Buchanan-specific claim.
""",
    )

    append_once(
        Path("docs/BUCHANAN_THREAD_HANDOVER.md"),
        "## BDP-001P Handover Update",
        """
## BDP-001P Handover Update

The inserted Buchanan passage has been linked to `Body without Organs` through one reviewed concept mention.

Completed:

1. Inserted one `concept_mentions` row linking the citation-backed Buchanan passage to `Body without Organs`.
2. Preserved the canonical source count at two.
3. Preserved the passage count at two.
4. Preserved the citation count at two.
5. Confirmed no concept relation was inserted.
6. Confirmed no interpretation or generated Buchanan claim was inserted.
7. Added `sql/016_link_bdp_001p_buchanan_passage_to_bwo_concept_mention_only.sql`.
8. Added `scripts/read_bdp_001p_buchanan_concept_mention.py`.
9. Added `scripts/verify_bdp_001p_buchanan_concept_mention_only.py`.
10. Added `scripts/update_bdp_001p_docs_and_state.py`.

Current invariant after successful verification:

```text
sources_count = 2
source_candidates_count = 3
passage_candidates_count = 1
passages_count = 2
citations_count = 2
concept_mentions_count = 2
concept_relations_count = 0
interpretations_count = 0
BDP-001P migration_count = 1
buchanan_article_passage_count = 1
buchanan_article_citation_count = 1
buchanan_article_concept_mention_count = 1
```

Boundary:

```text
No canonical source inserted.
No source candidate inserted.
No passage candidate inserted.
No passage inserted.
No citation inserted.
No concept relation inserted.
No interpretation inserted.
No generated Buchanan claim created.
No frontend work.
```

Next step:

```text
BDP-001Q — Prepare Buchanan Body without Organs concept readback after reviewed concept mention, without interpretation.
```
""",
    )


if __name__ == "__main__":
    main()
