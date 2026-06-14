#!/usr/bin/env python3
"""
Update Buchanan docs and state for BDP-001Q.

This script records a read-only evidence readback phase. It does not mutate the
database and does not create any SQL migration.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


PHASE = "BDP-001Q"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
NEXT_STEP = "BDP-001R — Prepare first source-bound Buchanan Body without Organs description candidate, without interpretation."


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
        "bdp_001q_migration_count": 0,
        "buchanan_article_passage_count": 1,
        "buchanan_article_citation_count": 1,
        "buchanan_article_concept_mention_count": 1,
    }

    state["bdp_001q_buchanan_bwo_evidence_readback"] = {
        "phase": PHASE,
        "title": "Prepare Buchanan Body without Organs evidence readback only",
        "status": "complete",
        "completed_at": NOW,
        "controlled_slice": "read_only_evidence_readback_only",
        "database_mutation": False,
        "sql_migration": False,
        "inserted_rows": {
            "sources": 0,
            "source_candidates": 0,
            "passage_candidates": 0,
            "passages": 0,
            "citations": 0,
            "concept_mentions": 0,
            "concept_relations": 0,
            "interpretations": 0,
            "schema_migrations": 0,
        },
        "readback_target": {
            "concept": "Body without Organs",
            "source_author": "Ian Buchanan",
            "source_title": "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?",
            "evidence_chain": "concepts -> concept_mentions -> passages -> citations -> sources",
            "passage_text_display": "omitted_by_rights_policy",
            "rights_status": "restricted",
        },
        "verified_invariant": invariant,
        "authority_boundary": {
            "source_bound_description_allowed": True,
            "buchanan_interpretation": False,
            "buchanan_claim": False,
            "generated_synthesis": False,
            "concept_relation": False,
        },
        "boundary": {
            "new_source": False,
            "new_source_candidate": False,
            "new_passage_candidate": False,
            "new_passage": False,
            "new_citation": False,
            "new_concept_mention": False,
            "concept_relation": False,
            "interpretation": False,
            "generated_buchanan_claim": False,
            "frontend_work": False,
        },
        "next_step": NEXT_STEP,
    }

    state["current_verified_invariant"] = invariant
    state["next_step"] = NEXT_STEP

    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    print(f"[OK] updated {path}")


def main() -> None:
    update_state(Path("ai_boot/BUCHANAN_SYSTEM_STATE.json"))

    append_once(
        Path("docs/BUCHANAN_SCHEMA_CONTROL.md"),
        "## BDP-001Q Evidence Readback Boundary",
        """
## BDP-001Q Evidence Readback Boundary

BDP-001Q prepares a read-only evidence readback for the `Body without Organs` concept after the Buchanan passage has been linked through a reviewed concept mention.

Schema status:

```text
sql_migration = false
database_mutation = false
new_tables = false
new_columns = false
```

Readback chain:

```text
concepts
→ concept_mentions
→ passages
→ citations
→ sources
```

Validation addition:

BDP-001Q is valid only if verification proves:

1. `sources_count = 2`.
2. `source_candidates_count = 3`.
3. `passage_candidates_count = 1`.
4. `passages_count = 2`.
5. `citations_count = 2`.
6. `concept_mentions_count = 2`.
7. exactly one reviewed direct Buchanan `Body without Organs` concept mention is readable through the evidence chain.
8. `concept_relations_count = 0`.
9. `interpretations_count = 0`.
10. `BDP-001Q migration_count = 0`.
11. restricted passage text is not displayed.
""",
    )

    append_once(
        Path("docs/BUCHANAN_INGESTION_WORKFLOW.md"),
        "## BDP-001Q Evidence Readback Step",
        """
## BDP-001Q Evidence Readback Step

BDP-001Q adds no new ingestion stage and performs no database write.

It confirms the controlled sequence has reached a readable evidence spine:

```text
canonical source metadata
→ reviewed passage candidate
→ canonical passage
→ citation
→ reviewed concept mention
→ evidence readback
→ relation or interpretation only after later governed review
```

Boundary:

```text
The platform may now display a rights-aware evidence card.
The evidence card may describe the chain of records.
The evidence card must not attribute a position, argument, conceptual meaning, or theoretical consequence to Buchanan.
```
""",
    )

    append_once(
        Path("docs/BUCHANAN_CONCEPT_ONTOLOGY.md"),
        "## BDP-001Q Body without Organs Evidence Readback Boundary",
        """
