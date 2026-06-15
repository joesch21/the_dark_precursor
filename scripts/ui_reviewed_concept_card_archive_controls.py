#!/usr/bin/env python3
"""Streamlit controls for local reviewed concept card archive writing.

BDP-003E.15 scope:
- frontend controls only
- local reviewed payloads only
- explicit operator archive path
- no backend service
- no adapter endpoint
- no database table
- no SQL migration
- no evidence promotion
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.local_reviewed_concept_card_archive_writer import (
    INPUT_SCHEMA_VERSION,
    ArchiveWriterError,
    write_reviewed_concept_card_archive,
)


CONTROL_LABEL = "Local reviewed concept card archive"
CONFIRM_LABEL = "I confirm this card is locally reviewed and archiving will not promote evidence."
ARCHIVE_BUTTON_LABEL = "Archive locally reviewed card"


def _is_reviewed_archive_payload(value: Any) -> bool:
    """Return True when value looks like the reviewed archive payload expected by the writer."""

    if not isinstance(value, Mapping):
        return False
    governance = value.get("governance")
    if not isinstance(governance, Mapping):
        return False
    return (
        value.get("schema_version") == INPUT_SCHEMA_VERSION
        and value.get("review_status") == "locally_reviewed"
        and isinstance(value.get("archive_record_id"), str)
        and governance.get("evidence_promotion_approved") is False
        and governance.get("citations_created") is False
        and governance.get("concept_relations_created") is False
        and governance.get("interpretations_created") is False
        and governance.get("buchanan_claims_created") is False
    )


def _walk_for_reviewed_payload(value: Any, *, depth: int = 0, max_depth: int = 5) -> dict[str, Any] | None:
    """Find the first reviewed archive payload inside nested session-state values."""

    if depth > max_depth:
        return None

    if _is_reviewed_archive_payload(value):
        return dict(value)

    if isinstance(value, Mapping):
        for item in value.values():
            found = _walk_for_reviewed_payload(item, depth=depth + 1, max_depth=max_depth)
            if found is not None:
                return found

    if isinstance(value, list | tuple):
        for item in value:
            found = _walk_for_reviewed_payload(item, depth=depth + 1, max_depth=max_depth)
            if found is not None:
                return found

    return None


def find_reviewed_archive_payload(session_state: Any) -> dict[str, Any] | None:
    """Find a local reviewed concept card archive payload from Streamlit session state."""

    if hasattr(session_state, "to_dict"):
        try:
            session_state = session_state.to_dict()
        except Exception:
            session_state = dict(session_state)

    return _walk_for_reviewed_payload(session_state)


def _payload_preview(payload: Mapping[str, Any]) -> dict[str, Any]:
    concept = payload.get("concept") if isinstance(payload.get("concept"), Mapping) else {}
    card = payload.get("card") if isinstance(payload.get("card"), Mapping) else {}
    return {
        "archive_record_id": payload.get("archive_record_id"),
        "review_status": payload.get("review_status"),
        "concept_id": concept.get("concept_id"),
        "concept_label": concept.get("label"),
        "card_title": card.get("title"),
        "evidence_promotion_approved": False,
    }


def render_bdp_003e15_archive_controls(st: Any, session_state: Any | None = None) -> None:
    """Render the BDP-003E.15 archive controls inside The Dark Precursor UI."""

    if session_state is None:
        session_state = st.session_state

    with st.expander(f"{CONTROL_LABEL} · BDP-003E.15", expanded=False):
        st.caption(
            "Local archive only. This does not promote evidence, create citations, "
            "create concept relations, create interpretations, or create Buchanan-specific claims."
        )

        payload = find_reviewed_archive_payload(session_state)
        if payload is None:
            st.info("No locally reviewed concept card payload is currently available for archive.")
            return

        st.caption("Reviewed archive payload detected.")
        st.json(_payload_preview(payload), expanded=False)

        archive_root = st.text_input(
            "Explicit local archive folder path",
            value="",
            key="bdp_003e15_archive_root",
            help="Required. No archive folder is created until you press the archive button.",
        )

        confirmed = st.checkbox(
            CONFIRM_LABEL,
            value=False,
            key="bdp_003e15_archive_confirmed",
        )

        disabled = not archive_root.strip() or not confirmed
        if st.button(ARCHIVE_BUTTON_LABEL, key="bdp_003e15_archive_button", disabled=disabled):
            try:
                result = write_reviewed_concept_card_archive(payload, archive_root.strip(), create_root=True)
            except ArchiveWriterError as exc:
                st.error(f"Archive rejected by safety gates: {exc}")
                return
            except Exception as exc:  # pragma: no cover - UI safety net
                st.error(f"Archive failed: {exc}")
                return

            if result.get("idempotent"):
                st.success("Archive already exists and matches the reviewed payload.")
            else:
                st.success("Local reviewed concept card archived.")

            st.code(result.get("path", ""), language="text")
