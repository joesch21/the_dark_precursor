#!/usr/bin/env python3
"""Verify BDP-003F.16 F14 progression guard repair v3."""

from __future__ import annotations

import py_compile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
F14 = ROOT / "scripts" / "verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py"
F16_NEXT_STEP = "BDP-003F.17 — Define Concept Lens limited control expansion contract after F16 readiness decision."

FORBIDDEN = [
    ROOT / "frontend" / "dark_precursor.py",
    ROOT / "scripts" / "concept_lens_archive_evidence_posture_service.py",
    ROOT / "scripts" / "concept_lens_existing_archive_evidence_readback_bridge.py",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> None:
    if not F14.exists():
        fail(f"Missing F14 verifier: {rel(F14)}")

    py_compile.compile(str(F14), doraise=True)
    text = F14.read_text(encoding="utf-8")

    required_markers = [
        'F16_NEXT_STEP = "BDP-003F.17 — Define Concept Lens limited control expansion contract after F16 readiness decision."',
        '("BDP-003F.14", "BDP-003F.15", "BDP-003F.16")',
        'state.get("next_recommended_step") in {NEXT_STEP, F16_NEXT_STEP}',
        'state.get("next_step") in {NEXT_STEP, F16_NEXT_STEP}',
        'str(state.get("next_step", "")).startswith(("BDP-003F.16", "BDP-003F.17"))',
        'str(state.get("next_recommended_step", "")).startswith(("BDP-003F.16", "BDP-003F.17"))',
    ]
    for marker in required_markers:
        if marker not in text:
            fail(f"F14 verifier missing required marker: {marker}")

    if F16_NEXT_STEP not in text:
        fail("F14 verifier does not contain the F16/F17 next safe step string")

    for path in FORBIDDEN:
        if not path.exists():
            fail(f"Required boundary file missing: {rel(path)}")

    print("[OK] BDP-003F.16 F14 progression guard repair v3 verified")


if __name__ == "__main__":
    main()
