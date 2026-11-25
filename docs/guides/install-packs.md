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
npx skills add <source> -g -a <agent> -y --skill bc-autoresearch-loop bc-brainstorming bc-code-review bc-codebase-design bc-codebase-docs bc-council-audit-security bc-council-chain bc-council-challenge-plan bc-council-find-bugs bc-council-improve-codebase bc-council-mode bc-diagnosing-bugs bc-dispatching-parallel-agents bc-domain-modeling bc-executing-plans bc-find-bugs bc-finishing-development-branch bc-grilling bc-guardrails bc-handoff bc-improve-codebase-architecture bc-init-agent bc-json-canvas bc-minimal-solution-ladder bc-obsidian-bases bc-obsidian-markdown bc-pipeline-to-done bc-plain-language bc-plan-slicing bc-plan-to-pipeline bc-prd-drafting bc-prompting-agents bc-prototype bc-qmd bc-reflect bc-research bc-security-audit bc-seo bc-show-me bc-subagent-driven-development bc-swarm bc-tdd bc-teach bc-to-spec bc-to-tickets bc-triage bc-ui-design bc-unslop bc-using-git-worktrees bc-wiki-maintain bc-work-sync bc-writing-plans
```

## Packs

Each pack is one skill plus every skill it needs, directly or through another needed skill.

### bc-code-review

```bash
npx skills add <source> -g -a <agent> -y --skill bc-code-review bc-codebase-docs bc-show-me bc-tdd
```

### bc-codebase-docs

```bash
npx skills add <source> -g -a <agent> -y --skill bc-codebase-docs bc-show-me
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
npx skills add <source> -g -a <agent> -y --skill bc-council-find-bugs bc-council-chain bc-council-mode bc-find-bugs
```

### bc-council-improve-codebase

```bash
npx skills add <source> -g -a <agent> -y --skill bc-council-improve-codebase bc-council-chain bc-council-mode bc-improve-codebase-architecture
```

### bc-init-agent

```bash
npx skills add <source> -g -a <agent> -y --skill bc-init-agent bc-teach
```

### bc-pipeline-to-done

```bash
npx skills add <source> -g -a <agent> -y --skill bc-pipeline-to-done bc-codebase-docs bc-show-me bc-tdd
```

### bc-plan-to-pipeline

```bash
npx skills add <source> -g -a <agent> -y --skill bc-plan-to-pipeline bc-domain-modeling bc-grilling bc-plan-slicing bc-prd-drafting
```

### bc-swarm

```bash
npx skills add <source> -g -a <agent> -y --skill bc-swarm bc-tdd
```
