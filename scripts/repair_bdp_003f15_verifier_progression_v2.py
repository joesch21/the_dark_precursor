#!/usr/bin/env python3
"""Repair BDP-003F.15 successor-state verifier progression checks.

This is a narrow verifier/doc hygiene repair. It teaches historical Concept Lens
verifiers that, after a successful BDP-003F.15 running-frontend review, global
state may legitimately be:

- current_phase / last_updated_phase: BDP-003F.15
- next_step: BDP-003F.16 — either readiness decision or bounded repair

It does not modify frontend, service, bridge, adapter, route, SQL, archive,
citation, claim, interpretation, or concept relation code.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path.cwd()

PHASE_10 = "BDP-003F.10"
PHASE_11 = "BDP-003F.11"
PHASE_12 = "BDP-003F.12"
PHASE_13 = "BDP-003F.13"
PHASE_14 = "BDP-003F.14"
PHASE_15 = "BDP-003F.15"
PHASE_16 = "BDP-003F.16"

VERIFY_F10 = Path("scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py")
VERIFY_F11 = Path("scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py")
VERIFY_F12 = Path("scripts/verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py")
VERIFY_F13 = Path("scripts/verify_bdp_003f13_concept_lens_ui_integration_contract.py")
VERIFY_F14 = Path("scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py")
HANDOVER = Path("BUCHANAN_THREAD_HANDOVER.md")

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


def tuple_literal(items: list[str]) -> str:
    return "(" + ", ".join(repr(item) for item in items) + ("," if len(items) == 1 else "") + ")"


def set_literal(items: list[str]) -> str:
    return "{" + ", ".join(repr(item) for item in items) + "}"


def patch_allowed_next_prefixes(path: Path, prefixes: list[str]) -> bool:
    text = read(path)
    original = text
    replacement = "ALLOWED_NEXT_PREFIXES = " + tuple_literal(prefixes)

    if "ALLOWED_NEXT_PREFIXES" in text:
        text, count = re.subn(
            r"ALLOWED_NEXT_PREFIXES\s*=\s*(?:\([^)]*\)|\[[^\]]*\]|\{[^}]*\})",
            replacement,
            text,
            count=1,
            flags=re.DOTALL,
        )
        require(count == 1, f"Could not update ALLOWED_NEXT_PREFIXES in {path}")
    else:
        # Fallback: insert near the phase constants if a verifier has no prefix tuple.
        text = text.replace(
            "PHASE = ",
            replacement + "\nPHASE = ",
            1,
        )

    require(PHASE_16 in text, f"{path} still does not allow {PHASE_16} next-step progression")
    return write_if_changed(path, text) or text != original


def patch_current_phase_set(path: Path, allowed: list[str]) -> bool:
    text = read(path)
    original = text
    replacement = "ALLOWED_CURRENT_PHASES = " + set_literal(allowed)

    if "ALLOWED_CURRENT_PHASES" in text:
        text, count = re.subn(
            r"ALLOWED_CURRENT_PHASES\s*=\s*(?:\{[^}]*\}|\[[^\]]*\]|\([^)]*\))",
            replacement,
            text,
            count=1,
            flags=re.DOTALL,
        )
        require(count == 1, f"Could not update ALLOWED_CURRENT_PHASES in {path}")

    require(PHASE_15 in text, f"{path} still does not allow {PHASE_15} current phase progression")
    return write_if_changed(path, text) or text != original


def patch_f10_to_f12_next_steps() -> list[str]:
    changed: list[str] = []
    targets = [
        (VERIFY_F10, [PHASE_10, PHASE_11, PHASE_12, PHASE_13, PHASE_14, PHASE_15], [PHASE_10, PHASE_11, PHASE_12, PHASE_13, PHASE_14, PHASE_15, PHASE_16]),
        (VERIFY_F11, [PHASE_11, PHASE_12, PHASE_13, PHASE_14, PHASE_15], [PHASE_11, PHASE_12, PHASE_13, PHASE_14, PHASE_15, PHASE_16]),
        (VERIFY_F12, [PHASE_12, PHASE_13, PHASE_14, PHASE_15], [PHASE_12, PHASE_13, PHASE_14, PHASE_15, PHASE_16]),
    ]
    for path, current_allowed, next_prefixes in targets:
        file_changed = False
        if patch_current_phase_set(path, current_allowed):
            file_changed = True
        if patch_allowed_next_prefixes(path, next_prefixes):
            file_changed = True
        if file_changed:
            changed.append(str(path))
    return changed


def patch_f13() -> bool:
    path = VERIFY_F13
    text = read(path)
    original = text

    # Current phase can remain at F13 during original verification, or later be F14/F15.
    text = text.replace(
        'data.get("current_phase") in {PHASE, "BDP-003F.14"}',
        'data.get("current_phase") in {PHASE, "BDP-003F.14", "BDP-003F.15"}',
    )
    text = text.replace(
        'data.get("current_phase") in {PHASE, "BDP-003F.14", "BDP-003F.15", "BDP-003F.15"}',
        'data.get("current_phase") in {PHASE, "BDP-003F.14", "BDP-003F.15"}',
    )

    # Replace exact F13/F14 next-step equality with a descendant-safe prefix check.
    text = re.sub(
        r'require\(\s*data\.get\("next_step"\)\s+in\s+\{NEXT_STEP,\s*NEXT_AFTER_F14\}\s*,\s*"Global next_step should remain in approved F13-F14 progression"\s*\)',
        'require(data.get("next_step", "").startswith(("BDP-003F.14", "BDP-003F.15", "BDP-003F.16")), "Global next_step should remain in approved F13-F16 progression")',
        text,
        count=1,
        flags=re.DOTALL,
    )

    # Fallback for differently formatted exact next-step checks.
    text = text.replace(
        'require(data.get("next_step") in {NEXT_STEP, NEXT_AFTER_F14}, "Global next_step should remain in approved F13-F14 progression")',
        'require(data.get("next_step", "").startswith(("BDP-003F.14", "BDP-003F.15", "BDP-003F.16")), "Global next_step should remain in approved F13-F16 progression")',
    )
    text = text.replace(
        'require(data.get("next_step") in {NEXT_STEP, NEXT_AFTER_F14}, "Global next_step should remain in approved F13-F15 progression")',
        'require(data.get("next_step", "").startswith(("BDP-003F.14", "BDP-003F.15", "BDP-003F.16")), "Global next_step should remain in approved F13-F16 progression")',
    )

    require(PHASE_15 in text, f"{path} still does not allow {PHASE_15} current phase progression")
    require(PHASE_16 in text, f"{path} still does not allow {PHASE_16} next-step progression")
    return write_if_changed(path, text) or text != original


def patch_f14() -> bool:
    path = VERIFY_F14
    text = read(path)
    original = text

    # Make current/last-updated checks tolerate F15 successor state.
    replacements = {
        'data.get("current_phase") == PHASE': 'data.get("current_phase") in {PHASE, "BDP-003F.15"}',
        'data.get("last_updated_phase") == PHASE': 'data.get("last_updated_phase") in {PHASE, "BDP-003F.15"}',
        'data.get("current_phase") == "BDP-003F.14"': 'data.get("current_phase") in {"BDP-003F.14", "BDP-003F.15"}',
        'data.get("last_updated_phase") == "BDP-003F.14"': 'data.get("last_updated_phase") in {"BDP-003F.14", "BDP-003F.15"}',
        'data.get("current_phase") in {PHASE}': 'data.get("current_phase") in {PHASE, "BDP-003F.15"}',
        'data.get("last_updated_phase") in {PHASE}': 'data.get("last_updated_phase") in {PHASE, "BDP-003F.15"}',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # If first repair already changed message but missed literal condition, normalize all literal F14 membership checks.
    text = text.replace(
        'data.get("last_updated_phase") in {"BDP-003F.14"}',
        'data.get("last_updated_phase") in {"BDP-003F.14", "BDP-003F.15"}',
    )
    text = text.replace(
        'data.get("current_phase") in {"BDP-003F.14"}',
        'data.get("current_phase") in {"BDP-003F.14", "BDP-003F.15"}',
    )

    # Allow F15 and the post-F15 F16 next step.
    if "ALLOWED_NEXT_PREFIXES" in text:
        text, _ = re.subn(
            r"ALLOWED_NEXT_PREFIXES\s*=\s*(?:\([^)]*\)|\[[^\]]*\]|\{[^}]*\})",
            'ALLOWED_NEXT_PREFIXES = ("BDP-003F.15", "BDP-003F.16")',
            text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        # Convert common exact F15 next-step checks if present.
        text = text.replace(
            'data.get("next_step") == NEXT_STEP',
            'data.get("next_step", "").startswith(("BDP-003F.15", "BDP-003F.16"))',
        )
        text = text.replace(
            'data.get("next_step") == "BDP-003F.15 — Review the Concept Lens read-only evidence posture display in the running frontend before expanding controls or concept coverage."',
            'data.get("next_step", "").startswith(("BDP-003F.15", "BDP-003F.16"))',
        )

    # Robustly patch any remaining require around last_updated_phase that still demands only F14.
    text = re.sub(
        r'data\.get\("last_updated_phase"\)\s*==\s*PHASE',
        'data.get("last_updated_phase") in {PHASE, "BDP-003F.15"}',
        text,
    )
    text = re.sub(
        r'data\.get\("last_updated_phase"\)\s*==\s*"BDP-003F\.14"',
        'data.get("last_updated_phase") in {"BDP-003F.14", "BDP-003F.15"}',
        text,
    )

    text = text.replace(
        "last_updated_phase not advanced to BDP-003F.14",
        "last_updated_phase should remain in approved F14-F15 progression",
    )
    text = text.replace(
        "Global next_step should remain in approved F14-F15 progression",
        "Global next_step should remain in approved F14-F16 progression",
    )

    require(PHASE_15 in text, f"{path} still does not allow {PHASE_15} last-updated progression")
    # F14 verifier may not have a next-step check in all repo versions, but if it does it should allow F16.
    return write_if_changed(path, text) or text != original


def strip_trailing_whitespace(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    new_text = "\n".join(line.rstrip() for line in text.splitlines())
    if text.endswith("\n"):
        new_text += "\n"
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    for forbidden in FORBIDDEN_MODIFICATION_TARGETS:
        require(forbidden.exists(), f"Expected untouched runtime target missing: {forbidden}")

    changed: list[str] = []
    changed.extend(patch_f10_to_f12_next_steps())
    if patch_f13():
        changed.append(str(VERIFY_F13))
    if patch_f14():
        changed.append(str(VERIFY_F14))
    if strip_trailing_whitespace(HANDOVER):
        changed.append(str(HANDOVER))

    print("[OK] BDP-003F.15 verifier progression repair V2 applied")
    if changed:
        print("[OK] Changed files:")
        for item in dict.fromkeys(changed):
            print(f" - {item}")
    else:
        print("[OK] No file changes were needed; V2 repair was already applied")
    print("[OK] Runtime frontend/service/bridge files were not modified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
