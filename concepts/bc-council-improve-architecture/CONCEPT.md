---
test_kind: pressure
test_status: partial # roster, agreement and citation rules held (2026-11-22, 2026-11-24); full live review never pressure-tested end to end; Kind line rides on the bc-setup-project placement rule (tested 2026-11-24); this skill's Kind/hand-off lines not run; plan-every-item change 2026-11-24 (recommend paragraph removed; hand-off via parent skill) not run (bc-plan-to-pipeline/tests/pressure-plan-every-item-results-2026-11-24.md covers bc-find-bugs only)
tested: 2026-11-24
deployed: yes
---
# Concept: bc-council-improve-architecture

Runs `bc-improve-codebase-architecture` through the advisor council (`bc-council-mode`): one scout maps the codebase, every advisor proposes deep-module candidates from that map, they cross-examine each other's candidates, and candidates are ranked by evidence-backed agreement before the normal report and grilling.

## Design decisions

- **`Kind: architecture` and a slicing hand-off (owner decision 2026-11-24).** Filed items carry `Kind: architecture`; placement follows the kind, not the skill, below the existing top group so new items cannot flood ahead of the owner's. After filing, the council recommends `/bc-plan-to-pipeline` per chosen item, reusing the grill's settled answers so the owner is not asked twice.
- **One shared map (owner, 2026-11-22).** A single scout maps the codebase once; advisors judge the map rather than each scanning the tree. Why: separate scans make disagreements come from what each advisor happened to read, not from judgment.
- **Agreement by evidence, not vote (owner, 2026-11-22).** Disputes the code cannot settle go to the user; unanimity is not required, and single-advisor finds are kept as Speculative.
- **Roster discovered at run time, thresholds as shares of N.** The council's membership changes; a rule written for three advisors breaks when a fourth joins.
- **The map scout runs on a strong model with high effort (owner, 2026-11-22, after the first live run).** Every advisor judges from the map, so its depth caps the review.
- **Citations checked before merging (owner, 2026-11-22, from a session reflection).** In the first live run an advisor cited a test file that does not exist.
- **Sandboxed advisors get a copy of the map inside the repo.** In the first live run an Antigravity advisor's sandbox refused the run directory twice; the copy goes under `.git/` and step 7 deletes it.
- **Composes the two parent skills by reference; it restates neither.**
- **Shared council steps moved to `bc-council-chain` (2026-11-24, owner plan `work/3-done/2026-11/019-council-find-bugs.md`).** Roster, shared map, pass 1, merge, pass 2, fallbacks and sandbox-copy cleanup now live in [bc-council-chain](../bc-council-chain/CONCEPT.md), moved without behaviour change when `bc-council-find-bugs` became the second chain. This skill keeps only its job-specific parts: map contents, candidate card, duplicate and agreement rules, report, filing and hand-off. The private overlay `~/.config/agent-concepts/overlays/bc-council-improve-architecture.md` is replaced by `~/.config/agent-concepts/overlays/bc-council-chain.md`, which every chain reads.
- **Published 2026-11-24 (owner decision); machine specifics moved to a private overlay.** Written as a private concept because it depended on the owner's `council-*` profiles. Publishing replaced the named map-scout model with "a strong model with high effort" and the Antigravity-specific paragraphs with a general sandbox rule, and points strangers to `bc-council-mode`'s example advisor profiles. The optional overlay `~/.config/agent-concepts/overlays/bc-council-improve-architecture.md` names a fixed roster and the map-scout model; when it names a roster, discovery is skipped. The owner's overlay uses two advisors for this review while `/council` keeps all three (owner, 2026-11-24).
- **Renamed 2026-11-24 from `bc-improve-codebase-council` (owner decision).** More skills that run a parent skill through the council are planned; a shared `bc-council-` prefix groups them in skill lists and slash-command completion, and the rest of the name keeps the job. Work items filed before the rename keep `Source: bc-improve-codebase-council`.
- **Planning handoff moved to the parent (2026-11-24, owner decision).** The closing recommendation to run `bc-plan-to-pipeline` is gone: `bc-improve-codebase-architecture`'s filing step now runs it on every chosen item, and this chain hands over to that step unchanged, so a copy here would be a second home.

## Provenance

- Owner design, 2026-11-22; live run and session reflection the same day.
- Composes [bc-council-chain](../bc-council-chain/CONCEPT.md), [bc-improve-codebase-architecture](../bc-improve-codebase-architecture/CONCEPT.md) and [bc-council-mode](../bc-council-mode/CONCEPT.md).
- Owner decision 2026-11-24: every item in work-planned gets the `bc-plan-to-pipeline` treatment before it starts (filing-time handoff, pickup rule, `Planned:` marker).

## Tests

[tests/scenario.md](tests/scenario.md) — roster cap, forced consensus and citation checks (2026-11-22), and the public/overlay roster split (2026-11-24). Gap: a full live review has not been pressure-tested end to end.

## Deploy targets

`scripts/deploy-local-skills.py`: `~/.agents/skills/`, `~/.pi/agent/skills/`, `~/.claude/skills/` (relative symlinks to `body/`).