## BDP-001Q Body without Organs Evidence Readback Boundary

BDP-001Q treats `Body without Organs` as an anchor concept with one Buchanan evidence chain available for readback.

Allowed after BDP-001Q:

```text
The platform can show that a citation-backed Buchanan passage is linked to Body without Organs by a reviewed concept mention.
```

Still blocked after BDP-001Q:

```text
Buchanan's interpretation of the Body without Organs is X.
Buchanan argues that the Body without Organs means X.
Body without Organs has a reviewed Buchanan relation to another concept.
```

BDP-001Q is an evidence card, not an interpretation layer.
""",
    )

    append_once(
        Path("docs/BUCHANAN_SEMANTIC_WORKBENCH.md"),
        "## BDP-001Q Buchanan Evidence Card Readback",
        """
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
""",
    )

    append_once(
        Path("docs/BUCHANAN_SOURCE_INTAKE_REGISTRY.md"),
        "## BDP-001Q Evidence Readback Record",
        """
## BDP-001Q Evidence Readback Record

The Buchanan `Body without Organs` evidence chain is now prepared for read-only display.

Successful BDP-001Q result:

```text
canonical Buchanan source exists = true
canonical Buchanan passage exists = true
Buchanan citation exists = true
Buchanan concept mention exists = true
evidence readback prepared = true
concept relation inserted = false
interpretation inserted = false
buchanan claim inserted = false
```

Boundary:

```text
The readback is not a new source.
The readback is not a new passage.
The readback is not a new citation.
The readback is not a new concept mention.
The readback is not a relation, interpretation, or synthesis.
```

Next step:

```text
BDP-001R — Prepare first source-bound Buchanan Body without Organs description candidate, without interpretation.
```
""",
    )

    append_once(
        Path("docs/BUCHANAN_CITATION_AND_RIGHTS.md"),
        "## BDP-001Q Evidence Readback Rights Boundary",
        """
## BDP-001Q Evidence Readback Rights Boundary

BDP-001Q prepares a read-only evidence card over the existing restricted Buchanan passage, citation, and concept mention.

Rights and display treatment:

```text
rights_status = restricted
display_rule = reference_only
passage_text_display = omitted_by_rights_policy
long_quotation_displayed = false
article_reproduction_authorized = false
```

BDP-001Q may display bibliographic metadata, locator, citation display rule, concept mention status, and authority boundary.

It must not display the restricted passage text or convert the evidence chain into a Buchanan interpretation or generated claim.
""",
    )

    append_once(
        Path("docs/BUCHANAN_THREAD_HANDOVER.md"),
        "## BDP-001Q Handover Update",
        """
## BDP-001Q Handover Update

The Buchanan `Body without Organs` evidence readback has been prepared as a read-only slice.

Completed:

1. Added `scripts/read_bdp_001q_buchanan_bwo_evidence_readback.py`.
2. Added `scripts/verify_bdp_001q_buchanan_bwo_evidence_readback.py`.
3. Added `scripts/update_bdp_001q_docs_and_state.py`.
4. Added `scripts/verify_bdp_001q_docs_and_state.py`.
5. Prepared a rights-aware evidence card over `concepts → concept_mentions → passages → citations → sources`.
6. Confirmed no SQL migration was added.
7. Confirmed no database mutation was performed.
8. Confirmed no source, passage, citation, concept mention, concept relation, interpretation, generated Buchanan claim, or frontend work was created.
9. Confirmed restricted passage text is not displayed.

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
BDP-001Q migration_count = 0
buchanan_article_passage_count = 1
buchanan_article_citation_count = 1
buchanan_article_concept_mention_count = 1
```

Boundary:

```text
No SQL migration.
No database mutation.
No canonical source inserted.
No source candidate inserted.
No passage candidate inserted.
No passage inserted.
No citation inserted.
No concept mention inserted.
No concept relation inserted.
No interpretation inserted.
No generated Buchanan claim created.
No frontend work.
Restricted passage text not displayed.
```

Next step:

```text
BDP-001R — Prepare first source-bound Buchanan Body without Organs description candidate, without interpretation.
```
""",
    )


if __name__ == "__main__":
    main()
