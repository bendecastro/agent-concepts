# Reconnaissance and coverage

Read source, manifests, routes, policies and tests without executing them. Record
source revision, scope and exclusions; inspect compatible prior audit records as
leads, not proof of current coverage. Recheck current source before reusing a claim.

Write `architecture.md` (roughly 500 words): protected assets, principals and their
normal authority, entry surfaces, subsystem map, trust boundaries, source-visible
controls and source locations, deployment unknowns, selected companions and why.
Model a lower-trust actor's capabilities before choosing attacks. Language or a
package name alone does not select a companion. General classes remain applicable
when a specialized boundary has no companion; disclose limits rather than inventing
support for the six unported upstream domains.

## Coverage ledger

`coverage-ledger.json` is an array. A unit is **surface × boundary × subsystem ×
attack_class**. Use stable repository-relative identities, not line numbers or
verdicts; assign a unique ID such as `U001` per unique tuple. Keep IDs unchanged
throughout the run. Split material boundaries rather than recording “whole repo”.

Each unit has string fields `id`, `surface`, `boundary`, `subsystem`, `attack_class`,
`status`, and `evidence` (an array of nonempty source references or check summaries).
Allowed statuses:
- `planned`: identified, not reviewed;
- `candidate`: reviewed with an unresolved candidate;
- `covered`: assigned invariant checked, with evidence, not a guarantee of safety;
- `blocked`: required fact/control unavailable;
- `deferred`: omitted from this single pass;
- `out_of_scope`: explicitly excluded, **never counted as covered**.

Use exactly one status; there is no separate covered boolean. `blocked`, `deferred`
and `out_of_scope` also require a nonempty `reason`. Mark a candidate unit covered
only after all its candidates have independent dispositions; a needs-validation
result normally leaves it blocked. The coordinator owns the ledger, records source
checks and candidate links, and counts only `status == "covered"` in coverage.

```json
[
  {"id":"U001","surface":"api.py#get_document","boundary":"caller -> owner data",
   "subsystem":"documents","attack_class":"access control","status":"planned",
   "evidence":[]}
]
```

Prioritize lowest-trust reachable entries and valuable assets, then changed source
and known gaps. One pass does not exhaust a target: new surfaces discovered too
late become deferred units with reasons. Report counts of every status and explain
partial scope, blocked checks and unresolved candidates explicitly.
