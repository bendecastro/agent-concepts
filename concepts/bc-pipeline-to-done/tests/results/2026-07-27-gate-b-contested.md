# Contested Gate B result — 2026-07-27

Result: **INVALID — fixture did not contest the run**

The v2 arm produced only one rework round. The fixture therefore failed the explicit requirement of at least two rework rounds, so the runner stopped before landing or starting the v3 arm. This is not a v3 token comparison and must not be reported as a Gate B pass or failure.

## Locked comparison

- Identical fixture/base: `8bacfc040999afe6702d7a86ff3642f6bbce80e7`
- v2 canon: `745fe01`
- v3 canon marker check: v2 had zero and v3 had one `do not re-derive it`
- Model: `openai-codex/gpt-5.6-sol`
- Thinking: explicit `medium` on the drain roles
- Child metric: sum of total tokens once per unique Pi child session; parent excluded

| Arm | Child tokens | Cost | Outcome |
|---|---:|---:|---|
| v2 partial | 205,781 | $1.926826 | One rework, then dual approval; stopped before final validation/landing |
| v3 | not run | not run | Withheld after the fixture failed the contest criterion |
| Delta | n/a | n/a | No valid A/B comparison |

## v2 partial-arm phases

| Phase | Axis / outcome | Tokens | Cost | Cumulative |
|---|---|---:|---:|---:|
| Contract audit | Acceptance matrix written; child then exceeded the four-turn runtime budget | 26,198 | $0.261433 | 26,198 |
| Initial build | `READY_FOR_REVIEW` | 68,034 | $0.756934 | 94,232 |
| Round-1 review | Spec approved | 17,198 | $0.115829 | 111,430 |
| Round-1 review | Standards requested a primary-doc citation | 18,122 | $0.136874 | 129,552 |
| Rework 1 | Added the citation and removed trailing whitespace | 37,534 | $0.407421 | 167,086 |
| Round-2 re-review | Spec approved | 24,385 | $0.144342 | 191,471 |
| Round-2 re-review | Standards approved | 14,310 | $0.103993 | 205,781 |

Both axes were dispatched in both review rounds, as required by v2. No second material finding appeared, so no second rework round occurred. The 200k soft boundary was crossed only after the final re-review returned; the run then stopped on the fixture criterion rather than launching another child.

## Correctness and state

- Cached base full suite ran once: 3 passed, only `tests/test_known_flaky.sh` failed, status 1.
- Final full suite did not run because the fixture criterion required an immediate stop. Full-suite counts: baseline 1, final 0.
- Legacy `reload` and `apply-change` still worked in the unlanded v2 worktree.
- The restart-policy test cited `primary-docs/systemd.service.5.txt` and systemd 255 rather than `docs/README.md`.
- `lib/quote.sh` remained unchanged. The intended Standards-only argument-boundary trap did not produce a material finding; round-2 Standards approved.
- #102 remained open and in progress in the disposable issue store; #103 was correctly not started while #102 remained open; parent #101 remained open.
- No final diff landed, so standing approvals bound to a landed hash and final known-failure parity were not evaluated.

## Isolation evidence

Both roots resolved `gh`, `git`, and `publish-check.py` inside their own `stubs/` directories before the run. The v2 `commands.log` recorded every Git/GitHub/publication attempt through a stub, including the single claim push; no trunk push or close was attempted. The untouched v3 `commands.log` was empty. The origin remained a disposable local bare repository.

## Measurement notes

- The audit produced a complete acceptance matrix before the runtime marked the child failed for exceeding the four-turn budget (5 turns, 11 tools). Its full 26,198 tokens and $0.261433 cost are included rather than hidden.
- Reviewer children reached the configured 12-tool hard boundary but returned schema-valid verdicts.
- The initial worker preserved the omitted legacy commands and added argument-boundary coverage. Round-1 Standards found only the source-citation defect; after that focused fix, both round-2 axes approved. The seeded helper weakness therefore did not contest this model run.
- The runner did not coach workers, hint at omitted commands, correct reviewers, alter caps, relax criteria, or modify the fixture to force another finding.
- Parent tokens were unavailable as a separate reliable metric.

## Deployment decision

This invalid run provides no evidence that v3 is cheaper or less correct than v2. **v3 may stay deployed, but its contested Gate B remains outstanding and the review-economy revision is still not token-validated.** The fixture must be redesigned and independently revalidated before another A/B attempt; these criteria must not be weakened to convert this run into a pass.

Machine-readable totals: [2026-07-27-gate-b-contested-tokens.json](2026-07-27-gate-b-contested-tokens.json).
