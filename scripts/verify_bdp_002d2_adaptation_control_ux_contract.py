#!/usr/bin/env python3
"""
BDP-002D.2 Verifier
Checks that the Adaptation Control UX Contract doctrine is correctly in place.
"""

import os
import sys
import json

REQUIRED_FILES = [
    "docs/BDP_002D2_ADAPTATION_CONTROL_UX_CONTRACT.md",
    "scripts/update_bdp_002d2_adaptation_control_ux_contract.py",
    "scripts/verify_bdp_002d2_adaptation_control_ux_contract.py"
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

def check_doctrine_content():
    path = "docs/BDP_002D2_ADAPTATION_CONTROL_UX_CONTRACT.md"
    with open(path, "r") as f:
        content = f.read()

    required_sections = [
        "Inspect",
        "Pause",
        "Reset",
        "Override",
        "Explanatory Layer",
        "session-scoped by default",
        "explicit informed consent"
    ]

    for section in required_sections:
        if section not in content:
            print(f"❌ Missing required section/content: {section}")
            return False

    print("✅ Doctrine content contains required UX contract elements")
    return True

def check_state():
    with open("ai_boot/BUCHANAN_SYSTEM_STATE.json", "r") as f:
        state = json.load(f)

    if "BDP-002D.2" not in state.get("phases", {}):
        print("❌ BDP-002D.2 not recorded in system state")
        return False

    phase = state["phases"]["BDP-002D.2"]
    if phase.get("type") != "doctrine_ux_contract":
        print("❌ Phase type incorrect")
        return False

    print("✅ System state correctly records BDP-002D.2")
    return True

def main():
    print("=== BDP-002D.2 Adaptation Control UX Contract Verifier ===\n")

    checks = [
        check_files_exist(),
        check_doctrine_content(),
        check_state()
    ]

    if all(checks):
        print("\n✅ BDP-002D.2 verification PASSED")
        sys.exit(0)
    else:
        print("\n❌ BDP-002D.2 verification FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()