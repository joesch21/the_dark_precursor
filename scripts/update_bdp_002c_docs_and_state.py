#!/usr/bin/env python3
"""Update Buchanan docs/state for BDP-002C without touching the database."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

PHASE = "BDP-002C"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

EXPECTED_INVARIANT = {
    "sources_count": 2,
    "source_candidates_count": 3,
    "passage_candidates_count": 1,
    "passages_count": 2,
    "citations_count": 2,
    "concept_mentions_count": 2,
    "concept_relations_count": 0,
    "interpretations_count": 0,
    "bdp_001p_migration_count": 1,
    "bdp_002c_migration_count": 0,
    "buchanan_article_passage_count": 1,
    "buchanan_article_citation_count": 1,
    "buchanan_article_concept_mention_count": 1,
}

DOC_APPENDICES = {
    Path("docs/BUCHANAN_SEMANTIC_WORKBENCH.md"): """
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
""",
    Path("docs/BUCHANAN_SCHEMA_CONTROL.md"): """
## BDP-002C Richer Semantic Readback Surface Boundary

BDP-002C is a read-only semantic readback phase.

Schema status:

```text
sql_migration = false
database_mutation = false
new_tables = false
new_columns = false
```

Implementation status:

```text
psql_subprocess_only = true
psycopg_dependency = false
psycopg2_dependency = false
frontend_renderer = false
```

Validation addition:

BDP-002C is valid only if verification proves:

1. the existing invariant is preserved before and after readback.
2. `BDP-002C migration_count = 0`.
3. no SQL string passed to psql contains mutation keywords.
4. every generated card field has a controlled authority label.
5. restricted passage text is not displayed.
6. Buchanan-specific explanation, relation, interpretation, and claim remain blocked.
""",
    Path("docs/BUCHANAN_CONCEPT_ONTOLOGY.md"): """
## BDP-002C Richer Semantic Readback Boundary

BDP-002C treats `Body without Organs` as a Tier 1 Anchor Concept with a readable Buchanan evidence spine.

Allowed after BDP-002C:

```text
The platform may show a 15-section evidence-posture card over the existing citation-backed Buchanan passage and reviewed concept mention.
```

Still blocked after BDP-002C:

```text
Buchanan-specific interpretation.
Buchanan-specific author-position claim.
Concept relation creation.
Theoretical consequence attribution.
Objective psycho-linguistic scoring.
```

Psycho-linguistic placeholders may appear only as `experimental_modelling` records linked to the governed passage locator and flagged as requiring human review.
""",
    Path("docs/BUCHANAN_INGESTION_WORKFLOW.md"): """
## BDP-002C Readback Step

BDP-002C adds no new ingestion stage and performs no database write.

It confirms the controlled sequence has reached a richer readable evidence surface:

```text
canonical source metadata
→ reviewed passage candidate
→ canonical passage
→ citation
→ reviewed concept mention
→ richer semantic readback card
→ source-bound description candidate later
→ relation or interpretation only after later governed review
```

Boundary:

```text
The readback card may describe the chain of governed records.
The readback card must not reproduce restricted passage text.
The readback card must not generate a Buchanan interpretation or author-position claim.
```
""",
    Path("docs/BUCHANAN_CITATION_AND_RIGHTS.md"): """
## BDP-002C Richer Readback Rights Boundary

BDP-002C prepares a richer read-only card over the existing restricted Buchanan passage, citation, and concept mention.

Rights and display treatment:

```text
rights_status = restricted
display_rule = reference_only
passage_text_display = omitted_by_rights_policy
long_quotation_displayed = false
article_reproduction_authorized = false
```

The card may display bibliographic metadata, locator data, citation display rule, concept mention status, authority label, and evidence posture.

It must not display restricted passage text or convert the evidence chain into a Buchanan interpretation, theoretical consequence, or generated author-position claim.
""",
    Path("docs/BUCHANAN_THREAD_HANDOVER.md"): """
## BDP-002C Handover Update

BDP-002C prepares a richer semantic readback surface for the Buchanan `Body without Organs` evidence spine.

Completed:

1. Added `docs/BDP_002C_RICHER_SEMANTIC_READBACK_SURFACE.md`.
2. Added `scripts/read_bdp_002c_richer_bwo_semantic_card.py`.
3. Added `scripts/verify_bdp_002c_richer_semantic_readback.py`.
4. Added `scripts/update_bdp_002c_docs_and_state.py`.
5. Defined the expanded 15-section evidence card contract.
6. Preserved the existing governed evidence spine.
7. Confirmed no SQL migration is added.
8. Confirmed no database mutation is performed by the readback.
9. Confirmed restricted passage text remains omitted by rights policy.
10. Confirmed Buchanan-specific explanation, relation, interpretation, and claim remain blocked.
11. Confirmed psycho-linguistic observations remain experimental modelling placeholders only.

Current invariant expected by verifier:

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
BDP-002C migration_count = 0
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
}


def append_once(path: Path, marker: str, content: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Required document missing: {path}")
    text = path.read_text(encoding="utf-8")
    if marker in text:
        print(f"[OK] {path} already contains {marker}")
        return
    path.write_text(text.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
    print(f"[OK] appended {marker} to {path}")


def update_state() -> None:
    path = Path("ai_boot/BUCHANAN_SYSTEM_STATE.json")
    if not path.exists():
        raise FileNotFoundError(f"Required state file missing: {path}")
    state = json.loads(path.read_text(encoding="utf-8"))
    state["bdp_002c_richer_semantic_readback_surface"] = {
        "phase": PHASE,
        "title": "Richer Semantic Readback Surface",
        "status": "prepared",
        "updated_at": NOW,
        "controlled_slice": "read_only_semantic_readback_surface",
        "database_mutation": False,
        "sql_migration": False,
        "new_tables": False,
        "new_columns": False,
        "psql_subprocess_only": True,
        "psycopg_dependency": False,
        "psycopg2_dependency": False,
        "frontend_renderer": False,
        "anchor_concept": "Body without Organs",
        "evidence_depth_tier": "Tier 1 — Anchor Concept",
        "card_section_count": 15,
        "rights_boundary": {
            "passage_text_display": "omitted_by_rights_policy",
            "long_quotation_displayed": False,
            "article_reproduction_authorized": False,
        },
        "buchanan_explanation_status": "buchanan_pending",
        "buchanan_interpretation_status": "blocked_until_governed_interpretation_phase",
        "buchanan_claim_status": "blocked_until_interpretive_authority_exists",
        "psycho_linguistic_status": {
            "authority_label": "experimental_modelling",
            "requires_human_review": True,
            "current_ceiling": "Level 2 Embedding Deviation",
            "objective_score_claimed": False,
        },
        "expected_invariant": EXPECTED_INVARIANT,
        "next_recommended_operator_action": "BDP-001R — Prepare first source-bound Buchanan Body without Organs description candidate, without interpretation.",
    }
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"[OK] updated {path}")


def main() -> int:
    for path, content in DOC_APPENDICES.items():
        append_once(path, "BDP-002C", content)
    update_state()
    print("BDP-002C docs/state update complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
