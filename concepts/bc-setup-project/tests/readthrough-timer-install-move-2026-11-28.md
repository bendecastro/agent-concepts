# Read-through: timer install moved to bc-wiki-maintain (2026-11-28)

Work item `060-wiki-timer-install-to-wiki-maintain`. A read-through check, not a model run:
it follows setup step 10 into the moved file literally on a throwaway fixture and compares
what an agent would reach with the pre-move text (`git show ae13159:concepts/bc-setup-project/body/SKILL.md`, step 10).

## Fixture

`mktemp -d` with `skills/bc-setup-project -> concepts/bc-setup-project/body` and
`skills/bc-wiki-maintain -> concepts/bc-wiki-maintain/body` (the shared-bus symlink shape), plus
an empty `proj/.bc-agent/`. Deleted afterwards.

## Path the agent follows

1. Setup's `wiki_skill_dir` lookup: candidate 1 (`<dir>/../bc-wiki-maintain`) misses because
   `..` resolves past the symlink; candidate 2 (`<dir>/../../bc-wiki-maintain/body`) holds
   `wiki_lint.py`. Same result as before the move.
2. `test -f "$wiki_skill_dir/INSTALL-TIMER.md"`: present. `runner/README.md`,
   `runner/bc-wiki-maintain.service` and `runner/bc-wiki-maintain.timer`: present.
3. Step 10, unchanged lines: run `wiki_lint.py` on the vault for every archetype; the
   `wiki-lint-vaults.txt` detection-only note; code, ops and hybrid skip to step 11.
4. Step 10, learning and knowledge: "offer the per-vault promotion timer: read
   `$wiki_skill_dir/INSTALL-TIMER.md` and follow it; install nothing until the user confirms."
5. `INSTALL-TIMER.md`, in order: why the timer matters (no overnight promotion without it; not
   the qmd refresh timer; templates do not install themselves); show slug-suffixed names and env,
   offer, install only on confirm; never the unsuffixed `bc-wiki-maintain.service`; never vendor
   runner scripts; no `systemctl --user` → parking-lot TODO pointing at
   `$wiki_skill_dir/runner/README.md`; on confirm copy (not symlink), edit the placeholders
   (WorkingDirectory, VAULT_ROOT, PI_BIN, SyslogIdentifier, ExecStart, the timer's `Unit=`),
   stagger `OnCalendar` 15 minutes from other `bc-wiki-maintain*.timer`; the `install -Dm644`,
   `systemd-analyze --user verify`, `daemon-reload`, `enable --now`, `status` block; `PI_BIN`
   resolution; skip an existing matching unit; decline → same TODO.
6. Step 11 still notes the timer offer outcome.

## Comparison with the pre-move text

A script compared every non-blank line of the old step 10 learning/knowledge block (37 lines)
with the lines of `INSTALL-TIMER.md`. 35 appear verbatim. The other two are the block's opening
sentence, rewrapped: "For learning and knowledge" stays in setup as the offer line, and
"capture into `.bc-agent/log.md` is cheap; promotion is not" opens the moved file. The shell
block is byte-identical. Nothing was lost.

Result: PASS. Setup still offers the timer, and the procedure the agent reaches describes it
as before.
