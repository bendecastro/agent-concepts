# Source: kepano/obsidian-skills

- **Upstream:** [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)
- **Pinned commit:** [`a1dc48e68138490d522c04cbf5822214c6eb1202`](https://github.com/kepano/obsidian-skills/tree/a1dc48e68138490d522c04cbf5822214c6eb1202)
- **Snapshot date:** 2026-08-17
- **License:** MIT; the upstream notice is preserved in [`LICENSE`](LICENSE).
- **Upstream format references:** [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown), [Bases syntax](https://help.obsidian.md/bases/syntax), and [JSON Canvas 1.0](https://jsoncanvas.org/spec/1.0/).

This directory is an immutable evidence snapshot, not a deploy source. It contains the upstream README, license, and complete `skills/` tree at the pinned commit, including `obsidian-cli` and `defuddle` so the selective-ingestion decision remains auditable.

Only the three format skills were ingested into canonical concepts and deployed from this workspace:

- `obsidian-markdown`
- `obsidian-bases`
- `json-canvas`

`obsidian-cli` and `defuddle` were deliberately excluded from runtime deployment. The former overlaps the existing agent-safe `pi-obsidian-vault` boundary with broad writes and live-app evaluation; the latter is a generic network/content-extraction workflow already covered by the harness and is not an Obsidian format authority.

## Snapshot contents

- `LICENSE`
- `README.md`
- `skills/obsidian-markdown/` and its three references
- `skills/obsidian-bases/` and its functions reference
- `skills/json-canvas/` and its examples reference
- `skills/obsidian-cli/`
- `skills/defuddle/`

The canonical concepts adapt the format guidance and add this workspace's mutation-authority boundary; they do not symlink to or load this raw directory at runtime.

## Selected blob hashes

These SHA-256 values make the fetched evidence easy to compare with a future refresh:

- `LICENSE`: `64c64d48361edfe8610016441bf593256ea9b67f133b00f47c55aa29ee878567`
- `README.md`: `916f32671a4f0c8fdec84f8aa2ac1427d45aaa198edf41b7055e0da88ef251e1`
- `skills/obsidian-markdown/SKILL.md`: `7ad72e1f0a9081ed325e76b6402ad5de50a00e63e2341fd403a92f147234a007`
- `skills/obsidian-bases/SKILL.md`: `c0037f20926c7d8591cdd040365e4c0e4c0c4146386a506f28f241faee9a27d9`
- `skills/json-canvas/SKILL.md`: `97d1ae0728955c4203922753d5656890e5e4dd371b8306ea11884f9b510f1b85`
- `skills/obsidian-cli/SKILL.md`: `b54257cdc0e5d04488b35b0c797bfe427b24359f0848d3c73924dcacf8da6358`
- `skills/defuddle/SKILL.md`: `10673a4dc70a0a057612d443243ab7a5aa4abdd4a0fadc3f6eec5fd71ad5a971`
