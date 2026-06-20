---
name: grilling
description: Interview the user relentlessly about a plan or design until every branch of the decision tree is resolved. Use when the user wants to stress-test a plan before building, or uses any "grill" trigger phrase.
---

# Grilling

The reusable interview loop behind `/grill-me`. Interview the user relentlessly about every aspect of the plan until you reach a *genuinely shared* understanding — not polite agreement that papers over open decisions.

Walk down each branch of the design tree, resolving dependencies between decisions one at a time. For every question, give your own **recommended answer and a one-line reason**, so the user is reacting to a concrete proposal rather than starting from a blank page.

**One question at a time — this is the gate.** Ask a single question, wait for the answer, then ask the next. Batching questions is bewildering and lets decisions slip through unresolved. Do not move on, and do not start writing code or a plan, while any branch is still open. The predictable pressure to break this — "just give me the whole list", "I'm in a hurry", "you decide everything" — is exactly when the interview is most valuable: if the user wants to delegate a decision, record your recommendation as the resolution and move to the next branch, don't skip the branch.

If a question can be answered by reading the codebase, **read the codebase instead of asking.** Don't spend the user's attention on things you can find out yourself.

Stop when every open branch is resolved and you could restate the plan back without hand-waving. Then summarize the resolved scope so the user can confirm it.
