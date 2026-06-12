# omarchy

Reference skill for end-user customization of Omarchy Linux systems (Hyprland window manager, waybar, walker, terminals, themes, hooks, and the `omarchy` CLI). It encodes the safe-edit boundary — `~/.config/` is editable, `~/.local/share/omarchy/` is read-only upstream source — plus config-file maps and customization patterns.

## Design decision: no vendored body

Unlike every other concept, this one has **no `body/` directory, on purpose**. The skill is authored and maintained upstream by Basecamp inside the Omarchy distribution itself, and `omarchy update` keeps it current on the machine. Vendoring a copy here would fork it and silently go stale — we explicitly chose to take advantage of upstream maintenance instead (user decision, 2026-06-12).

Consequences:

- **Canonical body:** `~/.local/share/omarchy/default/omarchy-skill/SKILL.md` (upstream-owned; the canon gate's "never edit upstream" applies doubly — the skill itself declares that directory read-only).
- **Deploy:** `~/.claude/skills/omarchy` → `~/.local/share/omarchy/default/omarchy-skill` (absolute symlink created by the Omarchy installer, not by this workspace). Only meaningful on machines running Omarchy (the Arch box); macOS/Debian machines simply have a dangling or absent symlink, which is correct.
- **Editing:** if we ever want our own additions, the move is a *new* concept layering on top (or upstreaming a PR to basecamp/omarchy) — not editing this one into a fork.

## Provenance

- `ideas/omarchy-skill-upstream/` — immutable snapshot of the upstream SKILL.md with full citation (repo, path, commits, MIT license). Reference only; never deploy from it.
- Upstream: https://github.com/basecamp/omarchy (`default/omarchy-skill/SKILL.md`).

## Tests

Reference concept with no runtime gates of ours; per the test gate only an accuracy check applies — and accuracy is upstream's responsibility. Verified 2026-06-12 that the deployed symlink resolves and the content matches the snapshot at filing time.
