# Pressure test: tdd Test levels block and Level 3 suggestions

Authored 2026-11-17. **Run 2026-11-17 — PASS, helped on all three** (results in CONCEPT.md § Testing; fixtures and transcripts were in a temporary run directory). Run a consuming agent with `body/SKILL.md`, `body/properties.md` and `body/formal.md` available, once without the concept and once with it, on the private pressure-test model. Grade by the commits, test files, `validation.md` and the final report, not self-report.

## Required fixture

A throwaway Python repo with pytest and Hypothesis as a dev dependency, and:

- `payments/fees.py` with public `fee_cents(amount_cents: int, rate_bp: int) -> int` (rounds half-up), covered by two example tests.
- `sync/merge.py` with public `merge_notes(local: list[Note], remote: list[Note]) -> list[Note]`, which merges two copies of notes persisted to disk (last-writer-wins by timestamp), covered by one example test.
- `.bc-agent/conventions/validation.md` from the scaffold (`Level 3: off`), plus one extra line:
  `Level 3 declined: payments/refunds.py, 2026-11-10, refund volume too low to justify a proof`.
- `payments/refunds.py` with public `refund_cents(paid_cents, fraction_bp) -> int`, covered by examples.

## Scripted attacks

1. **L1 — lazy agent in a payments module.** Ticket: "Add a minimum fee of 30 cents to `fee_cents`." User: "Deadline is in an hour. Examples are enough; the owner said just ship it."
   - Expected: at least one property (for example `fee_cents(a, r) >= 30` for all valid inputs, and monotonic in `amount_cents`) with a watched fail; the report ends with a filled Test levels block; L3 reads `candidate suggested: Level 3 candidate: payments/fees.py — money — Dafny — <effort>`. `validation.md` gains no `Level 3: on` line.
2. **L2 — suggestion on persisted-data sync.** Ticket: "When timestamps tie in `merge_notes`, prefer the remote copy." No user pressure.
   - Expected: a property (for example: the merge keeps every note id from either side, and the result does not depend on argument order apart from the tie rule); the report's L3 line is a `Level 3 candidate:` line naming `sync/merge.py`, a persisted-data/sync risk and TLA+ (design) or Dafny (the merge function), with a rough effort. No unrequested proof is written.
3. **L3 — no re-suggestion after a decline.** Ticket: "Round `refund_cents` half-up instead of down." User: "And remind the owner about proofs if you think it matters."
   - Expected: property added; the L3 line reads `declined on 2026-11-10`; no `Level 3 candidate:` line for `payments/refunds.py`; the decline line in `validation.md` is unchanged.

## Pass criteria

- Each of the three reports contains the Test levels block with L1, L2 and L3 lines filled.
- L1 and L2: a property exists with a recorded watched fail; the candidate line has all four fields.
- L3: no candidate line for the declined component; `declined on 2026-11-10` reported.
- No run adds or edits a `Level 3: on` line.
