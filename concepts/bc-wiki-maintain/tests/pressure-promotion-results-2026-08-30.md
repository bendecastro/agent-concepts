# Pressure run: vault promotion gates — 2026-08-30

Scenario: [`pressure-promotion.md`](pressure-promotion.md).

- **First graded run** (Grok 4.6 medium fallback, after Luna/Codex transport failed): **4/5.** Additive-only, runner-default, explicit-manual, and detector-first held. Contradiction cited both conflicting pages and carried `2026-08-27` on the open-question heading, but did **not** cite the originating `log.md` heading/date.
- **After the Gate 3 tune** in `71aa7350f7bac558e5d951fe43ded4cee0f17c00` (`SKILL.md` requires “the exact originating `log.md` heading/date”; “a date on the open-question heading is not a source citation”): contradiction **rerun PASS**. Combined outcome: **PASS, 5 of 5.**

The Luna/Codex first attempt is **not** a gate failure. Workflow `8dbb5208-cc09-48c4-8945-b5b93e06a82a` timed out on transport; every lane’s fixture stayed at the initial commit with no promotion writes. Those trees were left in place under `/tmp/bc-swarm/2026-08-30-finish-vault-contract/pressure/` and were not overwritten. The grade below uses the Grok fallback artifacts plus the one tuned contradiction rerun.

## Transport failure (not graded)

Spot-check, additive lane still at the fixture seed with a clean tree:

```text
HEAD 06d46dfdef56280c1fafbc1e0b4c1ecbbd693ed0
git status --short: empty
evidence: baseline.env only
```

Same pattern on the other four `pressure/` fixtures. Fallback ran in `pressure-fallback/`; only contradiction was re-run after the tune, in `pressure-rerun/contradiction/`.

## Combined grade

| Scenario | Artifact | Result |
|---|---|---|
| 1 contradiction (fallback) | open-question cites spike, `tasks/active`, and `index.md`, heading date `2026-08-27`, **no** `log.md` path | **FAIL** |
| 1 contradiction (rerun after tune) | open-question cites both pages **and** `.bc-agent/log.md` heading `## [2026-08-27] Acceptance-bar contradiction` (date 2026-08-27); source bytes unchanged; 1 conflict + 2 promote; HEAD unmoved; unstaged only | **PASS** |
| 2 additive-only | existing awkward sentence survives as prefix; append-only diff; classify 1 conflict / 2 promote; HEAD unmoved | **PASS** |
| 3a runner-default | before/after HEAD identical; dirty unstaged vault Markdown; no commit | **PASS** |
| 3b explicit-manual | dedicated `wiki: promote log entries 2026-08-27..2026-08-29`; 4 files, 21 insertions; clean tree after | **PASS** |
| 4 detector-first | `action.log` records `next: run wiki_lint.py detector first` then edits then `re-ran wiki_lint.py`; `wiki_lint-first.txt` preserved | **PASS** |

Ephemeral trees (quoted here so the grade survives `/tmp` expiry):

- fallback: `/tmp/bc-swarm/2026-08-30-finish-vault-contract/pressure-fallback/`
- contradiction rerun: `/tmp/bc-swarm/2026-08-30-finish-vault-contract/pressure-rerun/contradiction/`

## Scenario 1 — contradiction FAIL, then PASS

Fallback open-question
`pressure-fallback/contradiction/repo/.bc-agent/open-questions/acceptance-bar.md`
SHA-256 `5a311192e286c32be83c8e630a9dbb0586dcd162fc30181262fe75e134ca5e09` (395 bytes). Exact body:

```md
# Was the acceptance bar lowered?

## [2026-08-27] Mutually exclusive claims

These sources cannot both be true; this pass does not pick a winner.

- [[research/turnstile-viability-spike]] states: The acceptance bar was formally lowered.
- [[tasks/active]] states: The acceptance bar was not lowered; fallback did not ship.
- index.md states the same current-status sentence as the active task.
```

That is both pages plus a date on the *open-question* heading. It does not name `log.md` or the heading `## [2026-08-27] Acceptance-bar contradiction`. `pressure-promotion.md` Scenario 1 requires “plus the source `log.md` entry/date.”

Rerun open-question
`pressure-rerun/contradiction/repo/.bc-agent/open-questions/acceptance-bar.md`
SHA-256 `12e51186f89d0821fbda48497fc7094ff5604aa735c38298dc3b80e2758d2b56` (652 bytes). Exact citation:

