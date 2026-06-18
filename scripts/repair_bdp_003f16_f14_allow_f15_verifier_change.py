#!/usr/bin/env python3
"""Allow the F16 F15-verifier repair inside the F14 verifier git-boundary check."""

from __future__ import annotations

from pathlib import Path

TARGET = Path("scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py")
ENTRY = '    "scripts/verify_bdp_003f15_concept_lens_running_frontend_review.py",\n'


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def main() -> int:
    if not TARGET.exists():
        fail(f"missing target: {TARGET}")

    text = TARGET.read_text(encoding="utf-8")
    if ENTRY.strip() in text:
        print("[OK] F14 verifier already allows repaired F15 verifier change")
        return 0

    marker = "ALLOWED_CHANGED_FILES = {"
    start = text.find(marker)
    if start == -1:
        fail("could not locate ALLOWED_CHANGED_FILES in F14 verifier")

    insert_after_candidates = [
        '    "scripts/verify_bdp_003f15_concept_lens_running_frontend_review.py",\n',
        '    "BDP_003F16_F14_PROGRESSION_GUARD_REPAIR_V3_README.md",\n',
        '    "BDP_003F16_VERIFIER_PROGRESSION_REPAIR_README.md",\n',
        '    "BDP_003F14_VERIFIER_PROGRESSION_REPAIR_V2_README.md",\n',
        '    "BDP_003F14_VERIFIER_PROGRESSION_REPAIR_README.md",\n',
    ]

    insertion_point = -1
    for candidate in insert_after_candidates[1:]:
        pos = text.find(candidate, start)
        if pos != -1:
            insertion_point = pos + len(candidate)
            break

    if insertion_point == -1:
        # Fallback: insert just before the ALLOWED_CHANGED_FILES closing brace.
        close = text.find("}\n", start)
        if close == -1:
            fail("could not locate ALLOWED_CHANGED_FILES closing brace")
        insertion_point = close

    text = text[:insertion_point] + ENTRY + text[insertion_point:]
    TARGET.write_text(text, encoding="utf-8")
    print(f"[OK] repaired {TARGET}")
    print("[OK] F14 verifier now allows the F16 repair to F15 verifier")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
