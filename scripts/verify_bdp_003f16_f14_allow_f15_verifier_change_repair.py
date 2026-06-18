#!/usr/bin/env python3
"""Verify the F14 verifier allows the F16 repair to the F15 verifier."""

from __future__ import annotations

import subprocess
from pathlib import Path

TARGET = Path("scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py")
ENTRY = '"scripts/verify_bdp_003f15_concept_lens_running_frontend_review.py"'


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    require(TARGET.exists(), f"missing target: {TARGET}")
    text = TARGET.read_text(encoding="utf-8")
    require(ENTRY in text, "F14 verifier still does not allow repaired F15 verifier change")

    proc = subprocess.run(
        ["python3", str(TARGET)],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        fail("F14 verifier still fails after allow-list repair:\n" + (proc.stdout + proc.stderr).strip())

    print("[OK] BDP-003F.16 F14 allow-F15-verifier-change repair verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
