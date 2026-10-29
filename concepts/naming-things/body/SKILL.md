---
name: naming-things
description: Choose clear domain and public code names. Use when a project's domain names or public code names are first introduced or chosen, or when asked to audit or rename existing names. Not for local variables or one-line fixes.
---

# Naming Things

Apply this advisory checklist, choose names, and list the chosen names in your reply; do not pause to ask for naming approval. Cover pipeline steps, job/card classes, states, ids, config keys, files, ledgers, timers/services, glossary terms, modules, public functions and CLI flags.

## New names

Read the project's glossary before choosing words. Apply the rules below and the cold-read test before the first persisted write. Load `domain-modeling` for glossary persistence, conflicting terms and ADR decisions; its reconciliation contract still applies, rather than silently overriding an established term.

| Rule | Bad → good | Why |
|---|---|---|
| One name, one job; split a class reused for another job. | `ProposalJob` for proposals and benchmarks → `ProposeImprovementsJob` / `SelectBenchmarkJob` | Shared names hide different responsibilities. |
| One word, one meaning project-wide; check the glossary before adopting a word. | `contract` for acceptance and billing → `acceptance-criteria` / `billing-agreement` | Overloaded words make correct reasoning depend on hidden context. |
| Steps are verb-object and name their output; reserve `review` for a verdict. | `buyer-review` generating proposals → `propose-improvements` | The name should predict the result, not imply a verdict that never happens. |
| Name what it does, not who triggers/runs it or the current tool, harness or provider. | `tool-refresh` → `refresh-catalog` | Implementations and operators change without changing the job. |
| Each state covers exactly one state; states partition the lifecycle. | `Building` including Built → `build-in-progress` / `built-awaiting-publication` | Overlapping states obscure valid transitions. |
| Avoid jargon/metaphor needing decoding; be grep-friendly. | `sense` → `collect-site-signals` | Readers and searches should find the same concept without translation. |
| Use the same word in code, config, timers, docs and UI labels. | `collect` / `refill` / `store scan` for one job → `collect-listings` everywhere | Parallel vocabularies break discoverability. |
| List and settle persisted names before the first write; avoid mutable names in derived ids/hashes unless an alias reader is planned. | hash input `current-step-name` → stable `step-id` | Persisted spellings are expensive to change, not cosmetic labels. |

**Cold-read test:** can a newcomer guess the input, output and verdict/result from the name alone? Bad `shortlist` → good `check-site-terms`. Why: this catches names that sound plausible only after an explanation.

## Record the choice

Each new name gets a glossary entry through `domain-modeling`'s rules, with its meaning and a `Saved in:` line. List conceptual surface categories only: `job ids; ledger filename; config key; state value; hash input`, or `none` if not persisted. Mark persisted names **expensive to change**. No file paths, module names or literal keys in the glossary: its purity rule still owns the boundary. If exact locations are useful, put them in a code comment beside the name's single source of truth, not in the glossary.

Example: **Propose improvements** — Turn site findings into ranked improvement proposals. **Saved in:** job ids; ledger filename. **Expensive to change.**

## Audit or rename

Load [rename-recipe.md](rename-recipe.md) only for an existing-project audit or rename. Audit first and propose a rename map; execute only within the requested scope.
