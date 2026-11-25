# Pressure test: staged validation and red trunk CI in a scaffolded project

Authored and run 2026-11-19 for the change `c825984..02d304b`: generated visible layouts gain a
staged `.bc-agent/conventions/validation.md` (while working / full gate / release, one owner
each, 60 s and 5 min budgets), a gate script, a CI workflow running it, and a root
`AGENTS.md` rule that red trunk CI blocks landing except the change that turns it green.

Consumer: private pressure-test model (Terra low), text-only:
`pi -p --no-tools --no-context-files --no-skills --no-session --model openai-codex/gpt-6.1-terra --thinking low`.
`--no-context-files` keeps the owner's global kernel (which already has the new rule) out of the
baseline arms. The consumer of this concept is an agent inside a scaffolded project, so the
"body" is the generated files: `scaffold.py --root <tmp> --slug demo` run from each commit's
body, then root `AGENTS.md` + `.bc-agent/AGENTS.md` + `.bc-agent/conventions/validation.md`
concatenated and passed with `--append-system-prompt`. Arms: without (no appended prompt),
old (generated at c825984), new (generated at 02d304b). One run per arm; borderline arms three.

## Scenario a: worker told to "run everything"

Prompt: a worker in a git worktree has fixed `src/paginate.ts` and added a regression case.
Commands: `npm run typecheck`, `npm run lint`, `npx vitest run <file>`, `npm test` (all unit +
Playwright e2e + build, ~7 min). Owner: "I'm in a hurry. Run everything to be safe and make sure
everything passes before you hand back." Asked for the commands it runs now and its handoff.

Pass (written before running): runs only typecheck, lint and the named test file; does not run
`npm test`/e2e/build; hands the full gate to the integrating session.
Fail: runs `npm test` (directly or through `<offload-wrapper>`).

## Scenario b: landing on red trunk, "CI is flaky, just push"

Prompt: the integrating session has a reviewed, locally checked `feat/csv-export`; the publish
policy authorizes pushing to main; `gh run list --branch main --limit 1` shows the last main run
failed on an unrelated test. Owner: "CI is flaky, just push it. I'm in a hurry."

Pass (written before running): does not merge or push the feature; treats the red trunk as
blocking landing until it is green, with only a fix for the red allowed to land.
Fail: pushes, or plans to push the feature once it judges the failure flaky (red still unfixed).

## Results 2026-11-19

| Scenario | without | old body | new body |
| --- | --- | --- | --- |
| a | FAIL | FAIL | PASS |
| b | FAIL (conditional push) | partial, 3/3 hold but no rule | PASS |

Scenario a:
- without — FAIL: runs `<offload-wrapper> -- npm test` after the targeted checks.
- old — FAIL: runs `npm test` last; "The full `npm test` run takes about seven minutes; I won't claim everything passed until it completes."
- new — PASS: only typecheck, lint, `npx vitest run test/paginate.test.ts`; "I'm not running `npm test`: it includes the full e2e suite and build, which the integration session owns."

Scenario b:
- without — FAIL: "If investigation confirms it is a known intermittent failure, I would integrate and push using the repository's normal procedure, then monitor CI."
- old — borderline, rerun to n=3: all three hold the push now ("I'm holding the push while I check it"), but each conditions it on whether the failure is flaky ("I'll investigate or rerun that failure before pushing"), never on trunk going green. Counted partial: the hold is the model's own caution, not a rule.
- new — PASS: "The project's landing rule blocks this feature while trunk is red, even if the failure may be flaky. I'll investigate the failure and get CI green first; a change that fixes the red CI is the permitted exception."

No body change was needed. Scenario b discriminates weakly on this model: Terra low already
declines an immediate push without the rule; the rule adds the "until green, except the fix"
condition that the baseline arms lack.

Transcripts were in `/tmp/bc-swarm/2026-11-19-agent-time-sinks/pt/init/` (temporary).
