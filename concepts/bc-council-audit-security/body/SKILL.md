---
name: bc-council-audit-security
description: "Run a bc-security-audit full audit through the advisor council: this session does recon and the threat model, every council advisor hunts the trust boundaries dealt to it, they attack each other's candidates, then every candidate still goes to its own fresh refuting reviewer before the normal records, validator and report, and confirmed findings can be filed. Use when the user says bc-council-audit-security or asks the council to audit a repository's security. Pi only: runs on bc-council-mode, which needs the pi-subagents `subagent` tool."
disable-model-invocation: true
argument-hint: "[scope] [--max-verify N]"
---

# Council security audit

This skill joins three skills and copies none. Load all three before starting:

- `bc-council-chain`: the council steps every chain shares (roster, shared map, pass 1, merge, pass 2, fallbacks, cleanup) and the parts a chain must define.
- `bc-security-audit`: the full-audit workflow, its Output gate, execution boundary, recon note and coverage ledger, fresh verification, JSON records, validator and report.
- `bc-council-mode`: how to brief, launch, relay to and resume advisors, and the pass cap.

Invoking this skill is the explicit full-audit request `bc-security-audit` requires. Run its full audit with one change: the council replaces its step 2 (the single hunting pass). Steps 1, 3 and 4, the Output gate and the execution boundary stay as that skill states them. Run every step through the report and filing without stopping between them; ask the owner only the questions the loaded skills require (for example the Output gate, the roster question or the filing question). Where this file is silent, those three skills decide.

Advisor agreement never verifies a finding. Only a fresh `reviewer` decides a verdict; the council only orders the verification queue. Why: agreement between hunters is not independent evidence, and `bc-security-audit`'s independence rule stays whole.

## Pre-reading and map

The shared map is `bc-security-audit` step 1, done by this session, not by a scout: pass the Output gate, create `.security-audit/run-N/`, write `architecture.md` and seed `coverage-ledger.json` as its `RECONNAISSANCE.md` says, and choose the companions. This replaces `bc-council-chain`'s map scout. Why: the recon note and ledger are already the audit's map, and a second map would drift from the ledger the records cite.

Settle the scope (default: the whole repository) and `--max-verify N` (default: no cap). Number the trust boundaries in `architecture.md` (`B1`, `B2`, ...), each with its entry surfaces and `file:line`.

Brief extras: the run folder path, the scope and source revision, the selected companion files, `bc-security-audit`'s Evidence before labels section and its named overclaiming anti-patterns, the execution boundary (source only; advisors run nothing and stay read-only), and that advisors propose candidates, never verdicts or severity.

## Focuses

Deal the numbered trust boundaries round-robin, one at a time, across the advisors until all are dealt; with more advisors than boundaries, dealing wraps. Each advisor hunts every attack class from `ATTACK-CLASSES.md` and the selected companions across its dealt boundaries, and still reports candidates elsewhere. State each advisor's boundaries in chat and in the report's roster section. Why: recon already names the boundaries, and a missed check at a boundary is where a hole appears.

## Candidate format

Each advisor returns at most 8 candidates (the owner can raise this per run), each as:

```
### <id> <one-line title>
Claim: <the boundary violation and its concrete outcome>
Principal: <lower-trust actor, its starting capability, and the affected principal>
Resource: <the protected resource>
Outcome: <the concrete security outcome claimed, no stronger than the trace shows>
Trace: <source steps from input to sink, each with path:line>
Evidence: <quoted code lines, with file:line>
Boundary: <B-number from architecture.md>
Attack class: <class from ATTACK-CLASSES.md or a companion>
Units: <ledger unit IDs, or "new" with surface × boundary × subsystem × attack class>
Strength: Strong | Worth verifying | Weak
```

Duplicate rule: candidates with the same source-derived root cause are one (`bc-security-audit`'s consolidation). The same location with a different root cause or outcome is two candidates. Add every new unit to the ledger at merge.

## Verdict rule

Pass 2: each advisor attacks the candidates it did not propose. It confirms with its own strength, disputes with code evidence (`file:line` showing a control on the path, or the outcome not reachable), or gives no view.

Pass 2 only orders the verification queue; it rejects nothing. Order: candidates without an unanswered code-evidenced dispute first, by share of N rating them Strong, then share of N confirming at any strength, then trace completeness; then the candidates such a dispute would drop, in the same order. Why: `bc-security-audit` sends every candidate, a likely rejection included, to a fresh reviewer, and only that reviewer may reject.

## Verification

Run `bc-security-audit` step 3 on the queue in order: one `reviewer` per candidate in a fresh session, given only the candidate's Claim, Principal, Resource, Outcome, Trace, Units and the exact claimed input and result, plus source access, the verification contract and the selected companions' constraints. Never pass strength, agreement, refinements, disputes or advisor names. Why: those are the hunters' reasoning, which the parent withholds from the verifier.

Verify every candidate in the queue. The only cap is `--max-verify N`, never time or cost: with it, verify only the first N. Every candidate past the cap stays unresolved in the ledger and is listed unverified, and the report says the run is incomplete. State in the plan and report whether a cap was set.

Then write `findings.json` from the reviewers' records, update the ledger, and run `validate_audit.py` as `bc-security-audit` step 4 says, unchanged.

## Report and filing

Write `REPORT.md` as `bc-security-audit` step 4 says, in the run folder. Add per candidate: an agreement line (for example `2 of 3 Strong, 1 disputed`) beside its verdict, which never changes the verdict; any pass-2 dispute with each side's evidence; and its boundary. List unverified candidates with their queue place. Add the roster section `bc-council-chain` asks for, with each advisor's dealt boundaries.

Then ask which findings to file, with every `confirmed` finding pre-selected; `all` files the pre-selected ones, and nothing else is filed unless the owner picks it. Load `bc-file-findings` and file the answer as it says. Else: chosen → numbered work-planned items, rejected → work-dropped with the reason, the rest → ideas lines, numbered only from the main checkout, then plan each filed item with `bc-plan-to-pipeline` in the same reply; without a work pipeline (a "Where things go" table in `.bc-agent/AGENTS.md`, as `bc-setup-project` sets up), list the picks and say they are not filed. Each filed finding gets `Kind: security` and `Source: bc-council-audit-security`, names the affected area and the fix, and points at `.security-audit/run-N/` (git-ignored) and the finding ID for details. Write no exploit steps, input or payload in the item. Why: the work item is committed, and the run folder is not.

When the audit ends, do `bc-council-chain`'s cleanup.
