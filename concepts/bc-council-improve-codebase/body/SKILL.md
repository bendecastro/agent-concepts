---
name: bc-council-improve-codebase
description: "Run improve-codebase-architecture through the advisor council: one scout maps the codebase, every available council advisor proposes and cross-examines deep-module candidates, and candidates are ranked by evidence-backed agreement before the normal report and grilling. Use when the user says bc-council-improve-codebase, council architecture review, or asks the council to review the codebase architecture."
---

# Council architecture review

This skill joins three skills and copies none. Load all three before starting:

- `council-chain`: the council steps every chain shares (roster, shared map, pass 1, merge, pass 2, fallbacks, cleanup) and the parts a chain must define.
- `improve-codebase-architecture`: inputs to read, candidate card fields, the visual report, grilling, and where chosen, rejected and remaining items are filed.
- `council-mode`: how to brief, launch, relay to and resume advisors, and the pass cap.

Run the `council-chain` steps in order. This file defines only the parts that recipe leaves to the chain. Where this file is silent, those three skills decide.

## Pre-reading and map

Pre-reading: the first step of `improve-codebase-architecture`: read the glossary, decision records and architecture lines in the ideas file.

Map contents: modules, their interfaces, seams, call fan-in and fan-out, and places where one change touches many files.

Brief extras: the glossary and decision-record paths, and recorded rejections not to re-propose. No focuses or stances are dealt.

## Candidate format

Return each candidate as:

```
Candidate: <short name>
Module / seam: <names from the map>
Problem: <one or two sentences>
Direction: <recommended change>
Evidence: <file:line for every claim>
Strength: Strong | Worth exploring | Speculative
```

Duplicate rule: candidates that name the same module and seam with the same direction are one; a different direction is a disagreement.

## Agreement rule

Rank candidates by evidence, not by vote alone:

- **Strong:** more than half of N rate it Strong, and no advisor holds an unanswered evidence-backed dispute.
- **Worth exploring:** more than half of N confirm it at any strength, or it would be Strong but carries an open dispute.
- **Speculative:** half or fewer confirm it, with no dispute refuting it. Keep these: a find only one model sees is still worth listing.
- **Dropped:** a dispute shows with code evidence that the problem is absent, and no one answers it. List it in the report with the reason.

## Report and grilling

Produce the report `improve-codebase-architecture` describes, with two additions per card: an agreement line (for example `3 of 4 Strong, 1 no view`) and any open dispute, plus the roster section `council-chain` adds. Then hand over to that skill's grilling and filing steps unchanged, except that a work item filed from this review gets the header lines `Kind: architecture` and `Source: bc-council-improve-codebase`, so tools that list work items can filter the ones it filed.

After filing, recommend running `/bc-plan-to-pipeline` on each chosen item to slice it, passing the grilling's settled answers along so the owner is not asked the same questions twice.

When the review ends, do `council-chain`'s cleanup.
