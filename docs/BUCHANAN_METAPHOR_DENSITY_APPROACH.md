# Buchanan Metaphor Density Approach

**Status:** Reference Document  
**Version:** 1.0  
**Date:** June 2026  
**Related:** `BUCHANAN_PSYCHOLINGUISTIC_MODELLING_BLUEPRINT.md`

---

## 1. Purpose

This document defines how the platform will approach the modelling of **metaphor density** as the first psycho-linguistic dimension.

The objective is to identify passages where metaphorical and figurative language is particularly active or dense, as these moments often coincide with conceptual intensity and movement in Deleuze, Guattari, and Buchanan’s writing.

---

## 2. Definition of Metaphor Density (in this Context)

Metaphor density refers to the concentration and activity of non-literal language in a passage. It includes:

- Conventional and novel metaphors
- Sustained metaphorical mappings
- Blurring between literal and figurative usage
- Metaphorical transformation across sentences or paragraphs

**Important distinction**: We are not primarily counting individual metaphors. We are interested in **zones of heightened metaphorical activity** that may reward closer human attention.

---

## 3. Five-Level Progression

The platform will approach metaphor density modelling through five increasing levels of sophistication:

| Level | Name | Description | Status | Governance |
|-------|------|-------------|--------|------------|
| **Level 1** | Lexical Pattern Matching | Flag passages containing known metaphorical source domains (body, machine, flow, territory, etc.) | Future | Low |
| **Level 2** | Embedding Deviation Detection | Identify passages that deviate semantically from more literal/explanatory baseline language | **Current focus** | Medium |
| **Level 3** | Structured Metaphor Identification | Apply systematic metaphor identification (inspired by MIP/MIPVU) with human review | Planned | High |
| **Level 4** | Metaphorical Mapping Networks | Track source → target domain mappings and their evolution | Future | Very High |
| **Level 5** | Psycho-Linguistic + Affective Integration | Combine metaphor density with rhythm, intensity, and reader-effect signals | Future | Very High |

This document focuses primarily on **Level 2**, with awareness of the longer progression.

---

## 4. Level 2: Embedding Deviation Detection (Current Approach)

### 4.1 Core Idea

Compare each passage against a baseline of relatively literal or explanatory language from the same author or corpus. Passages that show significant semantic deviation are flagged as potentially higher in metaphorical density.

### 4.2 Implementation Outline

1. **Define a baseline**
   - Select or curate a set of passages considered more literal/explanatory.
   - Generate embeddings for these baseline passages.
   - Compute a baseline centroid (mean embedding) or distribution.

2. **Embed all target passages**
   - Generate sentence or paragraph embeddings for passages under analysis.

3. **Measure deviation**
   - Calculate cosine distance (or another suitable metric) between each passage embedding and the baseline.
   - Optionally apply statistical methods (e.g., z-score, Mahalanobis distance) for more robust flagging.

4. **Flag and report**
   - Rank passages by deviation score.
   - Present high-deviation passages to the operator with:
     - Original text / locator
     - Deviation score
     - Comparison context
     - Clear experimental label

### 4.3 Governance Requirements for Level 2

- All outputs must be labelled **Experimental – Level 2 Embedding Deviation**.
- The baseline selection process must be documented and reviewable.
- No passage should be automatically promoted or linked to concepts based solely on deviation score.
- Human review is required before any observation influences interpretation or further analysis.
- The module must remain isolated from core Evidence Cards until explicitly approved.

### 4.4 Known Limitations (Level 2)

- Embedding models may struggle with highly abstract philosophical language.
- Deviation can result from technical terminology, not just metaphor.
- Context window limitations may miss longer metaphorical developments.
- Scores are indicative only and should not be treated as objective measures of “metaphoricity.”

---

## 5. Output Labelling Standard

Every Level 2 output must include:

```text
[Experimental Modelling Observation – Level 2]
Method: Embedding Deviation Detection
Baseline: [Description of baseline used]
Review Status: Requires human review
Limitations: May flag technical language as well as metaphorical language.
Evidence Link: [Passage ID(s) or locator]
```

---

## 6. Integration Path

Level 2 metaphor density observations should eventually be able to:

- Surface interesting passages for the operator during concept exploration
- Be attached as optional annotations to existing passages (never replacing canonical records)
- Feed into higher-level modelling (Level 3+)

However, integration into operator-facing surfaces (such as the Evidence Card) must follow a formal review and approval process defined in the Psycho-Linguistic Modelling Blueprint.

---

## 7. Risks and Safeguards

| Risk | Safeguard |
|------|-----------|
| Over-interpretation of scores | Strong labelling + human review gate |
| Confusion between technical and metaphorical language | Documented baseline + operator training |
| Scope creep into interpretation | Strict separation from canonical evidence |
| Poor reproducibility | Use of documented models and baseline selection process |

---

## 8. Next Steps (June 2026)

1. Finalise baseline selection approach for the existing Buchanan 1997 passages.
2. Implement a standalone experimental script for Level 2.
3. Test on the current small corpus and review results manually.
4. Refine governance rules based on initial findings.
5. Document lessons before considering Level 3.

---

**End of Document**