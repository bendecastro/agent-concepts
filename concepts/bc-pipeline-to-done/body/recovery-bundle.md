# Deferred rework recovery bundle

Before releasing an agent-fixable deferred issue, the driver captures a machine-local bundle at:

```text
${XDG_STATE_HOME:-$HOME/.local/state}/bc-drain/recovery/<repo-key>/issue-<n>/
├── manifest.json
├── tracked.patch
├── untracked.tar.gz
├── acceptance-matrix.json
├── findings.json
└── validation.json
```

The separate GitHub `## Agent Rework Brief` is the portable fallback; uncommitted code recovery is not promised across machines. Keep this contract instruction-level and use safe platform tools rather than assuming a particular harness or script.

## Exact contents

- `manifest.json`: schema version, repository and remote identity, issue number, run ID, base SHA, Git object format, canonical captured-tree OID, review round, exact changed-file set, validation artifact hashes, archive/patch byte hashes, and explicit exclusions.
- `tracked.patch`: binary-safe full tracked diff from the recorded base, including deletions and mode changes, generated without external diff drivers using the equivalent of `git diff --binary --full-index --no-ext-diff <base> --`.
- `untracked.tar.gz`: only safe untracked files in the exact issue changed-file set, stored as relative paths.
- `acceptance-matrix.json`: current requirements/evidence mapping.
- `findings.json`: all review findings, dispositions, attempt count, and unresolved material findings.
- `validation.json`: commands, exit status, failing test IDs, baseline delta, concise summaries, non-absolute durable raw-log identifiers (or paths relative to the recovery root), and content hashes. Raw logs stay outside the project worktree and need not be embedded.

Never include ignored files, caches/build products, credentials or secret-shaped content, absolute paths, `.pi-subagents`, files outside the issue changed-file set, repository metadata, or paths that escape through `..` or absolute/archive-root syntax. Reject untracked symlinks, hard links, and special files. These exclusions prevent a recovery artifact from becoming a credential leak or arbitrary-file-write primitive.

## Canonical captured-tree identity

Exactness is defined by Git's tree object, not by tar metadata or a model-invented diff hash. In a temporary index that cannot alter the real worktree index:

1. initialize from the recorded base with the equivalent of `GIT_INDEX_FILE=<temp> git read-tree <base>`;
2. stage exactly the manifest changed-file set from the candidate worktree with `GIT_INDEX_FILE=<temp> git add -A -- <paths...>` after path/type/secret checks;
3. record `GIT_INDEX_FILE=<temp> git write-tree` as `captured_tree_oid` plus the repository's Git object format.

Repeat the same recipe in the fresh matching-base round trip and require the OID to match. Git then canonically covers path bytes, file bytes, executable modes, additions, and deletions. Patch/archive SHA-256 values are byte-integrity checks for the one published bundle; generators are not expected to produce byte-identical tar archives independently.

## Capture validation

Before releasing the worktree:

1. derive and record the exact changed-file set from status and the base diff; inspect every untracked candidate;
2. reject unsafe names/types and secret-shaped content rather than silently broadening or omitting required issue work;
3. compute the canonical captured-tree identity with the temporary-index recipe above;
4. create all six artifacts in a temporary sibling location, hash their exact bytes, then atomically publish the completed bundle;
5. list the archive without extraction and verify every member is a safe expected relative regular file;
6. restore into a fresh temporary checkout at the recorded base, inspect status/diff, and require the changed-file set and recomputed captured-tree OID to match the manifest exactly;
7. verify JSON parses, identities/base agree, referenced hashes resolve, and validation evidence is internally consistent.

Only a successfully round-tripped bundle permits destructive worktree release. Do not commit or push a recovery branch.

## Restore

First verify manifest version, repository/remote/issue identity, all artifact hashes, safe paths/types, and the expected changed-file set.

**Matching base SHA:** restore the tracked patch and safe untracked regular files into a clean issue worktree; verify the entire status/diff and changed-file set, then recompute and require the canonical captured-tree OID exactly; run relevant validation before continuing focused review/rework.

**Changed base SHA:** apply the tracked patch with a three-way mechanism, restore only validated safe untracked files, inspect the **entire** resulting diff for conflicts/scope, and run relevant validation. The old captured-tree OID identifies the captured input but cannot equal a tree integrated onto a different base. Treat all prior approvals as invalid and run full fresh Spec and Standards review.

Never overwrite an existing unrelated path, guess through an ambiguous conflict, or extract an archive before member validation.

## Portable issue brief

Post without secrets or machine-dependent absolute paths:

```text
## Agent Rework Brief
Base SHA: <sha>
Unresolved findings:
- <severity, requirement, location, evidence, attempts>
Validation: <commands/outcomes, baseline delta, durable artifact identifiers>
Next agent:
- <specific restore/reproduce/fix/re-review actions>
Recovery: machine-local bundle captured and validated | unavailable
```

## Fail safe

Unsafe paths, secret suspicion, identity/hash mismatch, missing required content, failed round-trip, restore failure, or ambiguous conflict must stop restoration/release. Preserve the original worktree and evidence when possible. Route the issue to `HUMAN_BLOCKED` with exact evidence if safe preservation or interpretation requires human action; if infrastructure prevents capture across issues, classify the run `SYSTEMIC_FAILURE`. Never claim exact recovery, delete useful work, or improvise a partial bundle after validation fails.
