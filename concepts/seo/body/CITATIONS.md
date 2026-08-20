# Citations: claim → source map

Maps the load-bearing claims in `SKILL.md` and `IMAGE-SEO.md` to the primary sources held in `../../../docs/research/raw/ingested/seo-primary-sources/` (each file's header carries its origin URL). Maintained with the concept: when a body claim changes, update its row; when a row has no held source, that's a lint-worthy gap. Snapshot dates matter — these documents evolve; re-verify at runtime for time-sensitive use, per the body's own rules.

| Claim in body | Held source | Status |
|---|---|---|
| CWV "good" thresholds: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1, measured at p75 field data | `webdev-core-web-vitals.md` | Verified 2026-06-12. 2026 SEO-blog claims of changed thresholds did NOT match official docs at snapshot time. |
| Link schemes, cloaking, doorway pages, scaled content abuse, expired-domain abuse, hidden text = spam violations | `google-spam-policies.md` | Verified 2026-06-12 |
| Google uses alt text, computer vision, and page content to understand images; descriptive filenames give a light clue | `google-image-seo.md` | Verified 2026-06-12 |
| `max-image-preview:large` is a robots-meta directive controlling preview size (precondition for large previews/Discover treatment) | `google-robots-meta.md` | Verified 2026-06-12 |
| `<meta name="rating" content="adult">` is the documented SafeSearch flagging mechanism; structural separation of explicit content recommended | `google-safesearch.md` | Verified 2026-06-12 |
| Google-Extended is a robots.txt control for Gemini/Vertex training that does not affect Google Search rankings | `google-common-crawlers.md` | Verified 2026-06-12 |
| OpenAI splits GPTBot (training) from OAI-SearchBot (search citations); blocking one ≠ blocking the other | `openai-bots.md` | Verified 2026-06-12 |
| Decorative images get empty `alt=""`; functional images describe the action; complex images need a long description | `w3c-alt-decision-tree.md` | Verified 2026-06-12 |
| ClaudeBot (training) vs Claude-SearchBot (search) split | — (Anthropic docs not yet snapshotted) | Corroborated via 2026-06-12 web research only — fetch support.anthropic.com bot docs to close |
| IPTC/XMP fields powering the Licensable badge (Creator, Web Statement of Rights, Licensor URL) | — (cite by URL: iptc.org standard + Google image-license-metadata page) | Not yet snapshotted |
| llms.txt not honored by major AI systems (Q1 2026) | — | Secondary sources only (limy.ai, nohacks.co, digitalapplied.com surveys, 2026-06-12); inherently time-sensitive — always re-verify |
| E-E-A-T cluster, topical authority, internal-linking effect sizes | — | Mixture of Google guidance and correlational field studies; body already labels these as correlation/verify-at-runtime — no single citable document |

## Maintenance

- Re-verify "Verified" rows when a body claim is edited or a Google core update ships; refresh snapshots rather than trusting old ones for current advice.
- Close the three open rows opportunistically (Anthropic bots page, IPTC/licensable pages).
