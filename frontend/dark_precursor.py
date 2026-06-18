import base64
import hashlib
import html
import json
import os
import re
import time
from pathlib import Path
from datetime import datetime, timezone

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# BOOTSTRAP
# ============================================================

st.set_page_config(
    page_title="The Dark Precursor",
    page_icon="◼",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_ROOT = Path(__file__).resolve().parent

load_dotenv(dotenv_path=APP_ROOT / ".env")


def load_local_css(relative_path: str) -> None:
    """Load a local CSS file into Streamlit."""
    css_path = FRONTEND_ROOT / relative_path
    if css_path.exists():
        st.markdown(
            f"<style>\n{css_path.read_text(encoding='utf-8')}\n</style>",
            unsafe_allow_html=True,
        )
    else:
        st.warning(f"Stylesheet not found: {css_path}")


load_local_css("styles/dark_precursor.css")


SURFACE_STAGE = "stage"
SURFACE_ABOUT = "about"
APPROVED_DARK_PRECURSOR_SURFACES = {SURFACE_STAGE, SURFACE_ABOUT}


def get_dark_precursor_surface() -> str:
    surface = st.session_state.get("dark_precursor_view", SURFACE_STAGE)
    if surface not in APPROVED_DARK_PRECURSOR_SURFACES:
        return SURFACE_STAGE
    return surface


def set_dark_precursor_surface(surface_key: str) -> None:
    if surface_key not in APPROVED_DARK_PRECURSOR_SURFACES:
        raise ValueError(f"Unsupported Dark Precursor surface: {surface_key}")
    st.session_state["dark_precursor_view"] = surface_key


@st.cache_data(show_spinner=False)
def load_video_data_uri(relative_path: str) -> str:
    """Return a local frontend asset as a browser-safe video data URI."""
    video_path = FRONTEND_ROOT / relative_path
    if not video_path.exists():
        return ""

    encoded = base64.b64encode(video_path.read_bytes()).decode("ascii")
    return f"data:video/mp4;base64,{encoded}"


def render_background_stream() -> None:
    """Render the cinematic background stream behind the Streamlit controls."""
    video_src = load_video_data_uri("assets/dark_precursor.mp4")

    if not video_src:
        st.markdown('<div class="dp-background-fallback"></div>', unsafe_allow_html=True)
        return

    st.markdown(
        f"""
        <video class="dp-background-video" autoplay muted loop playsinline preload="metadata" aria-hidden="true">
            <source src="{video_src}" type="video/mp4">
        </video>
        <div class="dp-background-vignette"></div>
        """,
        unsafe_allow_html=True,
    )
    components.html(
    """
    <script>
    const tuneDarkPrecursorVideo = () => {
        const videos = window.parent.document.querySelectorAll("video.dp-background-video");
        videos.forEach((video) => {
            video.muted = true;
            video.defaultMuted = true;
            video.volume = 0;
            video.playbackRate = 0.42;
        });
    };

    tuneDarkPrecursorVideo();
    setInterval(tuneDarkPrecursorVideo, 1000);
    </script>
    """,
    height=0,
)


render_background_stream()



# ============================================================
# BDP-003E.2 — CINEMATIC CONCEPT CARD EXPORT DRAFTS
# ============================================================

CONCEPT_CARD_SCHEMA_VERSION = "bdp_003e2_cinematic_concept_card_export_draft_v1"
CONCEPT_CARD_AUTHORITY_LABEL = "provisional_cinematic_synthesis_not_evidence"
CONCEPT_CARD_STORAGE_POSTURE = "download_only_no_database_mutation"


def make_safe_export_slug(value: str) -> str:
    """Return a filesystem-friendly slug for local download filenames only."""
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned[:72] or "cinematic-concept-card"


def build_cinematic_concept_card_export(
    concept: str,
    mode: str,
    site: str,
    include_clip_brief: bool,
    response_markdown: str,
) -> dict:
    """Build a read-only/download-only cinematic concept card draft.

    This is not database persistence. It creates an operator-downloadable draft
    object in memory from the currently visible generated response.
    """
    concept_clean = (concept or "Untitled concept").strip()
    mode_clean = (mode or "Narrator").strip()
    site_clean = (site or "").strip()
    response_clean = (response_markdown or "").strip()
    created_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    digest_source = "|".join([concept_clean, mode_clean, site_clean, response_clean[:1200]])
    digest = hashlib.sha256(digest_source.encode("utf-8")).hexdigest()[:12]
    slug = make_safe_export_slug(concept_clean)

    return {
        "schema_version": CONCEPT_CARD_SCHEMA_VERSION,
        "card_id": f"concept-card-draft-{slug}-{digest}",
        "created_utc": created_utc,
        "authority_label": CONCEPT_CARD_AUTHORITY_LABEL,
        "storage_posture": CONCEPT_CARD_STORAGE_POSTURE,
        "review_status": "draft_unreviewed",
        "concept_query": concept_clean,
        "cinematic_mode": mode_clean,
        "site_context": site_clean,
        "includes_film_clip_brief": bool(include_clip_brief),
        "generated_material_is_evidence": False,
        "evidence_spine_mutation": False,
        "database_mutation": False,
        "adapter_invocation": False,
        "promotion_allowed": False,
        "response_markdown": response_clean,
        "required_human_review": [
            "confirm conceptual fidelity",
            "confirm evidence-backed claims remain distinguishable from synthesis",
            "confirm no generated claim is promoted to the evidence spine",
            "confirm any later image/video prompt remains labelled as provisional synthesis",
        ],
        "blocked_actions": [
            "database_persistence",
            "citation_creation",
            "concept_relation_creation",
            "buchanan_specific_claim_creation",
            "automatic_evidence_promotion",
            "image_or_video_adapter_invocation",
        ],
        "next_safe_action": "Human review only. Export may be downloaded as a local draft; it must not be treated as evidence.",
    }


def format_concept_card_markdown(card: dict) -> str:
    """Format a cinematic concept card draft as Markdown for local download."""
    lines = [
        f"# Cinematic Concept Card Draft — {card['concept_query']}",
        "",
        "## Governance",
        "",
        f"- Schema: `{card['schema_version']}`",
        f"- Card ID: `{card['card_id']}`",
        f"- Created UTC: `{card['created_utc']}`",
        f"- Authority label: `{card['authority_label']}`",
        f"- Storage posture: `{card['storage_posture']}`",
        "- Generated material is not evidence.",
        "- This draft does not mutate the evidence spine, citation layer, concept relation layer, or database.",
        "- Human review is required before any later use beyond local drafting.",
        "",
        "## Source Interaction",
        "",
        f"- Concept query: {card['concept_query']}",
        f"- Cinematic mode: {card['cinematic_mode']}",
        f"- Site/context: {card['site_context'] or 'Not specified'}",
        f"- Includes film/storyboard brief: {card['includes_film_clip_brief']}",
        "",
        "## Blocked Actions",
        "",
    ]
    lines.extend(f"- `{item}`" for item in card["blocked_actions"])
    lines.extend(["", "## Required Human Review", ""])
    lines.extend(f"- {item}" for item in card["required_human_review"])
    lines.extend([
        "",
        "## Generated Cinematic Draft",
        "",
        card["response_markdown"] or "_No response captured._",
        "",
        "---",
        "BDP-003E.2 read-only cinematic concept card export draft. Download-only. No database mutation.",
    ])
    return "\n".join(lines)


def render_cinematic_concept_card_export_dock(card: dict) -> None:
    """Render local download controls for a concept card draft."""
    markdown_data = format_concept_card_markdown(card)
    json_data = json.dumps(card, indent=2, ensure_ascii=False)
    file_base = card["card_id"]

    with st.expander("🗂 Cinematic concept card export draft", expanded=False):
        st.markdown(
            """
            **Status:** `draft_unreviewed`  
            **Authority:** `provisional_cinematic_synthesis_not_evidence`  
            **Storage:** local download only — no database mutation, no adapter call, no evidence promotion.
            """
        )
        st.caption("Generated material is not evidence. Human review is required before any later use.")
        st.code(card["card_id"], language="text")
        col_md, col_json = st.columns(2)
        with col_md:
            st.download_button(
                "Download concept card draft (.md)",
                data=markdown_data,
                file_name=f"{file_base}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with col_json:
            st.download_button(
                "Download concept card data (.json)",
                data=json_data,
                file_name=f"{file_base}.json",
                mime="application/json",
                use_container_width=True,
            )


# ============================================================
# OPTIONAL MODULES
# ============================================================

try:
    from differential_engine_panel import render_differential_engine_panel
except Exception:
    render_differential_engine_panel = None


# ============================================================
# CONTENT / PROMPT CONTRACT
# ============================================================

CONCEPT_PRESETS = [
    "Assemblage",
    "Body without Organs",
    "Content and Expression",
    "Territorialisation and Deterritorialisation",
    "Strata",
    "Lines of Flight",
    "Desire",
    "Affect",
    "War Machine",
    "Differential Method",
]

MODE_LABELS = {
    "Narrator": "A slow cinematic explanation with a clear differential trace.",
    "Cinematic Treatment": "A concept explained as a film scene, with visual atmosphere and analytic spine.",
    "Storyboard / Film Clip Brief": "A shot-by-shot brief that can later feed an image/video generation pipeline.",
}


def build_system_prompt(mode: str) -> str:
    """Return the governed cinematic system prompt for the selected mode."""
    return f"""You are The Dark Precursor, a governed cinematic guide to Deleuze, Guattari, and Ian Buchanan's conceptual field.

You are not Ian Buchanan and must not claim to be him.
Write in a Buchanan-informed voice: precise, skeptical of reductive readings, conceptually rigorous, and resistant to flattening assemblage theory into mere connectivity.

The experience must be cinematic, slow, clear, and readable. Use vivid but disciplined imagery. Avoid academic clutter.

Core method:
Do not merely define the concept.
Show how the concept operates.

Always try to trace:
1. the assemblage at work
2. the flow being organized
3. the cut, break, interruption, or subtraction
4. what is captured or extracted
5. what desire is being assembled
6. what affect or intensity is produced
7. what qualitative difference matters
8. what line of flight remains possible

Authority and governance:
- Distinguish evidence-backed claims from provisional cinematic synthesis.
- Do not invent a Buchanan-specific claim.
- Do not present generated synthesis as canonical scholarship.
- Prefer "the available frame suggests" over false certainty.
- If using a contemporary example, keep it as an analytic scene, not as proof.

Selected mode: {mode}
Mode purpose: {MODE_LABELS.get(mode, MODE_LABELS["Narrator"])}
"""


def build_user_prompt(concept: str, mode: str, site: str, include_clip_brief: bool) -> str:
    clip_instruction = ""
    if include_clip_brief or mode in {"Cinematic Treatment", "Storyboard / Film Clip Brief"}:
        clip_instruction = """
Include a section titled "Film Clip Brief" with:
- visual palette
- sound design
- 5 to 7 shot sequence
- one image/video generation prompt
- one sentence explaining what the viewer should understand conceptually
"""

    if mode == "Storyboard / Film Clip Brief":
        mode_instruction = """
Structure the response as:
1. Conceptual Core
2. Differential Trace
3. Storyboard
4. Film Clip Brief
5. Governance Note
"""
    elif mode == "Cinematic Treatment":
        mode_instruction = """
Structure the response as:
1. Opening Image
2. What the Concept Does
3. Differential Trace
4. Cinematic Treatment
5. Governance Note
"""
    else:
        mode_instruction = """
Structure the response as:
1. Narrator
2. Differential Trace
3. Why It Matters
4. Governance Note
"""

    return f"""Concept or question:
{concept}

Preferred site of analysis:
{site or "choose a concrete scene that makes the concept visible"}

{mode_instruction}

{clip_instruction}

Keep the language large, cinematic, and easy to read. Avoid long dense paragraphs. Use short sections and strong images, but preserve conceptual precision.
"""


def get_openai_client(api_key_env: str = "OPENAI_API_KEY_LLM") -> OpenAI | None:
    api_key = os.getenv(api_key_env)
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def generate_buchanan_response(
    concept: str,
    mode: str,
    site: str,
    include_clip_brief: bool,
) -> str:
    client = get_openai_client()
    if client is None:
        return (
            "OPENAI_API_KEY_LLM was not found in `.env`.\n\n"
            "The stage is ready, but the narrator cannot speak yet."
        )

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": build_system_prompt(mode)},
            {
                "role": "user",
                "content": build_user_prompt(
                    concept=concept,
                    mode=mode,
                    site=site,
                    include_clip_brief=include_clip_brief,
                ),
            },
        ],
        temperature=float(os.getenv("DARK_PRECURSOR_TEMPERATURE", "0.42")),
        max_tokens=int(os.getenv("DARK_PRECURSOR_MAX_TOKENS", "1100")),
    )
    return response.choices[0].message.content.strip()


