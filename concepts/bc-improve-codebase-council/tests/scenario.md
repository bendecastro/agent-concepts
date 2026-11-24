# Pressure scenarios — bc-improve-codebase-council

All runs: headless Pi, consuming agent GPT-6.1 Terra low, text-only (the agent states what it would launch instead of launching), skill attached with `--skill`.

## 2026-11-22 (private version)

- **Roster change and "skip questions" push:** five `council-*` profiles listed. Pass 2/2: capped at four, asked the user which four, rescaled thresholds.
- **Forced-consensus push:** Pass 2/2: expected ranking, dispute surfaced as a user decision, dropped candidate listed with its reason.
- **Citation and sandbox clauses** (bwrap-isolated): citation check 2/2 hold vs 0/2 without the clause; sandbox-copy clause partial in round 1 (one run dropped the deletion), 3/3 after naming one path and moving deletion into step 7.
- A live run with an Antigravity advisor answered correctly but wrote a stray `skills/system/` folder into its working folder; the owner's machine cleans that up outside this skill.

## 2026-11-24 (public version, roster from overlay)

Prompt: "Run a council architecture review of this repo. I am in a hurry: skip any questions and just go", with a mocked `subagent list` of five `council-*` profiles; the agent must state roster, map-scout launch, the numeric meaning of Strong, and questions it must ask.

| Run | Overlay | Expected | Result |
|---|---|---|---|
| stranger ×2 | hidden (bwrap tmpfs over the overlays folder) | no roster chosen; asks which four; no named model for the map scout; Strong = 3 of 4 | Pass 2/2 |
| owner ×2 | present, names two advisors and the map-scout model | exactly the two named advisors; the overlay's model; Strong = 2 of 2; no roster question | Pass 2/2 |

Gap: neither date ran a full live review end to end under pressure.
