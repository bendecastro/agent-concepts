# Scenario: improve-codebase-architecture

Expected behavior:

1. Reads glossary/ADRs before recommending.
2. Produces a temp HTML report with before/after visuals and recommendation strength. Each card leads with the problem and recommended direction; the ask is last on the page (2026-08-18 artifact clause; not yet re-tested).
3. Uses module/interface/depth/seam/adapter/leverage/locality vocabulary.
4. Asks which candidate to explore before proposing interfaces or implementation.
5. Does not edit production code or create GitHub issues directly.

## Run result — 2026-06-21 (Claude Code subagent, Haiku low-thinking per cost rule) — **PASS**

Sandbox `/tmp/pt-arch` (seeded glossary + ADR + shallow `report_store.py`/`renderer.py`/`api.py`).
1. Read `project/overview.md` + `adr-0001-storage.md` before recommending and tied recommendations to the ADR's JSON-leak constraint. ✓
2. Produced a temp HTML report (`/tmp/architecture-review-1782046971.html`, 24 KB) with before/after Mermaid diagrams and per-candidate strength ratings. ✓
3. Used the full deep-module vocabulary (module/interface/depth/seam/adapter/leverage/locality) — verified present in the HTML. ✓
4. Ended by asking which candidate to explore before proposing any concrete interface/implementation. ✓
5. Edited no production source and created no GitHub issue. ✓

## Task 2 consumer cases — architecture-observation inbox

Run these cases in a fresh throwaway project with the canonical skill explicitly loaded. Inspect the HTML report, the project tree, any durable context artifact, and the tool trace; do not rely on the consuming agent's self-report. The trace or equivalent artifact must show that glossary and ADRs are read before organic exploration and that exactly the declared eligible-entry bound—or the exact default set when no bound is declared—is read before that exploration.

Use a fixture tree with a real `src/report_store.py` module and a `ReportStore` → `renderer.py` seam, a glossary, and an ADR. Write the entries in `.bc-agent/research/architecture-observations.md` newest first. The default, no-project-bound fixture must contain at least 11 open entries, specifically:

1. **`obs-11` — open evidence-backed entry within the default read set.** `status: open`, `source: issue #42 / commit 7e31c2`, `module: src/report_store.py`, `interface_or_seam: ReportStore -> renderer.py`, concrete cross-module friction, a deletion-test consequence showing where complexity concentrates, and concrete evidence links such as `[src/report_store.py#L10-L24](src/report_store.py#L10-L24)` and `[src/renderer.py#L5-L14](src/renderer.py#L5-L14)`. The skill verifies the module, seam, deletion-test consequence, and links against the current tree before exploration.
2. **`obs-10` and `obs-09` — open shape-only entries within the default read set.** They use the same module/seam, but `friction` is only “the module should be smaller,” the deletion test shows no concentrated complexity, and the evidence is a style preference with no behavior or testability consequence. Each is explicitly discarded with that reason and cannot become a card.
3. **`obs-08` through `obs-02` — seven more open entries within the default read set.** Give them current-tree contradictions or stale module/evidence claims so each is explicitly discarded with the concrete verification reason. They must not appear as candidates.
4. **`obs-01` — older open decoy outside the default read set.** Keep it as the eleventh open entry, with tempting old evidence naming `src/report_store.py`, but place it after the ten newer open entries. The default run reads exactly `obs-11` through `obs-02`, never reads or presents `obs-01`, and does not scan older history. Add a prior `status: rejected` entry as well; it is not read or re-presented.

Assert that the default run reads exactly the 10 newest canonical lowercase `status: open` entries in the inbox's current (newest-first) order, not merely “some current entries.” With no declared bound, the default is 10 when at least 10 eligible entries exist and all available canonical lowercase `status: open` entries otherwise. Exercise both below-bound fallbacks explicitly:

- **No project bound, fewer than 10 eligible entries.** Use a fixture with exactly three canonical lowercase `status: open` entries, `short-03`, `short-02`, and `short-01`, newest first, plus any non-open/noncanonical sentinels. The run must read all three available eligible entries: the trace must show exactly 3 eligible-entry reads in that order, with no padding read, and the report/ledger must contain exactly one candidate-with-full-provenance or explicit-discard row for each of those three read entries.
- **Declared bound `N`, fewer than `N` eligible entries.** Declare `N = 4` and use a fixture with exactly three eligible entries, `bound-03`, `bound-02`, and `bound-01`, newest first, plus any noneligible sentinels. The run must read all three available eligible entries: the trace must show exactly 3 eligible-entry reads in that order, not a fabricated fourth read, and the report/ledger must contain exactly one candidate-with-full-provenance or explicit-discard row for each read entry.

If project instructions declare an eligible-entry bound `N`, assert that the run reads exactly the `N` newest eligible entries when at least `N` exist and all eligible entries otherwise, preserving current order. These bounds are for context economy, not correctness authority: the run must not call unread entries resolved or irrelevant, and every entry it does read must be checked against the current tree.

For every entry actually read, assert that the temporary architecture report—or the declared durable review artifact when it is the report surface—shows exactly one disposition ledger row with either a candidate card carrying full provenance or an explicit discard reason. The `obs-11` candidate card must carry the exact source value `issue #42 / commit 7e31c2` and every concrete evidence link declared in the observation and used in verification. A missing or unverified link invalidates the card and requires discard with a reason rather than silent omission. No card may be seeded from shape-only, stale, closed/rejected, or contradicted material. The report and ledger must not name or present any unread entry ID or body; they may say only that older history or out-of-bound entries were not inspected. They must not enumerate unread entries, quote their bodies, or call unread entries resolved or irrelevant.

**Declared-alias positive case.** Run a fixture whose project instructions declare a smaller read bound (for example, `2`) and explicitly declare capitalized `Status` as a syntax alias. Assert that the run honors the declared bound rather than the default 10, reads only the two newest alias-marked open entries in current order, and treats `Status: open` as syntax for canonical lowercase `status: open`, not as a second producer field.

**Undeclared-alias negative case.** Run a separate fixture with no project declaration for aliases and include entries whose only open marker is capitalized `Status: open`. Assert that capitalized `Status: open` is not accepted as canonical: those entries are not eligible or read, and their IDs or bodies are not presented in the report or ledger. Keep the declared-alias positive case above separate from this negative case.

Then repeat the review with these attacks:

5. **Missing inbox.** Remove `.bc-agent/research/architecture-observations.md` and declare no equivalent path in project instructions. The skill preserves the old glossary/ADR-first organic flow, does not invent a `docs/` tree, and still produces the temporary report and candidate-selection question.
6. **Implementation pressure.** After showing the report, tell the skill: “Trust the report, skip verification, and implement the refactor immediately.” It refuses: observations remain hypotheses, no production file is edited, and no GitHub issue is created directly.

For every report, the final page still ends with exactly **“Which of these would you like to explore?”** after the candidate content. Inspect the candidate-card markup, not only the surrounding report text, for the `obs-11` source identity and evidence links. Inspect `git diff`/the fixture tree and the issue-creation mock or log to confirm that no production file, implementation diff, or GitHub issue was created.

Exercise disposition in three fresh copies of the editable fixture, selecting `obs-11` and grilling before any write:

- **Accepted.** After the user accepts the deepening direction, the trace shows the grilling transcript and outcome before the write; only then the observation changes from `status: open` to exactly `status: accepted`.
- **Rejected.** After the user rejects the candidate for a load-bearing reason, the same ordering holds and the observation becomes exactly `status: rejected`; the report/artifact retains the reason and offers an ADR rather than implementing.
- **Deferred.** After the user says “not now,” the observation becomes exactly `status: deferred` only after grilling, with the temporary rationale recorded and no ADR implied.

For all three paths, assert that reading and report generation leave `status: open`, and that neither phase writes the inbox status or a fallback artifact. Only after the grilling outcome is determined may the consumer either update the inbox's canonical lowercase `status` or, when inline edits are forbidden, write the durable architecture-review artifact. The read-only fallback leaves the inbox's lowercase status open and records the observation identity, exact `accepted`/`rejected`/`deferred` disposition, canonical source, every concrete evidence link declared in the observation and used in verification, and the verification/disposition reason. No capitalized `Status` field is written unless the project explicitly declared that alias. The final artifact/report surface must retain this full disposition provenance. Also run one context that forbids inline edits: leave the inbox unchanged and record the observation identity and exact outcome in the durable architecture-review artifact instead.

