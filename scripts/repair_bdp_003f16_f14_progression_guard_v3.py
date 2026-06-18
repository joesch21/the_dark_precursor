#!/usr/bin/env python3
"""Repair the BDP-003F.14 verifier progression guard for BDP-003F.16.

This repair is verifier-only. It updates the completed F14 verifier so it
continues to prove the F14 boundary after the global state has legitimately
advanced through the F16 decision and now recommends the F17 contract phase.

It does not touch the frontend, Concept Lens service, or archive bridge.
"""

from __future__ import annotations

import py_compile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "scripts" / "verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py"
F16_NEXT_STEP_LINE = 'F16_NEXT_STEP = "BDP-003F.17 — Define Concept Lens limited control expansion contract after F16 readiness decision."'

FORBIDDEN_TO_TOUCH = {
    "frontend/dark_precursor.py",
    "scripts/concept_lens_archive_evidence_posture_service.py",
    "scripts/concept_lens_existing_archive_evidence_readback_bridge.py",
}


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def replace_once(text: str, old: str, new: str, label: str) -> tuple[str, bool]:
    if new in text:
        return text, False
    if old not in text:
        fail(f"Could not locate expected F14 verifier segment for {label}")
    return text.replace(old, new, 1), True


def main() -> None:
    if rel(TARGET) in FORBIDDEN_TO_TOUCH:
        fail(f"Refusing to touch forbidden file: {rel(TARGET)}")
    if not TARGET.exists():
        fail(f"Missing F14 verifier: {rel(TARGET)}")

    before = TARGET.read_text(encoding="utf-8")
    text = before
    changed = False

    if F16_NEXT_STEP_LINE not in text:
        marker = 'NEXT_STEP = '
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if line.startswith(marker):
                lines.insert(index + 1, F16_NEXT_STEP_LINE)
                text = "\n".join(lines) + ("\n" if before.endswith("\n") else "")
                changed = True
                break
        else:
            fail("Could not locate NEXT_STEP constant for F16 next-step insertion")

    text, did = replace_once(
        text,
        'str(state.get("last_updated_phase", "")).startswith(("BDP-003F.14", "BDP-003F.15"))',
        'str(state.get("last_updated_phase", "")).startswith(("BDP-003F.14", "BDP-003F.15", "BDP-003F.16"))',
        "last_updated_phase F16 progression",
    )
    changed = changed or did

    text, did = replace_once(
        text,
        'state.get("next_recommended_step") == NEXT_STEP',
        'state.get("next_recommended_step") in {NEXT_STEP, F16_NEXT_STEP}',
        "next_recommended_step F17 allowance",
    )
    changed = changed or did

    text, did = replace_once(
        text,
        'state.get("next_step") == NEXT_STEP',
        'state.get("next_step") in {NEXT_STEP, F16_NEXT_STEP}',
        "next_step F17 allowance",
    )
    changed = changed or did

    text, did = replace_once(
        text,
        'str(state.get("next_step", "")).startswith("BDP-003F.16")',
        'str(state.get("next_step", "")).startswith(("BDP-003F.16", "BDP-003F.17"))',
        "next_step descendant prefix",
    )
    changed = changed or did

    text, did = replace_once(
        text,
        'str(state.get("next_recommended_step", "")).startswith("BDP-003F.16")',
        'str(state.get("next_recommended_step", "")).startswith(("BDP-003F.16", "BDP-003F.17"))',
        "next_recommended_step descendant prefix",
    )
    changed = changed or did

    if not changed and text == before:
        print(f"[OK] already compatible {rel(TARGET)}")
    else:
        TARGET.write_text(text, encoding="utf-8")
        print(f"[OK] repaired {rel(TARGET)}")

    py_compile.compile(str(TARGET), doraise=True)
    print("[OK] BDP-003F.16 F14 progression guard repair v3 complete")


if __name__ == "__main__":
    main()
