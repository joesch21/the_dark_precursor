#!/usr/bin/env python3
"""Verify BDP-003F.5 Dark Precursor navigation wiring."""

from __future__ import annotations

import json
import py_compile
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND_PATH = ROOT / "frontend" / "dark_precursor.py"
DOC_PATH = ROOT / "docs" / "BDP_003F5_DARK_PRECURSOR_NAVIGATION_WIRING.md"
STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
F4_VERIFIER_PATH = ROOT / "scripts" / "verify_bdp_003f4_navigation_architecture.py"

PHASE_KEY = "bdp_003f5_dark_precursor_navigation_wiring"


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read_text(path: Path) -> str:
    require(path.exists(), f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run_f4_verifier() -> None:
    require(F4_VERIFIER_PATH.exists(), "F4 verifier is missing")
    subprocess.run(
        [sys.executable, str(F4_VERIFIER_PATH)],
        cwd=ROOT,
        check=True,
    )


def verify_frontend(frontend_text: str) -> None:
    py_compile.compile(str(FRONTEND_PATH), doraise=True)

    required_tokens = [
        "SURFACE_STAGE",
        "SURFACE_ABOUT",
        "APPROVED_DARK_PRECURSOR_SURFACES",
        "get_dark_precursor_surface",
        "set_dark_precursor_surface",
    ]
    for token in required_tokens:
        require(token in frontend_text, f"frontend missing {token}")

    forbidden_raw_assignments = [
        'st.session_state["dark_precursor_view"] = "stage"',
        'st.session_state["dark_precursor_view"] = "about"',
    ]
    for forbidden in forbidden_raw_assignments:
        require(forbidden not in frontend_text, f"raw navigation assignment remains: {forbidden}")

    require(
        "if get_dark_precursor_surface() == SURFACE_ABOUT:" in frontend_text,
        "About route does not use governed surface helper",
    )
    require(
        "Return to concept stage" in frontend_text,
        "Return to concept stage control missing",
    )
    require(
        "About The Dark Precursor" in frontend_text,
        "About The Dark Precursor control missing",
    )
    require(
        "set_dark_precursor_surface(SURFACE_STAGE)" in frontend_text,
        "Return to concept stage does not use governed setter",
    )
    require(
        "set_dark_precursor_surface(SURFACE_ABOUT)" in frontend_text,
        "About button does not use governed setter",
    )

    surface_constants = set(
        re.findall(r"^SURFACE_[A-Z0-9_]+\s*=", frontend_text, flags=re.MULTILINE)
    )
    require(
        surface_constants == {"SURFACE_STAGE =", "SURFACE_ABOUT ="},
        f"unexpected public surface constants found: {sorted(surface_constants)}",
    )

    require(
        'APPROVED_DARK_PRECURSOR_SURFACES = {SURFACE_STAGE, SURFACE_ABOUT}' in frontend_text,
        "approved surface set is not limited to stage/about",
    )


def verify_documentation(doc_text: str) -> None:
    required_phrases = [
        "BDP-003F.5 wires the already-approved navigation architecture into the existing Dark Precursor frontend.",
        "It does not add pages.",
        "It does not add a dashboard.",
        "It does not add backend/database/evidence/citation/interpretation/concept-relation work.",
        "The verified launch authority is README/docs.",
        "cd ~/Applications/the_dark_precursor/buchanan_platform_docs",
        ". ./venv/bin/activate",
        "python -m streamlit run frontend/dark_precursor.py",
        "frontend/dark_precursor.py",
    ]
    for phrase in required_phrases:
        require(phrase in doc_text, f"F5 documentation missing required phrase: {phrase}")


def verify_state_and_handover(state_text: str, handover_text: str) -> None:
    state = json.loads(state_text)
    require(PHASE_KEY in state, "root BUCHANAN_SYSTEM_STATE.json missing F5 record")
    record = state[PHASE_KEY]

    require(record.get("phase") == "BDP-003F.5", "F5 state phase mismatch")
    require(record.get("status") == "complete", "F5 state status is not complete")
    require(record.get("controlled_slice") == "minimal_frontend_navigation_wiring_only", "F5 controlled slice mismatch")
    require(record.get("frontend_target") == "frontend/dark_precursor.py", "F5 frontend target mismatch")
    require(record.get("review_output") == "docs/BDP_003F5_DARK_PRECURSOR_NAVIGATION_WIRING.md", "F5 review output mismatch")
    require(record.get("verifier") == "scripts/verify_bdp_003f5_navigation_wiring.py", "F5 verifier path mismatch")
    require(record.get("verified_launch_authority") == "README/docs", "F5 launch authority mismatch")
    require(
        record.get("verified_launch_method")
        == [
            "cd ~/Applications/the_dark_precursor/buchanan_platform_docs",
            ". ./venv/bin/activate",
            "python -m streamlit run frontend/dark_precursor.py",
        ],
        "F5 verified launch method mismatch",
    )
    require(record.get("approved_surface_keys") == ["stage", "about"], "F5 approved surface keys mismatch")
    require(record.get("new_public_pages_added") is False, "F5 must not add new public pages")
    require(record.get("dashboard_added") is False, "F5 must not add a dashboard")
    require(record.get("adaptive_navigation_added") is False, "F5 must not add adaptive navigation")
    require(record.get("hidden_personalization_added") is False, "F5 must not add hidden personalization")

    forbidden_true_flags = [
        "backend_services_added",
        "adapter_endpoints_added",
        "database_tables_added",
        "sql_migrations_added",
        "archive_workflow_expanded",
        "evidence_promotion_added",
        "citations_created",
        "concept_relations_created",
        "interpretations_created",
        "buchanan_claims_created",
    ]
    for flag in forbidden_true_flags:
        require(record.get(flag) is False, f"F5 state must keep {flag}=false")

    forbidden_authorization_terms = [
        "backend_authorization",
        "database_authorization",
        "sql_authorization",
        "evidence_authorization",
        "citation_authorization",
        "interpretation_authorization",
        "concept_relation_authorization",
        "buchanan_claim_authorization",
    ]
    record_text = json.dumps(record, sort_keys=True).lower()
    for term in forbidden_authorization_terms:
        require(term not in record_text, f"forbidden F5 authorization term appears: {term}")

    require("## BDP-003F.5 — Navigation Wiring" in handover_text, "root handover missing F5 section")
    require("README/docs" in handover_text, "root handover missing README/docs launch authority")
    require(". ./venv/bin/activate" in handover_text, "root handover missing repo venv launch command")
    require(
        "python -m streamlit run frontend/dark_precursor.py" in handover_text,
        "root handover missing Streamlit launch target",
    )


def verify_verifier_source(verifier_text: str) -> None:
    require(
        'STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"' in verifier_text,
        "verifier must hardcode root BUCHANAN_SYSTEM_STATE.json",
    )
    require(
        'HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"' in verifier_text,
        "verifier must hardcode root BUCHANAN_THREAD_HANDOVER.md",
    )
    require("first_" + "existing(" not in verifier_text, "verifier must not use fallback path helper")
    require("--exclude-dir=" + "venv" not in verifier_text, "verifier should not shell-grep through venv")
    require("rg" + "lob(" not in verifier_text, "verifier should not recursively scan the repo")


def main() -> None:
    run_f4_verifier()

    frontend_text = read_text(FRONTEND_PATH)
    doc_text = read_text(DOC_PATH)
    state_text = read_text(STATE_PATH)
    handover_text = read_text(HANDOVER_PATH)
    verifier_text = read_text(Path(__file__).resolve())

    verify_frontend(frontend_text)
    verify_documentation(doc_text)
    verify_state_and_handover(state_text, handover_text)
    verify_verifier_source(verifier_text)

    print("[OK] BDP-003F.5 Dark Precursor navigation wiring verified")


if __name__ == "__main__":
    main()