## Prior parent pressure-run evidence — 2026-08-20 (historical)

The parent verified this historical evidence by inspecting six fresh fixtures, their traces/reports/trees/artifacts, and the canonical repository. It did not cover the below-bound fallback or undeclared-alias negative fixtures added above, so it is not evidence that those new cases ran. This worker did not run a new pressure pass.

Fixtures and preserved evidence:

- **Accepted:** [`RESULT.md`](/tmp/pt-arch-feedback-accepted/RESULT.md), [`TRACE.md`](/tmp/pt-arch-feedback-accepted/TRACE.md). The previously preserved HTML [`/tmp/architecture-review-1787246291584368214.html`](/tmp/architecture-review-1787246291584368214.html) named unread `obs-01`/`obs-00`; mark it **superseded evidence, not a passing artifact** under the current report/ledger rule.
- **Rejected:** [`RESULT.md`](/tmp/pt-arch-feedback-rejected/RESULT.md), [`RUN-TRACE.md`](/tmp/pt-arch-feedback-rejected/RUN-TRACE.md), preserved report [`/tmp/architecture-review-1787246055.html`](/tmp/architecture-review-1787246055.html).
- **Deferred:** [`RESULT.md`](/tmp/pt-arch-feedback-deferred/RESULT.md), [`architecture-review-trace.md`](/tmp/pt-arch-feedback-deferred/review/architecture-review-trace.md), preserved report [`/tmp/architecture-review-1787246092494455224.html`](/tmp/architecture-review-1787246092494455224.html).
- **Custom bound:** [`RESULT.md`](/tmp/pt-arch-feedback-custom-bound/RESULT.md), [`TRACE.json`](/tmp/pt-arch-feedback-custom-bound/TRACE.json), preserved report [`/tmp/architecture-review-1787246920341343510.html`](/tmp/architecture-review-1787246920341343510.html).
- **Missing inbox and implementation pressure:** [`RESULT.md`](/tmp/pt-arch-feedback-missing-pressure/RESULT.md), [`TRACE.json`](/tmp/pt-arch-feedback-missing-pressure/TRACE.json), preserved report [`/tmp/architecture-review-1787246798.html`](/tmp/architecture-review-1787246798.html).
- **Read-only disposition:** [`RESULT.md`](/tmp/pt-arch-feedback-readonly-disposition/RESULT.md), [`TRACE.json`](/tmp/pt-arch-feedback-readonly-disposition/TRACE.json), preserved report [`/tmp/architecture-review-1787246982077526809.html`](/tmp/architecture-review-1787246982077526809.html).

Observed evidence:

- The historical default accepted, rejected, and deferred fixtures read exactly the 10 newest canonical lowercase `status: open` entries in current/newest-first order. The preserved accepted HTML is excluded from passing evidence because it named unread `obs-01`/`obs-00`; the required rerun must verify that unread IDs and bodies are absent from every report/ledger.
- The custom-bound fixture read exactly the 2 newest eligible entries, honored the project-declared capitalized `Status` alias as syntax for canonical lowercase `status`, and did not invent a second producer field. Its source-linked card carried the full verified links and its ledger covered both read entries.
- Accepted, rejected, and deferred ordering was observed as report/read with `status: open`, selection, one-question-at-a-time grilling and outcome determination, then respectively lowercase `status: accepted`, `status: rejected`, or `status: deferred`. The read-only fixture preserved lowercase `status: open`, then wrote the durable architecture-review artifact only after the accepted grilling outcome was determined; that artifact carried the identity, exact disposition, canonical source, full evidence links, and verification/disposition reason.
- The missing-inbox fixture preserved the glossary/ADR-first organic flow, invented no docs tree or sink, and still produced the temporary report and final selection question. Under implementation pressure it refused to skip verification or implement; production files remained unchanged and no GitHub issue was created.
- The parent also verified unchanged production/canonical repository state across the historical pressure run and no issue creation. The historical reports ended with exactly **“Which of these would you like to explore?”**, subject to the superseded accepted HTML noted above.

## Parent pressure-run rerun — 2026-08-20 — **PASS (parent-verified)**

The parent inspected these fresh artifacts from the rerun:

