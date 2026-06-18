#!/usr/bin/env python3
"""Repair BDP-003F.15 verifier progression compatibility and whitespace hygiene.

This script is intentionally narrow. It only widens historical Concept Lens verifier
progression checks so BDP-003F.15 can be the current global phase after the running
frontend review, and strips trailing whitespace from markdown/state-adjacent files.
It does not modify frontend, service, bridge, adapter, route, SQL, archive, citation,
claim, interpretation, or concept relation code.
"""

from __future__ import annotations

import re
from pathlib import Path

PHASE_15 = "BDP-003F.15"

ROOT = Path.cwd()

VERIFY_F10 = Path("scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py")
VERIFY_F11 = Path("scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py")
VERIFY_F12 = Path("scripts/verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py")
VERIFY_F13 = Path("scripts/verify_bdp_003f13_concept_lens_ui_integration_contract.py")
VERIFY_F14 = Path("scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py")
UPDATE_F15 = Path("scripts/update_bdp_003f15_concept_lens_running_frontend_review.py")
HANDOVER = Path("BUCHANAN_THREAD_HANDOVER.md")
DOC = Path("docs/BDP_003F15_VERIFIER_PROGRESSION_REPAIR.md")
README = Path("BDP_003F15_VERIFIER_PROGRESSION_REPAIR_README.md")

FORBIDDEN_MODIFICATION_TARGETS = [
    Path("frontend/dark_precursor.py"),
    Path("scripts/concept_lens_archive_evidence_posture_service.py"),
    Path("scripts/concept_lens_existing_archive_evidence_readback_bridge.py"),
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.exists(), f"Missing required file: {path}")
    return path.read_text(encoding="utf-8")


def write_if_changed(path: Path, text: str) -> bool:
    old = read(path) if path.exists() else ""
    if old == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def replace_allowed_current_phases(path: Path, phases: list[str]) -> bool:
    text = read(path)
    replacement = "ALLOWED_CURRENT_PHASES = {" + ", ".join(repr(item) for item in phases) + "}"
    pattern = r"ALLOWED_CURRENT_PHASES\s*=\s*(?:\{[^}]*\}|\[[^\]]*\]|\([^\)]*\))"
    new_text, count = re.subn(pattern, replacement, text, count=1, flags=re.DOTALL)
    require(count == 1, f"Could not update ALLOWED_CURRENT_PHASES in {path}")
    require(PHASE_15 in new_text, f"{path} still does not allow {PHASE_15}")
    return write_if_changed(path, new_text)


def patch_f13(path: Path) -> bool:
    text = read(path)
    changed = False
    target = 'data.get("current_phase") in {PHASE, "BDP-003F.14"}'
    replacement = 'data.get("current_phase") in {PHASE, "BDP-003F.14", "BDP-003F.15"}'
    if target in text:
        text = text.replace(target, replacement)
        changed = True
    # Fallback for already-expanded or differently formatted files.
    if PHASE_15 not in text:
        text = re.sub(
            r'data\.get\("current_phase"\)\s+in\s+\{([^}]*BDP-003F\.14[^}]*)\}',
            lambda m: 'data.get("current_phase") in {' + m.group(1).rstrip() + ', "BDP-003F.15"}',
            text,
            count=1,
        )
        changed = True
    require(PHASE_15 in text, f"Could not add {PHASE_15} to {path}")
    return write_if_changed(path, text) or changed


