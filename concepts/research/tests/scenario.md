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
