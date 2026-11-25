---
name: bc-council-find-bugs
description: "Run bc-find-bugs through the advisor council: one scout maps the area, every council advisor hunts it with a dealt focus, they attack each other's candidates, then one worker reproduces the strongest as failing tests on a hunt branch before the normal two-tier report and filing. Use when the user says bc-council-find-bugs or asks the council to hunt for bugs."
disable-model-invocation: true
argument-hint: "[area] [--since <ref>] [--max-repro N]"
---

# Council bug hunt

This skill joins three skills and copies none. Load all three before starting:

- `bc-council-chain`: the council steps every chain shares (roster, shared map, pass 1, merge, pass 2, fallbacks, cleanup) and the parts a chain must define.
- `bc-find-bugs`: scope, the hunted kinds, the candidate block, reproduction, the report and filing.
- `bc-council-mode`: how to brief, launch, relay to and resume advisors, and the pass cap.

Run the `bc-council-chain` steps in order, then reproduction, report and filing below, without stopping between them: the owner is asked only the questions those skills require (for example the roster question or the filing question). Why: a hunt that stops after the map or a pass has produced nothing the owner can use. This file defines only the parts that recipe leaves to the chain. Where this file is silent, those three skills decide.

A bug is confirmed only by a reproduction watched failing for the stated reason (`bc-find-bugs`). Advisor agreement never confirms a bug: it orders candidates for reproduction and orders the suspected tier. Why: agreement is not evidence that a bug is real.

## Pre-reading and map

Pre-reading: `bc-find-bugs` §1. Settle the area (or the whole repo when small), `--since <ref>` and `--max-repro N` (default 12), and name the hunt. Read the area's README and tests.

Map contents, each claim with `file:line`: entry points; data flow through the area; error paths (what raises, what catches, what is cleaned up); shared and mutable state, caches and locks; contracts between modules (units, indexing, None vs empty, what a caller assumes of a callee); existing tests and what they cover. With `--since`, mark which files changed.

Brief extras: the area and hunt name, the hunted kinds from `bc-find-bugs` §2, and that advisors stay read-only and only propose reproductions.

## Focuses

Deal one focus per advisor, round-robin from `bc-find-bugs` §2's list in this order: inputs and edge cases; error and failure paths; state and data lifecycle; concurrency and ordering; contracts between modules. With fewer advisors than focuses, the undealt focuses are still hunted by everyone; with more, dealing wraps. State each advisor's focus in chat and in the report's roster section.

Each advisor hunts its focus first and still reports bugs outside it. Why: unstanced advisors converge on the obvious.

## Candidate format

Each advisor returns at most 8 candidates (the owner can raise this per run), each as `bc-find-bugs`' candidate block plus two lines:

```
### <id> <one-line title>
Kind: bug | security
Location: <path>:<line(s)>
Evidence: <quoted code lines, with file:line>
Claim: <what goes wrong, in behaviour terms>
Reproduction: input <...>; steps <...>; expected <...>; actual <...>
Focus: <the dealt focus, or the focus it falls under>
Strength: Strong | Worth reproducing | Weak
```

Duplicate rule: candidates with the same location and the same claimed wrong result are one. Same location with a different claimed result is two candidates.

## Verdict rule

Pass 2: each advisor attacks the candidates it did not propose. It confirms with its own strength, disputes with code evidence (`file:line`, or an input whose actual result is the expected one), or gives no view.

- **Dropped:** a code-evidenced dispute nobody answers with code shows the claimed wrong result does not happen. List it in the report with the dispute.
- **Everything else goes to the reproduction queue**, ordered by: share of N confirming it as Strong, then share of N confirming at any strength, then the strength of the quoted evidence. An open dispute does not drop a candidate; reproduction settles it.

This order only chooses what is reproduced first and how the suspected tier is ranked. No share of N confirms a candidate.

## Reproduction

After pass 2, launch ONE `worker` to run `bc-find-bugs` §3 on the top `--max-repro` candidates of the queue: its own worktree on branch `find-bugs/<hunt-name>`, one test per candidate, kept only if it fails for the stated reason, committed on the hunt branch. Launch it with `skill: ["bc-find-bugs", "bc-minimal-solution-ladder", "bc-codebase-design", "bc-codebase-docs", "bc-diagnosing-bugs", "bc-tdd"]`. Why: a launch skill list replaces the role's default skills, so the defaults are listed with it. Give it the queue in order with each candidate block, and ask it to return, per candidate, the test path and name with the failing assertion lines, or its suspected reason (`bc-find-bugs` §3 wording). Advisors stay read-only and write no reproductions.

## Report and filing

Write the `bc-find-bugs` §4 report in the hunt worktree and commit it on the hunt branch. Add per candidate: an agreement line (for example `2 of 3 Strong, 1 disputed`), any open dispute with each side's evidence, and its focus; in Suspected, rank by the verdict order above. List dropped candidates with their dispute. Add the roster section `bc-council-chain` asks for, with each advisor's dealt focus.

Filing is `bc-find-bugs` §5 unchanged, except that every filed item carries `Source: bc-council-find-bugs` instead of `Source: find-bugs`.

When the hunt ends, do `bc-council-chain`'s cleanup.
