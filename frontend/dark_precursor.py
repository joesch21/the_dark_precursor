import streamlit as st
import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

load_dotenv(dotenv_path=".env")

st.set_page_config(page_title="The Dark Precursor", layout="wide", initial_sidebar_state="expanded")

# === Cinematic + Sensual Minimalist Theme ===
st.markdown("""
<style>
    .stApp {
        background-color: #050505;
        color: #e8e8e8;
    }
    .cinematic-wall {
        background-color: #0a0a0a;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        padding: 60px 80px;
        margin: 25px 0;
        box-shadow: 0 0 70px rgba(0,0,0,0.55);
    }
    .narrator-text {
        font-family: 'Georgia', serif;
        font-size: 1.55rem;
        line-height: 1.9;
        color: #e8e8e8;
        letter-spacing: 0.2px;
    }
    .section-label {
        font-family: 'Georgia', serif;
        color: #d4af37;
        font-size: 1.1rem;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
    }
    .stButton > button {
        background-color: #1a1a1a;
        color: #d4af37;
        border: 1px solid #3a3a3a;
    }
    .stButton > button:hover {
        background-color: #d4af37;
        color: #050505;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# GOVERNED REFERENCES PANEL
# ============================================================
with st.expander("📚 Governed References — Methodological & Resource Documents", expanded=False):
    st.markdown("""
    **Purpose**: Human-curated reference material supporting differential reading, 
    rhizomatic cartography, and Vault resource integration.  
    **Governance**: All documents are read-only. Content must be reviewed by a human 
    operator before any application to analysis or interpretation.  
    **Label**: `governed_reference_only` — not evidence, not training data.
    """)

    reference_docs = [
        "docs/BUCHANAN_DIFFERENTIAL_METHOD_EXPLORATION.md",
        "docs/BUCHANAN_DELEUZIAN_CONCEPT_MAPPING_INVESTIGATION.md",
        "docs/BUCHANAN_VAULT_RESOURCES_INTEGRATION.md",
        "docs/BUCHANAN_VAULT_USABLE_ELEMENTS_ASSESSMENT.md",
        "docs/INTEGRATION_OF_METHODOLOGICAL_DOCS.md",
        "docs/LAYER_INTERACTION_WORKED_EXAMPLE.md",
    ]

    selected_doc = st.selectbox(
        "Select governed reference document",
        reference_docs,
        index=0,
        help="These are human-curated reference documents only. Human review required."
    )

    if selected_doc:
        doc_path = Path(selected_doc)
        if doc_path.exists():
            with open(doc_path, "r", encoding="utf-8") as f:
                content = f.read()
            st.markdown(content, unsafe_allow_html=False)
            st.caption(f"Source: {selected_doc} — governed_reference_only — human review required")
        else:
            st.warning(f"Document not found: {selected_doc}. Verify path or run from project root.")

# End of Governed References Panel

# === Rest of your original code continues here ===
# (the rest of your file remains unchanged)

# Sidebar
with st.sidebar:
    st.header("The Vault")
    st.caption("Reviewed passages & conceptual intensities")

    st.markdown("### Concepts")
    concepts = ["What's an assemblage?", "Content and Expression", "Territorialisation & Deterritorialisation", "Strata", "Lines of Flight"]
    for concept in concepts:
        if st.button(concept, key=concept):
            st.session_state.selected_concept = concept

    st.markdown("---")
    st.header("Settings")
    auto_voice = st.checkbox("Auto Voice Narration", value=True)

# === Main Cinematic Area ===
st.markdown('<p class="section-label">THE NARRATOR SPEAKS</p>', unsafe_allow_html=True)

default_query = st.session_state.get("selected_concept", "What's an assemblage")
query = st.text_input("What conceptual intensity calls to you?", value=default_query)

def generate_buchanan_response(concept: str) -> str:
    try:
        api_key = os.getenv("OPENAI_API_KEY_LLM")
        if not api_key:
            return "Error: OPENAI_API_KEY_LLM not found in .env file."

        client = OpenAI(api_key=api_key)

        system_prompt = """You are Ian Buchanan. You speak with precision, rigor, and a healthy skepticism toward reductive or fashionable readings of Deleuze and Guattari.

Core principles:
- Concepts are tools for analysis, not static objects.
- Resist simplification and flattening of complexity.
- Follow the movement of concepts (lines of flight, territorialisation/deterritorialisation, strata).
- Use concrete examples (such as the university) to illuminate ideas without replacing conceptual work.
- Maintain conceptual fidelity and nuance."""

        user_prompt = f"""Respond to this conceptual intensity. Use the university as a concrete site of analysis where helpful, but do not reduce the concept to the example.

Concept: {concept}

Your response:"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.35,
            max_tokens=720
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {e}"

if st.button("Invoke the Precursor", type="primary"):
    with st.spinner("The Narrator enters..."):
        time.sleep(0.8)

        full_response = generate_buchanan_response(query)

        wall = st.empty()
        displayed = ""
        for char in full_response:
            displayed += char
            wall.markdown(f'<div class="cinematic-wall"><div class="narrator-text">{displayed}</div></div>', unsafe_allow_html=True)
            time.sleep(0.026)

        st.caption("Grounded in The Vault • Experimental Intensity")

        if auto_voice:
            try:
                voice_key = os.getenv("OPENAI_API_KEY_VOICE")
                voice_model = os.getenv("VOICE_MODEL", "gpt-4o-mini-tts")
                client = OpenAI(api_key=voice_key)
                audio = client.audio.speech.create(model=voice_model, voice="onyx", input=full_response)
                st.audio(audio.content, format="audio/mp3", autoplay=True)
            except Exception as e:
                st.warning(f"Voice unavailable: {e}")

        st.markdown("---")
        st.markdown('<p class="section-label">THE NARRATOR ASKS</p>', unsafe_allow_html=True)
        st.info("If we were to take the university — or any institution you know well — as our site of analysis, what would content and expression look like on the different strata at play? Where do you sense lines of flight beginning to emerge?")

        user_reply = st.text_area("Your reply to the Narrator", height=100)

        if st.button("Send reply to the Narrator"):
            if user_reply.strip():
                st.markdown('<p class="section-label">THE NARRATOR REPLIES</p>', unsafe_allow_html=True)
                st.markdown("Your observation is precise. What you describe is a tension between strata — the administrative coding that seeks to capture and measure, versus those minoritarian spaces where thought still escapes. The question becomes: how do these lines of flight endure?")

# === Bottom Section ===
st.markdown("---")
st.markdown('<div style="background-color:#0a0a0a; padding:30px; border-radius:8px; border:1px solid #2a2a2a;">', unsafe_allow_html=True)
st.header("Voices from The Vault")
st.caption("Publicly available talks by Ian Buchanan")

st.markdown("""
**Machinic Unconscious Happy Hour – Ian Buchanan on Assemblage Theory (2024)**  
[Listen to the real Ian Buchanan](https://www.youtube.com/results?search_query=ian+buchanan+assemblage+theory+machinic+unconscious+happy+hour)
""")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<p class="section-label">EXPLORE FURTHER</p>', unsafe_allow_html=True)

cols = st.columns(5)
buttons = ["Content & Expression", "Lines of Flight", "Territorialisation", "Strata", "Assemblage"]

for i, label in enumerate(buttons):
    with cols[i]:
        if st.button(label, key=f"explore_{i}"):
            st.session_state.selected_concept = label
            st.rerun()

st.caption("The Dark Precursor • Phase 1 • Slower • More Sensual")
