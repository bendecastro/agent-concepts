# Install with `npx skills`

<!-- GENERATED from concepts/public-skills.json by `python3 scripts/lint.py --write-install-packs` -- do not edit by hand. -->

These commands use the [`skills` CLI](https://github.com/vercel-labs/skills).
Replace `<source>` with this repository at a release tag (`<owner>/<repo>@<tag>`)
or a local checkout path, and `<agent>` with your agent's id from the CLI's
[agent list](https://github.com/vercel-labs/skills/blob/main/docs/agents.md).
`-g` installs for your user rather than the current project; `-y` skips prompts.
Each command names its skills, so concepts not published as skills are never installed.

## All public skills

```bash
npx skills add <source> -g -a <agent> -y --skill bc-brainstorming bc-code-review bc-codebase-design bc-codebase-docs bc-council-audit-security bc-council-chain bc-council-challenge-plan bc-council-find-bugs bc-council-improve-architecture bc-council-mode bc-delegate-investigation bc-design bc-diagnosing-bugs bc-dispatching-parallel-agents bc-domain-modeling bc-durable-subagents bc-executing-plans bc-explain-visually bc-find-bugs bc-finishing-development-branch bc-grilling bc-handoff bc-improve-codebase-architecture bc-json-canvas bc-minimal-solution-ladder bc-obsidian-bases bc-obsidian-markdown bc-optimize-code bc-performance-guardrails bc-pipeline-to-done bc-plain-language bc-plan-slicing bc-plan-to-pipeline bc-prd-drafting bc-prompting-agents bc-prototype bc-qmd bc-research bc-safe-runs bc-security-audit bc-self-improve bc-seo bc-setup-project bc-subagent-driven-development bc-swarm bc-tdd bc-teach bc-to-spec bc-to-tickets bc-triage bc-ui-design bc-unslop bc-using-git-worktrees bc-wiki-maintain bc-work-sync bc-writing-plans
```

## Packs

Each pack is one skill plus every skill it needs, directly or through another needed skill.

### bc-code-review

```bash
npx skills add <source> -g -a <agent> -y --skill bc-code-review bc-codebase-docs bc-explain-visually bc-safe-runs bc-tdd bc-using-git-worktrees
```

### bc-codebase-docs

```bash
npx skills add <source> -g -a <agent> -y --skill bc-codebase-docs bc-explain-visually
```

### bc-council-audit-security

```bash
npx skills add <source> -g -a <agent> -y --skill bc-council-audit-security bc-council-chain bc-council-mode bc-security-audit
```

### bc-council-chain

```bash
npx skills add <source> -g -a <agent> -y --skill bc-council-chain bc-council-mode
```

### bc-council-challenge-plan

```bash
npx skills add <source> -g -a <agent> -y --skill bc-council-challenge-plan bc-council-chain bc-council-mode bc-grilling
```

### bc-council-find-bugs

```bash
npx skills add <source> -g -a <agent> -y --skill bc-council-find-bugs bc-council-chain bc-council-mode bc-find-bugs bc-safe-runs bc-using-git-worktrees
```

### bc-council-improve-architecture

```bash
npx skills add <source> -g -a <agent> -y --skill bc-council-improve-architecture bc-council-chain bc-council-mode bc-improve-codebase-architecture
```

### bc-delegate-investigation

```bash
npx skills add <source> -g -a <agent> -y --skill bc-delegate-investigation bc-durable-subagents bc-safe-runs bc-swarm bc-tdd bc-using-git-worktrees
```

### bc-diagnosing-bugs

```bash
npx skills add <source> -g -a <agent> -y --skill bc-diagnosing-bugs bc-safe-runs bc-using-git-worktrees
```

### bc-dispatching-parallel-agents

```bash
npx skills add <source> -g -a <agent> -y --skill bc-dispatching-parallel-agents bc-safe-runs bc-using-git-worktrees
```

### bc-durable-subagents

```bash
npx skills add <source> -g -a <agent> -y --skill bc-durable-subagents bc-safe-runs bc-using-git-worktrees
```

### bc-executing-plans

```bash
npx skills add <source> -g -a <agent> -y --skill bc-executing-plans bc-safe-runs bc-using-git-worktrees
```

### bc-find-bugs

```bash
npx skills add <source> -g -a <agent> -y --skill bc-find-bugs bc-safe-runs bc-using-git-worktrees
```

### bc-finishing-development-branch

```bash
npx skills add <source> -g -a <agent> -y --skill bc-finishing-development-branch bc-safe-runs bc-using-git-worktrees
```

### bc-optimize-code

```bash
npx skills add <source> -g -a <agent> -y --skill bc-optimize-code bc-safe-runs bc-using-git-worktrees
```

### bc-pipeline-to-done

```bash
npx skills add <source> -g -a <agent> -y --skill bc-pipeline-to-done bc-codebase-docs bc-explain-visually bc-performance-guardrails bc-safe-runs bc-tdd bc-using-git-worktrees
```

### bc-plan-to-pipeline

```bash
npx skills add <source> -g -a <agent> -y --skill bc-plan-to-pipeline bc-domain-modeling bc-grilling bc-plan-slicing bc-prd-drafting
```

### bc-prototype

```bash
npx skills add <source> -g -a <agent> -y --skill bc-prototype bc-safe-runs bc-using-git-worktrees
```

### bc-safe-runs

```bash
npx skills add <source> -g -a <agent> -y --skill bc-safe-runs bc-using-git-worktrees
```

### bc-setup-project

```bash
npx skills add <source> -g -a <agent> -y --skill bc-setup-project bc-teach
```

### bc-subagent-driven-development

```bash
npx skills add <source> -g -a <agent> -y --skill bc-subagent-driven-development bc-safe-runs bc-using-git-worktrees
```

### bc-swarm

```bash
npx skills add <source> -g -a <agent> -y --skill bc-swarm bc-durable-subagents bc-safe-runs bc-tdd bc-using-git-worktrees
```

### bc-tdd

```bash
npx skills add <source> -g -a <agent> -y --skill bc-tdd bc-safe-runs bc-using-git-worktrees
```

### bc-ui-design

```bash
npx skills add <source> -g -a <agent> -y --skill bc-ui-design bc-design
```

### bc-using-git-worktrees

```bash
npx skills add <source> -g -a <agent> -y --skill bc-using-git-worktrees bc-safe-runs
```

### bc-writing-plans

```bash
npx skills add <source> -g -a <agent> -y --skill bc-writing-plans bc-safe-runs bc-using-git-worktrees
```
