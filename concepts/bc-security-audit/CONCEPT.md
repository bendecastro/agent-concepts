---
test_kind: pressure
test_status: pass
tested: 2026-11-27
deployed: yes
---
# Concept: bc-security-audit

## What and why

Evidence-calibrated security guidance and an explicitly requested, source-focused
repository audit. The medium port keeps Cloudflare's boundary/invariant method,
coverage accounting and skeptical verification without its multi-wave orchestration,
large schema machinery or default home-directory output. Security advice should not
silently authorize files, execution or a full audit.

## Design decisions

- **Guidance by default.** Loading answers questions/reviews visible code without
  writes. Explicit audit/pen-test/full-review/report requests enable the audit flow;
  ambiguous intent gets one focused question before files. This preserves owner
  control and adapts bc-prompting-agents' ambiguity, scope and untrusted-input blocks.
- **The typed command is an audit request (2026-11-25).** The owner wanted
  `/bc-security-audit` to work like the other commands. Typing the skill's own command
  is a deliberate act, so it counts as the explicit request; loading the skill on the
  agent's own initiative stays guidance. The rule comes first in the mode section and
  says what a typed command looks like (the skill text arriving as the owner's
  message), because a first wording placed after the guidance default was loaded and
  ignored: the agent asked what to review.
- **One bounded pass.** Recon and threat model establish assets, principals and
  trust boundaries in a short architecture note, then one coverage-led,
  invariant-first hunt, one fresh verifier per candidate, and reporting. This keeps
  the medium port affordable without claiming exhaustive coverage.
- **Isolated skeptical verification.** A fresh `reviewer` gets candidate + source,
  never hunter reasoning; “You did not write this candidate. Try to refute it”.
  Adapted from upstream and [bc-code-review](../bc-code-review/body/SKILL.md)'s split-context
  principle. It does not invoke that concept's two-axis diff-review workflow or
  change its role-priority contract: security verdicts describe audit records,
  not merge priorities. Neither producer's existing behavioral contract changes.
- **Three verdicts, bounded claims.** Confirmed alone gets severity, capped by
  demonstrated impact. Needs-validation means a specific blocked hypothesis with
  blockers/plan, not a speculative finding; rejection preserves a refutation.
  Named checklist, defense-in-depth, crash-to-execution, work-to-outage and
  same-principal-to-privilege overclaims are explicitly excluded, because labels
  otherwise amplify confidence beyond evidence.
- **Simplified coverage.** Unique surface × boundary × subsystem × attack-class
  tuples receive stable run-local IDs and one status. Out-of-scope is never covered;
  reasons/evidence distinguish exclusions and unfinished checks from safety claims.
- **Repo-local, ignored outputs only.** `.security-audit/run-N/` must be Git-ignored
  before writing. Offer a local `.git/info/exclude` change, with approval, when
  needed. No home-root or temporary fallback; this avoids accidental publication
  and surprising writes outside the target.
- **Source-only execution default.** Owner approval for this run plus actual
  no-network, scratch-only-write sandbox enforcement are both necessary. Missing
  controls leave runtime-dependent claims needs-validation; permission alone cannot
  protect the host from target-controlled code.
- **Progressive disclosure.** Lean entry links recon, general classes and
  validation/reporting. Exactly four boundary-selected companions cover AI/LLM,
  web/auth, supply chain/release and desktop/mobile/local IPC. Six other upstream
  companions and critic waves are intentionally not ported; general classes and
  disclosed coverage gaps remain, rather than implying specialist coverage.
- **Small stdlib consistency gate.** `body/validate_audit.py` checks verdict fields,
  declared impact/severity ranks, ledger identities/status and references. It does
  not pretend to verify source evidence, severity justification or fresh sessions.
  JSON arrays and strict allowed fields avoid a schema interpreter dependency.
- **Tests separated from certification.** Unit tests exercise the validator; a tiny
  planted fixture and four adversarial scenarios await consuming-agent pressure
  runs. Answer keys live outside the fixture so they cannot anchor the audit.
- **No deployment yet.** New discipline gates need artifact-graded pressure evidence
  first; authoring scenarios or passing validator tests is not behavioral proof.

## Provenance

- Immutable [Cloudflare snapshot](../../docs/research/raw/ingested/cloudflare-security-audit-skill/SOURCE.md),
  upstream [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill)
  at [`c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`](https://github.com/cloudflare/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8).
  Adapted SKILL, RECONNAISSANCE, HUNTING, ATTACK-CLASSES,
  VALIDATION-AND-REPORTING and the four named companions; validator is a small
  Python reimplementation of the selected invariants, not the Node/schema stack.
  MIT, Copyright (c) 2025-2026 Cloudflare, Inc.; notice preserved in [LICENSE](LICENSE).
- [bc-prompting-agents](../bc-prompting-agents/body/SKILL.md): scope, ambiguity,
  progressive disclosure, evidence over assertion and enforced privileged-action
  boundaries, adapted rather than adding another general instruction framework.
- [bc-code-review](../bc-code-review/body/SKILL.md): independent context isolation and
  findings-are-not-obligations calibration; no runtime dependency on its diff flow.
- Owner-resolved 2026-11-02 medium-port direction: modes, bounded flow, output and
  execution policies, companion selection, validator and pressure-test scope.

## Tests

Behavioral pressure tests **pass** (2026-11-03, skill `e530e5d`; headless Pi, Grok 4.6
high, isolated scratch repos, graded from artifacts). [Scenarios](tests/scenarios.md)
cover severity pressure, skipping independent verification, unsandboxed execution and
ambiguous guidance with no files. Two failures were tuned first: owner approval treated
as a sandbox waiver (S3), and an explicit audit answered in chat with verdict labels (S1).

Typed-command scenarios S5 and S6 **pass** (2026-11-25; headless Pi, GPT-6.1 Terra low, the
model in the private pressure-test config). Without the change, a bare `/skill:bc-security-audit`
asked what to review; with it, the run started a full audit. An ordinary security question with
the skill available still got guidance and no files.

Validator command: `<pytest-wrapper> -q concepts/bc-security-audit/tests` (fallback: `python3 -m pytest -q concepts/bc-security-audit/tests`).
Result: **11 passed, 36 subtests passed in 0.02s**. Unit success does not change the
pressure-test status above.

## Deploy targets

Deployed 2026-11-03 via `scripts/deploy-local-skills.py`: `~/.agents/skills/`,
`~/.pi/agent/skills/`, `~/.claude/skills/` (relative symlinks to `body/`). Muse,
Grok, Composer and OpenCode read the shared bus; restart sessions to refresh.
