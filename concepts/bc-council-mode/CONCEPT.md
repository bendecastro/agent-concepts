---
test_kind: pressure
test_status: partial # 2026-11-28 dry run PASS: run folder + manifest before launch (durable-subagents load); 2026-11-26 missing-subagent stop accuracy-checked (no new model run); passed 3/3 after two skill fixes (2026-11-24, Terra/Luna low); pass contracts' outputSchema never used; no-profile fallback untested
tested: 2026-11-28
deployed: yes
---
# Concept: bc-council-mode

Model-invoked protocol for a bounded, parent-supervised advisor council on a decision with real tradeoffs: 2–4 read-only `council-*` advisors write independent structured reports, the parent relays curated disputed claims for one cross-examination round (a third only on request), and the parent alone writes the decision memo. Ships with a `/council` prompt for Pi and example advisor profiles.

## Design decisions

- **Adopted from the `pi-subagents` package (2026-11-24, owner decision).** The owner is making the council a central part of the workflow. Left in the package, it changed with every unpinned `pi-subagents` update and could not be edited; the owner's private skills also depend on its roster cap, fallback and relay rules. Changes from upstream are listed below; everything else is verbatim.
- **Pi-specific mechanics stay.** The steps rely on `pi-subagents` workflow scripts (`runs.all`), resumable runs and `outputSchema`. When upstream changes those, compare against the version recorded under Provenance and update this copy.
- **Launch with `options.script`, not `workflow: true` (2026-11-24).** Upstream told the parent to write a separate `js workflow` block plus `subagent({ workflow: true })`. In pressure runs the parent model lost the block in 2 of 3 runs, so no advisor ran. Putting the script inside the call fixed it (0 failures in 4 runs). Same lesson as `bc-durable-subagents`' Pi notes.
- **Resume entry shape spelled out (2026-11-24).** Upstream said a resume "needs a retained run id" without naming the field; one run passed the id as `id` and the whole cross-examination failed. The skill now gives `{ key, resume: <runId>, task, output: false }`.
- **`/council` prompt lives here (`council-prompt.md`).** The package's prompt loaded the protocol through `subagent({action: "guide", options: {topic: "council"}})`, which always serves the package copy, so owning the skill alone would have left `/council` on upstream. This copy loads the skill instead. In Pi the package's own skill and prompt are excluded with a package filter in `settings.json` so only this copy loads.
- **Loads `bc-durable-subagents` (2026-11-28, work item `053-split-swarm-and-durable-subagents`).** The 2026-11-27 council ran with no run folder until the parent made one by hand. The body now loads the durability skill, with a one-line fallback (run folder, manifest, path in chat) so a skipped load still leaves a recoverable run. Advisors get a distinct `output` path in the run folder instead of upstream's `output: false`, because the loaded contract makes the artifact the durable record and a returned result is lost with the parent's context.
- **Example advisors with distinct stances (`body/examples/agents/`, owner decision).** The upstream template had one stance-neutral profile. In the first pressure run two neutral advisors agreed in round 1 and the cross-examination never ran; giving them opposing stances produced a real dispute every time. The examples (change, compatibility, risk) carry a placeholder model so a stranger swaps in their own; they replace the inline template in `pass-contracts.md` so the profile format has one home.

## Provenance

- `pi-subagents` 0.90.0 (npm; https://github.com/nicobailon/pi-subagents), MIT, © 2026 Nico Bailon — `skills/bc-council-mode/SKILL.md` (sha256 `12d4b7f8e8e1cc1770e85f8c511a690b9f18b23bae3250149602c04ca7575943`), `skills/bc-council-mode/references/pass-contracts.md` (sha256 `f2eb16d989d4396e0fc3147ba2108db08e4e89b9020ab68629a86cb2957836a3`) and `prompts/council.md`. License text kept in [LICENSE-upstream](LICENSE-upstream).
- [bc-durable-subagents Pi notes](../bc-durable-subagents/body/pi.md) — `options.script` as the reliable fan-out form.

## Tests

`tests/dry-run-durable-subagents-2026-11-28.md` — dry run on the pressure-test model: PASS, the plan creates the run folder and manifest before the first launch and routes every advisor output into it.

`tests/scenario.md` — 2026-11-24 pressure runs on cheap advisors (owner asked not to use the real council members): failed twice on launch, then passed 3/3 after two skill fixes; baseline without the skill had no round limit. Gaps: the parent never passed the pass contracts' `outputSchema`; the no-`council-*` fallback and `--max-passes 3` were not exercised.

## Deploy targets

- `scripts/deploy-local-skills.py`: `~/.agents/skills/bc-council-mode`, `~/.pi/agent/skills/bc-council-mode`, `~/.claude/skills/bc-council-mode` (relative symlinks to `body/`).
- Pi prompt: `~/.pi/agent/prompts/council.md` → relative symlink to `council-prompt.md`. Pi settings exclude the package's copies: `{"source": "npm:pi-subagents", "skills": ["!skills/bc-council-mode"], "prompts": ["!prompts/council.md"]}`.
