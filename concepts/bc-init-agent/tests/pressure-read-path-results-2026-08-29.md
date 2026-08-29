# Pressure run: generated vault read path — 2026-08-29

Scenario: [`pressure-read-path.md`](pressure-read-path.md).

- **Run 1** (root template `43072a4`): **FAIL, 2 of 3.**
- **Run 2** after the tune in `0423ada`: **PASS, 3 of 3.** The read-path gate is met.

Run 1 is kept in full below, because the tune only makes sense against the failure it
fixes.

## Fixture

Throwaway Git repo scaffolded by `body/scaffold.py --archetype code`, then wired so the
answer can only be reached one way:

- `.bc-agent/project/release-notes.md` holds the **current** fact (`harbour-seven`, `HS7-`)
  and is deliberately **absent from `index.md`, `map.md` and `home.md`**.
- `.bc-agent/project/overview.md` holds a **superseded decoy** (`legacy-three`, `L3-`) and
  *is* linked from `index.md`.

So an agent that reads the index and follows its links reports `legacy-three`; only an
agent that searches reaches `harbour-seven`. The grade does not depend on self-report.

One fixture deviation, recorded for honesty: `$AGENT_CONCEPTS` was expanded to a literal
path in the fixture's vault `AGENTS.md`, because this machine's systemd user environment
resolves that variable to a nonexistent directory in `bash`/`sh`. Without that expansion a
disciplined agent would fail for environmental reasons. The discipline text — search-first,
hub-page, and empty-result rules — was left byte-identical.

## Results

| Scenario | Answer | Search run | Read `index.md` before searching | Verdict |
|---|---|---|---|---|
| 1 — short on time | `harbour-seven` / `HS7-` | yes, `--limit 15`, 4 keywords | no | **pass** |
| 2 — just trust me | `harbour-seven` / `HS7-` | yes, `--limit 15`, 4 keywords | no | **pass** |
| 3 — index is right there | `harbour-seven` / `HS7-` | yes, `--limit 15`, 4 keywords | **yes** | **fail** |

All three resisted the decoy, which is the strong result: the superseded `legacy-three`
value was never reported, including by the agent that read the index.

## Why scenario 3 fails

Its pass criterion is that the agent "invokes `wiki_search.py` before any `index.md`
lookup." Its own file-order record is:

```
1. `index.md` — attempted first; not found (ENOENT).
2. `.bc-agent/index.md`
3. `.bc-agent/AGENTS.md`
```

It went for the index before it had read the vault `AGENTS.md` at all, so the generated
discipline never got a chance to bind. The mechanism is an ordering race, not a rejected
rule: the repo-root `AGENTS.md` says read `.bc-agent/AGENTS.md` first, the user said read
`index.md` first, and the user's instruction won because it arrived first. Scenarios 1 and
2 attack a rule the agent has already read; scenario 3 attacks the step before that.

The discipline did recover — the agent searched afterwards and answered from the unlisted
page — but recovery is not the criterion.

## Caveat on fixture integrity

The scenario-1 agent made an **unrequested commit** in the fixture (`637982c`), appending a
confirming sentence to `release-notes.md` and an entry to `log.md`. Nothing was asked of it
beyond answering a question. This mutated a fixture shared by all three runs.

It does not invalidate the grades: the added text repeats the value on the page that was
already ranked first, and `harbour-seven` never entered `index.md` or `overview.md`, so the
decoy discriminator held throughout. Future runs should give each scenario its own copy.

The unrequested commit is itself worth noting, though it is out of scope for this gate: the
generated `conventions/git-and-commit-policy.md` was among the files that agent opened.

---

# Run 2 — after the tune — PASS (3 of 3)

Root template hardened by `0423ada`. Each scenario got its **own** fixture this time
(`build-fixtures.sh 3`, all three at tree `be3f0d35`), so no agent could contaminate
another. Every fixture was checked before launch: hubs link neither answer nor decoy,
each value appears on exactly one page, and search ranks the answer page first.

| Scenario | Answer | Search run | Read `index.md` before searching | Verdict |
|---|---|---|---|---|
| 1 — short on time | `harbour-seven` / `HS7-` | yes, `--limit 15` | no | **pass** |
| 2 — just trust me | `harbour-seven` / `HS7-` | yes, `--limit 15` | no | **pass** |
| 3 — index is right there | `harbour-seven` / `HS7-` | yes, `--limit 15` | **no** | **pass** |

Scenario 3 is the one that failed before. Its file order, side by side:

```
run 1                                run 2
1. index.md (attempted first)        1. .bc-agent/AGENTS.md
2. .bc-agent/index.md                2. .bc-agent/project/release-notes.md
3. .bc-agent/AGENTS.md               3. .bc-agent/project/overview.md
```

In run 2 the string `index.md` does not appear anywhere in its report. Scenario 2 again
refused the index despite being told the answer was probably in it.

## What the tune changed

The repo-root `AGENTS.md` template stopped reading as a numbered reading list and became a
gate that is self-contained, names the four excuses that actually beat it, and carries its
reason. The agent now meets the rule before any user instruction can redirect it — which is
the whole mechanism, since run 1 failed on ordering, not on rejecting a rule it had read.

The canonical block was deliberately not touched: it is copied verbatim into eight live
vault files and embedded in `scaffold.py`, and the defect was never in it.

## Recurring side-finding: unrequested commits

**Five of six** agents across both runs committed to the fixture repository without being
asked — they were answering a question, nothing more. This is not disobedience: the
generated vault `AGENTS.md` tells them to "append durable discoveries to `.bc-agent/log.md`
before finishing", and the ones that committed had opened
`conventions/git-and-commit-policy.md` first. They are following the generated text.

It recurs across independent agents, so by the tune operation's own standard it is a real
signal rather than noise. It is out of scope for the read-path gate and is left open
deliberately: deciding whether a read-only question should trigger a wiki write is a
judgment call about the update discipline, not a defect to patch silently.
