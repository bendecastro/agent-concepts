---
test_kind: pressure
test_status: pass # 2 with-skill runs each confirmed 9/10 planted bugs, no decoy; blind baseline also confirmed 10/10 but kept no report, tiers or worktree; filing step not run
tested: 2026-11-24
deployed: yes
---
# Concept: find-bugs

User-invoked bug hunt over a named area (or a small whole repo). It collects candidates with quoted evidence, reproduces the strongest as failing tests on a hunt branch in a separate worktree, and reports two tiers: **Confirmed** (a reproduction watched failing for the stated reason) and **Suspected** (ranked by evidence, each with why it is not confirmed). After the owner answers, confirmed bugs become `Kind: bug` work items linked to their tests.

## Design decisions

All from the owner-approved [council bug hunt plan](../../docs/plans/implemented/council-find-bugs.md); numbers below are that plan's decisions.

- **Standalone parent, council chain later (decision 1).** This skill is the single-agent form. A later `bc-council-find-bugs` chain reuses its candidate block (section 2), reproduction step (3), report (4) and filing (5) unchanged and adds only the council steps; keep those sections self-contained so the chain can point at them.
- **Bounded scope (decision 2).** A named area, or the whole repo only when small; `--since <ref>` narrows to changed code.
- **Proof, not confidence (decision 3).** Only a reproduction watched failing for the stated reason confirms a bug; the test asserts the expected behaviour so it turns green when the bug is fixed. This applies `tdd`'s "watch it fail for the right reason" to bug reports.
- **Reproductions on their own branch (decisions 4, 9).** One agent writes them in a separate worktree on `find-bugs/<hunt-name>`, in the project's test framework or, without one, a script that prints the wrong result and exits non-zero. Failing reproductions are kept and committed: the branch's suite is red on purpose, and filed items name the test.
- **Hunted kinds (decision 7).** Five focuses (inputs/edge cases, error paths, state/data lifecycle, concurrency/ordering, contracts between modules); the chain deals the same list to advisors (decision 8). Security seen in passing is reported as `Kind: security` with a pointer to `security-audit`, not audited. Slowness is out of scope (that is `diagnosing-bugs`' performance loop).
- **Limits (decision 11).** 12 reproductions by default, 10 minutes each, `--max-repro N` raises it; the rest stay suspected, "not attempted". The per-advisor candidate cap belongs to the chain.
- **Filing mirrors improve-codebase-architecture (decision 5).** Report first, owner decides, then: confirmed → `Kind: bug`, `Source: find-bugs` work items placed by the project's work-item rules and `work_index.py --check`; picked suspected → investigation items; rejected → dropped item with the reason; the rest → ideas-file lines; numbered items only from the main checkout. Without a work pipeline the skill files nothing and says so, as `improve-codebase-architecture` does without its table.
- **Report lives on the hunt branch.** A Markdown report at the hunt worktree root, committed with the tests, so items and the report travel together. Choice made here (the plan does not say where the report goes): the branch already holds the evidence and outlives the session, and a temp file would not.

## Provenance

- [Council bug hunt plan](../../docs/plans/implemented/council-find-bugs.md) — owner decisions 1–11 and build order.
- [improve-codebase-architecture](../improve-codebase-architecture/body/SKILL.md) — report-then-owner-decides flow, filing roles, `Kind:`/`Source:` lines, main-checkout numbering, no-pipeline fallback.
- [diagnosing-bugs](../diagnosing-bugs/body/SKILL.md) — reproduction-first stance; owns diagnosing and fixing a bug once filed.
- [security-audit](../security-audit/body/SKILL.md) — hand-off target for security findings.
- [tdd](../tdd/body/SKILL.md) — a reproduction must be watched failing for the stated reason.
- [prompting-agents](../prompting-agents/body/SKILL.md) — instruction phrasing (rule plus why).
- [bc-init-agent](../bc-init-agent/CONCEPT.md) — `Kind:` placement by `work_index.py --check`.

## Tests

[`tests/scenario.md`](tests/scenario.md) runs the skill on [`tests/practice-project/`](tests/practice-project/) (ten planted bugs, two per focus, plus decoys; key in [`tests/answer-key.md`](tests/answer-key.md), never copied into a run). [Results 2026-11-24](tests/results-2026-11-24.md): both with-skill runs pass; the filing step (owner's answer, work items) was not exercised. Invoke the skill by slash command in tests: `disable-model-invocation` hides it from the model's list.

## Deploy targets

Not deployed. When deployed: the shared skill bus via `scripts/deploy-local-skills.py`.
