# Pressure test: bc-agent-reflect open-report check and Decisions record

Run under the skill's former name `retro` (renamed `bc-agent-reflect` 2026-11-19); recorded prompts and outputs keep it.

Authored and run 2026-11-19. Consumer: `pi -p --no-tools --no-context-files --no-skills --no-session --model openai-codex/gpt-6.1-terra --thinking low --append-system-prompt <arm>`. Without arm: `body/SKILL.md` before this change (git HEAD); with arm: current body. n=2 per arm per scenario. Every prompt opens "You cannot run tools in this reply." and embeds the real `<report-dir>/2026-11-19.md` (undecided, 2 proposals).

Scenarios and pass criteria (written before running):
- (a) owner types `/retro since 2026-11-19`, latest report undecided → shows its open proposals and asks for picks before a new review.
- (b) previous turn showed the proposals; owner answers `1 2` → says it will append `## Decisions` to that report, one line per number (acted, filled in when work lands).
- (c) control: same report with a `## Decisions` section appended → proceeds to the new review without re-asking about old proposals (here: says it needs tools).

## Results

| Scenario | without (old body) | with (new body) |
|---|---|---|
| (a) undecided → show + ask first | 0/2 (both: "can't run without tools", proposals ignored) | 2/2 (lists both with path, "I'll start the new review after your answer") |
| (b) `1 2` → append `## Decisions` | 0/2 (keeps report as history / "record your selection", no section) | 2/2 (appends `## Decisions` with `1. acted — pending`, `2. acted — pending`, updated as work lands) |
| (c) control → proceed | 2/2 | 2/2 (notes it is decided, does not block) |

Verdict: with-arm beats without-arm on (a) and (b); control holds in both. Scenarios (a)/(b) were re-run on the final wording in the isolated retest below. Not exercised: batch carry-over (`## Still undecided from <date>`), declined/deferred lines, and real file writes (no tools).

Future pressure scenario: a latest report has new proposals and carries proposals from an older report. Show both with distinct numbers, record carried-item decisions under their original numbers in the original report, and carry them through another headless batch if still undecided. Also check that an already-decided original is not re-offered.

## Isolated retest of the final body (2026-11-19, after commit 13b3080)