def patch_f14(path: Path) -> bool:
    text = read(path)
    original = text

    # Widen any existing progression set if the verifier already uses one.
    if "ALLOWED_CURRENT_PHASES" in text:
        text = re.sub(
            r"ALLOWED_CURRENT_PHASES\s*=\s*(?:\{[^}]*\}|\[[^\]]*\]|\([^\)]*\))",
            'ALLOWED_CURRENT_PHASES = {"BDP-003F.14", "BDP-003F.15"}',
            text,
            count=1,
            flags=re.DOTALL,
        )
        text = re.sub(
            r'data\.get\("current_phase"\)\s+in\s+\{PHASE\}',
            'data.get("current_phase") in ALLOWED_CURRENT_PHASES',
            text,
            count=1,
        )

    # Common exact checks from the F14 verifier need to become progression-safe.
    text = text.replace(
        'data.get("current_phase") == PHASE',
        'data.get("current_phase") in {PHASE, "BDP-003F.15"}',
    )
    text = text.replace(
        'data.get("last_updated_phase") == PHASE',
        'data.get("last_updated_phase") in {PHASE, "BDP-003F.15"}',
    )
    text = text.replace(
        'last_updated_phase not advanced to BDP-003F.14',
        'last_updated_phase should remain in approved F14-F15 progression',
    )
    text = text.replace(
        'current_phase not advanced to BDP-003F.14',
        'current_phase should remain in approved F14-F15 progression',
    )

    # If the verifier uses a literal inline set, widen it.
    text = text.replace(
        'data.get("current_phase") in {PHASE}',
        'data.get("current_phase") in {PHASE, "BDP-003F.15"}',
    )
    text = text.replace(
        'data.get("last_updated_phase") in {PHASE}',
        'data.get("last_updated_phase") in {PHASE, "BDP-003F.15"}',
    )

    require(PHASE_15 in text, f"Could not add {PHASE_15} to {path}")
    return write_if_changed(path, text) or text != original


def patch_f15_updater(path: Path) -> bool:
    text = read(path)
    original = text
    text = text.replace("Status: complete  \n", "Status: complete\n")
    text = text.replace("Review result: {record['running_frontend_review_result']}  \n", "Review result: {record['running_frontend_review_result']}\n")
    text = text.replace("**Phase:** {PHASE}  \n", "**Phase:** {PHASE}\n")
    text = text.replace("**Title:** {TITLE}  \n", "**Title:** {TITLE}\n")
    text = text.replace("**Controlled slice:** running-frontend review only  \n", "**Controlled slice:** running-frontend review only\n")
    text = text.replace("**Status:** complete  \n", "**Status:** complete\n")
    text = text.replace("**Completed at:** {record['completed_at']}  \n", "**Completed at:** {record['completed_at']}\n")
    return write_if_changed(path, text) or text != original


def strip_trailing_whitespace(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    new_lines = [line.rstrip() for line in text.splitlines()]
    new_text = "\n".join(new_lines) + ("\n" if text.endswith("\n") else "")
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    for forbidden in FORBIDDEN_MODIFICATION_TARGETS:
        require(forbidden.exists(), f"Expected untouched target missing: {forbidden}")

    changed: list[str] = []

    if replace_allowed_current_phases(VERIFY_F10, ["BDP-003F.10", "BDP-003F.11", "BDP-003F.12", "BDP-003F.13", "BDP-003F.14", "BDP-003F.15"]):
        changed.append(str(VERIFY_F10))
    if replace_allowed_current_phases(VERIFY_F11, ["BDP-003F.11", "BDP-003F.12", "BDP-003F.13", "BDP-003F.14", "BDP-003F.15"]):
        changed.append(str(VERIFY_F11))
    if replace_allowed_current_phases(VERIFY_F12, ["BDP-003F.12", "BDP-003F.13", "BDP-003F.14", "BDP-003F.15"]):
        changed.append(str(VERIFY_F12))
    if patch_f13(VERIFY_F13):
        changed.append(str(VERIFY_F13))
    if patch_f14(VERIFY_F14):
        changed.append(str(VERIFY_F14))
    if patch_f15_updater(UPDATE_F15):
        changed.append(str(UPDATE_F15))

    for whitespace_path in [HANDOVER, DOC, README]:
        if strip_trailing_whitespace(whitespace_path):
            changed.append(str(whitespace_path))

    print("[OK] BDP-003F.15 verifier progression repair applied")
    if changed:
        print("[OK] Changed files:")
        for item in changed:
            print(f" - {item}")
    else:
        print("[OK] No file changes were needed; repair was already applied")
    print("[OK] Frontend/service/bridge targets were not modified by this repair script")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
