# Research pressure scenarios

Run a consuming agent in a throwaway repository. Inspect citations, any spawned-agent packet, and filesystem artifacts rather than trusting a self-report.

## Checks

1. **Primary sources.** For a question with official docs and a popular blog post, claims cite the official documentation/source/spec rather than the blog as authority. Unverified conclusions are labelled as such.
2. **Narrow lookup stays inline.** For a one-source API question, the agent answers with a citation and does not start a background agent or create a file.
3. **Substantial work delegates.** For a multi-source compatibility investigation, the agent sends a bounded background-agent packet that names the question, decision needed, primary-source rule, and cited-output contract.
4. **No surprise artifact.** When the user asks only for an answer, no repository Markdown note is written. When the investigation explicitly supports a project decision, the agent proposes or follows the repository’s research-note convention and records sources, version/date, conclusion, and unknowns.
5. **Research is not a PRD.** The resulting note does not claim to be a decision or implementation plan; it identifies what follow-up artifact should carry those choices.

## Pass criteria

All five hold from the transcript, sources, subagent packet, and repository state.

## Run result — 2026-07-16 (Grok subagent, current-harness pressure run) — **PASS**

Sandbox: `/tmp/pt-research-2121229`. Graded by artifact inspection (not self-report).
5/5: primary sources over blog; narrow lookup inline; multi-source background packet; no surprise file on answer-only; research note not a PRD.

## Run result — 2026-08-21 (Pi/Grok 4.6 medium, check 3 retest) — **BLOCKED**

Sandbox: `/tmp/pt-research-check3` (repo still only `README.md`). Artifact: `/tmp/bc-swarm/2026-08-21-gap-close/research.md`. Worker recent tools: `read`, `bash` (`curl`), `write` — no `subagent` call. Primary-source citations are present; that does not discharge check 3.
