# Independent validation and reporting

## Fresh verifier contract

Consolidate candidates by source-derived root cause. Every candidate, including a
likely rejection or blocked lead, goes to one `reviewer` in a fresh session. Give
only the candidate (claim, ledger IDs, minimal source trace and exact claimed
input/result) and source access, together with this verification contract and the
selected companion's constraints. Do not pass the hunter's reasoning, architecture
narrative, prior verdict arguments or other reviewers' conclusions. Candidate facts
must be independently checked, not accepted as context.

> You did not write this candidate. Try to refute it from current source. Reconstruct
> identity, authorization, framework defaults, normalization and containment along
> the complete path. Name the lower-trust actor, protected principal/resource and
> concrete outcome. Return one final record with exactly one verdict: confirmed,
> needs_validation, or rejected. Confirm only demonstrated impact; otherwise state
> a precise blocker and safe validation plan, or a rejection reason. Source-only
> unless the owner approved execution for this run AND an enforced no-network,
> scratch-only-write sandbox is available. Do not contact live services or change
> target source. Do not strengthen the claimed outcome.

Fresh review is mandatory, not a time-budget option. An unavailable verifier leaves
a ledger candidate unresolved and the run incomplete, not an invented finding.
If a reviewer discovers a different root cause, treat it as a new candidate needing
its own fresh reviewer. The coordinator checks the returned record against source
and updates the ledger without upgrading its impact or verdict.

## Bounded execution and evidence

Both run-specific approval and sandbox enforcement are prerequisites, not implied
by an audit request. Use OS-enforced network isolation, read-only target/tool mounts,
only scratch writable, no secrets, empty allowlisted environment and explicit CPU,
memory, process, output-size and time bounds. Never install/fetch dependencies.
Use dummy principals/resources and the smallest observation that settles the
boundary. Do not escalate a crash or continue to persistence, outage or exploitation.

When approval arrives without a sandbox, keep the source verdicts, record the
missing-confinement blocker, and offer the owner three choices: set up an
enforced sandbox (such as bwrap or podman) and rerun; the owner runs the
bounded command themselves and pastes the output; or leave the candidate as is.

These rationalizations do not waive confinement — approval is one gate, not a
waiver of the other:
- "owner approved" → approval without confinement is still one gate missing.
- "it's tiny/harmless" → judged from the code you are about to trust, not before it.
- "no dependencies" → dependency-free code still runs arbitrary top-level code on the host.
- "it's just a fixture" → fixture status still writes to the host (e.g. `__pycache__`).
- "rule is too strict here" → the strictness is the control; intent does not confine.

Record exact input, command, sandbox controls, safe allowlisted variables and minimum
result; never dump the environment or credentials. Scratch and its contents become
hostile after execution. Do not bulk-copy scratch, follow its links or open special
files as evidence. Prefer a bounded captured text result; if a file is decisive,
trusted coordinator-side code must read a predeclared, size-bounded regular file
without following links or racing path replacement after all sandbox processes exit.
If safe evidence extraction is unavailable, retain needs_validation. Sandbox setup
is an actual enforced configuration, not a suggested shell command in the report.

## JSON contract

The run contains `findings.json` and `coverage-ledger.json`, each a JSON array.
Duplicate object keys are invalid. Ledger format is in [recon](RECONNAISSANCE.md).
Unknown fields are rejected. IDs are nonempty strings; findings IDs are unique.
One record per root cause, referencing one or more existing units in `units`.

Every finding requires `id`, `title`, `units` (nonempty string array), `trace`
(nonempty array of repository-relative `path:line` references with source steps),
and a single string `verdict`. Add only that verdict's required fields:

| Verdict | Required fields beyond common fields |
| --- | --- |
| `confirmed` | `principal`, `resource`, `outcome`, `impact`, `severity`, `evidence` (nonempty string array), `remediation` |
| `needs_validation` | `hypothesis`, `blockers` (nonempty string array), `validation_plan` (nonempty string array of bounded steps resolving the blockers) |
| `rejected` | `reason` |

Other fields in the table are nonempty strings. `impact` and `severity` use the
same ordered scale, with severity no greater than impact:

1. `informational`: demonstrated boundary effect with minimal security consequence;
2. `low`: limited non-secret disclosure or minimal concrete gain requiring effort;
3. `medium`: limited resource set, constrained blast radius or uncommon prerequisites;
4. `high`: demonstrated cross-principal private read/write, authentication bypass,
   authenticated code execution or actual shared-service stop;
5. `critical`: demonstrated unauthenticated arbitrary-account takeover, full data-store
   compromise or code execution.

These are evidence anchors, not automatic scores. `outcome` and `evidence` must
justify the impact label; the script compares declared ranks but cannot establish
that a source trace proves them. Missing headers alone do not qualify even as
informational confirmed findings. Likelihood can lower severity, never raise the
impact ceiling. Never put severity (even null) on another verdict.

Example confirmed record (illustrative, not evidence about a target):

```json
[{"id":"F001","title":"Cross-owner document read","units":["U001"],
  "trace":["api.py:12 accepts authenticated caller and document ID", "api.py:18 returns another owner's record"],
  "verdict":"confirmed","principal":"user A","resource":"user B's private document",
  "outcome":"A receives B's private content via the source-visible return path",
  "impact":"high","severity":"high","evidence":["Source trace establishes missing owner binding on the only return path"],
  "remediation":"Bind the selected document owner to the authenticated caller before returning it; add a two-owner regression test."}]
```

Run `python3 <skill-dir>/validate_audit.py <run-dir>`. Nonzero exit means fix the
records before reporting. Success checks shape, verdict-specific fields, rank ceiling,
unique IDs/tuples, coverage status and references, not source truth or independence.

## Report from records

Write `REPORT.md` only from independently decided records and the ledger. Include
revision/scope, source-only or approved sandbox execution limits, short architecture
summary, confirmed findings with severity and smallest effective fix/regression,
separate needs-validation hypotheses/blockers/plans without severity, rejection
reasons and separate hardening notes. Count all ledger statuses, excluding
out_of_scope from covered. Disclose incomplete verifier work and all blocked,
deferred and excluded areas. Never claim that a single pass proves safety. Prose
must not upgrade JSON verdicts or effects. A zero-confirmed report is valid.
