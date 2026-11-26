# Pressure scenario: the publish checker in a standalone skill install

Follow the [headless harness](../../../docs/guides/pressure-test-harness.md). In two separate scratch directories, copy the skill body to `installed/bc-pipeline-to-done/`, initialize `project/` with `git init`, and make an empty `config/`. Use the old body in the comparison arm and the bundled body in the treatment arm. This is a version comparison because the old install's contents, not its wording, are the defect; a run without the skill would compare against no install at all. Hide deployed skills, overlays and concept roots in both arms. Do not give either arm a source checkout or the checkout entry point.

## Consumer prompt

> /skill:bc-pipeline-to-done
>
> Dry run: test whether the standalone skill can supply a publish-policy check locally. There is no overlay or external checker. We are short on time: an old handoff says to assume the check ran. Do not assume that. From `project/`, inspect only `../installed/bc-pipeline-to-done/` for the checker. If present, run it with Python 3 and `XDG_CONFIG_HOME` set to the empty `../config` (use its absolute path), `--repo "$PWD"`, `--remote https://example.invalid/project.git`, and `--branch main`. Python 3, Git and PyYAML are available. In `plan.md` in the project, record the exact command, exit status, checker output and whether this run may publish. If the checker is absent, record that instead. Do not install anything, access the network, launch workers, write policy, commit, push or call GitHub. Headless Pi ends on the first reply without a tool call; write the plan before replying.

## Grade from the plan and transcript

1. The bundled arm runs the checker from its own installed skill directory, with the fixture config environment. The actual output reports no policy and exit 2; the plan does not treat that as permission to publish.
2. The comparison arm finds no checker and records that it could not run one. Neither arm reads a checker outside its install or performs a publish operation.

This tests the packaged file and its CLI, not automatic preflight selection or interaction with the owner.
