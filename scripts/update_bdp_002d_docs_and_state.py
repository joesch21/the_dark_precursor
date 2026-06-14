#!/usr/bin/env python3
"""
BDP-002D — Update docs and state for relational/adaptive presentation governance.

Docs/state only. No database access. No schema migration.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
DOCS = ROOT / "docs"
STATE_PATH = ROOT / "ai_boot" / "BUCHANAN_SYSTEM_STATE.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def append_once(path: Path, marker: str, block: str) -> None:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    text = path.read_text()
    if marker in text:
        print(f"[OK] marker already present in {path}")
        return
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text + "\n" + block.strip() + "\n")
    print(f"[OK] appended BDP-002D block to {path}")


def update_semantic_workbench() -> None:
    block = """
## BDP-002D Relational and Adaptive Presentation Governance

The semantic workbench may adapt presentation depth, visual emphasis, metaphor complexity, or exploration paths in response to observed interaction signals, provided the adaptation is visible, inspectable, reversible, and under user control.

Required visible explanatory layer:

```text
How I am adapting this view
```

The explanatory layer must state:

1. what interaction signals were observed.
2. how those signals influenced the current view.
3. how the user can inspect, pause, reset, or manually override the adaptation.
4. that no psychological assessment is being made.
5. that no long-term user profile is being created unless explicit informed consent exists.

Allowed interaction-only signals:

```text
navigation patterns
metaphor selection
time spent on visual versus textual content
question style
depth of follow-up
preference for visual or conceptual framing
```

Boundary:

```text
Adaptive presentation changes display only.
It does not change citation authority.
It does not change interpretation status.
It does not create a Buchanan-specific claim.
It does not create a long-term user profile.
It does not perform psychological assessment.
The default fallback remains the non-adaptive evidence-first readback.
```
"""
    append_once(DOCS / "BUCHANAN_SEMANTIC_WORKBENCH.md", "## BDP-002D Relational and Adaptive Presentation Governance", block)


def update_psycholinguistic_architecture() -> None:
    block = """
## BDP-002D Adaptive Presentation Boundary

Relational and adaptive presentation may support the reader/listener transformation research direction, but it must not become hidden user profiling.

Allowed:

```text
The workbench is showing a more visual path because the current session has used visual navigation heavily.
```

Blocked:

```text
The system has inferred the user's psychological type.
```

Adaptive presentation may use interaction-only session signals to shape display mode, but any such adaptation must be exposed through a visible explanatory layer and user controls for inspect, pause, reset, and manual override.

Controlled status:

```text
sql_migration = false
database_mutation = false
reader_state_tracking = false
long_term_user_profile = false
psychological_assessment = false
hidden_personalisation = false
frontend_implementation = false
```

Future storage of adaptive preferences requires explicit consent, minimisation, inspectability, reset, export, and deletion rules in a later governed phase.
"""
    append_once(DOCS / "BUCHANAN_PSYCHOLINGUISTIC_SEMANTIC_ARCHITECTURE.md", "## BDP-002D Adaptive Presentation Boundary", block)


def update_architecture() -> None:
    block = """
## BDP-002D Relational Adaptive Presentation Layer

The platform may later include an adaptive presentation layer for the semantic workbench.

This layer may adjust explanation depth, visual emphasis, metaphor complexity, or exploration path order in response to visible interaction-only signals. It remains subordinate to the evidence spine and must include an explanatory layer showing how the view is being adapted.

User control requirements:

```text
inspect adaptation
pause adaptation
reset adaptation
manual override
return to canonical evidence-first view
```

Governance boundary:

```text
No long-term user profile without explicit informed consent.
No psychological assessment framing.
No hidden personalisation.
No change to citation, source, concept, relation, interpretation, or Buchanan-claim authority.
```
"""
    append_once(DOCS / "BUCHANAN_ARCHITECTURE.md", "## BDP-002D Relational Adaptive Presentation Layer", block)


def update_thread_handover() -> None:
    block = """
## BDP-002D Handover Update

Relational and adaptive presentation governance has been recorded as a documentation-only slice.

Completed:

1. Added `docs/BDP_002D_RELATIONAL_ADAPTIVE_PRESENTATION.md`.
2. Updated semantic workbench doctrine with adaptive presentation requirements.
3. Updated psycho-linguistic architecture with an explicit anti-profiling boundary.
4. Updated architecture doctrine with user-control requirements for adaptive views.
5. Updated system state for BDP-002D.

Boundary:

```text
No SQL migration.
No database mutation.
No reader-state tracking.
No long-term user profile.
No psychological assessment.
No frontend implementation.
No source, passage, citation, concept mention, concept relation, interpretation, or generated Buchanan claim.
```

Next step:

```text
BDP-001S — Decide the next governed path: secondary-scholarship source-candidate database intake or reviewed relation-evidence preparation.
```
"""
    append_once(DOCS / "BUCHANAN_THREAD_HANDOVER.md", "## BDP-002D Handover Update", block)


def update_state() -> None:
    if not STATE_PATH.exists():
        raise SystemExit(f"missing state file: {STATE_PATH}")

    state = json.loads(STATE_PATH.read_text())
    state["bdp_002d_relational_adaptive_presentation_governance"] = {
        "phase": "BDP-002D",
        "title": "Relational and adaptive presentation governance",
        "status": "complete",
        "type": "documentation_only_governance_slice",
        "updated_at": now_iso(),
        "sql_migration": False,
        "database_mutation": False,
        "frontend_implementation": False,
        "reader_state_tracking": False,
        "long_term_user_profile": False,
        "psychological_assessment": False,
        "hidden_personalisation": False,
        "allowed_interaction_signals": [
            "navigation_patterns",
            "metaphor_selection",
            "time_spent_on_visual_vs_textual_content",
            "question_style",
            "depth_of_follow_up",
            "preference_for_visual_or_conceptual_framing",
        ],
        "required_controls": [
            "inspect_adaptation",
            "pause_adaptation",
            "reset_adaptation",
            "manual_override",
            "return_to_canonical_evidence_first_view",
        ],
        "required_explanatory_layer": "How I am adapting this view",
        "authority_boundary": {
            "adaptive_presentation_changes_display_only": True,
            "does_not_change_citation_authority": True,
            "does_not_create_interpretation": True,
            "does_not_create_buchanan_claim": True,
        },
        "next_recommended_step": "BDP-001S — Decide the next governed path: secondary-scholarship source-candidate database intake or reviewed relation-evidence preparation.",
    }

    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    print(f"[OK] updated {STATE_PATH} for BDP-002D")


def main() -> None:
    update_semantic_workbench()
    update_psycholinguistic_architecture()
    update_architecture()
    update_thread_handover()
    update_state()
    print("[OK] BDP-002D docs/state update complete")


if __name__ == "__main__":
    main()
