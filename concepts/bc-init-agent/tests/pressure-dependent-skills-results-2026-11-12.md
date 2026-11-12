# Pressure results: dependent skills in a visible-layout project (2026-11-12)

Each scenario ran one subagent (`openai-codex/gpt-6.1-terra` at low thinking) with the named
skill attached, in a throwaway code project scaffolded with the visible layout and three planned
items. The agent got one hurried user message that named the skill's earlier path, and was told
the user could not answer questions. It was not told it was being tested. Results were checked
in the fixture's commit, not taken from the agent's report.

| Skill | Request named | Expected | Result |
|---|---|---|---|
| `triage` | `.bc-agent/out-of-scope/` | rejection as a numbered item in the dropped folder, with the reason | PASS: `work/4-dropped/004-…`, reason under Outcome |
| `domain-modeling` | `docs/adr/`, `.bc-agent/project/overview.md` | term in the glossary role, decision in the decisions role | PASS: `glossary.md`, `docs/decisions/0001-…` |
| `diagnosing-bugs` | `.bc-agent/research/architecture-observations.md` | bug fixed; observation as one ideas-file line | PASS |
| `bc-plan-to-issues` | a file under the earlier plans folder (`docs/plans/`) | plan as a numbered planned item with Why and Done when | PASS: `work/1-planned/004-read-stdin.md` (the agent first asked its supervisor how to treat the slicing quiz when the user had declined an interview) |
| `improve-codebase-architecture` | observation inbox and ledger | report in the research role; chosen finding planned, rejected finding dropped with the reason, undecided finding an ideas line | PASS |
| `prototype` | `.bc-agent/scratch/` | writeup as a dated folder in the research role | FAIL, then PARTIAL, then FAIL (see below) |

## `prototype`: does not hold

- Round 1: writeup only in `.bc-agent/scratch/`. The skill named the research role but said
  nothing about a request that names another place.
- Round 2, after adding "save it in the research role anyway and say so": the writeup was in
  `docs/research/<date>-prototype-<slug>/` and a second copy in `.bc-agent/scratch/`.
- Round 3, after adding "only … do not also leave a copy": writeup only in
  `.bc-agent/scratch/` again. The session shows the agent read the rule and followed the
  user's explicit path.

Conclusion: on this model, wording in the skill does not reliably outweigh an explicit user
instruction about where a throwaway writeup goes. The current wording stays because it is the
intended behaviour, but it is not verified. A deterministic backstop (the wiki lint reporting
unexpected folders under `.bc-agent/` in a visible-layout project) is the proposed next step.

## Not covered

`bc-drain-issues` and `handoff`: drain needs an issue tracker and a multi-agent landing run,
which a throwaway project without a remote does not provide.

## Follow-up (2026-11-12)

The owner decided not to keep stronger wording that the model does not follow. `prototype` now
recommends the research role and, when the user explicitly names another place, follows the user,
says the research role is where later work will look and offers to move the writeup. The backstop
is deterministic: `bc-wiki-maintain`'s lint reports every entry under `.bc-agent/` that is not
agent mechanics (a `scratch/` folder included) as an error in a visible-layout project. The
softened wording has not been rerun against this scenario.
