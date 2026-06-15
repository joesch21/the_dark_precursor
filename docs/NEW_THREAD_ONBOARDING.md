# New Thread Onboarding Guide

**Status:** Mandatory Reading  
**Applies to:** Anyone starting a new thread or joining the project

---

## Purpose

This document ensures that every new thread begins with the correct context, governance boundaries, and understanding of the current state of the Buchanan Deleuze Intelligence Platform.

---

## Mandatory Reading Order (Do This First)

Before doing any work, read the following documents **in this order**:

| Order | Document | Why It Matters | Time |
|-------|----------|----------------|------|
| 1     | `BUCHANAN_THREAD_HANDOVER.md` | Contains the **Pre-Thread Requirements** at the top + current phase history and boundaries | 5–10 min |
| 2     | `docs/DOCS_UPDATE_POLICY.md` | Mandatory rules for when and how documentation must be updated | 5 min |
| 3     | `docs/WORKFLOW_PATCH_APPLICATION.md` | Official and preferred way of working (patch bundles) | 5 min |
| 4     | `BUCHANAN_SYSTEM_STATE.json` | Current invariants, what is allowed/blocked, and phase status | 3–5 min |
| 5     | `docs/BDP_003B_DARK_PRECURSOR.md` | Current main interface (The Dark Precursor) — vision, features, and governance | 5–8 min |

---

## Key Things You Must Understand

Before starting work, you must know:

- **Patch bundles are the official and preferred method** of delivering changes.
- **Documentation updates are mandatory** when architecture or control surfaces change.
- All work must respect the current invariants in `BUCHANAN_SYSTEM_STATE.json`.
- The main user-facing interface right now is **The Dark Precursor** (cinematic generative interface).
- Responses should follow a governed “Buchanan voice” (precise, skeptical of reductive readings, conceptually faithful).

---

## How to Run The Dark Precursor

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs

# Activate environment
./activate_env.sh

# Run the interface
streamlit run frontend/dark_precursor.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`).

---

## Governance Reminders

- Never bypass the evidence spine.
- Never make Buchanan-specific claims without proper grounding.
- Always update documentation when making architectural or control surface changes.
- Work via patch bundles when possible.

---

## Questions?

If anything is unclear after reading the mandatory documents, ask before proceeding.

**Welcome to the project.**
---

## Start Here

**Before reading anything else**, new threads must read:

→ **`docs/HOW_WE_WORK.md`**

This document explains the mandatory patch workflow and how we operate.
