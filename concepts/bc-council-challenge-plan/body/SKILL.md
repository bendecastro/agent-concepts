---
name: bc-council-challenge-plan
description: "Challenge a plan or PRD through the advisor council before it is sliced: one scout maps the code the plan touches, every council advisor attacks a dealt part of the plan for wrong premises, missing cases, cheaper paths and risky order, they attack each other's objections, the owner is grilled only on the surviving ones, the answers are written into the plan, then bc-plan-to-pipeline slices it as a settled source. Use when the user says bc-council-challenge-plan or asks the council to challenge a plan."
disable-model-invocation: true
argument-hint: "<plan or PRD path>"
---

# Council plan challenge

This skill joins four skills and copies none. Load all four before starting:

- `council-chain`: the council steps every chain shares (roster, shared map, pass 1, merge, pass 2, fallbacks, cleanup) and the parts a chain must define.
- `council-mode`: how to brief, launch, relay to and resume advisors, and the pass cap.
- `grilling`: how to ask the owner one question at a time, recommended answer first.
- `bc-plan-to-pipeline`: the hand-off at the end, in its settled-source mode.

The parent is the plan itself: its path is the argument. Run the `council-chain` steps in order, then the grill, the plan edits, the report and the hand-off below, without stopping between them; the owner is asked only the questions those skills and this file require (the roster question, the surviving objections). Why: a challenge that stops after a pass has changed nothing the owner can use. This file defines only the parts that recipe leaves to the chain. Where this file is silent, those skills decide.

The council never rewrites the plan. Only the owner's answers go into it. Why: the plan is the owner's decision record; an objection is a question to the owner, not an edit.

## Pre-reading and map

Pre-reading: read the plan whole, and number its sections or steps (the parts dealt below). Read the README of every area it names.

Map: the plan's code context. The scout maps the code the plan names or would touch, each claim with `file:line`: every file, function, type or behaviour the plan names, and what the code actually does there; callers and dependents of what the plan changes; existing helpers or modules that already do part of what the plan builds; tests covering those areas; and, per plan part, the plan lines that claim something about the code, each marked as matching the code, contradicting it, or unverifiable.

Brief extras: the plan path, the numbered part list, the objection kinds below, and that advisors stay read-only and propose no edits to the plan or the code.

## Focuses

Deal the plan's parts round-robin, one advisor after another, until every part is dealt (an advisor may get several parts; with more advisors than parts, dealing wraps). State each advisor's parts in chat and in the report's roster section.

Each advisor attacks its parts for every objection kind, and may still raise objections anywhere else in the plan. Why: the plan's sections are what the owner chose to split on, and every part then gets a dedicated reader.

Objection kinds:

- **Wrong premise:** the plan states something about the code or the world that is false.
- **Missing case:** an input, state, caller or failure the plan does not handle.
- **Cheaper path:** a smaller way to the same outcome, often something the code already has.
- **Risky order:** a step that breaks something if done before another.

## Objection format

Each advisor returns at most 8 objections (the owner can raise this per run):

```
### <id> <one-line title>
Kind: wrong premise | missing case | cheaper path | risky order
Plan line: "<the plan line it attacks, quoted>" (<plan path>:<line>)
Evidence: <file:line citations, required wherever the plan claims something about the code>
Objection: <what is wrong, and what happens if the plan goes ahead as written>
Proposed question: <the question the owner must answer, with a recommended answer>
Part: <the dealt part it falls under>
Strength: Strong | Worth asking | Weak
```

Duplicate rule: objections quoting the same plan line and making the same claim are one. Same line with a different claim is two objections.

## Verdict rule

Pass 2: each advisor attacks the objections it did not raise. It confirms with its own strength and any refinement, disputes with evidence (`file:line`, or a plan line that already answers the objection), or gives no view.

- **Dropped:** a dispute with evidence that nobody answers with evidence. List it in the report with the dispute.
- **Surviving:** everything else, ordered by share of N confirming it as Strong, then share of N confirming at any strength. An open dispute does not drop an objection; it goes to the owner with each side's evidence.

## Grill and plan edits

Grill the owner on the surviving objections only, one at a time, in verdict order, following `grilling`: state the objection, the quoted plan line, its evidence and agreement line, and the recommended answer. The owner may answer, accept the recommendation, or reject the objection.

After each answer, write it into the plan at the line it concerns, as the owner's decision with its why. A rejected objection changes nothing in the plan. Edit only what the answer settles.

## Report

Write the report to the run directory: per objection, its kind, quoted plan line, agreement line (for example `2 of 3 Strong, 1 disputed`), refinements under the advisor's name, any dispute with each side's evidence, and the owner's answer (or "rejected"). List dropped objections with their dispute. Add the roster section `council-chain` asks for, with each advisor's dealt parts.

## Hand-off

Run `council-chain`'s cleanup. Then run `/bc-plan-to-pipeline` on the edited plan in its settled-source mode. Pass it the owner's answers from the grill as settled, so it asks only the questions the plan still leaves open and none the owner has already answered. Why: the owner should never be asked the same question twice.
