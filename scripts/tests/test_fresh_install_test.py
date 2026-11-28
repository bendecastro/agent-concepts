#!/usr/bin/env python3
"""Unit checks for fresh installs and a kernel integration test with npm-installed Pi."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import fresh_install_test as fit  # noqa: E402
from install_packs import load_listing  # noqa: E402


class FreshInstallCheckTest(unittest.TestCase):
    def setUp(self):
        self.listing = load_listing(fit.ROOT)

    def test_all_skills_is_the_public_list(self):
        self.assertEqual(fit.expected_skills(self.listing), set(self.listing))

    def test_pack_expects_its_needed_skills(self):
        expected = fit.expected_skills(self.listing, fit.DEFAULT_PACK)
        self.assertIn(fit.HELPER_SKILL, expected)
        self.assertTrue(set(self.listing[fit.DEFAULT_PACK]) <= expected)

    def test_missing_needed_skill_fails_the_check(self):
        expected = fit.expected_skills(self.listing, fit.DEFAULT_PACK)
        installed = expected - {fit.HELPER_SKILL}
        self.assertEqual(fit.list_problems(expected, installed), [f"missing: {fit.HELPER_SKILL}"])
        with self.assertRaises(fit.CheckFailed):
            fit.check_listed("after install", expected, dict.fromkeys(installed, Path()))

    def test_extra_skill_fails_the_check(self):
        self.assertEqual(fit.list_problems({"a"}, {"a", "b"}), ["unexpected: b"])

    def test_pack_command_comes_from_the_guide_and_drops_on_request(self):
        command = fit.pack_command(fit.DEFAULT_PACK)
        self.assertEqual(command[:3], ["skills", "add", str(fit.ROOT)])
        self.assertEqual(set(command[command.index("--skill") + 1:]),
                         fit.expected_skills(self.listing, fit.DEFAULT_PACK))
        dropped = fit.pack_command(fit.DEFAULT_PACK, drop=fit.HELPER_SKILL)
        self.assertNotIn(fit.HELPER_SKILL, dropped)
        self.assertEqual(len(dropped), len(command) - 1)

    def test_local_install_uses_the_checkout(self):
        self.assertEqual(set(map(tuple, fit.install_sources(None).values())), {(str(fit.ROOT),)})

    def test_ref_install_pins_the_github_repository_in_each_cli_syntax(self):
        sources = fit.install_sources("v0.1.0")
        self.assertEqual(sources["pi"], ["git:github.com/bendecastro/agent-concepts@v0.1.0"])
        self.assertEqual(sources["claude"], ["bendecastro/agent-concepts#v0.1.0"])
        self.assertEqual(sources["codex"], ["bendecastro/agent-concepts", "--ref", "v0.1.0"])
        self.assertEqual(sources["npx"], ["bendecastro/agent-concepts@v0.1.0"])
        command = fit.pack_command(fit.DEFAULT_PACK, source=sources["npx"][0])
        self.assertEqual(command[:3], ["skills", "add", "bendecastro/agent-concepts@v0.1.0"])

    def test_packed_package_must_hold_kernel_roles_and_licence(self):
        complete = ["package.json", "README.md", "LICENSE", *fit.PACKED_REQUIRED]
        self.assertEqual(fit.packed_problems(complete), [])
        problems = fit.packed_problems([p for p in complete if p != "packages/agent-kernel-pi/AGENT-KERNEL.md"])
        self.assertEqual(problems, ["missing from the packed package: packages/agent-kernel-pi/AGENT-KERNEL.md"])

    def test_packed_package_must_not_hold_work_items_or_research(self):
        complete = ["package.json", "README.md", "LICENSE", *fit.PACKED_REQUIRED]
        problems = fit.packed_problems([*complete, "work/README.md", "concepts/bc-tdd/tests/x.md"])
        self.assertEqual(problems, ["outside the shipped files: concepts/bc-tdd/tests/x.md",
                                    "outside the shipped files: work/README.md"])

    def test_pi_npm_installs_the_packed_checkout_even_with_a_ref(self):
        self.assertIn("pi-npm", fit.METHODS)
        self.assertEqual(fit.install_sources("v0.1.0")["pi-npm"], [str(fit.ROOT)])

    def test_helper_exists_in_the_source(self):
        self.assertTrue((fit.ROOT / "concepts" / fit.HELPER_SKILL / "body" / fit.HELPER_RELPATH).is_file())


@pytest.mark.parametrize("has_checker", [False, True], ids=["missing", "present"])
def test_claude_install_checks_for_bundled_publish_checker(tmp_path, monkeypatch, has_checker):
    skill = "bc-pipeline-to-done"
    listing = {skill: [], fit.HELPER_SKILL: []}
    checker = Path("scripts/publish-check.py")

    def install(plugin):
        cache = plugin.box.home / ".claude" / "plugins" / "cache" / "concepts"
        for name, relpath in [(fit.HELPER_SKILL, fit.HELPER_RELPATH), (skill, checker)]:
            body = cache / name / "body"
            body.mkdir(parents=True)
            (body / "SKILL.md").touch()
            if name != skill or has_checker:
                (body / relpath).parent.mkdir(parents=True, exist_ok=True)
                (body / relpath).touch()

    def run(box, *args, **kwargs):
        if args[:3] == ("claude", "plugin", "list"):
            return '[{"id":"agent-concepts"}]' if not removed else "[]"
        if args[:3] == ("claude", "plugin", "details"):
            return f"Skills (2) {skill}, {fit.HELPER_SKILL}"
        if args[0] == sys.executable and args[-1] == "--help":
            return "usage"
        pytest.fail(f"unexpected sandbox command: {args}")

    removed = []
    monkeypatch.setattr(fit.Sandbox, "run", run)
    monkeypatch.setattr(fit.ClaudePlugin, "install", install)
    monkeypatch.setattr(fit.ClaudePlugin, "update", lambda plugin: None)
    monkeypatch.setattr(fit.ClaudePlugin, "uninstall", lambda plugin: removed.append(True))
    if has_checker:
        fit.run_method("claude", tmp_path, listing, fit.DEFAULT_PACK, None)
    else:
        with pytest.raises(fit.CheckFailed, match=r"bc-pipeline-to-done/scripts/publish-check\.py"):
            fit.run_method("claude", tmp_path, listing, fit.DEFAULT_PACK, None)


if __name__ == "__main__":
    unittest.main()


@pytest.fixture
def packed_pi(tmp_path):
    with TemporaryDirectory(dir=tmp_path) as scratch:
        box = fit.Sandbox(Path(scratch), "kernel")
        kernel = box.root / "package/packages/agent-kernel-pi/AGENT-KERNEL.md"
        kernel.parent.mkdir(parents=True)
        kernel.write_text("packaged kernel")
        yield fit.PiNpmPackage(box, [str(fit.ROOT)]), kernel


def test_pi_npm_rejects_array_instead_of_prompt_text(packed_pi, monkeypatch):
    agent, kernel = packed_pi

    def run(args, **kwargs):
        return subprocess.CompletedProcess(args, 0, json.dumps([kernel.read_text()]), "")

    monkeypatch.setattr(subprocess, "run", run)
    with pytest.raises(fit.CheckFailed, match="Pi system prompt is not non-empty text"):
        agent.check_kernel_prompt()


def test_pi_npm_rejects_empty_kernel_even_with_prompt_text(packed_pi, monkeypatch):
    agent, kernel = packed_pi
    kernel.write_text("")

    def run(args, **kwargs):
        return subprocess.CompletedProcess(args, 0, json.dumps("assembled prompt"), "")

    monkeypatch.setattr(subprocess, "run", run)
    with pytest.raises(fit.CheckFailed, match="packaged kernel is empty"):
        agent.check_kernel_prompt()


def test_pi_npm_reports_failed_probe_even_with_valid_stdout(packed_pi, monkeypatch):
    agent, kernel = packed_pi

    def run(args, **kwargs):
        return subprocess.CompletedProcess(args, 7, json.dumps(kernel.read_text()), "probe broke")

    monkeypatch.setattr(subprocess, "run", run)
    with pytest.raises(fit.CheckFailed,
                       match=r"(?s)could not read Pi system prompt: node exited 7:.*probe broke"):
        agent.check_kernel_prompt()


def test_pi_npm_checks_kernel_in_system_prompt(tmp_path):
    pi = shutil.which("pi")
    if not pi or not all(shutil.which(cmd) for cmd in ("npm", "node", "tar")):
        pytest.skip("Pi and npm tools are required")
    resolved = Path(pi).resolve()
    # Match the package root used by the probe, then verify the declared npm bin.
    root = resolved.parent.parent.parent
    try:
        pi_bin = json.loads((root / "package.json").read_text())["bin"]["pi"]
    except (OSError, ValueError, TypeError, KeyError):
        pi_bin = None
    if not isinstance(pi_bin, str) or (root / pi_bin).resolve() != resolved:
        pytest.skip("pi on PATH does not resolve to an npm package bin (it may be a shim)")

    with TemporaryDirectory(dir=tmp_path) as scratch:
        box = fit.Sandbox(Path(scratch), "kernel")
        agent = fit.PiNpmPackage(box, [str(fit.ROOT)])
        agent.install()
        extension = box.root / "package/packages/agent-kernel-pi/index.js"
        contents = extension.read_text()
        manifest = box.root / "package/package.json"
        manifest_text = manifest.read_text()
        data = json.loads(manifest_text)
        data["pi"]["extensions"] = []
        try:
            manifest.write_text(json.dumps(data))
            extension.unlink()
            with pytest.raises(fit.CheckFailed) as exc:
                agent.check_kernel_prompt()
            assert str(exc.value) == "kernel missing from Pi system prompt"
            print(f"  expected failure: {exc.value}")
        finally:
            extension.write_text(contents)
            manifest.write_text(manifest_text)
        agent.check_kernel_prompt()
