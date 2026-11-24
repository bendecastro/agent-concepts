---
name: bc-council-improve-codebase
description: "Run improve-codebase-architecture through the advisor council: one scout maps the codebase, every available council advisor proposes and cross-examines deep-module candidates, and candidates are ranked by evidence-backed agreement before the normal report and grilling. Use when the user says bc-council-improve-codebase, council architecture review, or asks the council to review the codebase architecture."
---

# Council architecture review

This skill joins two skills and copies neither. Load both before starting:

- `improve-codebase-architecture`: inputs to read, candidate card fields, the visual report, grilling, and where chosen, rejected and remaining items are filed.
- `council-mode`: how to brief, launch, relay to and resume advisors, and the pass cap.

This file adds only what neither says: the shared map, the roster rule, the card format advisors return, and the agreement rule. Where this file is silent, those two skills decide.

If `~/.config/agent-concepts/overlays/bc-council-improve-codebase.md` exists, read it: it names this machine's roster and map-scout model.

## 1. Roster: whoever is on the council today

The council changes over time. Never hard-code advisor names in this file. If the overlay names a roster, use exactly those advisors. Otherwise run `subagent({ action: "list" })` and use every executable profile whose name starts with `council-`, up to the four-advisor cap in `council-mode`. With more than four, ask the user which four. With fewer than two, follow `council-mode`'s fallback and say so in the report. To set up advisors, start from `council-mode`'s example profiles and give each a different model.

Write all thresholds below as shares of the roster size N, never as fixed counts. Why: a rule written for three advisors silently breaks when a fourth joins.

Before launching an advisor that runs through an external agent harness, check that its permission mode asks before edits: the harness's native tools are outside the read-only profile.

If an advisor's sandbox cannot read the run directory (some external harnesses can read only the tree under their working folder), copy the map and brief to `.git/council-<run-dir name>/` inside that tree (git ignores it) and give that advisor those paths; step 7 deletes the copy. Why: in the first live run such an advisor was refused twice and needed three launches, about 30 minutes.

## 2. One shared map

Do the first step of `improve-codebase-architecture` yourself: read the glossary, decision records and architecture lines in the ideas file. Then launch one `scout` to map the codebase into a file in the run directory: modules, their interfaces, seams, call fan-in and fan-out, and places where one change touches many files. Every claim needs a `file:line`.

Run every map scout (one, or several splitting a large codebase) on a strong model with high reasoning effort: the overlay's model if it names one, otherwise the strongest model you can run, rather than the scout role's default route. Why: every advisor judges from this map, so its depth sets the ceiling for the whole review. If that model is unavailable, use the next best, and say so in chat and in the report's roster section.

Advisors receive the map plus read access to the tree. They judge the map; they verify against the code only what they cite. Why: when each advisor scans on its own, disagreements come from what each happened to read rather than from judgment.

## 3. Pass 1: independent candidates

Give every advisor the same brief: the map path, the glossary and decision-record paths, recorded rejections not to re-propose, and this return format. Advisors do not see each other's output in this pass.

Return each candidate as:

```
Candidate: <short name>
Module / seam: <names from the map>
Problem: <one or two sentences>
Direction: <recommended change>
Evidence: <file:line for every claim>
Strength: Strong | Worth exploring | Speculative
```

## 4. Merge

First check every `file:line` in the advisors' cards: the file exists and has that line. Mark a claim whose citation does not resolve as unverified and do not count it as evidence; if it was the card's only evidence, ask that advisor for the right citation in pass 2. Why: in the first live run an advisor cited a test file that does not exist, and nothing caught it.

Deduplicate candidates that name the same module and seam with the same direction. Keep both when the direction differs: that is a disagreement, not a duplicate. Build a matrix: one row per candidate, one column per advisor, holding that advisor's strength or "not proposed".

## 5. Pass 2: cross-examination

Resume each advisor with the candidates it did not propose (curated per `council-mode`, at most five relayed claims per advisor). For each, it must answer one of:

- **Confirm** with a strength of its own.
- **Dispute** with code evidence (`file:line`) showing the problem is absent or the direction is wrong.
- **No view**, with a one-line reason.

Run a third pass only when a dispute affects the ranking and advisor evidence could settle it.

## 6. Agreement rule

Rank candidates by evidence, not by vote alone:

- **Strong:** more than half of N rate it Strong, and no advisor holds an unanswered evidence-backed dispute.
- **Worth exploring:** more than half of N confirm it at any strength, or it would be Strong but carries an open dispute.
- **Speculative:** half or fewer confirm it, with no dispute refuting it. Keep these: a find only one model sees is still worth listing.
- **Dropped:** a dispute shows with code evidence that the problem is absent, and no one answers it. List it in the report with the reason.

Never force agreement. An open dispute the code cannot settle becomes an owner decision, with each side's best evidence. Why: required consensus pushes advisors toward the safest candidate and loses the unusual finds that justify a council.

## 7. Report and grilling

Produce the report `improve-codebase-architecture` describes, with two additions per card: an agreement line (for example `3 of 4 Strong, 1 no view`) and any open dispute. Add a short roster section: advisors, passes run, fallbacks. Then hand over to that skill's grilling and filing steps unchanged, except that a work item filed from this review gets the header lines `Kind: architecture` and `Source: bc-council-improve-codebase`, so tools that list work items can filter the ones it filed.

After filing, recommend running `/bc-plan-to-pipeline` on each chosen item to slice it, passing the grilling's settled answers along so the owner is not asked the same questions twice.

When the review ends, delete any `.git/council-<run-dir name>/` copy made for a sandboxed advisor (`rm -r .git/council-<run-dir name>/`).
