#!/usr/bin/env python3
"""
BDP-002D.1 — update docs and state for Interaction Adaptation vs Text Psycho-Linguistics.

Docs-only/state-only update.
No database mutation.
No schema migration.
No reader-state tracking.
No user profile storage.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()

DOC_SOURCE = ROOT / "docs" / "BDP_002D1_INTERACTION_ADAPTATION_VS_TEXT_PSYCHOLINGUISTICS.md"
STATE_PATH = ROOT / "ai_boot" / "BUCHANAN_SYSTEM_STATE.json"

TARGET_DOCS = [
    ROOT / "docs" / "BDP_002D_RELATIONAL_ADAPTIVE_PRESENTATION.md",
    ROOT / "docs" / "BUCHANAN_SEMANTIC_WORKBENCH.md",
    ROOT / "docs" / "BUCHANAN_PSYCHOLINGUISTIC_SEMANTIC_ARCHITECTURE.md",
    ROOT / "docs" / "BUCHANAN_ARCHITECTURE.md",
    ROOT / "docs" / "BUCHANAN_THREAD_HANDOVER.md",
]

MARKER_START = "<!-- BDP-002D.1 INTERACTION ADAPTATION BOUNDARY START -->"
MARKER_END = "<!-- BDP-002D.1 INTERACTION ADAPTATION BOUNDARY END -->"

SECTION = f"""
{MARKER_START}

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

{MARKER_END}
"""


def replace_or_append(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(f"# {path.stem.replace('_', ' ').title()}\n\n{content.lstrip()}")
        print(f"[OK] created {path}")
        return

    text = path.read_text()

    if MARKER_START in text and MARKER_END in text:
        before = text.split(MARKER_START)[0].rstrip()
        after = text.split(MARKER_END, 1)[1].lstrip()
        path.write_text(f"{before}\n\n{content.strip()}\n\n{after}".rstrip() + "\n")
        print(f"[OK] refreshed BDP-002D.1 section in {path}")
    else:
        path.write_text(text.rstrip() + "\n\n" + content.strip() + "\n")
        print(f"[OK] appended BDP-002D.1 section to {path}")


def update_state() -> None:
    if not STATE_PATH.exists():
        raise SystemExit(f"Missing state file: {STATE_PATH}")

    state = json.loads(STATE_PATH.read_text())
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    state["bdp_002d1_interaction_adaptation_vs_text_psycholinguistics"] = {
        "phase": "BDP-002D.1",
        "title": "Interaction Adaptation vs Text Psycho-Linguistics Boundary",
        "status": "complete",
        "type": "governance_doctrine_only",
        "updated_at": now,
        "summary": (
            "Records the distinction between passage-linked text psycho-linguistics "
            "and session-scoped interface adaptation."
        ),
        "database_mutation": False,
        "sql_migration": False,
        "schema_change": False,
        "frontend_implementation": False,
        "reader_state_tracking": False,
        "long_term_user_profile_storage": False,
        "psychological_assessment": False,
        "buchanan_specific_claim": False,
        "generated_interpretation": False,
        "text_psycholinguistics": {
            "focus": "language movement in governed texts",
            "authority_label": "experimental_modelling",
            "linked_to_governed_passage_locator": True,
            "requires_human_review": True,
            "buchanan_claim_authorized": False,
        },
        "interaction_adaptation": {
            "focus": "session-scoped interface response to interaction signals",
            "allowed_signals": [
                "navigation choices",
                "time spent on visuals vs text",
                "question style",
                "metaphor preference",
                "depth of exploration",
            ],
            "explanatory_layer_required": True,
            "inspect_pause_reset_override_required": True,
            "session_scoped_by_default": True,
            "persistence_requires_explicit_informed_consent": True,
            "psychological_state_analysis_allowed": False,
            "cognitive_profile_analysis_allowed": False,
            "objective_psychological_insight_claim_allowed": False,
        },
        "docs": [
            "docs/BDP_002D1_INTERACTION_ADAPTATION_VS_TEXT_PSYCHOLINGUISTICS.md",
            "docs/BDP_002D_RELATIONAL_ADAPTIVE_PRESENTATION.md",
            "docs/BUCHANAN_SEMANTIC_WORKBENCH.md",
            "docs/BUCHANAN_PSYCHOLINGUISTIC_SEMANTIC_ARCHITECTURE.md",
            "docs/BUCHANAN_ARCHITECTURE.md",
            "docs/BUCHANAN_THREAD_HANDOVER.md",
        ],
        "next_recommended_action": (
            "BDP-002D.2 — Define inspect/pause/reset/override UX contract before any adaptive frontend implementation."
        ),
    }

    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    print("[OK] updated ai_boot/BUCHANAN_SYSTEM_STATE.json for BDP-002D.1")


def main() -> None:
    if not DOC_SOURCE.exists():
        raise SystemExit(f"Missing doctrine source file: {DOC_SOURCE}")

    for doc in TARGET_DOCS:
        replace_or_append(doc, SECTION)

    update_state()

    print("[OK] BDP-002D.1 docs/state update complete")
    print("[OK] no database mutation performed")


if __name__ == "__main__":
    main()
