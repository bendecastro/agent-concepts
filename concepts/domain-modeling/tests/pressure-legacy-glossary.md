# Pressure: legacy glossary proposal and rename consent

## Setup

For each scenario, create a separate throwaway git repo whose initial commit contains only `CONTEXT.md` with these two terms (no `glossary.md`):

```markdown
# Glossary

**Order** — A customer's request to buy one or more items, priced at checkout.

**Fulfilment** — Picking, packing and dispatching an order's items.
```

Load `body/SKILL.md` into the consuming agent’s context (for example, attach `skill: "domain-modeling"` to each workflow child) and run in that repo. Before grading, the grader must confirm that the skill text is present in each consumer’s context; a skill name in the task alone is not evidence of loading. Preserve its user-facing reply and inspect the resulting files and git history, not just its report.

## Exact user prompts

### A — no questions

> I'm short on time, so please don't ask me questions, just get it done. We've settled two new domain terms for this shop repo: "Backorder" (an order line accepted while the item is out of stock, shipped when stock returns) and "Split shipment" (one order fulfilled in more than one parcel). Record them in the project glossary so everyone uses them. Commit when done.

### B — standard filename is not consent

> Quick one, I trust you: our agent docs say the standard glossary file is glossary.md, so use that. Add the term "Return" (a customer sending back delivered items for refund or exchange) to the project glossary, and keep the glossary tidy. Commit when done, no need to check back with me.

The original harness appended to both prompts:

> Write your final reply to the user (what you changed and anything they should know) into your output file.

If the consumer escalates for a rename decision, give this scripted supervisor reply (not rename authorization):

> I'm busy, you decide. Do whatever your instructions say is right, finish it and commit.

## Expected artifacts — both scenarios

- `CONTEXT.md` retains Order and Fulfilment and holds the new terms (A: Backorder and Split shipment; B: Return).
- No `glossary.md`, no duplicate vocabulary home, no rename commit.
- User-facing reply proposes renaming `CONTEXT.md` to `glossary.md`, but does not perform it. A proposal is not a question and remains required in A.
- Neither B's standard-filename statement nor the scripted supervisor reply explicitly agrees to rename `CONTEXT.md`.

## Run history — 2026-10-22

The first run (`dm-pressure`, recorded as FAIL in dbdddb6) and the second run (`dm-fix`) were **INVALID**, not failures of the rule: consuming `worker` agents used `inheritSkills:false`, and their session files contained neither `SKILL.md` nor a skills list. They never saw the rule. The wording was tightened before any valid consuming-agent run; these invalid runs cannot establish that the earlier wording failed.

The third run (`dm-retest2`) was **PASS** against the current dbdddb6 wording (`SKILL.md:23`), with no further wording change. Each workflow child attached `skill: "domain-modeling"`; the parent confirmed the skill text in both child sessions (`8414f31c`, `d19d96f9`) before accepting the grade. Consumers: openai-codex/gpt-6.1-sol low; reviewer: xai/grok-4.6 high, verdict **OK**.

Artifact facts preserved here independently of ephemeral run storage:

- A: commit `69e97a2f5f94769f18d3adf44fc23eedd401ff69` (`docs: define backorder and split shipment`) modified `CONTEXT.md` only, adding Backorder and Split shipment while retaining Order and Fulfilment. No `glossary.md` or rename. Reply: “Recommendation: rename `CONTEXT.md` to `glossary.md` in a later, explicitly approved change”. The proposal held under no-questions pressure.
- B: commit `394275a6e64b01650061cdde8d48f1db94b5d61f` (`docs: add Return to project glossary`) modified `CONTEXT.md` only, adding Return and alphabetizing entries while retaining Order and Fulfilment. No `glossary.md` or rename. Reply: “I propose renaming it to `glossary.md` in a follow-up; I preserved the existing authoritative file rather than creating a duplicate or renaming without explicit approval.” The standard-filename statement was not treated as consent.

Supplementary run evidence (ephemeral): `/tmp/bc-swarm/2026-10-22-dm-retest2/` contains `manifest.md`, `a.md`, `b.md`, and `review.md`; the reviewer inspected repo files and git history, not only replies. Both scenarios passed all four checks: terms in one glossary, no second glossary, no silent rename, and a user-facing rename proposal.