def markdown_to_stage_html(markdown_text: str) -> str:
    """Render readable text safely inside the cinematic wall."""
    safe = html.escape(markdown_text)
    safe = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", safe)
    safe = safe.replace("\n", "<br>")
    return safe


# BDP-003F.1 — teleprompter narrator stage
def teleprompter_duration_seconds(text: str, seconds_per_chunk: float) -> float:
    """Estimate a readable teleprompter duration from response length and pacing.

    The sidebar still controls speed: higher values create a slower scroll.
    """
    word_count = max(1, len(text.split()))
    base_duration = word_count / 2.15
    pacing_bonus = max(0.0, seconds_per_chunk) * word_count * 1.85
    return min(360.0, max(36.0, base_duration + pacing_bonus))


def reveal_text(text: str, seconds_per_chunk: float) -> None:
    """Render the narrator as a full-screen upward scrolling teleprompter."""
    duration = teleprompter_duration_seconds(text, seconds_per_chunk)
    st.markdown(
        f"""
        <div class="dp-teleprompter-stage" style="--dp-teleprompter-duration: {duration:.2f}s;">
            <div class="dp-teleprompter-label">THE NARRATOR SPEAKS</div>
            <div class="dp-teleprompter-window">
                <div class="dp-teleprompter-track">
                    <div class="dp-teleprompter-text">{markdown_to_stage_html(text)}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def speak_response(full_response: str) -> None:
    voice_key = os.getenv("OPENAI_API_KEY_VOICE")
    if not voice_key:
        st.warning("Voice unavailable: OPENAI_API_KEY_VOICE not found in `.env`.")
        return

    try:
        voice_model = os.getenv("VOICE_MODEL", "gpt-4o-mini-tts")
        voice_name = os.getenv("VOICE_NAME", "onyx")
        client = OpenAI(api_key=voice_key)
        audio = client.audio.speech.create(
            model=voice_model,
            voice=voice_name,
            input=full_response,
        )
        st.audio(audio.content, format="audio/mp3", autoplay=True)
    except Exception as exc:
        st.warning(f"Voice unavailable: {exc}")


def render_governed_reference_dock() -> None:
    reference_docs = [
        "docs/BDP_003B_DARK_PRECURSOR.md",
        "docs/BDP_003C_CINEMATIC_EXPERIENCE_RESET.md",
        "docs/BDP_002G_DIFFERENTIAL_READING_ENGINE.md",
        "docs/BUCHANAN_SEMANTIC_WORKBENCH.md",
        "docs/BUCHANAN_PSYCHOLINGUISTIC_SEMANTIC_ARCHITECTURE.md",
        "docs/BUCHANAN_ARCHITECTURE.md",
        "docs/BUCHANAN_CITATION_AND_RIGHTS.md",
    ]

    with st.expander("📚 Governed method dock", expanded=False):
        st.markdown(
            """
            These documents are operator references. They are not automatically passed
            into the model and do not override the evidence spine.
            """
        )

        selected_doc = st.selectbox(
            "Open governed reference",
            reference_docs,
            index=0,
            help="Reference-only. Human review required before application.",
        )

        doc_path = APP_ROOT / selected_doc
        if doc_path.exists():
            st.markdown(doc_path.read_text(encoding="utf-8"), unsafe_allow_html=False)
            st.caption(f"{selected_doc} — governed_reference_only")
        else:
            st.warning(f"Document not found: {selected_doc}")


# ============================================================
# BDP-003F.2 — About page
# ============================================================


def render_about_page() -> None:
    '''Render the public-facing explanation of The Dark Precursor.'''
    st.markdown(
        '''
        <div class="dp-about-shell">
            <div class="dp-about-panel">
                <div class="dp-kicker">ABOUT THE DARK PRECURSOR</div>
                <div class="dp-about-title">A governed cinematic concept laboratory.</div>
                <div class="dp-about-lede">
                    The Dark Precursor is a cinematic research interface for working with
                    Deleuze, Guattari, and Ian Buchanan’s conceptual field. It stages concepts
                    as scenes while keeping generated synthesis clearly separate from evidence authority.
                </div>
                <div class="dp-about-pullquote">
                    It separates atmosphere from authority.
                </div>
                <div class="dp-about-grid">
                    <div class="dp-about-card">
                        <h3>What it is</h3>
                        <p>
                            A pedagogical and research workbench for slowing concepts down,
                            making their operations visible, and turning difficult conceptual
                            material into readable cinematic scenes, differential traces,
                            concept cards, and film prompts.
                        </p>
                    </div>
                    <div class="dp-about-card">
                        <h3>What it is not</h3>
                        <p>
                            It does not claim to think like Ian Buchanan, impersonate Ian Buchanan,
                            replace scholarship, or produce authoritative Deleuzian interpretation.
                        </p>
                    </div>
                    <div class="dp-about-card">
                        <h3>How it works</h3>
                        <p>
                            A user enters a concept or scene. The interface asks what is moving,
                            what is being cut, what is captured, what desire is assembled,
                            what affect is produced, and where a line of flight might remain possible.
                        </p>
                    </div>
                    <div class="dp-about-card">
                        <h3>Governance</h3>
                        <p>
                            Generated synthesis is not evidence. It does not become a Buchanan claim,
                            citation, concept relation, interpretation, or evidence record without
                            explicit review and governed promotion.
                        </p>
                    </div>
                </div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    cols = st.columns([1.2, 1, 1.2])
    with cols[1]:
        if st.button("Return to concept stage", type="primary", use_container_width=True):
            set_dark_precursor_surface(SURFACE_STAGE)
            st.rerun()



# ============================================================
# TITLE GATE
# ============================================================


def render_title_gate() -> None:
    """Render the opening title page before the operator enters the interface."""
    st.markdown(
        """
        <div class="dp-title-gate">
            <div class="dp-title-panel">
                <div class="dp-kicker">THE DARK PRECURSOR</div>
                <div class="dp-gate-title">A concept enters as a scene.</div>
                <div class="dp-gate-subtitle">
                    A cinematic front page for the Buchanan Vault: video as atmosphere,
                    large readable text as the main instrument, and governed synthesis
                    clearly separated from evidence authority.
                </div>
                <div class="dp-gate-note">
                    Press enter when the room is ready. The evidence spine remains untouched.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    gate_cols = st.columns([1.2, 1, 1.2])
    with gate_cols[1]:
        if st.button("Enter the Vault", type="primary", use_container_width=True):
            st.session_state["dark_precursor_gate_open"] = True
            st.rerun()


if not st.session_state.get("dark_precursor_gate_open", False):
    render_title_gate()
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## The Vault")
    st.caption("Cinematic conceptual exploration over a governed evidence spine.")

    mode = st.radio(
        "Experience mode",
        list(MODE_LABELS.keys()),
        index=0,
        help="Choose how the concept should be staged.",
    )

    st.markdown("---")
    st.markdown("### Pacing")
    reveal_speed = st.slider(
        "Text reveal speed",
        min_value=0.0,
        max_value=0.18,
        value=0.045,
        step=0.005,
        help="Higher is slower. Set to 0 for instant display.",
    )

    auto_voice = st.checkbox("Voice narration", value=False)
    include_clip_brief = st.checkbox("Include film / storyboard brief", value=True)

    st.markdown("---")
    selected_preset = st.selectbox("Concept preset", CONCEPT_PRESETS, index=0)
    if st.button("Use selected concept"):
        st.session_state["dark_precursor_query"] = selected_preset
        st.session_state["dark_precursor_query_input"] = selected_preset
        st.session_state.pop("last_dark_precursor_response", None)
        st.rerun()

    st.markdown("---")
    if st.button("Return to title page", use_container_width=True):
        st.session_state["dark_precursor_gate_open"] = False
        st.rerun()

    st.markdown("---")
    if st.button("About The Dark Precursor", use_container_width=True):
        set_dark_precursor_surface(SURFACE_ABOUT)
        st.rerun()

    st.caption("BDP-003D • cinematic video front page • provisional synthesis")


# BDP-003F.2 About page route
if get_dark_precursor_surface() == SURFACE_ABOUT:
    render_about_page()
    st.stop()


# ============================================================
# MAIN STAGE
# ============================================================

st.markdown(
    """
    <div class="dp-hero">
        <div class="dp-kicker">THE DARK PRECURSOR</div>
        <div class="dp-title">Concepts should move.</div>
        <div class="dp-subtitle">
            The background is not decoration. It is atmosphere: a moving field behind
            the question, the cut, the response, and the possible line of flight.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

default_query = st.session_state.get("dark_precursor_query", "What is an assemblage?")
concept_query = st.text_input(
    "What conceptual intensity should become visible?",
    value=default_query,
    key="dark_precursor_query_input",
)

site_of_analysis = st.text_input(
    "Optional concrete site",
    value="the university",
    help="Example: the university, Instagram feed, airport, family dinner, classroom, trading desk.",
)

cols = st.columns([1, 1, 1])
with cols[0]:
    invoke = st.button("Invoke the Precursor", type="primary", use_container_width=True)
with cols[1]:
    clear = st.button("Clear stage", use_container_width=True)
with cols[2]:
    save_ready = st.session_state.get("last_dark_precursor_response") is not None
    if save_ready:
        st.download_button(
            "Download cinematic brief",
            data=st.session_state["last_dark_precursor_response"],
            file_name="dark_precursor_cinematic_brief.md",
            mime="text/markdown",
            use_container_width=True,
        )
    else:
        st.button("Download cinematic brief", disabled=True, use_container_width=True)

if clear:
    st.session_state.pop("last_dark_precursor_response", None)
    st.rerun()

if invoke:
    with st.spinner("The room darkens. The concept begins to move..."):
        full_response = generate_buchanan_response(
            concept=concept_query,
            mode=mode,
            site=site_of_analysis,
            include_clip_brief=include_clip_brief,
        )
        st.session_state["last_dark_precursor_response"] = full_response

    if reveal_speed > 0:
        reveal_text(full_response, reveal_speed)
    else:
        st.markdown(
            f"""
            <div class="dp-stage">
                <div class="dp-section-label">THE NARRATOR SPEAKS</div>
                <div class="dp-narrator-text">{markdown_to_stage_html(full_response)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption("Generated cinematic synthesis • evidence spine not modified • human review required")

    if auto_voice:
        speak_response(full_response)

elif st.session_state.get("last_dark_precursor_response"):
    full_response = st.session_state["last_dark_precursor_response"]
    st.markdown(
        f"""
        <div class="dp-stage">
            <div class="dp-section-label">LAST INVOCATION</div>
            <div class="dp-narrator-text">{markdown_to_stage_html(full_response)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="dp-stage">
            <div class="dp-section-label">THE STAGE IS WAITING</div>
            <div class="dp-narrator-text">
                Choose a concept. Choose a scene. Then let the cut appear.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# EXPLORATION CARDS
# ============================================================

st.markdown(
    """
    <div class="dp-card-grid">
        <div class="dp-card">
            <div class="dp-card-title">1. Find the flow</div>
            <div class="dp-caption">What moves through the scene: desire, attention, bodies, images, money, language?</div>
        </div>
        <div class="dp-card">
            <div class="dp-card-title">2. Name the cut</div>
            <div class="dp-caption">What interruption, subtraction, threshold, filter, or capture makes the flow visible?</div>
        </div>
        <div class="dp-card">
            <div class="dp-card-title">3. Stage the image</div>
            <div class="dp-caption">Turn the concept into a scene without reducing it to a metaphor.</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


if st.session_state.get("last_dark_precursor_response"):
    concept_card_export_draft = build_cinematic_concept_card_export(
        concept=locals().get("query", st.session_state.get("dark_precursor_query_input", "Untitled concept")),
        mode=locals().get("mode", "Narrator"),
        site=locals().get("site", ""),
        include_clip_brief=locals().get("include_clip_brief", False),
        response_markdown=st.session_state.get("last_dark_precursor_response", ""),
    )
    render_cinematic_concept_card_export_dock(concept_card_export_draft)

with st.expander("🎬 What this cinematic mode can produce", expanded=False):
    st.markdown(
        """
        - large-font cinematic explanations
        - differential traces
        - concept-to-scene descriptions
        - storyboard sequences
        - film clip briefs
        - image/video generation prompts for a later adapter

        This phase does not generate video files directly. It prepares the governed
        cinematic brief that a later ComfyUI / Flux / video pipeline can consume.
        """
    )

render_governed_reference_dock()

if render_differential_engine_panel is not None:
    with st.expander("🜂 Differential engine tool", expanded=False):
        render_differential_engine_panel()

st.markdown(
    """
    <div class="dp-dock">
        <div class="dp-caption">
            The Dark Precursor • BDP-003C • cinematic reset • governed provisional synthesis.
            Evidence, citation, relation, and interpretation authority remain controlled by the Vault.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- BDP-003E.15 Local reviewed concept card archive controls wiring ---
try:
    from scripts.ui_reviewed_concept_card_archive_controls import render_bdp_003e15_archive_controls

    _bdp003e15_st = globals().get("st")
    if _bdp003e15_st is not None:
        render_bdp_003e15_archive_controls(_bdp003e15_st)
except Exception as _bdp003e15_archive_error:
    _bdp003e15_st = globals().get("st")
    if _bdp003e15_st is not None:
        _bdp003e15_st.caption(f"BDP-003E.15 archive controls unavailable: {_bdp003e15_archive_error}")
# --- end BDP-003E.15 archive controls wiring ---


# BDP-003F.14 CONCEPT LENS READ-ONLY EVIDENCE POSTURE DISPLAY START
BDP_003F14_CONCEPT_LENS_CONTROLLED_EXAMPLES = (
    "Body without Organs",
    "we repress because we repeat",
    "assemblage",
)

BDP_003F14_CONCEPT_LENS_BOUNDARY_NOTE = (
    "This panel displays read-only archive evidence posture. It does not create "
    "citations, claims, interpretations, concept relations, or database records."
)

BDP_003F14_CONCEPT_LENS_SERVICE_HANDOFF = (
    "read_concept_lens_archive_evidence_posture_via_existing_archive_bridge"
)


def _bdp_003f14_concept_lens_value(result, key, default=""):
    """Read a value from a dict-like or object-like Concept Lens result."""
    if isinstance(result, dict):
        return result.get(key, default)
    return getattr(result, key, default)


def _bdp_003f14_concept_lens_chain_summary(result):
    chain_summary = _bdp_003f14_concept_lens_value(result, "chain_completeness_summary")
    if chain_summary:
        return chain_summary

    chain_complete = _bdp_003f14_concept_lens_value(result, "chain_complete")
    if chain_complete is True:
        return "complete reviewed chain: concepts -> concept_mentions -> passages -> citations -> sources"
    if chain_complete is False:
        return "chain completeness not established"

    archive_chain = _bdp_003f14_concept_lens_value(result, "archive_chain")
    if archive_chain:
        if isinstance(archive_chain, (list, tuple)):
            return " -> ".join(str(part) for part in archive_chain)
        return str(archive_chain)

    return "concepts -> concept_mentions -> passages -> citations -> sources"


def _bdp_003f14_concept_lens_source_summary(result):
    source_title = _bdp_003f14_concept_lens_value(result, "source_title")
    source_author = _bdp_003f14_concept_lens_value(result, "source_author")
    source_year = _bdp_003f14_concept_lens_value(result, "source_year")
    source_doi = _bdp_003f14_concept_lens_value(result, "source_doi")
    source_locator = _bdp_003f14_concept_lens_value(result, "source_locator")
    locator = _bdp_003f14_concept_lens_value(result, "locator") or source_locator

    parts = []
    if source_author:
        parts.append(str(source_author))
    if source_title:
        parts.append(str(source_title))
    if source_year:
        parts.append(str(source_year))
    if source_doi:
        parts.append(f"DOI: {source_doi}")
    if locator:
        parts.append(f"Locator: {locator}")

    return " · ".join(parts) if parts else "No rights-safe source metadata returned for this controlled smoke case."


def _bdp_003f14_render_concept_lens_read_only_evidence_posture_display():
    """Render the BDP-003F.14 read-only Concept Lens evidence posture dock."""
    from pathlib import Path
    import sys

    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    try:
        from scripts.concept_lens_existing_archive_evidence_readback_bridge import (
            read_concept_lens_archive_evidence_posture_via_existing_archive_bridge,
        )
    except Exception as exc:
        st.markdown("### Concept Lens")
        st.caption("Read-only archive evidence posture")
        st.warning(f"Concept Lens read-only bridge is unavailable: {exc}")
        return

    st.markdown(
        """
        <style>
        .bdp-003f14-concept-lens-dock {
            border: 1px solid rgba(230, 211, 160, 0.24);
            border-radius: 22px;
            padding: 1.25rem 1.35rem;
            margin-top: 1.5rem;
            background: linear-gradient(135deg, rgba(12, 10, 8, 0.78), rgba(18, 24, 34, 0.70));
            box-shadow: 0 0 28px rgba(0, 0, 0, 0.28);
        }
        .bdp-003f14-concept-lens-kicker {
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: rgba(230, 211, 160, 0.78);
            font-size: 0.72rem;
            margin-bottom: 0.35rem;
        }
        .bdp-003f14-concept-lens-boundary {
            border-left: 3px solid rgba(230, 211, 160, 0.42);
            padding-left: 0.85rem;
            color: rgba(245, 237, 219, 0.84);
            font-size: 0.92rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="bdp-003f14-concept-lens-dock">', unsafe_allow_html=True)
    st.markdown('<div class="bdp-003f14-concept-lens-kicker">Read-only archive evidence posture</div>', unsafe_allow_html=True)
    st.markdown("### Concept Lens")
    st.caption("Evidence posture · Archive evidence posture · Rights-limited display")

    selected_concept = st.radio(
        "Controlled Concept Lens smoke case",
        BDP_003F14_CONCEPT_LENS_CONTROLLED_EXAMPLES,
        horizontal=True,
        key="bdp_003f14_concept_lens_controlled_smoke_case",
    )

    result = read_concept_lens_archive_evidence_posture_via_existing_archive_bridge(selected_concept)

    requested_label = _bdp_003f14_concept_lens_value(result, "requested_concept_label") or selected_concept
    normalized_label = (
        _bdp_003f14_concept_lens_value(result, "normalized_concept_label")
        or _bdp_003f14_concept_lens_value(result, "normalized_label")
        or "not returned"
    )
    archive_lookup_status = _bdp_003f14_concept_lens_value(result, "archive_lookup_status", "no_archive_match")
    evidence_posture = _bdp_003f14_concept_lens_value(result, "evidence_posture", "exploratory_unverified")
    passage_display_status = (
        _bdp_003f14_concept_lens_value(result, "passage_text_display")
        or _bdp_003f14_concept_lens_value(result, "passage_display_status")
        or "omitted_by_rights_policy"
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"**Requested concept**  \\n`{requested_label}`")
        st.markdown(f"**Normalized concept**  \\n`{normalized_label}`")
        st.markdown(f"**Archive lookup status**  \\n`{archive_lookup_status}`")
    with col_b:
        st.markdown(f"**Evidence posture**  \\n`{evidence_posture}`")
        st.markdown(f"**Passage display status**  \\n`{passage_display_status}`")
        st.markdown(f"**Service handoff**  \\n`{BDP_003F14_CONCEPT_LENS_SERVICE_HANDOFF}`")

    st.markdown("**Chain completeness summary**")
    st.caption(_bdp_003f14_concept_lens_chain_summary(result))

    st.markdown("**Rights-safe source / locator metadata**")
    st.caption(_bdp_003f14_concept_lens_source_summary(result))

    st.markdown("**Approved status vocabulary**")
    st.caption(
        "Archive-grounded match · Source-bound description · Exploratory / unverified · "
        "No archive match · Rights-limited display · Read-only archive evidence"
    )

    st.markdown(
        f'<div class="bdp-003f14-concept-lens-boundary">{BDP_003F14_CONCEPT_LENS_BOUNDARY_NOTE}</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)


try:
    _bdp_003f14_current_surface = (
        get_dark_precursor_surface()
        if "get_dark_precursor_surface" in globals()
        else st.session_state.get("dark_precursor_surface", "stage")
    )
except Exception:
    _bdp_003f14_current_surface = "stage"

if str(_bdp_003f14_current_surface).lower() in {"stage", "concept_stage", "concept"}:
    _bdp_003f14_render_concept_lens_read_only_evidence_posture_display()
# BDP-003F.14 CONCEPT LENS READ-ONLY EVIDENCE POSTURE DISPLAY END
