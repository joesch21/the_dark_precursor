# BDP-003F.9 — Concept Lens Evidence Posture Output Review

**Status:** Complete  
**Controlled slice:** review-only evidence posture output review  
**Authority:** Review only; no frontend wiring, no database mutation, no evidence promotion  
**Review target:** `scripts/concept_lens_archive_evidence_posture_service.py`  
**Prior phase:** BDP-003F.8 — Concept Lens Archive Evidence Posture Service Implementation

## Purpose

BDP-003F.9 reviews the output posture of the BDP-003F.8 Concept Lens archive evidence posture service against known archive cases before any UI integration.

The review answers one narrow question:

```text
Can the Concept Lens truthfully say Body without Organs is archive-grounded today, or must that wait for a live SQL archive adapter phase?
```

## Review boundary

BDP-003F.9 is review-only.

It does not add, approve, or modify:

1. frontend wiring;
2. Concept Lens UI dock;
3. Streamlit controls;
4. new navigation surface keys;
5. backend routes;
6. adapter endpoints;
7. SQL migrations;
8. database tables;
9. database mutation;
10. citation creation;
11. concept mention creation;
12. concept relation creation;
13. interpretation insertion;
14. evidence promotion;
15. Buchanan-specific claims;
16. automatic chat filtering;
17. external LLM routing.

## F8 verifier status

BDP-003F.8 remains the current implemented service phase.

The F8 verifier is expected to remain part of the required verification chain:

```bash
python3 scripts/verify_bdp_003f8_concept_lens_archive_evidence_posture_service.py
```

BDP-003F.9 does not modify the F8 service or verifier.

## Smoke test cases reviewed

The review requires the following smoke cases to be re-run against the F8 service:

```bash
python3 scripts/concept_lens_archive_evidence_posture_service.py "Body without Organs"
python3 scripts/concept_lens_archive_evidence_posture_service.py "we repress because we repeat"
python3 scripts/concept_lens_archive_evidence_posture_service.py "assemblage"
```

Expected default no-live-archive posture:

```text
archive_lookup_status: no_archive_match
evidence_posture: exploratory_unverified
notes: No live archive adapter was configured
```

This output is safe because it does not fabricate archive support when no live archive adapter is configured.

## Known archive case reviewed

The known archive case is:

```text
Body without Organs
```

Project state records a governed evidence chain for Body without Organs from earlier phases:

```text
concepts -> concept_mentions -> passages -> citations -> sources
```

The prior governed path includes read-only evidence posture work around scripts such as:

```text
scripts/read_bdp_001r_bwo_source_bound_description.py
scripts/read_bdp_002b_bwo_evidence_card.py
```

Those earlier readback paths show that the project has governed Body without Organs archive evidence posture in project history. BDP-003F.9 does not create or promote any new evidence from that history.

## Finding

BDP-003F.9 records **Outcome C**:

```text
The archive evidence exists in governed project state, but no approved live readback adapter is currently exposed for the Concept Lens service default path.
```

This means two things can both be true:

1. Body without Organs has governed archive evidence posture in project state.
2. The F8 service is correct to return `no_archive_match` / `exploratory_unverified` when no live archive adapter is configured.

## Should Body without Organs currently be archive-grounded?

For the broader project archive state: **yes, Body without Organs is a known governed archive case**.

For the current F8 default service invocation without configured SQLite/PostgreSQL/readback bridge: **no, the service must not claim `archive_grounded`**.

The Concept Lens must not show `archive_grounded` in the UI until the live bridge into the approved read-only archive evidence chain is defined and verified.

## Is F8 intentionally non-live?

Yes. F8 is safe as a local read-only service shell and fixture-verified classifier. Its default CLI path is intentionally conservative when no live archive adapter is configured.

The F8 service may classify supplied rows or optional database-backed rows, but BDP-003F.9 does not approve a specific live SQL archive adapter path for the Concept Lens UI.

## Is a live SQL archive adapter contract needed next?

Yes.

Before UI integration, the project needs a bounded read-only bridge/adapter contract that defines how the Concept Lens service may safely read the existing archive evidence chain:

```text
concepts -> concept_mentions -> passages -> citations -> sources
```

That bridge must preserve rights boundaries, omit restricted passage text, return metadata and posture only, and avoid creating citations, mentions, relations, interpretations, evidence promotion, or Buchanan-specific claims.

## UI integration status

UI integration remains blocked.

The Concept Lens must not be wired into The Dark Precursor until the archive evidence posture service can truthfully distinguish:

1. known archive-grounded concepts such as Body without Organs;
2. source-bound but incomplete concepts;
3. system synthesis only;
4. exploratory unverified concepts.

## Exact next safe step

```text
BDP-003F.10 — Define approved read-only bridge from existing archive evidence readback into the Concept Lens service.
```

This should be a contract/bridge-definition phase before implementation. It should not add the UI dock yet.

## Verification chain

After applying this review patch, run:

```bash
python3 -m py_compile frontend/dark_precursor.py
python3 -m py_compile scripts/concept_lens_archive_evidence_posture_service.py
python3 scripts/verify_bdp_003f6_concept_lens_architecture.py
python3 scripts/verify_bdp_003f7_concept_lens_archive_evidence_posture_service_contract.py
python3 scripts/verify_bdp_003f8_concept_lens_archive_evidence_posture_service.py
python3 scripts/verify_bdp_003f9_concept_lens_evidence_posture_output_review.py
git diff --check
```
