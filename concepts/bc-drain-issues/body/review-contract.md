# Independent review contract

The driver dispatches fresh **Spec** and **Standards** reviewers in parallel. Both are read-only and independent: no edits, commits, pushes, issue mutations, resets, cleanup, or worktree management. Independence is costly but necessary because one axis must not anchor the other or let implementation reasoning substitute for observable evidence.

## Minimal packet

Each reviewer receives only:

- explicit worktree path and base SHA;
- issue/latest Agent Brief and acceptance matrix;
- changed-file list and exact diff location/range;
- targeted-validation summary, baseline delta, and raw-log paths;
- on re-review only, prior findings and their dispositions.

Do not include worker reasoning, an accumulating implementation transcript, the parent transcript, or the other reviewer's report. The packet is complete: do not request generic `plan.md`, `progress.md`, or similarly conventional artifacts unless the driver explicitly supplied them; their absence is not a review blocker.

## Independent scopes

**Spec** checks requirement and acceptance-matrix fidelity, missing/wrong observable behavior, compatibility preservation, externally visible semantics, and scope creep. It does not perform a general style walkthrough.

**Standards** checks binding repository rules and material integration, correctness, test quality, portability, security, maintainability, and documentation risks. It does not re-grade product intent except where a standards defect makes the stated behavior unsafe or false. For material claims about external platforms, it checks available primary documentation/help rather than trusting repository prose or syntactic string tests alone.

Both may inspect repository context and run a bounded targeted reproduction needed to prove or refute a material finding. They must not run the full project suite; the driver already owns cached baseline and final full validation. Avoid broad investigation that is not tied to a plausible Critical/Important defect.

## Output

Return only strict compact JSON (no Markdown, walkthrough, `Correct` section, summary, or extra keys):

```json
{
  "verdict": "approved | changes_requested",
  "findings": [
    {
      "severity": "critical | important | minor",
      "requirement": "specific requirement or binding standard",
      "location": "file:line",
      "evidence": "concise observable evidence"
    }
  ]
}
```

`approved` requires an empty `findings` array. `changes_requested` requires at least one Critical or Important finding; Minor findings may accompany that material finding but never determine the verdict. Omit minor-only observations from this gate rather than making approval ambiguous. Findings must be actionable and evidence-backed; missing evidence is not itself proof of a defect unless the contract requires that evidence.

## Focused re-review

A fresh re-review receives previous findings/dispositions and focuses on the changed hunks, whether each prior material finding is resolved, and regression risk created by the fix. It retains authority to report a newly introduced material defect, but must not reopen unchanged, already-disposed questions without new evidence or expand into a full-codebase review. Output uses the same schema.
