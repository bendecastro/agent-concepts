# Two more council chains — `bc-council-audit-security`, `bc-council-challenge-plan`

Date: 2026-11-24
Status: active
Decided in a grilling session with the owner. Both are thin chains over `council-chain`, like
`bc-council-find-bugs`; neither copies its parent's steps.

## `bc-council-audit-security` (parent: `security-audit` full audit)

1. **Placement.** The council replaces the parent's single hunting pass (step 2). Recon and threat
   model (step 1) run first, by the chain's own session; their architecture note and coverage
   ledger are the shared map. Every candidate that survives pass 2 still goes to the parent's
   fresh refuting `reviewer` (step 3); advisor agreement never verifies a finding. The parent's
   output gate, `.security-audit/run-N/` and validator stay unchanged. Why: the parent's
   independence rule stays whole; the council adds hunting breadth.
2. **Focus.** Deal trust boundaries from the recon note round-robin; each advisor hunts every
   attack class across its boundaries. Why: recon already names the boundaries, and a missed
   check at a boundary is where a hole appears.
3. **Filing (owner chose the pre-selected variant).** Confirmed findings are pre-selected; `all`
   files each as a `Kind: security` work item that names the affected area and the fix, with no
   exploit steps, pointing at the git-ignored run folder for details. Nothing else is filed
   unless picked. Filed items then follow the work pipeline's planned-item rule
   (`bc-plan-to-pipeline` in settled-source mode), inherited, not restated as a recommendation.
4. **Verification count.** At most 8 candidates per advisor in pass 1. Every candidate surviving
   pass 2 gets its fresh reviewer, ordered by share of advisors rating it Strong. `--max-verify N`
   caps it; candidates over the cap are reported unverified and the run is incomplete, as the
   parent requires.

## `bc-council-challenge-plan` (parent: the plan, then `bc-plan-to-pipeline`)

5. **Output.** Objections, each quoting the plan line it attacks and citing `file:line` where the
   plan claims something about the code. Kinds: wrong premise, missing case, cheaper path, risky
   order. Pass 2 attacks and refines them. The owner is then grilled only on surviving
   objections, one at a time; answers are written into the plan before slicing. The council never
   rewrites the plan itself.
6. **Hand-off.** Standalone `/bc-council-challenge-plan <plan>`. After the answers are written,
   it runs `/bc-plan-to-pipeline` in settled-source mode, passing the settled answers through so
   the owner is not asked twice.
7. **Focus (owner chose sections).** Deal the plan's sections or steps round-robin; each advisor
   attacks every objection kind within its part and may still raise objections elsewhere.

## Testing

Dry runs, as for `bc-council-find-bugs` (owner, 2026-11-24): the consumer writes `plan.md`
and launches nothing; graded from that file on `openai-codex/gpt-6.1-terra` at low thinking,
two runs each. The first real run of each chain is the live test.

## Execution record

- 2026-11-24: both chains dispatched to two workers (bodies, CONCEPT, tests); parent does
  index, log, relationships, status and deploy.
