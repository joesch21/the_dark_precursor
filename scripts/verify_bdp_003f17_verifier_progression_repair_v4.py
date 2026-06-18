#!/usr/bin/env python3
"""Verify BDP-003F.17 verifier progression repair v4."""

from __future__ import annotations

import py_compile
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py",
    ROOT / "scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py",
    ROOT / "scripts/verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py",
    ROOT / "scripts/verify_bdp_003f13_concept_lens_ui_integration_contract.py",
    ROOT / "scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py",
    ROOT / "scripts/verify_bdp_003f15_concept_lens_running_frontend_review.py",
]


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def main() -> int:
    for path in TARGETS:
        if not path.exists():
            fail(f"missing target: {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        if "BDP-003F.17" not in text:
            fail(f"{path.relative_to(ROOT)} does not allow BDP-003F.17 progression")
        if "BDP-003F.18" not in text:
            fail(f"{path.relative_to(ROOT)} does not allow BDP-003F.18 progression")
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            fail(f"{path.relative_to(ROOT)} does not compile: {exc.msg}")

    chain = [
        "scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py",
        "scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py",
        "scripts/verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py",
        "scripts/verify_bdp_003f13_concept_lens_ui_integration_contract.py",
        "scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py",
        "scripts/verify_bdp_003f15_concept_lens_running_frontend_review.py",
    ]
    for rel in chain:
        proc = subprocess.run(["python3", rel], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if proc.returncode != 0:
            fail(f"{rel} still fails after repair:\n{proc.stdout}")
    print("[OK] BDP-003F.17 verifier progression repair v4 verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
