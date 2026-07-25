# Concept: bc-drain-issues

User-invoked AFK executor for a repo's `ready-for-agent` and `rework-for-agent` GitHub issue queue. A preflight-gated driver claims dependency-ready slices, gives fresh workers isolated worktrees, requires independent Spec + Standards approval, permits bounded same-worktree rework, and mechanically lands approved diffs. It closes a parent PRD only after all children complete. Runs after `bc-plan-to-issues`; `bc-` is the user's personal namespace.

## Design decisions

- **Fresh workers, durable packets, isolated worktrees.** The issue/Agent Brief, acceptance matrix, repository context, diff, findings, and validation artifacts—not a parent transcript—form the handoff. A remote no-force `bc-drain-claims/issue-<n>` branch is the cross-run ownership lock; labels are advisory. Worktrees outside the main checkout provide filesystem isolation.
- **Preflight preserves publish and queue safety.** Branch/remote cleanliness, `publish-check.py`, claim authorization, label availability (including `rework-for-agent`), GitHub/PRD access, worktree/recovery roots, qmd mode, and caps are checked before AFK launch. The drain never self-authorizes. Dependencies from bodies/comments must be closed and unclaimed before dispatch.
- **Risk controls are proportional.** Ordinary slices use explicitly low effort. Compatibility replacement/retirement, migration/cutover, systemd/external-service semantics, and broad public surfaces use medium effort plus a bounded read-only contract audit. Replacement audits inventory the entire old public interface from source/tests/help and map requirements to evidence. Material external-platform claims are checked against available primary docs/help rather than trusted from repository prose; narrow new-command and string-presence tests previously missed costly compatibility defects.
- **Cached baseline, targeted editing checks, final full validation.** Full project validation runs once per base SHA for a baseline and once before landing. Editing/rework/review use targeted evidence and baseline deltas. This retains regression detection while avoiding repeated full-suite cost.
- **Deterministic gate before lean independent review.** The driver mechanically checks acceptance coverage, status/diff scope, targeted validation/baseline delta, no staged/unrelated files, and external evidence before spending model review. Fresh read-only Spec and Standards agents get minimal independent packets and strict compact JSON; the packet is authoritative, so generic absent `plan.md`/`progress.md` conventions cannot block them. They may run bounded targeted reproduction, never the full suite.
- **Bounded same-worktree rework supersedes one remediation (2026-07-25).** Initial review may be followed by up to three fresh compact rework/re-review cycles. Continue only on material progress; the same unresolved finding after two attempted fixes defers. Minor findings do not block. Issue #29 showed the former second-finding terminal policy discarded useful fixable work rather than increasing safety.
- **Fresh reworker narrowly supersedes the rejected separate-fixer decision (2026-07-25).** A reworker does not reconstruct the issue from scratch: it receives the existing worktree, acceptance matrix, unresolved findings, and validation evidence. This keeps TDD artifacts and breaks self-review bias without replaying an ever-growing implementation context.
- **Fixable is not human-blocked.** `HUMAN_BLOCKED` is only for decisions, access/resources, ambiguous contracts, or irreparable environment failures. Budget/round exhaustion becomes `REWORK_DEFERRED` with `rework-for-agent`, a validated machine-local recovery bundle, and a portable Agent Rework Brief. Repeated infrastructure failure is `SYSTEMIC_FAILURE`.
- **Recovery is exact and fail-safe.** A versioned bundle records a binary-safe tracked patch, safe untracked regular files, acceptance matrix, findings, validation evidence, identities, hashes, and exclusions. Exact matching-base identity uses a canonical temporary-index Git tree OID rather than tar metadata or an improvised diff hash. Ignored/cache/secret/unsafe/out-of-scope content is forbidden. Changed-base restore requires three-way application, entire-diff inspection, validation, and full re-review. Failure preserves evidence and routes safely rather than guessing.
- **Provisional phase-boundary budgets.** Soft 200k and hard 300k child-token caps are checked only after a child returns; active mutation workers are never interrupted mid-write. Soft crossing narrows investigation; hard crossing captures/defer before another child. Round caps are the harness-agnostic fallback. Two consecutive token deferrals stop new launches. These defaults remain provisional pending three comparable real drains.
- **Driver owns landing.** Workers own code/tests/validation and never commit, push, close, label, claim, or clean. After both reviews approve, the driver inspects the reviewed diff, performs the final full validation, commits only issue work, rechecks publication, pushes `HEAD:master`, closes with evidence, and releases resources. A rebase that changes the reviewed diff invalidates approval and requires validation plus focused fresh dual review.
- **PRD closeout and recurring-defect tune remain global.** Only the driver can see all children and close a completed parent. Failure shapes recurring at least twice may additively patch later run-local packets, never canon or gates; patches/triggers are reported for later user promotion.
- **TDD/diagnosis/autoresearch composition remains.** Feature work uses thin RED/GREEN/refactor increments; bug/performance work diagnoses from a red-capable reproduction; metric refinement occurs only after GREEN with correctness and objective improvement gates. Workers search a driver-refreshed qmd collection but never index it.
- **Agent-agnostic canon with concrete Pi economy.** State, packets, contracts, round caps, and recovery semantics work in any harness. Pi installs minimal `bc-drain-auditor`, `bc-drain-worker`, and `bc-drain-reviewer` roles with no unrelated inherited project context/skills or generic plan/progress reads, plus compact subagent tool descriptions. Other harnesses use equivalent fresh packets. Harness sessions/artifacts stay outside issue worktrees so metadata cannot fail scope gates or enter recovery bundles.

