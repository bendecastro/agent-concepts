# Requirements: setup leaves a passing gate and a working CI job

## Problem Statement

`bc-setup-project` fills `./scripts/gate` only "with the verified commands its CI already runs". A repository with tests but no CI keeps the deliberately red stub, and red trunk CI blocks landing. The generated `.github/workflows/gate.yml` says "TODO: set up the toolchain scripts/gate needs", so a project needing Node, Rust or uv fails in CI while green locally. The validation and file-layout conventions are left for "the user" to fill.

## Solution

- **No CI:** derive the gate from the project's documented local commands (README, package scripts, Makefile/justfile, `pyproject`/`Cargo.toml` defaults), run it, and keep it only if it passes or fails only on known failures recorded as such; if no runnable command is found, the close-out names "fill the gate" as an owner action and adds a planned item for it.
- **CI toolchain:** fill the job's setup steps from existing CI when there is one, else from lockfiles and markers (setup actions for the detected languages, dependency install). Unknowns are reported, not guessed.
- **Conventions:** fill `conventions/validation.md` (while working, full gate) and `file-layout.md` from verified survey facts; Release stays TODO unless the survey found release checks, and the close-out says so.

## User Stories

1. As a stranger with tests but no CI, setup leaves me a gate that passes.
2. As a stranger, the generated CI job installs my toolchain.
3. As a stranger, my validation and file-layout conventions describe my project.
4. As a stranger, anything setup could not settle is an owner action I can see, not a silent TODO.

## Testing Decisions

- Pressure scenarios (pressure-test model, blind baseline) on two fixture repositories built by the test: a Python package with `pytest` and no CI, and a Node package with an existing CI workflow. Graded on the written gate, workflow and conventions, and on the gate actually passing in the fixture.

## Out of Scope

- Running CI remotely during setup; release automation; non-GitHub CI.
