#!/usr/bin/env python3
"""Apply BDP-003F.14 Concept Lens frontend read-only evidence posture wiring.

This script is intentionally file-system local and repository bounded. It writes only
frontend/docs/scripts/state/handover files for the F14 phase and does not touch any
SQL, database, backend route, adapter endpoint, citation, claim, interpretation,
concept relation, or evidence promotion path.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PHASE = "BDP-003F.14"
NEXT_STEP = 'BDP-003F.15 — Review the Concept Lens read-only evidence posture display in the running frontend before expanding controls or concept coverage.'
DOC_PATH = Path("docs/BDP_003F14_CONCEPT_LENS_FRONTEND_READ_ONLY_EVIDENCE_POSTURE_WIRING.md")
README_PATH = Path("BDP_003F14_PATCH_README.md")
FRONTEND_PATH = Path("frontend/dark_precursor.py")
STATE_PATH = Path("BUCHANAN_SYSTEM_STATE.json")
HANDOVER_PATH = Path("BUCHANAN_THREAD_HANDOVER.md")
START = "# BDP-003F.14 CONCEPT LENS READ-ONLY EVIDENCE POSTURE DISPLAY START"
END = "# BDP-003F.14 CONCEPT LENS READ-ONLY EVIDENCE POSTURE DISPLAY END"

F14_DOC = '# BDP-003F.14 — Concept Lens Frontend Read-only Evidence Posture Wiring\n\n**Status:** Complete after verifier pass  \n**Controlled slice:** Frontend read-only evidence posture display only  \n**Frontend target:** `frontend/dark_precursor.py`  \n**Service handoff:** `read_concept_lens_archive_evidence_posture_via_existing_archive_bridge`  \n**Database mutation:** No  \n**SQL migration:** No  \n**Evidence promotion:** No  \n**Buchanan-specific claim generation:** No\n\n## Purpose\n\nBDP-003F.14 wires the approved BDP-003F.13 Concept Lens UI integration contract into The Dark Precursor frontend as a conservative read-only evidence posture display.\n\nThe frontend panel answers only this bounded question:\n\n```text\nFor this controlled concept example, what does the existing archive bridge and Concept Lens evidence posture service currently report?\n```\n\nIt does not convert the display into an evidence source, a claim engine, a search system, a database writer, or a Buchanan-specific interpretation layer.\n\n## Contract source\n\nThis phase follows the BDP-003F.13 UI integration contract.\n\nApproved source of display data:\n\n```text\nscripts/concept_lens_archive_evidence_posture_service.py\nscripts/concept_lens_existing_archive_evidence_readback_bridge.py\n```\n\nRequired service handoff:\n\n```text\nread_concept_lens_archive_evidence_posture_via_existing_archive_bridge\n```\n\nPreserved archive chain:\n\n```text\nconcepts -> concept_mentions -> passages -> citations -> sources\n```\n\n## Implemented frontend surface\n\nBDP-003F.14 adds a controlled, read-only Concept Lens evidence posture dock inside the existing cinematic frontend.\n\nThe surface displays:\n\n1. the controlled requested concept label;\n2. the normalized concept label when the service returns one;\n3. `archive_lookup_status`;\n4. `evidence_posture`;\n5. chain completeness / chain summary;\n6. rights-safe source metadata when present;\n7. rights-safe locator metadata when present;\n8. passage display status, conservatively defaulting to `omitted_by_rights_policy`;\n9. the service handoff name;\n10. an explicit read-only boundary note.\n\n## Controlled smoke examples only\n\nThe first frontend implementation does not add a free-text concept search box.\n\nIt exposes only the controlled examples already approved for smoke review:\n\n```text\nBody without Organs\nwe repress because we repeat\nassemblage\n```\n\nExpected posture rules remain:\n\n1. `Body without Organs` may display archive-grounded only if the bridge/service path returns a complete rights-aware row.\n2. `we repress because we repeat` remains exploratory / unverified unless an approved archive row exists.\n3. `assemblage` must not be marked archive-grounded merely because it is philosophically important.\n\n## Required user-facing boundary note\n\nThe frontend includes the boundary note:\n\n```text\nThis panel displays read-only archive evidence posture. It does not create citations, claims, interpretations, concept relations, or database records.\n```\n\n## Approved labels\n\nThe frontend uses the approved vocabulary:\n\n```text\nConcept Lens\nEvidence posture\nArchive evidence posture\nArchive-grounded match\nSource-bound description\nExploratory / unverified\nNo archive match\nRights-limited display\nRead-only archive evidence posture\n```\n\n## Blocked paths\n\nBDP-003F.14 does not add:\n\n1. SQL mutation;\n2. database writes;\n3. archive row creation;\n4. citation creation;\n5. concept mention creation;\n6. concept relation creation;\n7. interpretation insertion;\n8. evidence promotion;\n9. external LLM routing;\n10. free-text concept search input;\n11. source ingestion;\n12. unrestricted passage reproduction;\n13. Buchanan-specific interpretive claim generation;\n14. backend routes or adapter endpoints;\n15. general chat filtering.\n\n## Files changed by this phase\n\n```text\nfrontend/dark_precursor.py\ndocs/BDP_003F14_CONCEPT_LENS_FRONTEND_READ_ONLY_EVIDENCE_POSTURE_WIRING.md\nscripts/update_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py\nscripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py\nBDP_003F14_PATCH_README.md\nBUCHANAN_SYSTEM_STATE.json\nBUCHANAN_THREAD_HANDOVER.md\n```\n\n## Verification\n\nRun the full F14 chain:\n\n```bash\npython3 -m py_compile frontend/dark_precursor.py\npython3 -m py_compile scripts/concept_lens_archive_evidence_posture_service.py\npython3 -m py_compile scripts/concept_lens_existing_archive_evidence_readback_bridge.py\npython3 scripts/verify_bdp_003f6_concept_lens_architecture.py\npython3 scripts/verify_bdp_003f7_concept_lens_archive_evidence_posture_service_contract.py\npython3 scripts/verify_bdp_003f8_concept_lens_archive_evidence_posture_service.py\npython3 scripts/verify_bdp_003f9_concept_lens_evidence_posture_output_review.py\npython3 scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py\npython3 scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py\npython3 scripts/verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py\npython3 scripts/verify_bdp_003f13_concept_lens_ui_integration_contract.py\npython3 scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py\ngit diff --check\n```\n\n## Next safe step\n\n```text\nBDP-003F.15 — Review the Concept Lens read-only evidence posture display in the running frontend before expanding controls or concept coverage.\n```\n'
README = '# BDP-003F.14 Patch Bundle — Concept Lens Frontend Read-only Evidence Posture Wiring\n\nThis bundle wires the approved Concept Lens read-only evidence posture display into `frontend/dark_precursor.py` after the BDP-003F.13 contract.\n\nRequired service handoff:\n\n```text\nread_concept_lens_archive_evidence_posture_via_existing_archive_bridge\n```\n\nRequired frontend boundary note:\n\n```text\nThis panel displays read-only archive evidence posture. It does not create citations, claims, interpretations, concept relations, or database records.\n```\n\nControlled smoke examples:\n\n```text\nBody without Organs\nwe repress because we repeat\nassemblage\n```\n\nIt is intentionally conservative:\n\n1. controlled smoke examples only;\n2. no free-text concept search input;\n3. no SQL mutation;\n4. no database writes;\n5. no citation, claim, interpretation, concept relation, or evidence promotion path;\n6. no backend route or adapter endpoint;\n7. no external LLM routing.\n\n## Apply from repo root\n\n```bash\ncd ~/Applications/the_dark_precursor/buchanan_platform_docs\nset +e\n\nunzip -o ~/Downloads/BDP_003F14_concept_lens_frontend_read_only_evidence_posture_wiring_PATCH_ONLY.zip\npython3 scripts/update_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py\n```\n\n## Verify\n\n```bash\ncd ~/Applications/the_dark_precursor/buchanan_platform_docs\nset +e\n\npython3 -m py_compile frontend/dark_precursor.py\npython3 -m py_compile scripts/concept_lens_archive_evidence_posture_service.py\npython3 -m py_compile scripts/concept_lens_existing_archive_evidence_readback_bridge.py\npython3 scripts/verify_bdp_003f6_concept_lens_architecture.py\npython3 scripts/verify_bdp_003f7_concept_lens_archive_evidence_posture_service_contract.py\npython3 scripts/verify_bdp_003f8_concept_lens_archive_evidence_posture_service.py\npython3 scripts/verify_bdp_003f9_concept_lens_evidence_posture_output_review.py\npython3 scripts/verify_bdp_003f10_concept_lens_read_only_bridge_contract.py\npython3 scripts/verify_bdp_003f11_concept_lens_existing_archive_readback_bridge_implementation.py\npython3 scripts/verify_bdp_003f12_concept_lens_bridge_output_smoke_review.py\npython3 scripts/verify_bdp_003f13_concept_lens_ui_integration_contract.py\npython3 scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py\ngit diff --check\n```\n\n## Inspect before commit\n\n```bash\ngit status -sb\ngit status --short\ngit diff -- frontend/dark_precursor.py\ngit diff -- BUCHANAN_SYSTEM_STATE.json BUCHANAN_THREAD_HANDOVER.md\ngit diff -- docs/BDP_003F14_CONCEPT_LENS_FRONTEND_READ_ONLY_EVIDENCE_POSTURE_WIRING.md scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py\n```\n\n## Commit only after successful verification\n\n```bash\ngit add frontend/dark_precursor.py docs/BDP_003F14_CONCEPT_LENS_FRONTEND_READ_ONLY_EVIDENCE_POSTURE_WIRING.md scripts/update_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py BDP_003F14_PATCH_README.md BUCHANAN_SYSTEM_STATE.json BUCHANAN_THREAD_HANDOVER.md\n\ngit commit -m "Wire BDP-003F.14 Concept Lens read-only evidence posture display"\ngit push\n```\n\n## Next safe step\n\nDo not expand Concept Lens controls in this phase.\n\nNext phase:\n\n```text\nBDP-003F.15 — Review the Concept Lens read-only evidence posture display in the running frontend before expanding controls or concept coverage.\n```\n'
FRONTEND_BLOCK = '# BDP-003F.14 CONCEPT LENS READ-ONLY EVIDENCE POSTURE DISPLAY START\nBDP_003F14_CONCEPT_LENS_CONTROLLED_EXAMPLES = (\n    "Body without Organs",\n    "we repress because we repeat",\n    "assemblage",\n)\n\nBDP_003F14_CONCEPT_LENS_BOUNDARY_NOTE = (\n    "This panel displays read-only archive evidence posture. It does not create "\n    "citations, claims, interpretations, concept relations, or database records."\n)\n\nBDP_003F14_CONCEPT_LENS_SERVICE_HANDOFF = (\n    "read_concept_lens_archive_evidence_posture_via_existing_archive_bridge"\n)\n\n\ndef _bdp_003f14_concept_lens_value(result, key, default=""):\n    """Read a value from a dict-like or object-like Concept Lens result."""\n    if isinstance(result, dict):\n        return result.get(key, default)\n    return getattr(result, key, default)\n\n\ndef _bdp_003f14_concept_lens_chain_summary(result):\n    chain_summary = _bdp_003f14_concept_lens_value(result, "chain_completeness_summary")\n    if chain_summary:\n        return chain_summary\n\n    chain_complete = _bdp_003f14_concept_lens_value(result, "chain_complete")\n    if chain_complete is True:\n        return "complete reviewed chain: concepts -> concept_mentions -> passages -> citations -> sources"\n    if chain_complete is False:\n        return "chain completeness not established"\n\n    archive_chain = _bdp_003f14_concept_lens_value(result, "archive_chain")\n    if archive_chain:\n        if isinstance(archive_chain, (list, tuple)):\n            return " -> ".join(str(part) for part in archive_chain)\n        return str(archive_chain)\n\n    return "concepts -> concept_mentions -> passages -> citations -> sources"\n\n\ndef _bdp_003f14_concept_lens_source_summary(result):\n    source_title = _bdp_003f14_concept_lens_value(result, "source_title")\n    source_author = _bdp_003f14_concept_lens_value(result, "source_author")\n    source_year = _bdp_003f14_concept_lens_value(result, "source_year")\n    source_doi = _bdp_003f14_concept_lens_value(result, "source_doi")\n    source_locator = _bdp_003f14_concept_lens_value(result, "source_locator")\n    locator = _bdp_003f14_concept_lens_value(result, "locator") or source_locator\n\n    parts = []\n    if source_author:\n        parts.append(str(source_author))\n    if source_title:\n        parts.append(str(source_title))\n    if source_year:\n        parts.append(str(source_year))\n    if source_doi:\n        parts.append(f"DOI: {source_doi}")\n    if locator:\n        parts.append(f"Locator: {locator}")\n\n    return " · ".join(parts) if parts else "No rights-safe source metadata returned for this controlled smoke case."\n\n\ndef _bdp_003f14_render_concept_lens_read_only_evidence_posture_display():\n    """Render the BDP-003F.14 read-only Concept Lens evidence posture dock."""\n    from pathlib import Path\n    import sys\n\n    repo_root = Path(__file__).resolve().parents[1]\n    if str(repo_root) not in sys.path:\n        sys.path.insert(0, str(repo_root))\n\n    try:\n        from scripts.concept_lens_existing_archive_evidence_readback_bridge import (\n            read_concept_lens_archive_evidence_posture_via_existing_archive_bridge,\n        )\n    except Exception as exc:\n        st.markdown("### Concept Lens")\n        st.caption("Read-only archive evidence posture")\n        st.warning(f"Concept Lens read-only bridge is unavailable: {exc}")\n        return\n\n    st.markdown(\n        """\n        <style>\n        .bdp-003f14-concept-lens-dock {\n            border: 1px solid rgba(230, 211, 160, 0.24);\n            border-radius: 22px;\n            padding: 1.25rem 1.35rem;\n            margin-top: 1.5rem;\n            background: linear-gradient(135deg, rgba(12, 10, 8, 0.78), rgba(18, 24, 34, 0.70));\n            box-shadow: 0 0 28px rgba(0, 0, 0, 0.28);\n        }\n        .bdp-003f14-concept-lens-kicker {\n            letter-spacing: 0.18em;\n            text-transform: uppercase;\n            color: rgba(230, 211, 160, 0.78);\n            font-size: 0.72rem;\n            margin-bottom: 0.35rem;\n        }\n        .bdp-003f14-concept-lens-boundary {\n            border-left: 3px solid rgba(230, 211, 160, 0.42);\n            padding-left: 0.85rem;\n            color: rgba(245, 237, 219, 0.84);\n            font-size: 0.92rem;\n        }\n        </style>\n        """,\n        unsafe_allow_html=True,\n    )\n\n    st.markdown(\'<div class="bdp-003f14-concept-lens-dock">\', unsafe_allow_html=True)\n    st.markdown(\'<div class="bdp-003f14-concept-lens-kicker">Read-only archive evidence posture</div>\', unsafe_allow_html=True)\n    st.markdown("### Concept Lens")\n    st.caption("Evidence posture · Archive evidence posture · Rights-limited display")\n\n    selected_concept = st.radio(\n        "Controlled Concept Lens smoke case",\n        BDP_003F14_CONCEPT_LENS_CONTROLLED_EXAMPLES,\n        horizontal=True,\n        key="bdp_003f14_concept_lens_controlled_smoke_case",\n    )\n\n    result = read_concept_lens_archive_evidence_posture_via_existing_archive_bridge(selected_concept)\n\n    requested_label = _bdp_003f14_concept_lens_value(result, "requested_concept_label") or selected_concept\n    normalized_label = (\n        _bdp_003f14_concept_lens_value(result, "normalized_concept_label")\n        or _bdp_003f14_concept_lens_value(result, "normalized_label")\n        or "not returned"\n    )\n    archive_lookup_status = _bdp_003f14_concept_lens_value(result, "archive_lookup_status", "no_archive_match")\n    evidence_posture = _bdp_003f14_concept_lens_value(result, "evidence_posture", "exploratory_unverified")\n    passage_display_status = (\n        _bdp_003f14_concept_lens_value(result, "passage_text_display")\n        or _bdp_003f14_concept_lens_value(result, "passage_display_status")\n        or "omitted_by_rights_policy"\n    )\n\n    col_a, col_b = st.columns(2)\n    with col_a:\n        st.markdown(f"**Requested concept**  \\\\n`{requested_label}`")\n        st.markdown(f"**Normalized concept**  \\\\n`{normalized_label}`")\n        st.markdown(f"**Archive lookup status**  \\\\n`{archive_lookup_status}`")\n    with col_b:\n        st.markdown(f"**Evidence posture**  \\\\n`{evidence_posture}`")\n        st.markdown(f"**Passage display status**  \\\\n`{passage_display_status}`")\n        st.markdown(f"**Service handoff**  \\\\n`{BDP_003F14_CONCEPT_LENS_SERVICE_HANDOFF}`")\n\n    st.markdown("**Chain completeness summary**")\n    st.caption(_bdp_003f14_concept_lens_chain_summary(result))\n\n    st.markdown("**Rights-safe source / locator metadata**")\n    st.caption(_bdp_003f14_concept_lens_source_summary(result))\n\n    st.markdown("**Approved status vocabulary**")\n    st.caption(\n        "Archive-grounded match · Source-bound description · Exploratory / unverified · "\n        "No archive match · Rights-limited display · Read-only archive evidence"\n    )\n\n    st.markdown(\n        f\'<div class="bdp-003f14-concept-lens-boundary">{BDP_003F14_CONCEPT_LENS_BOUNDARY_NOTE}</div>\',\n        unsafe_allow_html=True,\n    )\n    st.markdown(\'</div>\', unsafe_allow_html=True)\n\n\ntry:\n    _bdp_003f14_current_surface = (\n        get_dark_precursor_surface()\n        if "get_dark_precursor_surface" in globals()\n        else st.session_state.get("dark_precursor_surface", "stage")\n    )\nexcept Exception:\n    _bdp_003f14_current_surface = "stage"\n\nif str(_bdp_003f14_current_surface).lower() in {"stage", "concept_stage", "concept"}:\n    _bdp_003f14_render_concept_lens_read_only_evidence_posture_display()\n# BDP-003F.14 CONCEPT LENS READ-ONLY EVIDENCE POSTURE DISPLAY END\n'
HANDOVER_SECTION = '\n## BDP-003F.14 — Concept Lens Frontend Read-only Evidence Posture Wiring\n\n**Status:** Complete\n**Controlled slice:** frontend read-only evidence posture display only\n**Frontend target:** `frontend/dark_precursor.py`\n\nBDP-003F.14 wires the approved BDP-003F.13 Concept Lens UI integration contract into The Dark Precursor frontend as a conservative read-only evidence posture display.\n\nImplemented frontend surface:\n\n```text\nConcept Lens\nEvidence posture\nArchive evidence posture\nRead-only archive evidence posture\n```\n\nRequired service handoff used:\n\n```text\nread_concept_lens_archive_evidence_posture_via_existing_archive_bridge\n```\n\nControlled smoke cases only:\n\n```text\nBody without Organs\nwe repress because we repeat\nassemblage\n```\n\nBoundary note visible in frontend:\n\n```text\nThis panel displays read-only archive evidence posture. It does not create citations, claims, interpretations, concept relations, or database records.\n```\n\nBoundary:\n\n- no free-text concept search input\n- no backend route\n- no adapter endpoint\n- no SQL migration\n- no database mutation\n- no archive row creation\n- no source ingestion\n- no citation creation\n- no concept mention creation\n- no concept relation creation\n- no interpretation insertion\n- no evidence promotion\n- no Buchanan-specific claims\n- no external LLM routing\n- no unrestricted passage reproduction\n- no general chat filtering\n\nVerifier:\n\n```text\nscripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py\n```\n\nNext safe step:\n\n```text\nBDP-003F.15 — Review the Concept Lens read-only evidence posture display in the running frontend before expanding controls or concept coverage.\n```\n'

CONTROLLED_EXAMPLES = [
    "Body without Organs",
    "we repress because we repeat",
    "assemblage",
]


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _require_repo_root() -> None:
    required = [
        Path("docs/HOW_WE_WORK.md"),
        Path("docs/NEW_THREAD_ONBOARDING.md"),
        Path("docs/DOCS_UPDATE_POLICY.md"),
        FRONTEND_PATH,
        STATE_PATH,
        HANDOVER_PATH,
        Path("docs/BDP_003F13_CONCEPT_LENS_UI_INTEGRATION_CONTRACT.md"),
        Path("scripts/concept_lens_archive_evidence_posture_service.py"),
        Path("scripts/concept_lens_existing_archive_evidence_readback_bridge.py"),
        Path("scripts/verify_bdp_003f13_concept_lens_ui_integration_contract.py"),
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit(
            "BDP-003F.14 update must run from the repo root. Missing required files:\n- "
            + "\n- ".join(missing)
        )


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _replace_or_append_marker_block(path: Path, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if START in text and END in text:
        before = text.split(START, 1)[0].rstrip()
        after = text.split(END, 1)[1].lstrip()
        new_text = before + "\n\n" + block.strip() + "\n\n" + after
    else:
        new_text = text.rstrip() + "\n\n\n" + block.strip() + "\n"
    path.write_text(new_text, encoding="utf-8")


def _load_state() -> dict[str, Any]:
    with STATE_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit("BUCHANAN_SYSTEM_STATE.json must contain a JSON object.")
    return data


def _update_state() -> None:
    state = _load_state()
    completed_at = _now()
    phase_record = {
        "phase": PHASE,
        "title": "Wire the approved Concept Lens read-only evidence posture display into the frontend after contract verification",
        "status": "complete",
        "completed_at": completed_at,
        "controlled_slice": "frontend_read_only_evidence_posture_display_only",
        "implementation_type": "controlled_frontend_display_dock",
        "contract_source": "BDP-003F.13",
        "frontend_implementation": True,
        "frontend_target": "frontend/dark_precursor.py",
        "concept_lens_display_added": True,
        "concept_lens_ui_dock_added": True,
        "streamlit_display_added": True,
        "approved_service_handoff": "read_concept_lens_archive_evidence_posture_via_existing_archive_bridge",
        "controlled_concept_examples": CONTROLLED_EXAMPLES,
        "free_text_search_input_added": False,
        "backend_routes_added": False,
        "adapter_endpoints_added": False,
        "sql_migrations_added": False,
        "database_mutation": False,
        "database_writes_added": False,
        "archive_row_creation_added": False,
        "source_ingestion_added": False,
        "citation_creation_added": False,
        "concept_mention_creation_added": False,
        "concept_relation_creation_added": False,
        "interpretation_insertion_added": False,
        "evidence_promotion_added": False,
        "buchanan_claims_created": False,
        "external_llm_routing_added": False,
        "automatic_chat_filtering_added": False,
        "unrestricted_passage_reproduction_added": False,
        "rights_limited_display": True,
        "boundary_note": "This panel displays read-only archive evidence posture. It does not create citations, claims, interpretations, concept relations, or database records.",
        "preserved_archive_chain": ["concepts", "concept_mentions", "passages", "citations", "sources"],
        "documentation": str(DOC_PATH),
        "verifier": "scripts/verify_bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring.py",
        "next_step": NEXT_STEP,
    }

    phases = state.setdefault("phases", {})
    if not isinstance(phases, dict):
        raise SystemExit("BUCHANAN_SYSTEM_STATE.json field 'phases' must be an object.")
    phases[PHASE] = phase_record
    state["bdp_003f14_concept_lens_frontend_read_only_evidence_posture_wiring"] = phase_record
    state["last_updated_phase"] = PHASE
    state["last_updated_utc"] = completed_at
    state["current_phase"] = PHASE
    state["current_status"] = "complete"
    for key in (
        "next_recommended_step",
        "current_next_step",
        "next_step",
        "recommended_next_step",
        "next_safe_step",
    ):
        state[key] = NEXT_STEP

    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _update_handover() -> None:
    text = HANDOVER_PATH.read_text(encoding="utf-8")
    marker = "## BDP-003F.14 — Concept Lens Frontend Read-only Evidence Posture Wiring"
    if marker in text:
        return
    HANDOVER_PATH.write_text(text.rstrip() + "\n" + HANDOVER_SECTION, encoding="utf-8")


def main() -> None:
    _require_repo_root()
    _write_text(DOC_PATH, F14_DOC)
    _write_text(README_PATH, README)
    _replace_or_append_marker_block(FRONTEND_PATH, FRONTEND_BLOCK)
    _update_state()
    _update_handover()
    print("[OK] BDP-003F.14 patch applied locally")
    print("[OK] Updated frontend/dark_precursor.py with read-only Concept Lens evidence posture display")
    print("[OK] Updated BDP-003F.14 documentation, system state, and handover")


if __name__ == "__main__":
    main()
