# Planning asks the dependency question every time

Why: In the v0.4.1 stranger test, `bc-plan-to-pipeline` wrote a ready item without a `Dependencies:` line and asked no dependency question, although the project's test rules call for property tests (Hypothesis). The builder parked on it correctly, costing an owner question mid-build. In the 0.4.0 run planning did ask, so the step is followed unreliably on the pressure-test model. Evidence: `docs/research/2026-11-27-release-audit.md`, "v0.4.1 soak".
Done when: Planning on the pressure-test model asks the dependency question (or records an owner answer) whenever the item's tests need a package the project lacks, in at least three of three runs of a scenario like the stranger fixture, and a ready item never lacks a `Dependencies:` line.
Stage: next
Blocked by: nothing
Kind: bug
Source: stranger test v0.4.1 (release soak)
