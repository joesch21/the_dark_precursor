#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STATE_PATH = ROOT / "BUCHANAN_SYSTEM_STATE.json"
HANDOVER_PATH = ROOT / "BUCHANAN_THREAD_HANDOVER.md"
FRONTEND_PATH = ROOT / "frontend" / "dark_precursor.py"
F2_DOC_PATH = ROOT / "docs" / "BDP_003F2_ABOUT_PAGE.md"
F2_VERIFIER_PATH = ROOT / "scripts" / "verify_bdp_003f2_about_page.py"
F3_DOC_PATH = ROOT / "docs" / "BDP_003F3_ABOUT_PAGE_RUNNING_FRONTEND_REVIEW.md"

NEXT_STEP = "BDP-003F.4 — Define The Dark Precursor navigation architecture before adding further frontend pages."


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read_text(path: Path) -> str:
    require(path.exists(), f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run_verifier(path: Path) -> None:
    require(path.exists(), f"missing verifier: {path.relative_to(ROOT)}")
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")
    require(result.returncode == 0, f"verifier failed: {path.relative_to(ROOT)}")


def main() -> None:
    require(F2_DOC_PATH.exists(), "BDP-003F.2 document is missing")
    run_verifier(F2_VERIFIER_PATH)

    frontend = read_text(FRONTEND_PATH)
    for marker in [
        "def render_about_page",
        "About The Dark Precursor",
        "Return to concept stage",
        "It separates atmosphere from authority",
        "does not claim to think like Ian Buchanan",
    ]:
        require(marker in frontend, f"missing About page marker: {marker}")

    f3_doc = read_text(F3_DOC_PATH)
    require("review-only" in f3_doc, "F3 doc must state review-only boundary")
    require(NEXT_STEP in f3_doc, "F3 doc must record exact next step")

    state = json.loads(read_text(STATE_PATH))
    record = state.get("bdp_003f3_about_page_running_frontend_review")
    require(isinstance(record, dict), "missing F3 state record")

    require(record.get("phase") == "BDP-003F.3", "F3 phase mismatch")
    require(record.get("status") == "complete", "F3 status mismatch")
    require(record.get("review_only") is True, "F3 must be review-only")
    require(record.get("manual_frontend_inspection_recorded") is True, "manual inspection not recorded")
    require(record.get("next_step") == NEXT_STEP, "F3 record next step mismatch")
    require(state.get("next_step") == NEXT_STEP, "root next_step mismatch")
    require(state.get("current_next_step") == NEXT_STEP, "root current_next_step mismatch")
    require(state.get("last_updated_phase") == "BDP-003F.3", "last_updated_phase mismatch")

    for key in [
        "frontend_ux_changed",
        "new_controls_added",
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
    ]:
        require(record.get(key) is False, f"F3 must not allow {key}")

    handover = read_text(HANDOVER_PATH)
    require("## BDP-003F.3 — About Page Running Frontend Review" in handover, "handover missing F3 section")
    require(NEXT_STEP in handover, "handover missing exact next step")

    print("[OK] BDP-003F.3 About page running frontend review verified")


if __name__ == "__main__":
    main()
