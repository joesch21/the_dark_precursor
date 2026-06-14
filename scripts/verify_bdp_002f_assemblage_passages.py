#!/usr/bin/env python3
"""
BDP-002F Verifier — Assemblage Passage Review
"""

import os
import sys

REQUIRED_FILES = [
    "docs/BDP_002F_ASSEMBLAGE_PASSAGE_REVIEW_PLAN.md",
    "docs/BDP_002F_KEY_PASSAGES_REVIEWED.md"
]

def check_files_exist():
    missing = []
    for f in REQUIRED_FILES:
        if not os.path.exists(f):
            missing.append(f)
    if missing:
        print("❌ Missing required files:")
        for m in missing:
            print(f"   - {m}")
        return False
    print("✅ All required files present")
    return True

def check_content():
    # Basic content check for the review plan
    with open("docs/BDP_002F_ASSEMBLAGE_PASSAGE_REVIEW_PLAN.md", "r") as f:
        content = f.read()

    required = [
        "Passage Review",
        "Two Axes",
        "blocked_until_governed_citation_phase",
        "No interpretive claims"
    ]

    for item in required:
        if item not in content:
            print(f"❌ Missing expected content: {item}")
            return False

    print("✅ Doctrine content looks correct")
    return True

def main():
    print("=== BDP-002F Assemblage Passage Review Verifier ===\n")

    checks = [
        check_files_exist(),
        check_content()
    ]

    if all(checks):
        print("\n✅ BDP-002F verification PASSED")
        sys.exit(0)
    else:
        print("\n❌ BDP-002F verification FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()