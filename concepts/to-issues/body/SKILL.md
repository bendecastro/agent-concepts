---
name: to-issues
description: Break a plan, spec, or PRD into independently-grabbable GitHub issues using tracer-bullet vertical slices.
disable-model-invocation: true
---

# To Issues

Slice a plan into independently-grabbable vertical slices, then publish them as GitHub issues. The slicing is the `/issue-slicing` discipline; this orchestrator wraps it with publication.

**Issue tracker: GitHub**, via the `gh` CLI. Slices that are ready for an agent to grab are published with the `ready-for-agent` label.

## Process

1. **Slice.** Run `/issue-slicing`: gather context (fetch any passed issue reference), draft vertical tracer-bullet slices, and **quiz the user on granularity and dependencies until they approve**. It returns the approved breakdown in dependency order.

2. **Publish to GitHub.** For each approved slice, publish a GitHub issue **in dependency order** (blockers first) so you can reference real issue numbers in "Blocked by":
   ```
   gh issue create --title "<slice title>" --label ready-for-agent --body-file <path>
   ```
   Publish with `ready-for-agent` unless instructed otherwise. **Do NOT close or modify any parent issue.**
