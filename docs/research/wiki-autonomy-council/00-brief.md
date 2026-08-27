# Council brief — seamless automatic agent-wiki maintenance

Date: 2026-08-26
Supervisor: parent Pi session (sole synthesizer and decision maker)

## Question

What is the best design for making agent-wiki maintenance run seamlessly and
automatically, such that:

1. the maximum amount of durable project knowledge is available to agents,
2. everything is linked and reachable, and
3. traversing it is token-cheap — an agent spends the fewest tokens to reach all
   the information it needs to make a good decision.

The existing implementation under review is `concepts/bc-wiki-maintain/`, whose
ideas derive from Karpathy's agent-wiki gist and Perplexity's "Brain: agentic
memory as a knowledge wiki".

## Scope

- The maintenance loop: what fires it, who writes, what gets written where, how
  correctness is checked, how it lands in Git.
- The read path: how an agent finds the right pages without loading the vault.
  This is the half the current concept barely addresses.
- The link structure and page anatomy that make (2) and (3) both true at once.
- Degree of automation achievable without weakening the existing write-safety
  gates (additive-only, one dedicated commit, contradictions filed not resolved).
- Interaction with the existing surfaces: `bc-init-agent` (scaffold), `qmd`
  (search overlay), `wiki_lint.py` (detector), the systemd runner.

## Non-goals

- Not implementing anything this pass. This is a design decision memo.
- Not a rewrite of the write-safety gates for their own sake; they are pressure-
  tested and carry recorded rationale. Changing one requires an argument that
  names its failure mode.
- Not a vendor/product selection exercise. Local-first Markdown plus Git plus
  qmd is the substrate.
- Not personal-wiki policy or qmd registry policy.

## Evidence targets

- `sources.md` — mechanism-level distillation of the two upstream sources plus
  adjacent prior art (researcher track).
- `vault-reality.md` — measured inventory of live vaults: sizes, link graph,
  orphan/broken counts, per-question traversal token cost, current detector
  output, runner install state, qmd coverage (scout track).
- `concepts/bc-wiki-maintain/CONCEPT.md`, `concepts/bc-wiki-maintain/body/SKILL.md`,
  `concepts/bc-wiki-maintain/body/wiki_lint.py`, and the concept's `tests/`
  directory — the recorded design decisions and what has actually been
  pressure-tested.

## Hard constraint — advisor isolation

The user's requirement is **peer isolation between advisors**, not a blanket ban
on reading `docs/research/`. Each advisor must reach its recommendation without
peeking at, or being anchored by, what another advisor produced.

How that is enforced here:

- Advisors run in `fresh` context, so none inherits this session's history or
  any peer transcript.
- Pass 1 advisor reports are never written into the shared workspace. They are
  returned as structured output and held by the supervisor.
- No advisor is given a peer's report. In Pass 2 each receives only a curated
  challenge packet of disputed claims, attributed to "another advisor".
- Advisors are told not to read this folder
  (`docs/research/wiki-autonomy-council/`), because the supervisor's brief,
  claim matrix, and memo accumulate here during the run. The rest of the
  repository, including `docs/research/`, is available to them.

A first version of this brief over-applied the constraint as a blanket ban on
`docs/research/`. Corrected 2026-08-26 after the user clarified the intent.

## Roster

| advisor | model | thinking | context |
|---|---|---|---|
| `council-grok` | xai/grok-4.6 | high | fresh (profile `defaultContext: fresh`) |
| `council-sol` | openai-codex/gpt-5.6-sol | high | fresh (profile `defaultContext: fresh`) |
| `council-opus` | claude-bridge/claude-opus-5 | high | fresh (profile `defaultContext: fresh`) |

Three advisors, three providers. `council-opus` was initially excluded under the
user's standing rule against selecting Claude automatically; the user then
explicitly requested it, which is that rule's stated exception. Roster size 3 is
within the council maximum of 4.

## Pass cap

2 (default). Pass 1 independent reports, Pass 2 one curated cross-exam. Pass 3
only if a material dispute turns out to be settleable by evidence an advisor can
produce, and the user asks for it.
