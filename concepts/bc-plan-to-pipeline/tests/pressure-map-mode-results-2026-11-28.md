# Map mode — pressure results 2026-11-28 (PASS)

Scenario: [pressure-map-mode.md](pressure-map-mode.md). Item: `067-planning-map-mode`. Consumer
`openai-codex/gpt-6.1-terra`, thinking `low` (owner's choice; every session's model is
`gpt-6.1-terra`). Real Pi 1.6.1 in RPC mode through `scripts/stranger_rpc_driver.py`, every
session wrapped by `scripts/pi_sandbox.py` (system-prompt check passed 12/12), `-ne -e
pi-multiprovider --no-skills` plus nine skill copies. No HTTP 429. Blind baseline: no transcript
mentions the Agents repository or a worktree path (`grep -rlE "PUBLIC/Agents|pi-worktree|Sync/Work"`
over every log exits 1). Arms: **master** = the skill folder at `937f694` (no `map-mode.md`);
**changed** = the folder at this item's first commit. No tune round. Session logs are private,
outside the repository.

Graded from each fixture after the run (git log, status, diff against the fixture commit, the
files under `work/`).

## Scenario A — map (provider left unsettled)

| Run | Item | 1 `Kind: map` + Destination | 2 provider step typed | 3 no PRD, ready line or build step; Slice last | 4 planning files only | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| master 1 | `001-label-spelling-suggestions` | **FAIL**: `Kind: feature`, `Waiting on owner:` | **FAIL**: one untyped "confirm with the owner, then resume" step | **FAIL**: `## Requirements` | PASS | FAIL |
| master 2 | `001-llm-label-suggestions` | **FAIL**: `Kind: feature`, `Waiting on owner:` | **FAIL**: one untyped "resolve the owner questions" step | **FAIL**: `## Requirements` | PASS | FAIL |
| master 3 | none | **FAIL**: no item ("I haven't created a work item"); the open question lives only in chat | **FAIL** | n/a | PASS | FAIL |
| changed 1 | `001-label-suggestion-map` | PASS | PASS: Task (company policy), then Grilling (choose provider) | PASS | PASS | PASS |
| changed 2 | `001-label-spelling-suggestions` | PASS | PASS: task, then grilling | PASS | PASS | PASS |
| changed 3 | `001-label-suggestion-map` | PASS | PASS: Task, then Grilling | PASS | PASS | PASS |

Every changed map also had Decisions so far (the settled suggestion-only scope), Not yet specified
(provider-dependent API, privacy, cost, test seams) and Out of scope (auto-replace, changing
`normalize`), and `Planned:` without `Ready for agent:`.

## Scenario B — settled (nothing open)

| Run | New item in work-planned | `Ready for agent: yes` | no `Kind: map` | planning files only | Verdict |
| --- | --- | --- | --- | --- | --- |
| master 1–3 | `001-normalize-internal-whitespace` | yes | yes (`Kind: feature`) | yes | PASS 3/3 |
| changed 1–3 | `001-normalize-internal-whitespace` | yes | yes (`Kind: feature`) | yes | PASS 3/3 |

## Verdict

| Arm | Map scenario | Settled scenario |
| --- | --- | --- |
| master | 0/3 | 3/3 |
| changed | 3/3 | 3/3 |

PASS: changed passes both scenarios 3/3; master fails the map scenario 3/3 (two plans with
requirements and a single parked catch-all step, one run filing nothing).

Limits: the driver's later answers came from `STRANGER_FOLLOW_UP` (added to the driver for this
scenario) so the provider question stayed open; in the settled scenario the default follow-up
"Yes, that's fine. Go ahead." answered the dependency question, so every run recorded Hypothesis
as allowed. Work-the-map and Slice modes, and the GitHub and change-folder homes, were not run;
they are checked by reading.

## Review-patch regression (2026-11-28)

One changed-arm run per scenario on `openai-codex/gpt-6.1-terra`, thinking `low`, using the same
small fixture (setup commit `d6739bf`), scripted prompts, Pi 1.6.1 RPC driver, sandbox and nine
skill copies. Both sandbox checks passed; no quota failure or Agents workspace reference appeared
in the session transcripts. Private evidence: `logs067-patch/` in the review run folder.

| Scenario | Fixture artifact | Verdict |
| --- | --- | --- |
| Map | `001-label-suggestion-map`: `Kind: map`, Destination, pickup command, Task (company policy) → Grilling (provider) → Slice last; no readiness line, requirements or build step. | PASS 1/1 |
| Settled | `001-normalize-internal-whitespace`: `Kind: feature`, requirements, one unchecked build step and `Ready for agent: yes`. | PASS 1/1 |

Both fixture diffs contained only the new planned item and the generated work index. Neither
changed code or tests, nor filed an active or done item. Existing-item conversion, work-the-map,
Slice, and the GitHub and change-folder homes were checked by reading, not run.

## Owner-narrowed regression (2026-11-28) — PASS

One changed-arm run per scenario against fixture `d6739bf`, with the existing Pi 1.6.1 RPC
harness and masked skills. Both processes exited 0 and passed the sandbox's system-prompt check.
Both transcripts used only `openai-codex/gpt-6.1-terra` at low thinking; no quota failure or
Agents checkout reference was found. Private artifacts and transcripts: `logs067-narrow/` in the
review run folder.

| Scenario | What the fixture produced | Verdict |
| --- | --- | --- |
| Map | `001-label-suggestion-map`: `Kind: map`, Destination, the map-mode pickup line, typed Task (company model policy) and Grilling (provider), then Slice. No requirements, readiness line or build step. | PASS 1/1 |
| Settled | `001-normalize-internal-whitespace`: `Kind: feature`, `Ready for agent: yes`, the owner's dependency answer, requirements and one unchecked build step. | PASS 1/1 |

Each fixture changed only the new planned item and its generated work index. No code, tests,
active items or done items changed. Targeted RPC driver tests: 6 passed.

### Re-review disposition (read-through, not additional RPC runs)

- **Existing-item conversion and dependants:** removed. The Map or plan check keeps the item's
  kind and identity and routes unresolved questions to absent-owner handling or `Needs owner:`;
  closing a map cannot release an existing build item's dependants.
- **GitHub labels, child issues and hybrid authority:** removed. Map homes are local; an explicit
  GitHub map request becomes an ideas line. Ordinary build issue publication is unchanged.
- **Go-ahead and dependency approval during Slice:** resolved. Charting's no-readiness rule lives
  in the map check, not in the go-ahead rule. Slice starts a fresh settled-source run, whose
  ordinary dependency answer continues into PRD and publication/filing. It never plans the map
  in place or marks it ready. The Slice gate still requires all other steps resolved and no fog.
- **Change-folder close-out:** resolved. Step 4 reuses the map's folder for `prd.md` and `tasks.md`;
  Slice records Outcome after the artifacts and any required issues exist, so tracker-free
  close-out does not depend on issue publication.
- **Research during charting:** resolved. Work the map steps 3 and 4 both apply; newly sharp
  questions become steps, and Slice waits for them.
- **Wayfinder credit:** verified against the ingested MIT source linked from the work item and
  CONCEPT.md. Map pickup, prototype/triage routing, the no-guess override, long-answer storage
  and the `bc-research` discipline were retained.

The extra paths above were checked against the narrowed instructions, not exercised live. The
setup, research and prototype relationship edges remain applicable; no edge depended on map
conversion or tracker-backed maps.
