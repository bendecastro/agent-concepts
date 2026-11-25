# Targets from published guidelines

Use this when a limit is about what a person feels (smooth motion, a page appearing, a reply to a tap or keypress). Take the number from a guideline, cite it on the guardrails page, and record it as the agent's choice. These are guidelines for typical devices, not measurements of this project.

| Target | Default | Source |
|---|---|---|
| Animation and scrolling | one frame every 16 ms (60 per second); the app's own work about 10 ms, leaving about 6 ms for drawing | [Google RAIL](https://web.dev/articles/rail) |
| Web page: main content shown | 2.5 s or less (Largest Contentful Paint) | [Core Web Vitals](https://web.dev/articles/vitals) |
| Web page: reply to interaction | 200 ms or less (Interaction to Next Paint) | [Core Web Vitals](https://web.dev/articles/vitals) |
| Web page: layout shift | 0.1 or less (Cumulative Layout Shift) | [Core Web Vitals](https://web.dev/articles/vitals) |

Core Web Vitals are judged at the 75th percentile of page loads; measured in a test, use the same percentile over repeated runs.

## Splitting a target (budget decomposition)

When several steps share one target, give each step its own allowance and leave slack. Example: a 10 ms frame allowance for app work could be 4 ms for game logic, 4 ms for preparing what to draw, and 2 ms spare. Check the split against a real trace or timing, not a guess about where time goes. Source: [AWS Well-Architected, latency budgets](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentperf01-bp01.html).

## Size budgets

A download-size limit for a web app is a performance budget on bytes ([web.dev performance budgets](https://web.dev/articles/performance-budgets-101)). It has no published default: ratchet it from today's built size ([measuring.md](measuring.md)). Tools such as [Size Limit](https://github.com/ai/size-limit) or [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md#assert) can run it inside the gate.
