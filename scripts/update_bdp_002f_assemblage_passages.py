#!/usr/bin/env python3
"""
BDP-002F — Update System State for Assemblage Passage Review
"""

import json
from datetime import datetime

STATE_FILE = "ai_boot/BUCHANAN_SYSTEM_STATE.json"

def main():
    with open(STATE_FILE, "r") as f:
        state = json.load(f)

    if "phases" not in state:
        state["phases"] = {}

    state["phases"]["BDP-002F"] = {
        "status": "in_progress",
        "type": "passage_review_preparation",
        "description": "Review and prepare key passages from Ian Buchanan's Assemblage Theory and Method (2021)",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "deliverables": [
            "docs/BDP_002F_ASSEMBLAGE_PASSAGE_REVIEW_PLAN.md",
            "docs/BDP_002F_KEY_PASSAGES_REVIEWED.md"
        ],
        "boundaries": {
            "database_insertion": False,
            "citation_creation": False,
            "concept_mention_creation": False,
            "interpretation": False
        }
    }

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

    print("BDP-002F state updated successfully.")

if __name__ == "__main__":
    main()