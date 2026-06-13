# Buchanan Citation and Rights Policy

## Purpose

This document defines citation and rights handling for the Buchanan Deleuze Intelligence Platform.

The system must remain scholarly, source-grounded, and rights-aware.

## Citation Rule

Every interpretive claim should be traceable to one of the following:

1. direct source passage.
2. cited secondary source.
3. generated synthesis with evidence references.
4. user-created interpretation.

## Source Types

```text
book
article
chapter
lecture
interview
video_transcript
conference_paper
teaching_note
user_note
```

## Rights Statuses

```text
unknown
public_url
licensed
user_provided
fair_use_reference_only
restricted
```

## Display Rules

The system should distinguish between:

1. stored text.
2. searchable text.
3. quotable text.
4. summarizable text.
5. reference-only metadata.

## Quotation Rule

Long source passages should not be exposed unless the user has rights or the material is explicitly permitted.

The preferred default is:

```text
short quotation + citation + paraphrase + source trail
```

## Authority Labels

Responses should label interpretive authority clearly:

```text
Buchanan direct
Deleuze and Guattari primary text
Secondary scholarship
System synthesis
User interpretation
```

## Generated Synthesis Boundary

Generated synthesis must not overwrite canonical sources.

Generated notes should be stored as:

```text
provisional synthesis
source-backed
needs review
```

## Citation Fields

Each passage should preserve:

```text
source title
author
year
page number or timestamp
chapter or section
URL or bibliographic reference
rights status
```

## Scholarly Integrity Rule

The platform should prefer uncertainty over false authority.

Use:

```text
The available source material suggests...
```

rather than:

```text
This definitively means...
```

## BDP-001J Exact Buchanan Source Rights Note

The exact Buchanan source specified for Body without Organs candidate review is:

```text
Ian Buchanan, "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?", Body & Society 3(3), September 1997, pp. 73-91. DOI: 10.1177/1357034X97003003004.
```

Rights and display boundary:

```text
rights_status_recommendation = restricted
display_rule = reference_only
```

BDP-001J records bibliographic metadata only.

No article passage is inserted.
No citation record is inserted.
No Buchanan interpretation is inserted.
No generated Buchanan claim is authorized.

## BDP-001K Uploaded PDF Rights Boundary

The operator has provided a PDF copy of the exact Buchanan article selected in BDP-001J.

Rights and use boundary:

```text
access_status = user_provided_pdf_available
rights_status_review = user_provided_pdf_reference_only_short_quotation_later
display_rule = metadata_reference_only_in_bdp_001k
```

BDP-001K permits metadata-readiness review only.

It does not authorize article reproduction, long quotation, passage insertion, citation insertion, or Buchanan interpretation.

## BDP-001L Canonical Metadata Adoption Rights Boundary

The reviewed Buchanan article metadata has been adopted into canonical `sources` only.

Canonical source:

```text
Ian Buchanan, "The Problem of the Body in Deleuze and Guattari, Or, What Can a Body Do?", Body & Society 3(3), September 1997, pp. 73-91. DOI: 10.1177/1357034X97003003004.
```

Rights and display treatment:

```text
rights_status = restricted
pdf_access_status = user_provided_pdf_available
display_rule = reference_only
source_text_available_for_review = true
```

BDP-001L authorizes canonical bibliographic metadata only.

It does not authorize article reproduction, long quotation, passage insertion, citation insertion, concept mention insertion, concept relation insertion, interpretation, synthesis, or a Buchanan-specific claim.

The uploaded PDF availability remains metadata for later controlled review and does not change the quotation boundary.

## BDP-001M Passage Candidate Rights Boundary

BDP-001M prepares a passage-candidate envelope from the adopted Buchanan article metadata only.

Rights and display treatment:

```text
rights_status = restricted
display_rule = reference_only
candidate_text_stored = false
long_quotation_stored = false
article_reproduction_authorized = false
```

BDP-001M does not authorize quotation display, article reproduction, citation insertion, interpretation, generated synthesis, or a Buchanan-specific claim.

A later phase must review any proposed short excerpt and locator before the system may insert a canonical passage or citation.
