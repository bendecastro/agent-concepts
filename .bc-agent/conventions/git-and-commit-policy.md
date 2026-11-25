# Git and Commit Policy

Normal git discipline applies.

## Agent guidance

- Inspect `git status` first; stage and commit only your own changes — never sweep up
  unrelated edits the human has in progress.
- Commit agent-made changes before finishing the task.
- Push / close GitHub issues only when authorized by the user-owned publish policy
  (`~/.config/agent-concepts/publish.yaml`). After pushing, agents may close issues
  directly completed by the pushed work, leaving a comment with the commit SHA and a
  validation summary; never close partially satisfied or adjacent issues.
- Keep commits scoped, with concise messages. Do not rewrite history or re-init Git unless asked.
