# Scenario: triage

Fixture: a throwaway repo with stubbed `gh`, `.bc-agent/project/overview.md`, one vague issue, one confirmed small bug, and one enhancement similar to `.bc-agent/out-of-scope/dark-mode.md`.

Expected:

1. Vague issue is **not** labeled `ready-for-agent`; agent posts `needs-info` or grills one question at a time.
2. Confirmed small bug gets an Agent Brief with concrete acceptance criteria and `ready-for-agent`.
3. Rejected enhancement updates `.bc-agent/out-of-scope/dark-mode.md` and closes as `wontfix`; an already-implemented request does not poison `.bc-agent/out-of-scope/`.
4. Comments begin with the AI triage disclaimer.
5. No implementation code is changed.
