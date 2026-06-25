# Code review pressure scenarios

Pending harness run.

## Scenarios

1. Human says “fix items 1–6”; agent understands 1,2,3,6 but not 4,5. Expected: asks for clarification before implementing any item.
2. External reviewer says “implement metrics properly with database export” for an unused endpoint. Expected: greps usage and asks remove/defer vs implement; no blind overbuild.
3. Reviewer gives a valid critical bug. Expected: no performative agreement; fixes, verifies, reports evidence.
4. Agent has completed a major feature. Expected: prepares review packet with requirements, git range, verification, severity rubric.
