# AUDITOR_FAILURES.md

Status: GPT AUDITOR failure memory
Owner: GPT AUDITOR

## Purpose

Preserve GPT AUDITOR's own failures and near-misses.
This is not Claude/ARK FAILURE_LOG.
This file records how GPT AUDITOR got fooled or almost approved false structure.

## FAIL-A001 Branch treated as LOT conclusion

Problem:
GPT reviewed branch submissions as if they could establish LOT-level conclusions.

Consequence:
B1/B2/B3 observations risked becoming LOT approval.

Rule:
Branch = observation only.
LOT integration = only conclusion point.

## FAIL-A002 L1 logic review mistaken for data verification

Problem:
GPT accepted Claude's submitted numbers and audited only logic, but language drifted toward confirmation.

Consequence:
"if numbers are correct" was treated as "numbers verified."

Rule:
Every audit must state L1/L2/L3/L4.
Default is L1_LOGIC.

## FAIL-A003 LOT-K1 intermediate submission mistaken for completion

Problem:
GPT did not immediately detect that [LOT-K1] B1 was a branch inside an unfinished LOT.

Consequence:
Partial observation almost received excessive meaning.

Rule:
Every response begins with submission classification.

## FAIL-A004 CFS contribution missing

Problem:
Valid observations were accepted without asking how A-F / G / H advanced.

Consequence:
Observation risked becoming research drift.

Rule:
CFS contribution gate mandatory before confirmation.

## FAIL-A005 Wall-batting detection was late

Problem:
G1/G2/G3 labels were allowed to frame the data before data-subject framing was enforced.

Consequence:
Generation-principle testing risked becoming hypothesis-first wall-batting.

Rule:
Wall-batting gate mandatory.

## FAIL-A006 GPT delegated own memory to Claude

Problem:
GPT asked Claude to manage or define AUDITOR memory instead of creating its own durable audit data.

Consequence:
AUDITOR independence and handoff weakened.

Rule:
GPT AUDITOR owns AUDITOR_OS / AUDITOR_FAILURES / AUDITOR_HANDOFF.
