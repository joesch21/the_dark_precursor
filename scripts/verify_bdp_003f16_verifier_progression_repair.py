#!/usr/bin/env python3
"""Verify BDP-003F.16 verifier progression repair."""

from __future__ import annotations

import py_compile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
F16_PHASE = '"BDP-003F.16"'
F16_NEXT_STEP = "BDP-003F.17 — Define Concept Lens limited control expansion contract after F16 readiness decision."

TARGETS = [
    ROOT / "scripts" / "verify_bdp_003f10_concept_lens_read_only_bridge_contract.py",
    ROOT / "scripts" / "verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py",
    ROOT / "scripts" / "verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py",
    ROOT / "scripts" / "verify_bdp_003f13_concept_lens_ui_integration_contract.py",
    ROOT / "scripts" / "verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py",
    ROOT / "scripts" / "verify_bdp_003f15_concept_lens_running_frontend_review.py",
]

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
    for path in TARGETS:
        if not path.exists():
            fail(f"Missing verifier: {rel(path)}")
        py_compile.compile(str(path), doraise=True)
        text = path.read_text(encoding="utf-8")
        if F16_PHASE not in text:
            fail(f"{rel(path)} does not allow BDP-003F.16 progression")

    f14 = (ROOT / "scripts" / "verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py").read_text(encoding="utf-8")
    if F16_NEXT_STEP not in f14:
        fail("F14 verifier does not allow F16 next safe step")

    for path in FORBIDDEN:
        if not path.exists():
            fail(f"Required forbidden-boundary file missing: {rel(path)}")

    print("[OK] BDP-003F.16 verifier progression repair verified")


if __name__ == "__main__":
    main()
