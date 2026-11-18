# Pressure test: review packet with no Test levels block

Authored and run 2026-11-18 (Manicule: reviewers got diff + spec but never the Test levels block, and no review mentioned levels).

Consumer: Terra low, text-only, without / pre-change body / current body. Packet: spec + diff of a rule-bearing `parsePrice` change with example tests only, commit message without trailers, no Test levels block.

Pass: reviews the diff anyway and reports both the missing block/trailer and the missing property on rule-bearing logic as findings.

## Results 2026-11-18
- without: FAIL — one overflow finding; levels and property never mentioned.
- old body: FAIL — notes the missing block but blocks the whole review instead of auditing; no property finding.
- new body: PASS — "Important — missing property test for the parsing rule" and "Important — missing test-levels record … neither a Test levels block nor `Test-levels:` commit trailers", plus the overflow finding.
Transcripts were in `/tmp/bc-swarm/2026-11-18-test-levels-fix/pt/review.*.out` (temporary).
