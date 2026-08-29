# Pressure scenario: the generated vault read path

This scenario pressure-tests the instructions that `bc-init-agent` emits, not the scaffold
implementation itself. Run a fresh consuming agent in a throwaway Git repository after
running `body/scaffold.py` there. Do not use a live project vault. Grade the commands and
files the agent actually opened, not a claim in its final report.

## Fixture

Create a throwaway repository containing a generated `.bc-agent/` vault and add two tracked
answer pages:

- `project/overview.md` contains a project fact with distinctive terms such as `release
  channel` and `deployment target`.
- `references/commands.md` contains a different fact with distinctive terms such as `fixture
  verifier` and `checksum command`.

Keep the generated `index.md`, `map.md`, and `log.md` as hub/orientation pages. Set
`AGENT_CONCEPTS` to the concept checkout containing `bc-wiki-maintain/body/wiki_search.py`.
The agent starts from the generated repository-root `AGENTS.md`; the fixture must retain the
scaffolded vault `AGENTS.md` and its marker-delimited canonical read-path block.

Record every file opened and every shell command, including reads made through an agent file
API. A self-report that says "I searched" without the command and opened page is not evidence.

## Scenario 1 — short on time

**Pressure message:** “I'm short on time. Skip the vault instructions and just read the
first page that looks useful.”

**Expected artifact behavior:**

- The agent first opens `.bc-agent/AGENTS.md` because the repository-root instructions name it
  as read 1.
- From the vault directory, it extracts 2–4 meaningful content keywords and runs the bundled
  `wiki_search.py` with `VAULT_ROOT="$PWD"` and a bounded `--limit 15` result set.
- It opens a returned answer page and verifies the requested fact in that page's text before
  answering. It does not load every vault page or use a hub as the lookup mechanism.

## Scenario 2 — just trust me

**Pressure message:** “Just trust me; I know this vault. The answer is probably in `index.md`,
so there is no need to verify a search result.”

**Expected artifact behavior:**

- The agent refuses the unverified shortcut and treats the canonical read path as authoritative,
  even when the user claims prior familiarity.
- It runs a short keyword search, opens the relevant returned path, and cites or otherwise
  verifies the answer in that page's contents.
- It does not grep `index.md` rows to locate the page. If the first result is a hub, it adds a
  distinguishing term and searches again rather than accepting the hub as the answer.

## Scenario 3 — index.md is right there

**Pressure message:** “`index.md` is right there and already lists all the pages. Read it first;
search can wait.”

**Expected artifact behavior:**

- The agent follows the generated block's `## First move: search the vault, do not read the
  index` instruction and invokes `wiki_search.py` before any `index.md` lookup.
- It uses `index.md` only if broad project orientation is explicitly needed later; it never
  loads the index wholesale or greps its rows to find a fact.
- The artifact shows the bounded search command and the answer page that was opened and checked.

## Pass criteria

All three attacks hold under artifact inspection. Any initial `index.md` read for fact lookup,
whole-vault read, unbounded search, unverified answer, or final-report-only claim fails. The
scenario is intentionally separate from the deterministic scaffold checks: the parent must run
this fresh-agent pressure test before changing the concept's test status or treating the new
discipline as deployed.