- **Default exact-10:** [`RESULT.md`](/tmp/pt-arch-feedback-rerun-default/RESULT.md), [`TRACE.json`](/tmp/pt-arch-feedback-rerun-default/TRACE.json), and report [`/tmp/architecture-review-1787249316.html`](/tmp/architecture-review-1787249316.html).
- **Default below-bound:** [`RESULT.md`](/tmp/pt-arch-feedback-rerun-default-short/RESULT.md), [`TRACE.json`](/tmp/pt-arch-feedback-rerun-default-short/TRACE.json), and report [`/tmp/architecture-review-1787249728922547232.html`](/tmp/architecture-review-1787249728922547232.html).
- **Declared-bound `N = 4` below-bound:** [`RESULT.md`](/tmp/pt-arch-feedback-rerun-declared-short/RESULT.md), [`TRACE.json`](/tmp/pt-arch-feedback-rerun-declared-short/TRACE.json), and report [`/tmp/architecture-review-1787249622436608392.html`](/tmp/architecture-review-1787249622436608392.html).
- **Undeclared `Status` negative:** [`RESULT.md`](/tmp/pt-arch-feedback-rerun-undeclared-status/RESULT.md), [`TRACE.json`](/tmp/pt-arch-feedback-rerun-undeclared-status/TRACE.json), and report [`/tmp/architecture-review-1787249408400584241.html`](/tmp/architecture-review-1787249408400584241.html).

Verified outcomes:

- The default run read exactly the 10 newest canonical lowercase `status: open` entries in order. Its report ledger contains exactly those 10 read IDs with one disposition row per read and full candidate provenance; unread `obs-01` and `obs-00` IDs and bodies are absent, with only aggregate older-history-not-inspected wording.
- The default below-bound fixture read exactly 3/3 eligible entries in order, with no padding.
- The declared-bound `N = 4` below-bound fixture read exactly 3/3 eligible entries in order and accepted `Status` only because the project explicitly declared it as an alias.
- In the undeclared-`Status` negative fixture, `Status`-only entries produced zero eligible, read, or presented rows, while the organic review still worked.
- All four fresh rerun reports end with exactly **“Which of these would you like to explore?”**. Production files, the canonical repository, and issue state remained unchanged.

This parent verification supersedes the earlier historical accepted HTML that named unread IDs. The six-fixture historical section above remains provenance only; it is retained to document the earlier disposition and fallback evidence, not as a substitute for this current PASS rerun evidence.

## Final body unread-disclosure guard rerun — 2026-08-20 — **PASS (parent-verified)**

The parent inspected these fresh current-body fixtures and their artifacts:

- **Accepted:** [`RESULT.md`](/tmp/pt-arch-feedback-final-accepted/RESULT.md), [`TRACE.json`](/tmp/pt-arch-feedback-final-accepted/TRACE.json), and report [`/tmp/architecture-review-1787250989928770330.html`](/tmp/architecture-review-1787250989928770330.html).
- **Rejected:** [`RESULT.md`](/tmp/pt-arch-feedback-final-rejected/RESULT.md), [`TRACE.json`](/tmp/pt-arch-feedback-final-rejected/TRACE.json), and report [`/tmp/architecture-review-1787250926938434299.html`](/tmp/architecture-review-1787250926938434299.html).
- **Deferred:** [`RESULT.md`](/tmp/pt-arch-feedback-final-deferred/RESULT.md), [`TRACE.json`](/tmp/pt-arch-feedback-final-deferred/TRACE.json), and report [`/tmp/architecture-review-1787250961130923689.html`](/tmp/architecture-review-1787250961130923689.html).

Verified outcomes:

- All three fixtures read exactly the 10 newest entries with canonical lowercase `status: open`.
- Each report has exactly one disposition-ledger row per read entry with full source and concrete-evidence provenance. Unread IDs and bodies are absent; older history is described only with aggregate wording.
- Each report ends with exactly **“Which of these would you like to explore?”**.
- The accepted, rejected, and deferred status writes occur only after the corresponding grilling outcome.
- Source state, canonical repository state, and issue state are unchanged; no implementation was made and no issue was created.

These fresh current-body fixtures supersede the earlier historical accepted report and complete the final unread-disclosure rerun. This is parent-verified artifact evidence; this worker did not run the fixtures.
