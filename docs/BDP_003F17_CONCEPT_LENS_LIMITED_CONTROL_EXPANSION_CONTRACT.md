# BDP-003F.17 — Concept Lens Limited Control Expansion Contract

**Phase:** BDP-003F.17  
**Title:** Define Concept Lens limited control expansion contract after F16 readiness decision  
**Controlled slice:** limited-control contract only  
**Status:** complete  

## 1. Purpose

BDP-003F.17 defines the first bounded control expansion contract for the Concept Lens after the BDP-003F.16 readiness decision.

This phase is a contract phase only. It does not implement controls.

The purpose is to define which later user-interface controls may be considered safe for a subsequent implementation phase while preserving the read-only evidence posture boundary established by BDP-003F.14, reviewed by BDP-003F.15, and approved for bounded contract expansion by BDP-003F.16.

## 2. Input authority

The input to this contract is:

```text
BDP-003F.16 — Decide Concept Lens control and concept coverage expansion readiness after running frontend review.
```

BDP-003F.16 selected:

```text
Outcome C — Ready for both separate later contract tracks, but implementation remains blocked.
```

BDP-003F.17 handles only the first of those tracks:

```text
limited control expansion contract
```

It does not handle concept coverage expansion.

## 3. Contract-only boundary

BDP-003F.17 records a contract only.

No frontend changes were made.
No service changes were made.
No bridge changes were made.
No new frontend controls were added.
No concept examples were added.
No free-text search was added.
No database write path was added.
No citation, claim, interpretation, concept relation, concept mention, or archive record creation path was added.
No external LLM routing was added.
No unrestricted passage reproduction was added.

The read-only evidence posture boundary remains intact.

## 4. Existing controlled examples remain unchanged

The existing controlled examples remain the only examples in scope:

```text
Body without Organs
we repress because we repeat
assemblage
```

BDP-003F.17 does not add new examples and does not authorize later concept coverage expansion. Concept coverage expansion requires a separate contract phase.

## 5. Allowed later controls under this contract

A later implementation phase may implement only the following limited, read-only controls, and only if the implementation remains inside the existing Concept Lens display boundary.

### 5.1 Controlled preset selector

A later implementation may expose a selector for the existing controlled examples only:

```text
Body without Organs
we repress because we repeat
assemblage
```

The selector must not accept new options.
The selector must not provide free-text concept search.
The selector must not create concept examples.
The selector must not query unrestricted source text.
The selector must not create database records.

### 5.2 Display density control

A later implementation may expose a display-density control such as:

```text
compact
standard
detailed
```

This control may only change how already-returned read-only evidence posture data is displayed.
It must not change evidence authority, create interpretation, or trigger new backend behaviour.

### 5.3 Evidence detail expander

A later implementation may expose read-only expanders for already-returned metadata such as:

```text
evidence posture label
rights display rule
authority label
source spine summary
controlled concept example status
```

This control must not expose unrestricted passage text and must preserve `omitted_by_rights_policy` where rights require it.

### 5.4 Rights boundary explainer

A later implementation may expose a read-only explanatory toggle for the rights and evidence boundary.

It may explain why passage text is omitted, why evidence posture is not interpretation, and why read-only posture does not authorize Buchanan-specific claims.

### 5.5 Reset to default Concept Lens view

A later implementation may expose a reset control that returns the Concept Lens to the default read-only evidence posture view.

The reset control must not clear database records, session records, archive records, or evidence records because no such records may be created by these controls.

## 6. Explicitly blocked controls

The following remain blocked:

```text
free-text concept search input
new concept search box
new concept examples
accept-new-options selector behaviour
create / save / promote / cite / interpret controls
citation creation controls
claim creation controls
interpretation insertion controls
concept mention creation controls
concept relation creation controls
source ingestion controls
archive row creation controls
database write controls
backend route controls
adapter endpoint controls
external LLM routing controls
general chat filtering controls
unrestricted passage reproduction controls
Buchanan-specific interpretive claim generation controls
```

## 7. Later implementation acceptance criteria

A later control implementation phase must prove all of the following before it can be marked complete:

```text
The implementation touches only the approved frontend Concept Lens block.
The implementation uses only the existing read-only service handoff.
The implementation does not modify the Concept Lens evidence posture service.
The implementation does not modify the existing archive readback bridge.
The implementation does not add a backend route.
The implementation does not add an adapter endpoint.
The implementation does not add SQL migration or database writes.
The implementation does not add free-text concept search.
The implementation does not add concept examples.
The implementation does not create citations, claims, interpretations, concept mentions, concept relations, archive rows, passages, or sources.
The implementation preserves rights-limited display behaviour.
The implementation preserves the read-only evidence posture boundary note.
```

## 8. Concept coverage remains separate

Concept coverage expansion is not authorized by BDP-003F.17.

A separate later contract must define any controlled concept coverage expansion before any new concept examples are added.

## 9. Decision

BDP-003F.17 decides that limited read-only controls may proceed to a later implementation contract or implementation phase only under the boundaries recorded here.

Implementation remains blocked in BDP-003F.17.

## 10. Next safe step

The next safe step is:

```text
BDP-003F.18 — Define Concept Lens controlled concept coverage expansion contract after F17 control boundary.
```

This next step must remain contract-only unless explicitly re-scoped by the operator.
