#!/usr/bin/env python3
"""Repair completed Concept Lens verifier phase progression for BDP-003F.16.

The BDP-003F.16 decision updates the global state to F16. Several earlier
completed-phase verifiers still had hard-coded progression windows ending at
F14/F15. This script widens those verifier-only guards so the historical chain
can be re-run after F16 without weakening the F16 implementation boundary.
"""

from __future__ import annotations

import py_compile
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    ROOT / "scripts" / "verify_bdp_003f10_concept_lens_read_only_bridge_contract.py",
    ROOT / "scripts" / "verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py",
    ROOT / "scripts" / "verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py",
    ROOT / "scripts" / "verify_bdp_003f13_concept_lens_ui_integration_contract.py",
    ROOT / "scripts" / "verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py",
    ROOT / "scripts" / "verify_bdp_003f15_concept_lens_running_frontend_review.py",
]

F16_PHASE = '"BDP-003F.16"'
F16_NEXT_STEP = "BDP-003F.17 — Define Concept Lens limited control expansion contract after F16 readiness decision."
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


def add_to_braced_set_body(body: str, quoted_value: str) -> tuple[str, bool]:
    if quoted_value in body:
        return body, False

    if "\n" in body:
        lines = body.splitlines()
        entry_indent = "    "
        for line in lines:
            if '"BDP-' in line or "PHASE" in line:
                entry_indent = re.match(r"\s*", line).group(0)
                break
        stripped_body = body.rstrip()
        comma = "" if stripped_body.endswith(",") else ","
        return f"{stripped_body}{comma}\n{entry_indent}{quoted_value},\n", True

    stripped_body = body.strip()
    if not stripped_body:
        return quoted_value, True
    return f"{stripped_body}, {quoted_value}", True


def add_phase_to_named_set(text: str, name: str) -> tuple[str, bool]:
    pattern = re.compile(rf"({re.escape(name)}\s*=\s*\{{)(.*?)(\}})", re.DOTALL)
    changed = False

    def repl(match: re.Match[str]) -> str:
        nonlocal changed
        body, did_change = add_to_braced_set_body(match.group(2), F16_PHASE)
        changed = changed or did_change
        return f"{match.group(1)}{body}{match.group(3)}"

    return pattern.sub(repl, text), changed


def add_phase_to_membership_set(text: str, field: str) -> tuple[str, bool]:
    pattern = re.compile(rf'(data\.get\("{re.escape(field)}"\)\s+in\s+\{{)([^}}]*)(\}})', re.DOTALL)
    changed = False

    def repl(match: re.Match[str]) -> str:
        nonlocal changed
        body, did_change = add_to_braced_set_body(match.group(2), F16_PHASE)
        changed = changed or did_change
        return f"{match.group(1)}{body}{match.group(3)}"

    return pattern.sub(repl, text), changed


def repair_next_recommended_step_guard(text: str, path: Path) -> tuple[str, bool]:
    """Allow completed F14/F15 verifiers to tolerate F16's next safe step."""

    if F16_NEXT_STEP in text:
        return text, False

    pattern = re.compile(
        r'(?ms)^(?P<indent>\s*)require\(\s*'
        r'data\.get\("next_recommended_step"\)\s*==\s*(?P<rhs>[^,\n\)]+),\s*'
        r'"Global next_recommended_step must match F15 next safe step"\s*\)'
    )

    def repl(match: re.Match[str]) -> str:
        indent = match.group("indent")
        rhs = match.group("rhs").strip()
        return (
            f'{indent}allowed_next_recommended_steps = {{\n'
            f'{indent}    {rhs},\n'
            f'{indent}    "{F16_NEXT_STEP}",\n'
            f'{indent}}}\n'
            f'{indent}require(\n'
            f'{indent}    data.get("next_recommended_step") in allowed_next_recommended_steps,\n'
            f'{indent}    "Global next_recommended_step must match approved F15-F16 next safe step",\n'
            f'{indent})'
        )

    new_text, count = pattern.subn(repl, text)
    if count:
        return new_text, True

    # Fallback for verifiers that call fail(...) rather than require(...).
    fail_pattern = re.compile(
        r'(?ms)^(?P<indent>\s*)if\s+data\.get\("next_recommended_step"\)\s*!=\s*(?P<rhs>[^:\n]+):\s*\n'
        r'(?P=indent)\s+fail\("Global next_recommended_step must match F15 next safe step"\)'
    )

    def fail_repl(match: re.Match[str]) -> str:
        indent = match.group("indent")
        rhs = match.group("rhs").strip()
        return (
            f'{indent}allowed_next_recommended_steps = {{\n'
            f'{indent}    {rhs},\n'
            f'{indent}    "{F16_NEXT_STEP}",\n'
            f'{indent}}}\n'
            f'{indent}if data.get("next_recommended_step") not in allowed_next_recommended_steps:\n'
            f'{indent}    fail("Global next_recommended_step must match approved F15-F16 next safe step")'
        )

    new_text, count = fail_pattern.subn(fail_repl, text)
    if count:
        return new_text, True

    if "Global next_recommended_step must match F15 next safe step" in text:
        fail(f"Could not safely rewrite next_recommended_step guard in {rel(path)}")

    return text, False


def widen_progression_messages(text: str) -> str:
    replacements = {
        "approved F10-F14 progression": "approved F10-F16 progression",
        "approved F11-F14 progression": "approved F11-F16 progression",
        "approved F12-F14 progression": "approved F12-F16 progression",
        "approved F13-F14 progression": "approved F13-F16 progression",
        "approved F14-F15 progression": "approved F14-F16 progression",
        "approved F15 progression": "approved F15-F16 progression",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def repair_file(path: Path) -> bool:
    if not path.exists():
        fail(f"Missing verifier: {rel(path)}")

    before = path.read_text(encoding="utf-8")
    text = before
    changed_any = False

    for name in ("ALLOWED_CURRENT_PHASES", "ALLOWED_LAST_UPDATED_PHASES"):
        text, changed = add_phase_to_named_set(text, name)
        changed_any = changed_any or changed

    for field in ("current_phase", "last_updated_phase"):
        text, changed = add_phase_to_membership_set(text, field)
        changed_any = changed_any or changed

    text, changed = repair_next_recommended_step_guard(text, path)
    changed_any = changed_any or changed

    messaged = widen_progression_messages(text)
    changed_any = changed_any or (messaged != text)
    text = messaged

    if text != before:
        path.write_text(text, encoding="utf-8")
        py_compile.compile(str(path), doraise=True)
        print(f"[OK] repaired {rel(path)}")
        return True

    py_compile.compile(str(path), doraise=True)
    print(f"[OK] already compatible {rel(path)}")
    return False


def main() -> None:
    changed_files: list[str] = []
    for path in TARGETS:
        if rel(path) in FORBIDDEN_TO_TOUCH:
            fail(f"Refusing to touch forbidden file: {rel(path)}")
        if repair_file(path):
            changed_files.append(rel(path))

    print("[OK] BDP-003F.16 verifier progression repair complete")
    if changed_files:
        print("[OK] changed files:")
        for path in changed_files:
            print(f"  - {path}")


if __name__ == "__main__":
    main()
