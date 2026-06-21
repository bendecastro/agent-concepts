# Source: GoogleChrome/modern-web-guidance-src — Modern Web Guidance (design/UX subset)

Modern Web Guidance is Chrome DevRel's official set of agent **skills** that embed web-platform expertise and Baseline browser-compatibility data into coding agents, steering them away from legacy patterns. It is Google's closest analog to an "official frontend skill" — but note its center of gravity is *platform correctness, modernity, performance, and accessibility*, **not visual/aesthetic design** the way Anthropic's `frontend-design` and OpenAI's `frontend-skill` are. There is no Google "aesthetic direction" skill; for visual design the Google reference would be Material Design 3 (not captured here).

- **Repo:** https://github.com/GoogleChrome/modern-web-guidance-src (branch `main`)
- **Distribution repo (built skills):** https://github.com/GoogleChrome/modern-web-guidance
- **Docs:** https://developer.chrome.com/docs/modern-web-guidance
- **Captured:** 2026-06-21
- **Commit:** `eec2f8e5f7fad25b37fe592e4f62ad1e8168706e` (committed 2026-06-18)
- **Captured by:** agent, via blobless sparse `git clone` (design/UX-relevant paths only), `.git` removed.
- **License:** see upstream repo (Google/Chrome). Treat as upstream-owned; any concept we build is an adaptation, not redistribution.

## Why a partial snapshot

The full repo is ~110 MB / 1636 files, dominated by a bundled offline TensorFlow.js retrieval model (the CLI matches agent queries to guides locally — no API calls). That binary tooling is irrelevant to authoring our own skill. This snapshot keeps only the design/UX-relevant **content** in `snapshot/`:

| Path | What it is | Kept |
|---|---|---|
| `README.md`, `CONTEXT.md`, `EVALS.md`, `CONTRIBUTING.md` | project philosophy, structure, eval methodology | ✅ |
| `guides/AGENTS.md`, `guides/README.md` | how guides are authored/consumed | ✅ |
| `guides/user-experience/**` | 82 UX-pattern guides (the bulk of design-relevant material) | ✅ |
| `guides/css/**`, `guides/css-layout/**`, `guides/html/**` | modern CSS & layout guidance (3 guides + tasks/expectations) | ✅ |
| `guides/accessibility/**` | 2 a11y guides | ✅ |
| `.agents/skills/**` | Chrome team's own SKILL.md files (skill format + project workflow) | ✅ |
| `skills-src/README.md` | how the shipped skills are sourced | ✅ |
| `guides/{forms,performance,passkeys,security,privacy,built-in-ai,webmcp}` | platform/engineering guides, off-topic for a *design* skill | ❌ omitted |
| `skills-src/{chrome-extensions,cpp-on-the-web,passkeys,...}` reference trees | off-topic | ❌ omitted |
| `bin/`, `lib/`, `harness/`, `serving/`, `nightly/`, `eval-view/`, ML model | tooling/binaries | ❌ omitted |

Each guide directory typically holds `guide.md` (the guidance), `expectations.md` (what good looks like), and `tasks/task.md` (eval task) — useful as a model for how Google structures eval-backed agent guidance.

## Note for whoever ingests this

The genuinely transferable ideas here for our frontend-design concept are likely: (1) the **Baseline-gated "is this pattern safe yet"** discipline, (2) eval-backed guides (guide + expectations + task), and (3) the agent-skill structure. The aesthetic/"don't look templated" dimension comes from the Anthropic and OpenAI sources, not this one.
