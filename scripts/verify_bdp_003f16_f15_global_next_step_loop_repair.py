#!/usr/bin/env python3
"""Verify BDP-003F.16 F15 global next-step loop repair."""

from __future__ import annotations

import py_compile
import subprocess
from pathlib import Path

TARGET = Path("scripts/verify_bdp_003f15_concept_lens_running_frontend_review.py")


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    require(TARGET.exists(), f"missing target verifier: {TARGET}")
    text = TARGET.read_text(encoding="utf-8")

    require("def global_next_step_is_allowed" in text, "F15 verifier missing global next-step helper")
    require("text.startswith(\"BDP-003F.16\")" in text, "F15 verifier does not allow F16 progression")
    require("text.startswith(\"BDP-003F.17\")" in text, "F15 verifier does not allow F17 progression")
    require("approved F16/F17 progression" in text, "F15 verifier missing repaired failure message")
    require("state.get(key) == phase_record.get(\"next_safe_step\")" not in text, "old strict F15 next-step equality guard still present")

    py_compile.compile(str(TARGET), doraise=True)

    proc = subprocess.run(
        ["python3", str(TARGET)],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        fail("F15 verifier still fails after global next-step loop repair:\n" + proc.stdout + proc.stderr)

    print("[OK] BDP-003F.16 F15 global next-step loop repair verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
