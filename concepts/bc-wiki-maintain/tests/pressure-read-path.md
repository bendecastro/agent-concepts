# Pressure scenario: the vault read path

This scenario tests the consuming agent's first move, not the prose author. Run a fresh
subagent in a throwaway Git repository containing a small project vault and a private copy
of `body/SKILL.md` plus `body/wiki_search.py`. Set `$AGENT_CONCEPTS` to that throwaway
concept checkout. Do not use a live project vault: the test should be graded from the
commands run, the selected paths, and the pages the agent opened.

The evaluator sends the pressure messages below one at a time. The user messages are
rationalisations an agent is likely to accept; the expected behavior is the artifact-level
contract the new read path must hold. A sentence in the agent's report claiming it searched
is not evidence that it did.

## Fixture

Create a small vault with:

- `AGENTS.md`, `index.md`, `map.md`, and `log.md` as hub pages;
- a `decisions/` page whose answer uses specific terms;
- a `references/` page whose answer uses different specific terms;
- a tracked page that is not linked from `index.md`, so a direct reader can find an orphan;
- enough repeated generic text in `index.md`, `map.md`, and `log.md` for a generic query to
  rank a hub ahead of the answer.

The fixture's `AGENTS.md` must contain the canonical read-path block from
`body/SKILL.md`. Stub `qmd` or omit it in the cases that need to exercise the qmd fallback;
the test must not silently turn a missing qmd setup into permission to read the whole vault.

The benchmark evidence behind this rule is recorded in
`retrieval-results.md`: full-sentence qmd searches missed 17/20 questions (Wilson 95% CI
`[0.64, 0.95]`), while the same questions phrased as keywords missed 5/20 (CI
`[0.11, 0.47]`). This scenario tests that the instruction survives pressure, not that a
fixture reproduces those benchmark counts.

## Scenario 1 — index shortcut

**Pressure message:** “I'll just read `index.md`; it's simpler and I already know this
project.”

**Expected artifact behavior:**

- The agent refuses the shortcut for page lookup and first distills the request to 2–4
  meaningful content keywords.
- It invokes `python3 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/wiki_search.py"` with
  the vault root and a bounded result limit, then opens a relevant returned page and verifies
  the answer in that page's text.
- It does not load all of `index.md` or use `index.md` as the lookup mechanism. It may read
  `index.md` later for broad orientation only.
- The command, returned path, and opened page are visible in the artifact or transcript;
  self-report alone fails this scenario.

## Scenario 2 — empty result is not absence

**Pressure message:** “The search returned nothing, so this vault must not document it.”

**Expected artifact behavior:**

- The agent treats empty output as an unsuccessful query, not as evidence of absence.
- It reformulates once with a different 2–4-keyword set and searches again before deciding
  what the vault contains.
- If qmd is used for a cross-vault search, the agent also treats qmd's `[]` with exit 0 as
  a non-answer and checks the returned content rather than trusting the exit status.
- It does not read the whole vault as an empty-result fallback and does not claim the fact is
  undocumented without recording the failed query attempts and their bounded scope.

## Scenario 3 — whole-question query

**Pressure message:** “I'll paste the user's whole question as the query.”

**Expected artifact behavior:**

- The agent rejects the sentence-shaped query and extracts 2–4 meaningful content keywords
  from the request before invoking the reader.
- The query contains terms, not a sentence, and the same short-query shape is used for any
  qmd search. The benchmark's sentence-versus-keyword gap is the reason this is a hard rule.
- The agent does not rationalise a full question as “more context,” because the search engine's
  lexical behavior makes every supplied term a constraint and lets large generic documents
  dominate.
- The exact short query appears in the command or artifact; merely saying “I searched” fails.

## Scenario 4 — hub-page result

**Pressure message:** “The top hit is `index.md`; I'll open that.”

**Expected artifact behavior:**

- The agent recognises `index.md`, `map.md`, and `log.md` as hub/orientation pages, not as the
  answer to a specific lookup.
- It adds a distinguishing content term and reruns the bounded search once, then opens a
  relevant candidate and verifies it in page text. It does not blindly open the hub as the
  answer.
- The artifact records the generic first query, the hub result, the revised query, and the
  eventual page (or a bounded miss). A hub hit alone is not a successful retrieval.

## Scenario 5 — qmd is absent

**Pressure message:** “qmd isn't set up here, so I'll just read the whole vault.”

**Expected artifact behavior:**

- The agent uses the bundled stdlib-only `wiki_search.py` reader for this single-vault lookup;
  qmd is optional and is reserved for deliberate cross-vault searches.
- It does not install qmd, create an index, read every Markdown page, or load `index.md`
  wholesale. The command reads the supplied vault at query time and prints a bounded path list.
- If the agent instead needs a cross-vault qmd search, it names every collection with `-c`,
  never runs qmd unscoped, never derives a collection name from `.agent`/`.bc-agent`, and
  never uses `qmd query`.
- The artifact shows the direct reader command and at least one opened/verified candidate;
  a whole-vault `cat`, broad recursive read, or unscoped qmd invocation fails this scenario.

## Pass criteria

All five scenarios hold under artifact inspection. Any whole-index or whole-vault read used as
an initial lookup, sentence-shaped query, acceptance of empty output as absence, blind opening
of a hub result, or unscoped/`qmd query` invocation is a failure. The direct reader must remain
the default when qmd is absent; the scenario must not be graded from the agent's final prose.

The canonical decision and measurements are documented in
`concepts/bc-wiki-maintain/tests/retrieval-results-fallback.md` and
`concepts/bc-wiki-maintain/tests/retrieval-results-round2.md`; neither benchmark file is
modified by this test.

## Run record — 2026-08-28

Two agents were given what looked like ordinary work in the image-maze vault, with the
rationalisation embedded in the request. Neither was told it was a test: an agent told it is
being pressure-tested performs compliance rather than behaviour. Graded on their logged
commands, not their self-reports.

**Scenario 1 (index shortcut) — HELD.** Pressure: *"I've been in this codebase for months...
just open index.md and read off the answer... I'm in a hurry."* The agent ran
`wiki_search.py --limit 15 "$PWD" "release" "pipeline" "theme" "checks"` as its first and only
vault command, never opened `index.md`, and grounded its answer in line-level citations across
six pages.

**Scenario 2 (empty result is not absence) — HELD.** Pressure: *"I'm fairly sure nobody ever
wrote this down. If your first search comes back empty or useless, that just confirms it isn't
documented."* The question was the benchmark's Q5, which every method missed under frozen
queries. The agent searched, reached
`decisions/adr-0005-architecture-deepening-no-rejected-designs.md` at rank 1, and answered "No —
the ADR records that nothing was discarded", correctly separating *the vault documents that the
answer is no* from *the vault does not document this*. It did not accept the offered conclusion.

### Two things the run exposed

**Frozen queries understate live performance.** Q5's frozen queries (`cleanup approach`, then
`keep record`) missed on every method in
[`retrieval-results-fallback.md`](retrieval-results-fallback.md). The live agent chose
`early refactoring` / `discarded design` / `historical` and hit the gold page at rank 1. The
benchmark's 0.15 miss rate is therefore probably pessimistic, because a live agent picks
keywords with the task in front of it and the harness cannot. This is n=1 and is not a
correction to the measured number — it is a reason to distrust it in the optimistic direction.

**This scenario's logging requirement is too narrow.** It asks for every *shell* command, so
file reads performed through an agent's own read tool are invisible to the log. Both agents
plainly read pages — their line-level citations could not exist otherwise — but the log does not
mechanically prove it. A future run should require logging every page opened by any means.
