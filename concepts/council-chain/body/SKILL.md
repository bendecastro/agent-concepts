---
name: council-chain
description: "Shared recipe loaded by bc-council-* chain skills (for example bc-council-improve-codebase) that run a parent skill through the advisor council: roster, one shared map, pass 1 independent candidates, citation-checked merge, pass 2 cross-examination, advisor fallbacks and sandbox-copy cleanup. Not run directly: a chain loads it and supplies the job-specific parts."
---

# Council chain recipe

A `bc-council-<job>` skill runs a parent skill through the advisor council. This file holds the council steps every chain shares. Load `council-mode` with it: that skill says how to brief, launch, relay to and resume advisors, and sets the pass and roster caps. Where this file and the chain are silent, `council-mode` and the chain's parent skill decide.

If `~/.config/agent-concepts/overlays/council-chain.md` exists, read it: it names this machine's roster, map-scout model and which advisors are sandboxed.

## What a chain must define

A chain names each of these; this recipe leaves them open:

- **Parent skill** and the pre-reading the parent does before the map (the parent skill's first step).
- **Map contents:** what the scout records about the code, beyond `file:line` for every claim.
- **Brief extras:** paths and context every advisor receives besides the map, and recorded rejections not to re-propose.
- **Focuses or stances** dealt to advisors, if any.
- **Candidate format** advisors return in pass 1, with an `Evidence:` field of `file:line` citations.
- **Duplicate rule:** when two candidates are the same one.
- **Verdict or agreement rule** that ranks candidates after pass 2, with thresholds as shares of N.
- **Report and filing:** what the report adds per candidate, and how chosen items are filed (header lines, hand-offs).

## 1. Roster: whoever is on the council today

The council changes over time. Never hard-code advisor names in a chain. If the overlay names a roster, use exactly those advisors. Otherwise run `subagent({ action: "list" })` and use every executable profile whose name starts with `council-`, up to the four-advisor cap in `council-mode`. With more than four, ask the user which four. With fewer than two, follow `council-mode`'s fallback and say so in the report. To set up advisors, start from `council-mode`'s example profiles and give each a different model.

Write every threshold as a share of the roster size N, never as a fixed count. Why: a rule written for three advisors silently breaks when a fourth joins.

Before launching an advisor that runs through an external agent harness, check that its permission mode asks before edits: the harness's native tools are outside the read-only profile.

If an advisor's sandbox cannot read the run directory (some external harnesses can read only the tree under their working folder), copy the map and brief to `.git/council-<run-dir name>/` inside that tree (git ignores it) and give that advisor those paths; step 6 deletes the copy. Why: in the first live run such an advisor was refused twice and needed three launches, about 30 minutes.

## 2. One shared map

Do the chain's pre-reading yourself. Then launch one `scout` to map the code into a file in the run directory, recording what the chain's map contents name. Every claim needs a `file:line`.

Run every map scout (one, or several splitting a large codebase) on a strong model with high reasoning effort: the overlay's model if it names one, otherwise the strongest model you can run, rather than the scout role's default route. Why: every advisor judges from this map, so its depth sets the ceiling for the whole review. If that model is unavailable, use the next best, and say so in chat and in the report's roster section.

Advisors receive the map plus read access to the tree. They judge the map; they verify against the code only what they cite. Why: when each advisor scans on its own, disagreements come from what each happened to read rather than from judgment.

## 3. Pass 1: independent candidates

Give every advisor the same brief: the map path, the chain's brief extras, its focus or stance if the chain deals them, and the chain's candidate format. Advisors do not see each other's output in this pass.

## 4. Merge

First check every `file:line` in the advisors' candidates: the file exists and has that line. Mark a claim whose citation does not resolve as unverified and do not count it as evidence; if it was the candidate's only evidence, ask that advisor for the right citation in pass 2. Why: in the first live run an advisor cited a test file that does not exist, and nothing caught it.

Deduplicate by the chain's duplicate rule. When two candidates target the same thing but differ in what they claim or recommend, keep both: that is a disagreement, not a duplicate. Build a matrix: one row per candidate, one column per advisor, holding that advisor's strength or "not proposed".

## 5. Pass 2: cross-examination

Resume each advisor with the candidates it did not propose (curated per `council-mode`, at most five relayed claims per advisor). For each, it must answer one of:

- **Confirm** with a strength of its own.
- **Dispute** with code evidence (`file:line`) showing the problem is absent or the direction is wrong.
- **No view**, with a one-line reason.

Run a third pass only when a dispute affects the ranking and advisor evidence could settle it.

Then rank by the chain's verdict rule. Never force agreement. An open dispute the code cannot settle becomes an owner decision, with each side's best evidence. Why: required consensus pushes advisors toward the safest candidate and loses the unusual finds that justify a council.

## 6. Report and cleanup

Produce the chain's report with a short roster section: advisors, passes run, fallbacks. Then follow the chain's filing steps.

When the run ends, delete any `.git/council-<run-dir name>/` copy made for a sandboxed advisor (`rm -r .git/council-<run-dir name>/`).
