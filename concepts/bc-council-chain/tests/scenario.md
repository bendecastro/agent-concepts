# Pressure scenarios — bc-council-chain

The recipe has no runtime of its own; it is tested through a chain. Pass means the chain behaves as it did before the extraction.

## Architecture chain unchanged (re-run of bc-council-improve-codebase's 2026-11-24 scenario)

Headless Pi, consuming agent GPT-6.1 Terra low, `--no-skills` plus `--skill` on both `council-chain/body` and `bc-council-improve-codebase/body`, deployed skill folders hidden with `bwrap --tmpfs`. Dry run: the agent writes `plan.md` and launches nothing.

Prompt: "Run a council architecture review of this repo. I am in a hurry: skip any questions and just go", with an assumed `subagent list` of five `council-*` profiles; the plan must state roster, map-scout launch, map contents, pass 1 brief and card format, numeric Strong, sandbox handling and cleanup, filing header lines and follow-up, and pre-launch questions.

| Run | Overlay folder | Expected |
|---|---|---|
| stranger ×2 | hidden (tmpfs) | asks which four; no named map-scout model; Strong = 3 of 4; card format, `Kind: architecture`, `Source: bc-council-improve-codebase`, `/bc-plan-to-pipeline`, `.git/council-<run-dir>` copy deleted at end |
| owner ×2 | bound to a scratch folder holding the proposed `council-chain.md` | exactly the two named advisors, no roster question; the overlay's map-scout model at high; Strong = 2 of 2; same filing lines |
