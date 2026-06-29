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
