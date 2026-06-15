# BDP-003B — The Dark Precursor (Cinematic Generative Interface)

**Status:** Active Development
**Phase:** BDP-003B
**Date:** June 2026
**Related:** BDP-003A, BDP-002D.2, BUCHANAN_PSYCHOLINGUISTIC_MODELLING_BLUEPRINT.md

## 1. Purpose

BDP-003B introduces **The Dark Precursor**, a cinematic, relational, and Buchanan-informed cinematic generative interface built on top of the existing governed evidence spine.

This phase moves beyond simple retrieval chat into an immersive conceptual experience that embodies Deleuze & Guattari’s spirit of experimentation and intensity, while remaining strictly governed.

## 2. Core Vision

The Dark Precursor is designed as:

- A **cinematic intensity machine** rather than a conventional chatbot
- A space where concepts are encountered with depth, movement, and nuance
- A relational environment where the user can engage in conceptual dialogue
- A governed surface that respects the evidence spine and a Buchanan-informed governed analytic style

## 3. Key Features (Current)

| Feature                        | Description                                      | Status    |
|--------------------------------|--------------------------------------------------|-----------|
| Cinematic Wall Presentation    | Narrator text appears inside a dark, elegant container | Active    |
| Typewriter Effect              | Text appears gradually, like being written       | Active    |
| Optional Voice Narration       | Uses configured TTS voice when enabled             | Active    |
| Dynamic LLM Responses          | Uses configured text model + governed Buchanan-informed prompt  | Active    |
| Relational Questioning         | Narrator asks follow-up questions after responses| Active    |
| Clickable Concept Exploration  | Sidebar + bottom buttons trigger new responses   | Active    |
| Settings Panel                 | Toggle for auto voice narration                  | Active    |

## 4. Design Philosophy

- **Minimalist + Atmospheric**: Clean, dark, high-end aesthetic (Apple-like restraint with philosophical depth)
- **Sensual & Contemplative**: Larger, elegant typography with slower, human-like pacing
- **Relational**: Not one-way explanation, but conceptual dialogue
- **Governed**: Responses are shaped by a governed Buchanan-informed system prompt aligned with project documentation

## 5. Governance Boundaries

- All responses are generated through a strengthened system prompt designed to remain Buchanan-informed without claiming to be Ian Buchanan.
- The interface does **not** yet perform strict retrieval-augmented generation from the SQL database.
- Voice synthesis uses a separate API key (`OPENAI_API_KEY_VOICE`) when voice narration is enabled.
- Text generation uses `OPENAI_API_KEY_LLM` and the configured text model.

## 6. Current Limitations

- Responses are still primarily generative rather than strictly passage-linked.
- No direct connection to the canonical `passages` or `concept_mentions` tables yet.
- Voice autoplay can be blocked by browser policies.

## 7. Next Recommended Steps

1. Strengthen retrieval grounding (connect to SQL database).
2. Add local LLM option (Gemma / Qwen) as alternative to OpenAI.
3. Introduce simple visual generation (ComfyUI + Flux) for cinematic concept imagery.
4. Expand relational depth (multi-turn conceptual dialogue).

## 8. Files Created / Modified

- `frontend/dark_precursor.py` — Main cinematic interface
- `docs/BDP_003B_DARK_PRECURSOR.md` — This document
- `BUCHANAN_THREAD_HANDOVER.md` — Updated with BDP-003B
- `BUCHANAN_SYSTEM_STATE.json` — Updated with new phase

**End of Document**