Consumer: true stranger. Run from a scratch cwd whose trusted project `.pi/APPEND_SYSTEM.md` reads "Answer the user." (overrides the owner's agent-directory file), with `pi -p --no-session --no-context-files --no-skills --no-tools --no-extensions -a --model openai-codex/gpt-6.1-terra --thinking low --append-system-prompt <body/SKILL.md at 13b3080>`. Isolation probe rerun first (yes/no: does your context hold a heavy-runs rule / a home-folder rule): isolated No/No, control from /tmp without override or `--no-extensions` Yes/Yes. Every prompt opens "You cannot run tools in this reply." and gives the report directory listing and file contents inline (report dir `~/.local/state/retro/`). n=2 per scenario, new body only (no old-body arm).

Pass criteria (written before running):
- (a) interactive `/retro`, latest report undecided → shows its open proposals with path and asks before the new review.
- (b) interactive, latest report has `## Decisions` → does not re-offer; proceeds (here: says it needs tools).
- (d) headless `--report`, latest undecided → no asking; plans `## Still undecided from 2026-11-19` with original path and verbatim proposals, outside the sample.
- (e) latest report has 2 new proposals plus `## Still undecided from 2026-11-19` (original undecided). (e-show) `/retro` → carried items numbered after the new ones (3, 4) with original path. (e-pick) previous turn showed 1–4, owner answers `1 3` → decisions for 1/2 go to the latest report and carried 3/4 go to the original `2026-11-19.md` under original numbers 1/2.
- (f) directory holds `2026-11-19.md` (undecided, newer mtime) and `2026-11-20-project-a.md` (decided, older mtime) → picks `2026-11-20-project-a.md` as latest by date prefix.

| Scenario | result |
|---|---|
| (a) | 2/2 — lists both with path; "I'll start the new review after your answer" |
| (b) | 2/2 — "has a `## Decisions` section, so neither proposal is open"; needs tools |
| (d) | 2/2 — no asking; plans `## Still undecided from 2026-11-19` + original path + verbatim proposals; 2 says "without counting them as findings in the new sample" |
| (e-show) | 2/2 — new proposals 1–2, then 3–4 "Carried from" / "Still open from `~/.local/state/retro/2026-11-19.md`" |
| (e-pick) | 2/2 — appends `1. acted — pending` / `2. declined` to the latest report and `1. acted — pending` / `2. declined` to `2026-11-19.md` (3→1, 4→2 mapped back) |
| (f) | 2/2 — "latest is `2026-11-20-project-a.md`: its date prefix is later … despite the latter's newer modification time"; decided, so no carried items |

Verdict: 12/12 pass on the final body with an isolated consumer. Limits: new-body arm only, so this shows the wording holds, not that it is needed; no tools, so no real file writes; in (d) 1 of 2 did not state the carried items are outside the sample count explicitly. Observed by design in (f): the undecided older `2026-11-19.md` is not offered because only the latest report is checked. Raw prompts and outputs: `/tmp/bc-swarm/2026-11-19-retro-skill/pt-retro3/` (`prompt-<s>.txt`, `out-<s>-<n>.txt`, `probe-*.txt`).

## Transcripts

Verbatim except backticks removed around one project A path (repo lint reads it as a workspace path) and the owner's report directory replaced by `<report-dir>` (personal-path scrub). Raw files: run dir `out-<arm>-<scenario>-<n>.txt`.

### out-new-a-1
~~~~
The previous report is undecided: `<report-dir>/2026-11-19.md`.

1. **[Recommended] Review data growth at boundaries** — Add a `code-review` prompt to trace maximum size, duplication, growth and limit behavior across changed boundaries. Seen in 3 of 20 sampled sessions; two boundaries blocked work.
2. **Make the delivery check’s claim match what it verifies** — In project A’s scripts/delivery-check.mjs, narrow the success message and state that the loaded browser revision is unverified. One confirmed and one suspected version confusion across 2 of 20 sampled sessions.

Reply with the numbers to act on, e.g. `1 2`. I’ll start the new review after your answer.
~~~~

### out-new-a-2
~~~~
The latest report is still undecided: `<report-dir>/2026-11-19.md`.

1. **[Recommended] Review data growth at boundaries.** Add a `code-review` prompt to trace maximum data size, duplication, growth and behavior at limits across changed boundaries. Two sampled boundaries blocked work; a third showed substantial serialization amplification. Seen in **3 of 20 sampled sessions**. The proposed concept change needs a workspace pressure test before deployment.

2. **Make the delivery check’s claim match what it verifies.** In project A’s scripts/delivery-check.mjs, narrow “Everything is delivered” to the helper release and build-manifest checks performed, and state that the loaded browser revision is unverified. One confirmed and one suspected delivery/version confusion across **2 of 20 sampled sessions**. Verify the integrated tree before acting.

Reply with the numbers to act on, e.g. `1 2`. I’ll start the new review after your answer.
~~~~

### out-new-b-1
~~~~
Before starting work, I’ll append a `## Decisions` section to `<report-dir>/2026-11-19.md`:

~~~~md
## Decisions
1. acted — pending
2. acted — pending
~~~~

Then I’ll work on both selected proposals and update each line with the resulting file or commit when it lands. I can’t make the edits in this reply because tools are unavailable.
~~~~

### out-new-b-2
~~~~
Before starting work, I’ll append a `## Decisions` section to `<report-dir>/2026-11-19.md`, recording both proposals as **acted — pending**. I’ll update each entry with the resulting commit, PR, or file when it lands.
~~~~

### out-new-c-1
~~~~
The previous report, `<report-dir>/2026-11-19.md`, has a Decisions section, so it doesn’t block a new review.

I can’t run tools in this reply, so I can’t inspect or sample the sessions, delegate the review, or write the required batch report. No new retrospective has been performed and no files have been changed. Please rerun `/retro since 2026-11-19` with tools available.
~~~~

### out-new-c-2
~~~~
I can’t run tools in this reply, so I can’t inspect the sessions, delegate the review, or write the required batch report.

The supplied latest report has a `## Decisions` section, so it is decided and does not block a new review. Please enable tools for `/retro since 2026-11-19`.
~~~~

### out-old-a-1
~~~~
I can’t run the batch retrospective or write its required report without tools. The supplied report covers the previous sample, not the sessions since 2026-11-19, so it isn’t enough to establish new findings.

Please re-run `/retro since 2026-11-19` with tools available.
~~~~

### out-old-a-2
~~~~
I can’t run this retrospective in this reply: it requires inspecting session logs and writing a batch report, and tools are unavailable. The November 19 report covers an earlier period and can’t establish findings for the requested scope.

Please retry with tools enabled.
~~~~

### out-old-b-1
~~~~
I’ll preserve `<report-dir>/2026-11-19.md` as the historical report; I won’t delete or overwrite it. Your selection authorizes work on both proposals, subject to verifying the current guidance and project A tree first. The review-standards change will need a pressure test before deployment.
~~~~

### out-old-b-2
~~~~
I’ll keep `<report-dir>/2026-11-19.md` as the historical report, and record that you selected proposals 1 and 2 without treating either as completed yet. Then I’ll verify the current guidance and project A checkout before acting, including the required pressure test for the review-guidance change.
~~~~

### out-old-c-1
~~~~
I can’t run this retrospective without tool access: it requires sampling and reading session logs, checking current project guidance, and writing a batch report.

The previous report’s decisions are noted: proposal 1 was acted on (pending), and proposal 2 was declined. I can’t determine what recurred since 2026-11-19 from that report alone. Please enable tools and rerun `/retro since 2026-11-19`.
~~~~

### out-old-c-2
~~~~
I can’t run this retrospective in this reply: I have no tool access to enumerate or inspect sessions, dispatch scouts, or write the required batch report.

The supplied report covers the prior period, but it isn’t evidence for sessions since 2026-11-19. Please rerun `/retro since 2026-11-19` with tools available.
~~~~