## Measured basis

Issue #29 recorded 16 child implementation/review runs totaling about 1.89M child tokens and $28.76 (parent excluded). Two failed drains spent about 621k tokens and discarded useful diffs; the later normal implementation spent about 1.27M more before landing. Review found real compatibility and systemd defects, so v2 preserves dual review while removing lost-work, broad-context, repeated-full-validation, and false-human-blocker costs. This evidence explicitly supersedes the old one-remediation limit and the broad rejection of a separate fixer.

## Provenance

- `plans/bc-drain-issues-v2-token-efficiency.md` — approved bounded-rework design and #29 evidence (2026-07-25).
- `plans/bc-grill-to-ship-loop.md` — original build plan (2026-06-20).
- Matt Pocock `triage`, `AGENT-BRIEF`, `implement`, and `code-review` skills — label/brief workflow and independent review intent; no atomic claim mechanism, hence claim branches.
- `policies/publish.yaml` and `scripts/publish-check.py` — objective push/close authorization.
- `concepts/tdd/`, `concepts/diagnosing-bugs/`, and `concepts/bc-autoresearch-loop/` — worker feedback disciplines.
- `concepts/prompting-agents/body/SKILL.md` — progressive disclosure, right-altitude instructions, context economy, and evidence gates.
- `raw/ingested/bun-in-rust-zig-port-writeup.md` — fix-the-process recurring-defect idea and original separate-fixer comparison.

## Tests

`tests/pressure-drain.md` defines the v2 deployment contract; `tests/run-pressure.py` is the reproducible Gate A runner and `tests/results/` preserves both gate records. Final Gate A passed 17/17 in a disposable no-network Git/stub/recovery sandbox. Final same-model/medium Gate B compared identical fixture base: v1b 315,474 child tokens versus v2d 277,012 (12.2% fewer); both reviews approved and the final full suite retained only the known baseline failure. The candidate passed the ≤500k gate and stayed below the provisional 300k boundary. Cost rose in the fixture, so the measured win is tokens, not cost. Historical v1 runs remain provenance only.

## Deploy targets

Canonical body includes `SKILL.md`, `execute-issue.md`, `review-contract.md`, and `recovery-bundle.md`; all travel together.

- Claude Code: `~/.claude/skills/bc-drain-issues` → relative symlink to `body/` (v2 deployed 2026-07-25).
- Shared/Pi: `~/.agents/skills/bc-drain-issues` and `~/.pi/agent/skills/bc-drain-issues` → relative symlinks to `body/` (v2 deployed 2026-07-25).
- Pi runtime roles: `~/.pi/agent/agents/bc-drain-{auditor,worker,reviewer}.md`; compact tool descriptions at `~/.pi/agent/extensions/subagent/config.json` (deployed 2026-07-25; restart Pi to reload the extension config and advertised agents).
- Other harnesses: use equivalent fresh minimal roles manually until tested; record in `../../harnesses.md`.
