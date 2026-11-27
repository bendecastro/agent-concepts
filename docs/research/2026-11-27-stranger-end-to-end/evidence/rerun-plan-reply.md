Plan created in [`work/1-planned/003-normalize-internal-whitespace.md`](work/1-planned/003-normalize-internal-whitespace.md).

It has one slice: collapse runs of Python whitespace into ordinary spaces while preserving the API, punctuation, lowercase behavior, and empty results. It has no blockers and covers both user stories; the small public-function change and its tests fit one lifecycle.

The work index check passes. No implementation was made. The item is ready for an agent, and `/bc-pipeline-to-done` can build it unattended.