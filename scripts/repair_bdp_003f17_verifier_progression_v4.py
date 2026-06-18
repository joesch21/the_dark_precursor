#!/usr/bin/env python3
"""Repair Concept Lens verifier progression guards for BDP-003F.17/F18.

This script performs small, deterministic text repairs against the committed
BDP-003F.10-F15 verifier shapes. It does not touch frontend, service, bridge,
database, or Concept Lens implementation files.
"""

from __future__ import annotations

import py_compile
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

F10 = ROOT / "scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py"
F11 = ROOT / "scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py"
F12 = ROOT / "scripts/verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py"
F13 = ROOT / "scripts/verify_bdp_003f13_concept_lens_ui_integration_contract.py"
F14 = ROOT / "scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py"
F15 = ROOT / "scripts/verify_bdp_003f15_concept_lens_running_frontend_review.py"

PHASES_10_18 = [f"BDP-003F.{i}" for i in range(10, 19)]
PHASES_11_18 = [f"BDP-003F.{i}" for i in range(11, 19)]
PHASES_12_18 = [f"BDP-003F.{i}" for i in range(12, 19)]
PHASES_13_18 = [f"BDP-003F.{i}" for i in range(13, 19)]
PHASES_14_18 = [f"BDP-003F.{i}" for i in range(14, 19)]
PHASES_15_18 = [f"BDP-003F.{i}" for i in range(15, 19)]


def qset(values: list[str]) -> str:
    return "{" + ", ".join(repr(v) for v in values) + "}"


def qtuple(values: list[str]) -> str:
    return "(" + ", ".join(repr(v) for v in values) + ")"


