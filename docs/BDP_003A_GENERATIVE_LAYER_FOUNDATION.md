# BDP-003A — Generative Layer Foundation

**Status:** Active Direction  
**Phase Type:** Generative Layer Development  
**Date:** 14 June 2026  
**Related:** BDP-002F, BDP-002D.2, BUCHANAN_SEMANTIC_WORKBENCH.md, BUCHANAN_PSYCHOLINGUISTIC_SEMANTIC_ARCHITECTURE.md

## 1. Purpose

BDP-003A establishes the foundation for a **Buchanan-voiced generative layer** on top of the existing governed evidence spine.

The goal is to move beyond purely read-only evidence cards toward a more interactive, query-responsive system that can answer questions in Ian Buchanan’s analytical style while remaining grounded in reviewed source material.

This layer is **experimental but governed**. It must not bypass the evidence requirements established in earlier BDP phases.

## 2. Core Principle

The generative layer must operate under this rule:

> **Retrieval before generation.**  
> Every response should be grounded in reviewed Buchanan passages wherever possible. The system should retrieve first, then synthesize.

This protects the platform from drifting into generic academic prose or ungrounded interpretation.

## 3. Current Components (as of 14 June 2026)

| Component | File | Status | Purpose |
|---------|------|--------|--------|
| Interactive Chat Interface | `scripts/chat_buchanan.py` | Working | Allows natural language questions |
| Prompt Template (v2) | `prompts/buchanan_synthesis_prompt_v2.txt` | Active | Defines Buchanan-style tone and rules |
| Retrieval Engine | `scripts/retrieve_buchanan_passages.py` | Improved (keyword-based) | Searches `BDP_002F_KEY_PASSAGES_REVIEWED.md` |
| Prompt Constructor | `scripts/construct_buchanan_prompt.py` | Updated | Builds final prompt with context |
| Passage Catalogue | `docs/BDP_002F_KEY_PASSAGES_REVIEWED.md` | 7 passages | Core grounding material from *Assemblage Theory and Method* |

## 4. Governance Boundaries

The generative layer must respect the following non-negotiable boundaries:

- **No bypassing of evidence requirements** — Responses should prefer reviewed passages over general knowledge.
- **Clear authority labeling** — The system must be able to indicate when it is synthesizing vs staying close to source material.
- **Session-scoped adaptation only** — Any future adaptive behaviour must follow the BDP-002D.2 UX contract (Inspect / Pause / Reset / Override + Explanatory Layer).
- **No long-term user profiling** without explicit consent.
- **Buchanan-specific claims** must remain traceable to reviewed passages.

## 5. Current Limitations (to be addressed)

- Retrieval is currently keyword-based only (no embeddings/semantic search yet).
- The system sometimes produces plausible but loosely grounded responses.
- Terminology can still drift from Buchanan’s precise usage (Content/Expression, Territorialisation/Deterritorialisation, etc.).
- No automatic citation or source display in responses yet.

## 6. Recommended Development Priorities

| Priority | Task | Rationale |
|---------|------|---------|
| 1 | Improve retrieval quality (better parsing + scoring of `BDP_002F_KEY_PASSAGES_REVIEWED.md`) | Most important for grounding |
| 2 | Add automatic source display in chat responses | Transparency |
| 3 | Refine Prompt v2 further based on real outputs | Better Buchanan voice |
| 4 | Add support for multiple passage catalogues (not just BDP-002F) | Scalability |
| 5 | Create evaluation set of test questions | Measure progress objectively |

## 7. Relationship to Existing Doctrine

This layer sits **on top of** the existing evidence spine rather than replacing it.

- It should be able to fall back to the richer semantic readback surfaces (BDP-002C style) when appropriate.
- It must respect the distinction between **text psycho-linguistics** and **interaction adaptation** (BDP-002D.1 / 002D.2).
- It must not generate Buchanan-specific claims without reviewed passage support.

## 8. Success Criteria for BDP-003A

BDP-003A will be considered successful when:

- The chat interface can reliably retrieve and use passages from `BDP_002F_KEY_PASSAGES_REVIEWED.md`.
- Responses show visible improvement in grounding and Buchanan-like precision compared to generic academic output.
- The system maintains clear boundaries around what it can and cannot claim.
- Future development has a clear, documented foundation to build upon.

## 9. Next Recommended Actions

1. Continue improving `retrieve_buchanan_passages.py` (better parsing and relevance scoring).
2. Update `chat_buchanan.py` to automatically use the improved retriever.
3. Test with a wider set of questions (especially around *Assemblage*, *Strata*, and *Abstract Machine*).
4. Decide whether to expand the passage catalogue beyond the current 7 entries.

**End of Document**