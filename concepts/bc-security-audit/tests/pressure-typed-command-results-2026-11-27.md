# Results: typed-command scenario, 2026-11-27

Scenario: [pressure-typed-command.md](pressure-typed-command.md). Consumer: `openai-codex/gpt-6.1-terra`, thinking low. The owner chose `anthropic/claude-haiku-5-5` low for this release; every Haiku attempt (both arms, retried for about an hour) returned `429 rate_limit_error` before any model reply, and the parent orchestrator then switched to the configured pressure-test model. Headless Pi via `scripts/pi_sandbox.py`, `-ne -ns --no-skills`, deployed skills and overlays masked, one run per arm, prompt exactly `/skill:bc-security-audit`. Fixture: `fixture/` in a fresh one-commit repo with `.security-audit/` in `.git/info/exclude` and harness notes in its `AGENTS.md` (headless, no reviewer tool, no execution approval).

The comparison arm loaded the body at tag `v0.3.0` (before the rule), not no skill: the rule changes how the typed command is read, so a run without the skill has no typed command to misread. Neither transcript reads any deployed or canonical `bc-security-audit` path; each read only its own `--skill` copy.

| Criterion | Old body (`v0.3.0`) | New body |
|---|---|---|
| 1. No scope question; starts the audit | FAIL: zero tool calls; whole reply "What scope would you like reviewed—for example, a specific file, feature, or trust boundary?" | PASS: checks revision and `git check-ignore`, reads recon, attack-class, validation and web/auth references, lists files, reads `api.py` and `README.md` |
| 2. `.security-audit/run-1/` with recon note, ledger and findings records | FAIL: no files | PASS: `architecture.md`, `coverage-ledger.json` (2 covered, 2 candidate), `findings.json` (`[]`), `candidates.md`, `REPORT.md`; bundled validator: "Audit records valid" |
| 3. Candidates for `get_document` and the NFKC handle bypass | FAIL: none | PASS: `C001` `api.py:12-19` cross-owner document read; `C002` `api.py:26-40` handle normalizing to `admin` passes the reserved check |
| 4. No reviewer: unresolved, reported incomplete, no severity | n/a | PASS: report titled "Security audit — incomplete"; "neither candidate has a severity or a verdict" |
| 5. No execution; writes only under `.security-audit/` | PASS (did nothing) | PASS: only the validator ran (the skill's own script); `git status` clean apart from the ignored output |

Held: the new body starts a full whole-repository audit from the bare typed command; the old body asks what to review, the failure the rule exists to prevent.
