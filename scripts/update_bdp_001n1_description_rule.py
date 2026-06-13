#!/usr/bin/env python3
from pathlib import Path
import json
from datetime import datetime, timezone
import textwrap

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "ai_boot" / "BUCHANAN_SYSTEM_STATE.json"

phase_key = "bdp_001n1_description_rule"
phase_record = {
    "phase": "BDP-001N.1",
    "status": "complete",
    "title": "Record description versus claim authority rule before BDP-001O",
    "controlled_slice": "doctrine_only_description_rule",
    "database_mutation": False,
    "sql_migration": False,
    "rule": {
        "description_not_claim": True,
        "description_definition": "The platform may describe reviewed records, locators, excerpts, and evidence posture without creating interpretive claims.",
        "claim_threshold": "A description becomes a claim when it attributes a position, argument, intention, conceptual meaning, or theoretical consequence to Buchanan, Deleuze, Guattari, or another author.",
        "authority_requirement": "Descriptions must carry authority labels. Claims require stronger governed evidence."
    },
    "authority_ladder": [
        "metadata",
        "locator",
        "short_excerpt",
        "source_bound_description",
        "citation_backed_passage",
        "concept_mention",
        "interpretation",
        "synthesis"
    ],
    "allowed_now": [
        "Describe the reviewed Buchanan passage candidate record.",
        "Describe the locator and short excerpt as reviewed candidate evidence posture.",
        "Describe that the candidate is ready for later governed passage and citation insertion."
    ],
    "still_blocked": [
        "Buchanan argues X.",
        "Buchanan's view is X.",
        "The meaning of the Body without Organs in Buchanan is X.",
        "Any author-position claim without governed evidence."
    ],
    "boundaries": {
        "canonical_passage_insertion": False,
        "citation_insertion": False,
        "concept_mention_insertion": False,
        "concept_relation_insertion": False,
        "interpretation_insertion": False,
        "generated_buchanan_claim": False,
        "frontend_work": False,
        "psycho_linguistic_modelling_implementation": False
    },
    "next_step": "BDP-001O — Insert reviewed Buchanan passage and citation only, if operator approves.",
    "updated_at": datetime.now(timezone.utc).isoformat()
}

state = json.loads(STATE.read_text(encoding="utf-8"))
state[phase_key] = phase_record
state["current_phase"] = "BDP-001N.1"
state["next_recommended_step"] = phase_record["next_step"]
STATE.write_text(json.dumps(state, indent=4, sort_keys=True) + "\n", encoding="utf-8")

blocks = {
    "docs/BUCHANAN_THREAD_HANDOVER.md": """
## BDP-001N.1 Handover Update

The description-versus-claim authority rule has been recorded before BDP-001O.

Completed:

1. Added the BDP Description Rule.
2. Distinguished reviewed-record descriptions from interpretive claims.
3. Added the authority ladder from metadata to synthesis.
4. Confirmed descriptions must still carry authority labels.
5. Confirmed claims require stronger governed evidence.
6. Preserved the BDP-001N database invariant.
7. Added `scripts/update_bdp_001n1_description_rule.py`.
8. Added `scripts/verify_bdp_001n1_description_rule.py`.

BDP Description Rule:

```text
The platform may generate descriptions of reviewed records, locators, excerpts, and evidence posture without creating interpretive claims.

A description becomes a claim when it attributes a position, argument, intention, conceptual meaning, or theoretical consequence to Buchanan, Deleuze, Guattari, or another author.

Descriptions must carry authority labels.
Claims require stronger governed evidence.
```

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

Boundary:

```text
No SQL migration.
No database mutation.
No canonical passage insertion.
No citation insertion.
No concept mention insertion.
No concept relation insertion.
No interpretation insertion.
No generated Buchanan claim.
No frontend work.
```

Next step:

```text
BDP-001O — Insert reviewed Buchanan passage and citation only, if operator approves.
```
""",
    "docs/BUCHANAN_SCHEMA_CONTROL.md": """
## BDP-001N.1 Description Versus Claim Authority Rule

BDP-001N.1 records a doctrine-only rule. It does not introduce a schema change.

The platform now distinguishes:

```text
description ≠ claim
```

A description may report the state of reviewed records, locators, excerpts, and evidence posture.

A description becomes a claim when it attributes any of the following to Buchanan, Deleuze, Guattari, or another author:

```text
position
argument
intention
conceptual meaning
theoretical consequence
```

Descriptions must carry authority labels.

Claims require stronger governed evidence.

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

Controlled status:

```text
sql_migration = false
database_mutation = false
new_tables = false
new_columns = false
authority_rule_update = true
```
""",
    "docs/BUCHANAN_CITATION_AND_RIGHTS.md": """
## BDP-001N.1 Description Rule Rights Boundary

A rights-aware description may describe reviewed metadata, locator, excerpt status, and evidence posture without reproducing source material.

Allowed description:

```text
The reviewed candidate excerpt is short, restricted, reference-only, and located at printed article page 76 / PDF page 4.
```

Blocked claim without stronger governed evidence:

```text
Buchanan argues X.
```

Rule:

```text
Descriptions must carry authority labels.
Claims require stronger governed evidence.
Short excerpt handling does not authorize article reproduction.
```
""",
    "docs/BUCHANAN_INGESTION_WORKFLOW.md": """
## BDP-001N.1 Description Layer

BDP-001N.1 adds a missing layer between short excerpt review and canonical interpretation.

Updated ladder:

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

A source-bound description may describe the reviewed record and evidence posture.

It must not attribute a position, argument, intention, conceptual meaning, or theoretical consequence to an author unless the stronger governed evidence layer exists.

This prevents the system from jumping directly from excerpt review to interpretation.
""",
    "docs/BUCHANAN_SEMANTIC_WORKBENCH.md": """
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
""",
    "docs/BUCHANAN_CONCEPT_ONTOLOGY.md": """
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
"""
}

for rel, block in blocks.items():
    path = ROOT / rel
    if not path.exists():
        print(f"[SKIP] missing optional doc: {rel}")
        continue
    text = path.read_text(encoding="utf-8")
    marker = textwrap.dedent(block).strip().splitlines()[0]
    if marker in text:
        print(f"[OK] already present: {rel}")
        continue
    path.write_text(text.rstrip() + "\n\n" + textwrap.dedent(block).strip() + "\n", encoding="utf-8")
    print(f"[OK] updated: {rel}")

print("BDP-001N.1 description rule docs/state update complete.")