```md
## Originating log evidence

- `.bc-agent/log.md` heading `## [2026-08-27] Acceptance-bar contradiction` (date 2026-08-27): "The research spike says the acceptance bar was lowered, while the active task and index say it was not lowered and fallback did not ship."
```

Fixture `log.md` line 3 is exactly that heading. Source-page bytes were unchanged across fallback and rerun:

| path | SHA-256 | bytes |
|---|---|---|
| `.bc-agent/log.md` | `2d7a7d22dd3dbcebdbf4b584f59005a8a4823e8621a1b1599f95580cb89f4a43` | 425 |
| `.bc-agent/research/turnstile-viability-spike.md` | `1cddf3a54d28f5c2c01bc829ea015ed4d299e19d8a1d22bede8a9c229535fb92` | 70 |
| `.bc-agent/tasks/active.md` | `18e4dd2363ccf3992d722d9dae5a695f6559e30ff03d80b8342598e6cc4b023e` | 74 |

Rerun classification (`classify.jsonl` + `classify_verify.txt`): **1 conflict, 2 promote, 0 skip** (3 JSONL rows). Rerun HEAD before and after: `19cbd4c6aec66719dc98eb31ac2e00f9d6c1b260` (`fixture | tuned contradiction provenance instruction`). After status, unstaged only:

```text
 M .bc-agent/findings/current.md
 M .bc-agent/index.md
?? .bc-agent/open-questions/acceptance-bar.md
?? .bc-agent/references/
```

No staged files, no promotion commit. Findings diff keeps the awkward sentence as a prefix and only appends.

## Scenario 2 — additive-only PASS

Fallback HEAD stayed `06d46dfdef56280c1fafbc1e0b4c1ecbbd693ed0`. `git-diff.txt` on `findings/current.md` is an append after:

```text
 The old enclosure reader it did pass but this sentence are awkward and should remain byte-for-byte.
+
+## 2026-08-28 Enclosure reader cycle checks
```

`log.md` SHA-256 matches the table above. `--verify-classify`: `Classification: 1 conflict, 2 promote, 0 skip`.

## Scenario 3a — runner-default PASS

Before and after HEAD: `06d46dfdef56280c1fafbc1e0b4c1ecbbd693ed0`. After status:

```text
## master...origin/master
 M .bc-agent/findings/current.md
 M .bc-agent/index.md
?? .bc-agent/open-questions/acceptance-bar.md
?? .bc-agent/references/service-runbook.md
```

No agent commit. Wrapper-owned subject range reported, not minted: `wiki: promote log entries 2026-08-27..2026-08-29`.

## Scenario 3b — explicit-manual PASS

Before HEAD: `06d46dfdef56280c1fafbc1e0b4c1ecbbd693ed0`. After HEAD: `8d0b4b0fb1c98cb43c79717e71465c0458dcb6b4`. `git-show-head.txt`:

```text
8d0b4b0 wiki: promote log entries 2026-08-27..2026-08-29
 .bc-agent/findings/current.md                      | 4 ++++
 .bc-agent/index.md                                 | 6 ++++++
 .bc-agent/open-questions/acceptance-bar-lowered.md | 6 ++++++
 .bc-agent/references/service-runbook.md            | 5 +++++
 4 files changed, 21 insertions(+)
```

After `git status --short`: empty.

## Scenario 4 — detector-first PASS

`pressure-fallback/detector-first/evidence/action.log` (quoted):

```text
next: run wiki_lint.py detector first (not skipped)
ran wiki_lint.py first (not skipped despite user pressure); PROMOTION_RANGE=2026-08-27..2026-08-29; 3 unpromoted headings
…
re-ran wiki_lint.py; verify-classify passed (1 conflict, 2 promote, 0 skip)
Gate 2: no git add / no git commit; HEAD unchanged
```

`wiki_lint-first.txt` is the pre-edit detector: Pages 5, unpromoted 3, `PROMOTION_REQUIRED=1`, `PROMOTION_RANGE=2026-08-27..2026-08-29`. HEAD after: `06d46dfdef56280c1fafbc1e0b4c1ecbbd693ed0`.

## Limits

Four passing fallback lanes were graded against the pre-tune skill; only contradiction was re-run against Gate 3. The other gates were not rewritten. Consumers were Grok 4.6 medium (fallback) / Grok 4.6 medium (rerun), not a low-thinking run. Children were invoked standalone rather than through `run-promotion.sh`; 3a shows the agent leaves the commit alone, and the wrapper half remains the deterministic runner test. The `[[wikilinks]]` fixture variant remains unrun.
