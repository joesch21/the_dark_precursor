#!/usr/bin/env python3
"""Repair BDP-003F.15 verifier global next-step guard for F16/F17 progression.

This is a targeted verifier-progression repair. It does not alter frontend,
service, bridge, database, or Concept Lens behavior.
"""

from __future__ import annotations

from pathlib import Path

TARGET = Path("scripts/verify_bdp_003f15_concept_lens_running_frontend_review.py")

HELPER = '''\n\ndef global_next_step_is_allowed(value: object, f15_next_safe_step: object) -> bool:\n    """Allow F15 verifier to pass after later approved F16/F17 progression.\n\n    During F15 itself, global next-step fields should match the F15 record.\n    After F16, those same global fields may validly advance to the F16\n    readiness decision or the F17 limited-control contract next step.\n    """\n    text = str(value or "")\n    f15_text = str(f15_next_safe_step or "")\n    return (\n        text == f15_text\n        or text.startswith("BDP-003F.16")\n        or text.startswith("BDP-003F.17")\n        or "Decide Concept Lens control and concept coverage expansion readiness" in text\n        or "Define Concept Lens limited control expansion contract after F16 readiness decision" in text\n    )\n'''

OLD = '''    for key in ["next_recommended_step", "current_next_step", "next_step", "recommended_next_step", "next_safe_step"]:\n        require(state.get(key) == phase_record.get("next_safe_step"), f"Global {key} must match F15 next safe step")\n'''

NEW = '''    for key in ["next_recommended_step", "current_next_step", "next_step", "recommended_next_step", "next_safe_step"]:\n        require(\n            global_next_step_is_allowed(state.get(key), phase_record.get("next_safe_step")),\n            f"Global {key} must match F15 next safe step or approved F16/F17 progression",\n        )\n'''


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def main() -> int:
    if not TARGET.exists():
        fail(f"missing target verifier: {TARGET}")

    text = TARGET.read_text(encoding="utf-8")

    if NEW in text and "def global_next_step_is_allowed" in text:
        print("[OK] F15 global next-step loop already repaired")
        return 0

    if OLD not in text:
        fail("could not locate exact F15 global next-step loop at lines 193-194")

    if "def global_next_step_is_allowed" not in text:
        marker = "\ndef verify_state() -> None:\n"
        if marker not in text:
            fail("could not locate verify_state marker for helper insertion")
        text = text.replace(marker, HELPER + marker, 1)

    text = text.replace(OLD, NEW, 1)
    TARGET.write_text(text, encoding="utf-8")
    print(f"[OK] repaired {TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
