---
name: research
description: Research a technical question against high-trust primary sources. Use for multi-source investigations, API/documentation facts, or delegated reading legwork; keep narrow factual lookups inline.
---

# Evidence-First Research

Investigate a focused question using sources that own the relevant claims: official documentation, specifications, source code, first-party APIs, or maintainer statements. Do not treat secondary summaries as proof when a primary source is available.

## Choose the execution shape

- **Narrow lookup:** research inline when one or two sources answer the question quickly.
- **Substantial investigation:** launch a background research agent so the main session can continue. Give it the question, desired decision/output, source-quality rule, and this output contract.

## Research contract

1. State the question and any material assumptions.
2. Trace each factual claim to the source that owns it. Prefer a stable permalink, version, or dated official document.
3. Separate verified facts, reasoned recommendations, and unresolved uncertainty.
4. Return a concise cited finding: answer, evidence, implications for the project, and remaining unknowns.

## Durable artifacts are opt-in

Do **not** create a repository note for a disposable answer. Persist one cited Markdown note only when the user asks, a project instruction requires it, or the research directly informs a durable decision, PRD, or implementation plan. Match the repo’s established research-note location and format; if none exists, propose a path before writing.

A durable note records the question, conclusion, primary-source links, relevant version/date, and open questions. It is evidence for later work, not a substitute for the actual PRD or decision record.
