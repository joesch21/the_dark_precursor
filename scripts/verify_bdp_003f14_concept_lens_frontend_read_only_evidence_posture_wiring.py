#!/usr/bin/env python3
"""Verify BDP-003F.14 Concept Lens frontend read-only evidence posture wiring."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

PHASE = "BDP-003F.14"
NEXT_STEP = "BDP-003F.15 — Review the Concept Lens read-only evidence posture display in the running frontend before expanding controls or concept coverage."
FRONTEND = Path("frontend/dark_precursor.py")
DOC = Path("docs/BDP_003F14_CONCEPT_LENS_FRONTEND_READ_ONLY_EVIDENCE_POSTURE_WIRING.md")
README = Path("BDP_003F14_PATCH_README.md")
STATE = Path("BUCHANAN_SYSTEM_STATE.json")
HANDOVER = Path("BUCHANAN_THREAD_HANDOVER.md")
START = "# BDP-003F.14 CONCEPT LENS READ-ONLY EVIDENCE POSTURE DISPLAY START"
END = "# BDP-003F.14 CONCEPT LENS READ-ONLY EVIDENCE POSTURE DISPLAY END"
SERVICE_HANDOFF = "read_concept_lens_archive_evidence_posture_via_existing_archive_bridge"
BOUNDARY_NOTE = "This panel displays read-only archive evidence posture. It does not create citations, claims, interpretations, concept relations, or database records."
CONTROLLED_EXAMPLES = ["Body without Organs", "we repress because we repeat", "assemblage"]
ALLOWED_CHANGED_FILES = {
    "frontend/dark_precursor.py",
    "docs/BDP_003F14_CONCEPT_LENS_FRONTEND_READ_ONLY_EVIDENCE_POSTURE_WIRING.md",
    "scripts/update_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py",
    "scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py",
    "BDP_003F14_PATCH_README.md",
    "BUCHANAN_SYSTEM_STATE.json",
    "BUCHANAN_THREAD_HANDOVER.md",
    "BDP_003F14_VERIFIER_PROGRESSION_REPAIR_README.md",
    "docs/BDP_003F14_VERIFIER_PROGRESSION_REPAIR.md",
    "scripts/update_bdp_003f14_verifier_progression_repair.py",
    "scripts/verify_bdp_003f13_concept_lens_ui_integration_contract.py",
    "scripts/verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py",
    "scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py",
    "scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py",
    "scripts/update_bdp_003f14_verifier_progression_repair_v2.py",
    "docs/BDP_003F14_VERIFIER_PROGRESSION_REPAIR_V2.md",
    "BDP_003F14_VERIFIER_PROGRESSION_REPAIR_V2_README.md",
}


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing required file: {path}")
    return path.read_text(encoding="utf-8")


def extract_frontend_block(text: str) -> str:
    require(START in text and END in text, "frontend marker block missing")
    return text.split(START, 1)[1].split(END, 1)[0]


def verify_frontend() -> None:
    text = read(FRONTEND)
    block = extract_frontend_block(text)

    require("Concept Lens" in block, "Concept Lens display label missing")
    require("Evidence posture" in block, "Evidence posture label missing")
    require("Archive evidence posture" in block, "Archive evidence posture label missing")
    require("Read-only archive evidence posture" in block or "Read-only archive evidence" in block, "read-only evidence posture label missing")
    require(SERVICE_HANDOFF in block, "approved service handoff not referenced in frontend block")
    boundary_note_present = (
        BOUNDARY_NOTE in block
        or (
            "This panel displays read-only archive evidence posture. It does not create " in block
            and "citations, claims, interpretations, concept relations, or database records." in block
        )
    )
    require(boundary_note_present, "required read-only boundary note missing from frontend block")

    for example in CONTROLLED_EXAMPLES:
        require(example in block, f"controlled concept example missing from frontend block: {example}")

    for required in (
        "Archive-grounded match",
        "Source-bound description",
        "Exploratory / unverified",
        "No archive match",
        "Rights-limited display",
        "omitted_by_rights_policy",
        "concepts -> concept_mentions -> passages -> citations -> sources",
    ):
        require(required in block, f"required display vocabulary missing from frontend block: {required}")

    free_text_patterns = (
        r"\bst\.text_input\s*\(",
        r"\bst\.text_area\s*\(",
        r"\bst\.chat_input\s*\(",
        r"accept_new_options\s*=\s*True",
    )
    for pattern in free_text_patterns:
        require(not re.search(pattern, block), f"free-text search/input path appears inside F14 block: {pattern}")

    mutation_patterns = (
        r"\bINSERT\b",
        r"\bUPDATE\b",
        r"\bDELETE\b",
        r"\bDROP\b",
        r"\bALTER\b",
        r"\bCREATE\s+TABLE\b",
        r"\.execute\s*\(",
        r"\.executemany\s*\(",
        r"\.commit\s*\(",
        r"sqlite3\.connect",
        r"psycopg",
        r"sqlalchemy",
    )
    for pattern in mutation_patterns:
        require(not re.search(pattern, block), f"SQL/database mutation path appears inside F14 block: {pattern}")

    creation_path_patterns = (
        "insert_citation",
        "create_citation",
        "add_citation",
        "insert_claim",
        "create_claim",
        "insert_interpretation",
        "create_interpretation",
        "insert_concept_relation",
        "create_concept_relation",
        "insert_concept_mention",
        "create_concept_mention",
        "promote_evidence",
        "evidence_promotion",
        "source_ingestion",
        "external_llm",
        "llm_router",
        "adapter_endpoint",
        "route_handler",
    )
    lowered = block.lower()
    for token in creation_path_patterns:
        require(token.lower() not in lowered, f"blocked creation/promotion/routing path appears inside F14 block: {token}")


def verify_docs() -> None:
    doc = read(DOC)
    readme = read(README)
    handover = read(HANDOVER)

    for text_name, text in (("doc", doc), ("readme", readme), ("handover", handover)):
        require(PHASE in text, f"{text_name} does not record BDP-003F.14")
        require(SERVICE_HANDOFF in text, f"{text_name} does not record approved service handoff")
        require(BOUNDARY_NOTE in text, f"{text_name} does not record read-only boundary note")
        for example in CONTROLLED_EXAMPLES:
            require(example in text, f"{text_name} missing controlled example: {example}")

    for blocked in (
        "no free-text concept search input",
        "no SQL migration",
        "no database mutation",
        "no evidence promotion",
        "no Buchanan-specific claims",
        "no external LLM routing",
        "no unrestricted passage reproduction",
        "no general chat filtering",
    ):
        require(blocked in handover or blocked.replace("no ", "No ") in handover, f"handover missing boundary: {blocked}")

    require(NEXT_STEP in doc, "F14 doc does not set F15 as next safe step")
    require(NEXT_STEP in handover, "handover does not set F15 as next safe step")


def verify_state() -> None:
    state_text = read(STATE)
    state = json.loads(state_text)
    require(isinstance(state, dict), "system state is not a JSON object")

    phases = state.get("phases", {})
    require(isinstance(phases, dict), "system state phases field is not an object")
    phase_record = phases.get(PHASE) or state.get("bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring")
    require(isinstance(phase_record, dict), "system state does not record BDP-003F.14")
    require(phase_record.get("status") == "complete", "BDP-003F.14 is not marked complete in system state")
    require(phase_record.get("frontend_target") == "frontend/dark_precursor.py", "system state does not record frontend target")
    require(phase_record.get("approved_service_handoff") == SERVICE_HANDOFF, "system state does not record approved service handoff")
    require(phase_record.get("free_text_search_input_added") is False, "system state must record no free-text search input")

    false_flags = [
        "database_mutation",
        "database_writes_added",
        "archive_row_creation_added",
        "source_ingestion_added",
        "citation_creation_added",
        "concept_mention_creation_added",
        "concept_relation_creation_added",
        "interpretation_insertion_added",
        "evidence_promotion_added",
        "buchanan_claims_created",
        "external_llm_routing_added",
        "automatic_chat_filtering_added",
        "unrestricted_passage_reproduction_added",
        "backend_routes_added",
        "adapter_endpoints_added",
        "sql_migrations_added",
    ]
    for flag in false_flags:
        require(phase_record.get(flag) is False, f"system state flag must remain false: {flag}")

    require(state.get("last_updated_phase") == PHASE, "last_updated_phase not advanced to BDP-003F.14")
    require(state.get("next_recommended_step") == NEXT_STEP or state.get("next_step") == NEXT_STEP, "system state next step is not F15 running frontend review")


def verify_changed_file_scope_if_available() -> None:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only"],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except Exception:
        return
    if result.returncode != 0:
        return
    changed = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    if not changed:
        return
    unexpected = sorted(changed - ALLOWED_CHANGED_FILES)
    require(not unexpected, "unexpected changed files outside F14 boundary: " + ", ".join(unexpected))


def main() -> None:
    verify_frontend()
    verify_docs()
    verify_state()
    verify_changed_file_scope_if_available()
    print("[OK] BDP-003F.14 Concept Lens frontend read-only evidence posture wiring verified")


if __name__ == "__main__":
    main()
