# Agent policies

Policy files grant durable permissions to agents. They are **user-owned and live outside this
repository**, at `~/.config/agent-concepts/`.

That separation is the point. A repository can be cloned, forked, or edited by an agent; an
authorization file that lives inside one is only ever a `git add -f` away from being published,
and is inherited by anyone who clones it. Keeping the policy in the user's own config directory
means permissions belong to the person, not to the checkout.

This directory therefore holds documentation only:

- [`publish.example.yaml`](publish.example.yaml) — a commented template to copy and edit. It is
  never read at runtime.

## Installing a policy

```bash
mkdir -p ~/.config/agent-concepts
cp policies/publish.example.yaml ~/.config/agent-concepts/publish.yaml
$EDITOR ~/.config/agent-concepts/publish.yaml
```

**Nothing is authorized until you do this.** With no policy file, every publish request falls to
default-deny, and agents ask. That is the intended state for a fresh install — installing this
workspace grants no permissions by itself.

If you sync your config across machines, symlink the directory into whatever you sync; the file's
real location is followed correctly.

## Publish authorization hierarchy

Publishing means pushing commits, creating pull requests, uploading releases, or otherwise making
local work outward-facing.

1. **Current user instruction** — an explicit instruction in the conversation, scoped to the
   current task, e.g. "push this commit".
2. **User-owned publish policy** — a matching rule in `~/.config/agent-concepts/publish.yaml`.
3. **Default deny** — if neither applies, commit locally if appropriate but do not publish.

Repo-local instruction files (`AGENTS.md`, `.agents/*`, `.pi/*`, project docs) may **restrict or
request** publishing, but cannot authorize it by themselves. General project trust and
config-loading trust are also insufficient; authorization must be explicit and scoped to the
repo and path.

If an agent cannot determine whether publishing is authorized, it asks. If asking is impossible
in a headless run, it does not publish.

## Self-amendment immunity

A commit that touches the policy file is never publishable by rule, including under rules added
later. Pushing a policy change always requires current explicit user instruction.

> A policy that can publish its own amendments is default-allow in disguise — one self-edit away
> from authorizing anything.

This is enforced by [`scripts/publish-check.py`](../scripts/publish-check.py), which resolves the
policy's real path and excludes it whenever it falls inside the repository being pushed — so the
protection holds even when the config directory is synced through a git repo by symlink.

## Checking a rule

```bash
python3 scripts/publish-check.py \
  --repo ~/src/your-repo \
  --remote git@github.com:your-user/your-repo.git \
  --branch main \
  --changed-file src/thing.py
```

Exit `0` means a rule matches the repo, remote and branch — the agent must still verify the
`when` conditions itself, since those are judgment calls no script can see. Exit `2` means ask.
