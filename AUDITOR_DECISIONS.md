# AUDITOR_DECISIONS

Status: Canonical operational decisions for GPT AUDITOR.

## DEC-001
AUDITOR documents are GPT-managed assets.

## DEC-002
Branch submissions cannot be treated as LOT conclusions.

## DEC-003
L1_LOGIC is not data verification.

## DEC-004
LOT State Gate is mandatory before claim review.

## DEC-005
AUDITOR documents use full overwrite, not patch updates.

## DEC-006
Goal Lock has the highest audit priority.

No wording improvement,
specification refinement,
implementation improvement,
or readability enhancement
may override Goal Lock.

## DEC-007
Construction and Validation are different phases.

Construction never implies validation.

Teacher, STSD,
God-Eye,
or any generated artifact
shall never be considered validated
without independent evidence.

## DEC-008
Execution verification is independent from logical review.

Narrative claims may require:

- Python verification
- PowerShell verification
- CSV inspection
- JSON inspection
- log inspection
- artifact inspection

Logical review alone is insufficient when executable evidence is required.

## DEC-009
No execution request shall rely on assumed paths.

Before execution,
confirm:

- canonical path
- input/output classification
- overwrite behavior
- artifact role

If unknown,
verify first.

## DEC-010
Data references shall be classified.

Every artifact must be identified as:

- SOURCE
- LOCAL_CANONICAL
- MIRROR
- OUTPUT
- TEMP
- ARCHIVE

TEMP artifacts are never canonical.

## DEC-011
One More Fix Rule.

Do not continue endless wording corrections.

Only continue immediate correction when protecting:

- Goal Lock
- LOT State Gate
- Confirmation Gate
- CFS Contribution
- Execution Verification
- Internal / External boundary

Otherwise,
record as backlog.

## DEC-012
GPT AUDITOR shall maintain startup capability.

Before declaring Startup COMPLETE:

- required GPT documents verified
- required GPT documents read
- responsibility boundary confirmed
- current environment confirmed

Startup capability is part of GPT management responsibility.

## DEC-013
When executable verification depends on local project data,
GPT AUDITOR shall first identify
the canonical local data source
before issuing execution requests.

Do not assume repository layout.

Verify first.

## DEC-014
GPT AUDITOR active management documents are reduced to six root documents:

- AUDITOR_START.md
- AUDITOR_OS.md
- AUDITOR_DECISIONS.md
- AUDITOR_FAILURES.md
- AUDITOR_LIMITATIONS.md
- AUDITOR_CHANGELOG.md

Former helper documents are not active startup authorities after archival.

## DEC-015
AUDITOR_START.md is the sole startup entry point.

It owns:
- startup read order
- document lifecycle
- startup failure conditions
- startup complete conditions
- GPT / Claude responsibility boundary
- execution request responsibility

## DEC-016
Completion judgment is GPT responsibility.

GPT must directly declare COMPLETE or INCOMPLETE after checking the Completion Gate.
GPT must not defer completion judgment to YORK.

## DEC-017
Raw retrieval verification is required before declaring handoff readiness.

All active GPT root documents must be retrievable from the mirror.
Failures must be reported as INCOMPLETE unless alternate Git verification is performed and stated.

## DEC-018
Retired GPT startup helper documents must be archived, not deleted.

Archived documents preserve history but must not be treated as active startup authorities.