def read(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"[FAIL] missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def write_if_changed(path: Path, old: str, new: str) -> None:
    if new != old:
        path.write_text(new, encoding="utf-8")
        print(f"[OK] repaired {path.relative_to(ROOT)}")
    else:
        print(f"[OK] already compatible {path.relative_to(ROOT)}")


def replace_assignment(text: str, name: str, replacement: str, path: Path) -> str:
    pattern = rf"^{name}\s*=\s*.*$"
    new, count = re.subn(pattern, f"{name} = {replacement}", text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise SystemExit(f"[FAIL] could not replace {name} in {path.relative_to(ROOT)}")
    return new


def repair_f10_f12(path: Path, current: list[str], nxt: list[str]) -> None:
    text = read(path)
    new = text
    new = replace_assignment(new, "ALLOWED_CURRENT_PHASES", qset(current), path)
    new = replace_assignment(new, "ALLOWED_NEXT_PREFIXES", qtuple(nxt), path)
    new = new.replace("F10-F16 progression", "F10-F18 progression")
    new = new.replace("F11-F16 progression", "F11-F18 progression")
    new = new.replace("F12-F16 progression", "F12-F18 progression")
    write_if_changed(path, text, new)


def repair_f13(path: Path) -> None:
    text = read(path)
    new = text
    current_line = (
        "require(data.get(\"current_phase\") in {PHASE, \"BDP-003F.14\", \"BDP-003F.15\", \"BDP-003F.16\"}, "
        "\"Global current_phase should remain in approved F13-F16 progression\")"
    )
    replacement_line = (
        "require(data.get(\"current_phase\") in {PHASE, \"BDP-003F.14\", \"BDP-003F.15\", \"BDP-003F.16\", \"BDP-003F.17\", \"BDP-003F.18\"}, "
        "\"Global current_phase should remain in approved F13-F18 progression\")"
    )
    if current_line in new:
        new = new.replace(current_line, replacement_line, 1)
    else:
        new, count = re.subn(
            r"require\(data\.get\(\"current_phase\"\) in \{PHASE, \"BDP-003F\.14\", \"BDP-003F\.15\", \"BDP-003F\.16\"\},\s*\"Global current_phase should remain in approved F13-F16 progression\"\)",
            replacement_line,
            new,
            count=1,
        )
        if count != 1 and "BDP-003F.18" not in new:
            raise SystemExit(f"[FAIL] could not repair current_phase guard in {path.relative_to(ROOT)}")
    new = new.replace(
        'startswith(("BDP-003F.14", "BDP-003F.15", "BDP-003F.16"))',
        'startswith(("BDP-003F.14", "BDP-003F.15", "BDP-003F.16", "BDP-003F.17", "BDP-003F.18"))',
    )
    new = new.replace(
        "startswith(('BDP-003F.14', 'BDP-003F.15', 'BDP-003F.16'))",
        "startswith(('BDP-003F.14', 'BDP-003F.15', 'BDP-003F.16', 'BDP-003F.17', 'BDP-003F.18'))",
    )
    new = new.replace("F13-F16 progression", "F13-F18 progression")
    write_if_changed(path, text, new)


def repair_f14(path: Path) -> None:
    text = read(path)
    new = text
    for before in [
        'startswith(("BDP-003F.14", "BDP-003F.15", "BDP-003F.16"))',
        "startswith(('BDP-003F.14', 'BDP-003F.15', 'BDP-003F.16'))",
        'startswith(("BDP-003F.14", "BDP-003F.15", "BDP-003F.16", "BDP-003F.17"))',
        "startswith(('BDP-003F.14', 'BDP-003F.15', 'BDP-003F.16', 'BDP-003F.17'))",
    ]:
        if before in new:
            quote = '"' if '"' in before else "'"
            values = ", ".join(f"{quote}{v}{quote}" for v in PHASES_14_18)
            new = new.replace(before, f"startswith(({values}))")
    # Common F14 next-step branches use BDP-003F.16/F17 startswith checks.
    if 'startswith("BDP-003F.17")' in new and 'startswith("BDP-003F.18")' not in new:
        new = new.replace('or str(state.get("next_recommended_step", "")).startswith("BDP-003F.17")',
                          'or str(state.get("next_recommended_step", "")).startswith("BDP-003F.17")\n        or str(state.get("next_recommended_step", "")).startswith("BDP-003F.18")')
        new = new.replace('or str(state.get("next_step", "")).startswith("BDP-003F.17")',
                          'or str(state.get("next_step", "")).startswith("BDP-003F.17")\n        or str(state.get("next_step", "")).startswith("BDP-003F.18")')
    elif 'startswith("BDP-003F.16")' in new and 'startswith("BDP-003F.18")' not in new:
        new = new.replace('or str(state.get("next_recommended_step", "")).startswith("BDP-003F.16")',
                          'or str(state.get("next_recommended_step", "")).startswith("BDP-003F.16")\n        or str(state.get("next_recommended_step", "")).startswith("BDP-003F.17")\n        or str(state.get("next_recommended_step", "")).startswith("BDP-003F.18")')
        new = new.replace('or str(state.get("next_step", "")).startswith("BDP-003F.16")',
                          'or str(state.get("next_step", "")).startswith("BDP-003F.16")\n        or str(state.get("next_step", "")).startswith("BDP-003F.17")\n        or str(state.get("next_step", "")).startswith("BDP-003F.18")')
    new = new.replace("F14-F16 progression", "F14-F18 progression")
    new = new.replace("approved F16/F17 progression", "approved F16/F18 progression")
    write_if_changed(path, text, new)


def repair_f15(path: Path) -> None:
    text = read(path)
    new = text
    # F15 repair from F16 may already allow F16/F17. Add F18 to all state next-step branches.
    if 'startswith("BDP-003F.17")' in new and 'startswith("BDP-003F.18")' not in new:
        for key in ["next_recommended_step", "current_next_step", "next_step", "recommended_next_step", "next_safe_step"]:
            new = new.replace(
                f'or str(state.get("{key}", "")).startswith("BDP-003F.17")',
                f'or str(state.get("{key}", "")).startswith("BDP-003F.17")\n            or str(state.get("{key}", "")).startswith("BDP-003F.18")',
            )
    if 'startswith("BDP-003F.16")' in new and 'startswith("BDP-003F.18")' not in new:
        for key in ["next_recommended_step", "current_next_step", "next_step", "recommended_next_step", "next_safe_step"]:
            new = new.replace(
                f'or str(state.get("{key}", "")).startswith("BDP-003F.16")',
                f'or str(state.get("{key}", "")).startswith("BDP-003F.16")\n            or str(state.get("{key}", "")).startswith("BDP-003F.17")\n            or str(state.get("{key}", "")).startswith("BDP-003F.18")',
            )
    new = new.replace("approved F16/F17 progression", "approved F16/F18 progression")
    write_if_changed(path, text, new)


def main() -> int:
    repair_f10_f12(F10, PHASES_10_18, PHASES_10_18)
    repair_f10_f12(F11, PHASES_11_18, PHASES_11_18)
    repair_f10_f12(F12, PHASES_12_18, PHASES_12_18)
    repair_f13(F13)
    repair_f14(F14)
    repair_f15(F15)

    for path in [F10, F11, F12, F13, F14, F15]:
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            raise SystemExit(f"[FAIL] {path.relative_to(ROOT)} does not compile: {exc.msg}")
    print("[OK] BDP-003F.17 verifier progression repair v4 complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
