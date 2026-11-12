"""Migrate mode of the scaffold: earlier `.bc-agent/` vault layout -> visible layout."""
from pathlib import Path
import importlib.util
import subprocess
import sys

import pytest

SCAFFOLD = Path(__file__).resolve().parents[1] / "body/scaffold.py"
SECTIONS = ("MOVE", "CREATE", "REPLACE", "DELETE", "KEPT (review by hand)", "NEEDS JUDGMENT",
            "LINKS", "OTHER REFERENCES")


def _module():
    spec = importlib.util.spec_from_file_location("scaffold", SCAFFOLD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _git(root, *args):
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True).stdout


def _commit_all(root, message="fixture"):
    _git(root, "add", "-A")
    _git(root, "-c", "user.name=t", "-c", "user.email=t@example.invalid", "commit", "-qm", message)


def _write(root, files):
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)


def _migrate(root, archetype="code", *extra):
    return subprocess.run(
        [sys.executable, str(SCAFFOLD), "--root", str(root), "--slug", "demo", "--date", "2026-01-02",
         "--archetype", archetype, "--migrate", *extra],
        capture_output=True, text=True)


def _sections(stdout):
    """Map each section heading to its indented item lines."""
    result, current = {}, None
    for line in stdout.splitlines():
        if line in SECTIONS:
            current = line
            result[current] = []
        elif current and line.startswith("  "):
            result[current].append(line.strip())
        elif current and line and not line.startswith("  "):
            current = None
    return result


def _vault_repo(tmp_path, archetype="code"):
    m = _module()
    root = tmp_path / "proj"
    root.mkdir()
    _git(root, "init", "-q", "-b", "main")
    files = {
        "README.md": "# Demo\n\nSee [ADR](.bc-agent/decisions/adr-0001-x.md) and [log](.bc-agent/log.md).\n"
                     "```\n[fenced](.bc-agent/decisions/adr-0001-x.md)\n```\n"
                     "Broken: [gone](nowhere/missing.md).\n",
        "AGENTS.md": "# Project rules\n\nHand-written.\n",
        "tools/run.sh": "cat .bc-agent/decisions/adr-0001-x.md\n",
        ".bc-agent/AGENTS.md": "# Old vault instructions\n\nCustom rule.\n",
        ".bc-agent/map.md": "# Map\n\nProject-written map.\n",
        ".bc-agent/log.md": "# Log\n\n- entry\n",
        ".bc-agent/archetype.md": "# Archetype\n",
        ".bc-agent/decisions/.gitkeep": "",
        ".bc-agent/decisions/adr-0001-x.md": "# ADR 1\n\nTasks: [active](../tasks/active.md). "
                                             "Readme: [r](../../README.md#top). Web: [w](https://example.com).\n",
        ".bc-agent/research/README.md": "# Research\n",
        ".bc-agent/research/2026-01-01-r/notes.md": "# Notes\n\nBack to [ADR](../../decisions/adr-0001-x.md).\n",
        ".bc-agent/tasks/active.md": "# Active\n\n- a\n- b\n",
        ".bc-agent/tasks/completed.md": "# Completed\n\n- done\n",
        ".bc-agent/tasks/parking-lot.md": "# Parking\n\n- idea\n",
        ".bc-agent/tasks/issue-drafts/01-slice.md": "# Slice\n",
        ".bc-agent/plans/p.md": "# Plan\n",
        ".bc-agent/project/overview.md": "# Overview\n",
        ".bc-agent/project/feature-prd.md": "# PRD\n",
        ".bc-agent/project/x-plan.md": "# X plan\n",
        ".bc-agent/findings/f.md": "# Finding\n",
        ".bc-agent/open-questions/q.md": "# Q\n",
        ".bc-agent/home.md": "# Home\n\n[[decisions/adr-0001-x|ADR]] and [[map]].\n",
        ".bc-agent/index.md": "# Index\n\n- [ADR](decisions/adr-0001-x.md)\n- [decisions](decisions/)\n",
        ".bc-agent/.obsidian/app.json": "{}\n",
        ".bc-agent/scratch/.gitkeep": "",
        ".bc-agent/out-of-scope/.gitkeep": "",
        ".bc-agent/conventions/planning-workflow.md": m.render(m.PLANNING_WORKFLOW, "demo", "2025-05-05"),
        ".bc-agent/conventions/validation.md": "# Validation\n\nRun make test.\n",
        ".bc-agent/templates/plan.md": m.render(m.TPL_PLAN, "demo", "2025-05-05"),
        "docs/adr/0002-y.md": "# ADR 2\n\nSee [one](../../.bc-agent/decisions/adr-0001-x.md).\n",
        "docs/plans/old.md": "# Old plan\n",
    }
    if archetype in {"ops", "hybrid"}:
        files[".bc-agent/components/host.md"] = "# Host\n"
    if archetype == "hybrid":
        files[".bc-agent/learning/plan.md"] = "# Mission\n"
    _write(root, files)
    _commit_all(root)
    return root


def _tree(root):
    return _git(root, "status", "--porcelain", "--untracked-files=all"), \
        sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if ".git" not in p.parts)


# --- dry run --------------------------------------------------------------------------

def test_dry_run_writes_nothing_and_prints_sections_in_order(tmp_path):
    root = _vault_repo(tmp_path)
    before = _tree(root)
    result = _migrate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert _tree(root) == before
    out = result.stdout
    assert out.splitlines()[0] == f"Repo: {root}"
    assert "Branch: main" in out
    assert "Archetype: code (from --archetype)" in out
    positions = [out.index("\n" + name + "\n") for name in SECTIONS]
    assert positions == sorted(positions)
    assert "--migrate --apply" in out.splitlines()[-1]


def test_migrate_requires_explicit_archetype(tmp_path):
    root = _vault_repo(tmp_path)
    result = subprocess.run([sys.executable, str(SCAFFOLD), "--root", str(root), "--slug", "demo", "--migrate"],
                            capture_output=True, text=True)
    assert result.returncode == 1
    assert "--archetype" in result.stdout


# --- refusals ---------------------------------------------------------------------------

def test_refuses_non_git_root(tmp_path):
    root = tmp_path / "plain"
    _write(root, {".bc-agent/decisions/a.md": "# A\n"})
    result = _migrate(root)
    assert result.returncode == 1
    assert "not a git repository" in result.stdout
    assert not (root / "work").exists()


def test_refuses_dirty_tree_and_lists_paths(tmp_path):
    root = _vault_repo(tmp_path)
    (root / "README.md").write_text("changed\n")
    (root / "new.txt").write_text("x\n")
    result = _migrate(root, "code", "--apply")
    assert result.returncode == 1
    assert "README.md" in result.stdout and "new.txt" in result.stdout
    assert not (root / "work").exists()


def test_refuses_when_table_already_exists(tmp_path):
    root = _vault_repo(tmp_path)
    m = _module()
    (root / ".bc-agent/AGENTS.md").write_text("# x\n\n" + m.WHERE_THINGS_GO_HEADING + "\n\n"
                                              + m.where_things_go_table("code") + "\n")
    _commit_all(root, "table")
    result = _migrate(root)
    assert result.returncode == 1
    assert "Where things go" in result.stdout


@pytest.mark.parametrize("archetype", ["learning", "knowledge"])
def test_refuses_learning_and_knowledge(tmp_path, archetype):
    root = _vault_repo(tmp_path)
    before = _tree(root)
    result = _migrate(root, archetype, "--apply")
    assert result.returncode == 1
    assert archetype in result.stdout
    assert _tree(root) == before


def test_refuses_when_destination_exists_as_different_file(tmp_path):
    root = _vault_repo(tmp_path)
    _write(root, {"docs/decisions/adr-0001-x.md": "# Something else\n"})
    _commit_all(root, "clash")
    before = _tree(root)
    result = _migrate(root, "code", "--apply")
    assert result.returncode == 1
    assert "docs/decisions/adr-0001-x.md" in result.stdout
    assert _tree(root) == before


def test_refuses_project_without_vault(tmp_path):
    root = tmp_path / "novault"
    root.mkdir()
    _git(root, "init", "-q")
    _write(root, {"README.md": "x\n"})
    _commit_all(root)
    result = _migrate(root)
    assert result.returncode == 1
    assert "no .bc-agent" in result.stdout


# --- plan contents ----------------------------------------------------------------------

def test_plan_moves_vault_decisions_research_and_docs_adr(tmp_path):
    out = _sections(_migrate(_vault_repo(tmp_path)).stdout)
    moves = out["MOVE"]
    assert ".bc-agent/decisions/adr-0001-x.md -> docs/decisions/adr-0001-x.md" in moves
    assert "docs/adr/0002-y.md -> docs/decisions/0002-y.md" in moves
    assert ".bc-agent/research/README.md -> docs/research/README.md" in moves
    assert ".bc-agent/research/2026-01-01-r/notes.md -> docs/research/2026-01-01-r/notes.md" in moves
    assert not any(".gitkeep" in line for line in moves)
    assert not any("components" in line for line in moves)


def test_ops_moves_components(tmp_path):
    out = _sections(_migrate(_vault_repo(tmp_path, "ops"), "ops").stdout)
    assert ".bc-agent/components/host.md -> docs/components/host.md" in out["MOVE"]


def test_adr_filename_clash_goes_to_judgment(tmp_path):
    root = _vault_repo(tmp_path)
    _write(root, {"docs/adr/adr-0001-x.md": "# Other ADR 1\n"})
    _commit_all(root, "clash")
    out = _sections(_migrate(root).stdout)
    assert not any(line.startswith("docs/adr/adr-0001-x.md ->") for line in out["MOVE"])
    assert not any(line.startswith(".bc-agent/decisions/adr-0001-x.md ->") for line in out["MOVE"])
    judged = "\n".join(out["NEEDS JUDGMENT"])
    assert "docs/adr/adr-0001-x.md" in judged and ".bc-agent/decisions/adr-0001-x.md" in judged


def test_plan_creates_replaces_and_keeps(tmp_path):
    out = _sections(_migrate(_vault_repo(tmp_path)).stdout)
    for path in ("work/0-ideas.md", "work/1-planned/.gitkeep", "glossary.md",
                 ".bc-agent/templates/work-item.md", ".bc-agent/conventions/file-layout.md"):
        assert path in out["CREATE"], path
    assert "docs/decisions/.gitkeep" not in out["CREATE"]  # receives moved files
    assert out["REPLACE"] == [".bc-agent/AGENTS.md"]
    for path in ("AGENTS.md", ".bc-agent/map.md", ".bc-agent/log.md", ".bc-agent/conventions/validation.md"):
        assert path in out["KEPT (review by hand)"], path


def test_plan_deletes_only_placeholders_and_unmodified_generated_files(tmp_path):
    out = _sections(_migrate(_vault_repo(tmp_path)).stdout)
    assert sorted(out["DELETE"]) == sorted([
        ".bc-agent/decisions/.gitkeep", ".bc-agent/scratch/.gitkeep", ".bc-agent/out-of-scope/.gitkeep",
        ".bc-agent/conventions/planning-workflow.md", ".bc-agent/templates/plan.md"])


def test_modified_generated_file_and_content_scratch_are_judgment_not_deleted(tmp_path):
    root = _vault_repo(tmp_path)
    _write(root, {".bc-agent/templates/plan.md": "# My own plan template\n",
                  ".bc-agent/scratch/note.md": "keep me\n"})
    _commit_all(root, "content")
    out = _sections(_migrate(root).stdout)
    assert ".bc-agent/templates/plan.md" not in out["DELETE"]
    assert not any("scratch" in line for line in out["DELETE"])
    judged = "\n".join(out["NEEDS JUDGMENT"])
    assert ".bc-agent/templates/plan.md" in judged and ".bc-agent/scratch" in judged


def test_every_judgment_class_is_listed_with_its_rule(tmp_path):
    judged = _sections(_migrate(_vault_repo(tmp_path)).stdout)["NEEDS JUDGMENT"]

    def rule_for(path):
        return next(line for line in judged if line.startswith(path + " "))

    work = "only work still open becomes numbered work items"
    for path in (".bc-agent/tasks/active.md", ".bc-agent/tasks/completed.md", ".bc-agent/plans",
                 "docs/plans", ".bc-agent/project/x-plan.md"):
        assert work in rule_for(path), path
    assert "ideas file" in rule_for(".bc-agent/tasks/parking-lot.md")
    assert "parent work item" in rule_for(".bc-agent/tasks/issue-drafts")
    assert "glossary.md" in rule_for(".bc-agent/project/overview.md")
    assert "docs/PRD.md" in rule_for(".bc-agent/project/feature-prd.md")
    assert "git history" in rule_for(".bc-agent/findings")
    assert "blocking" in rule_for(".bc-agent/open-questions")
    for path in (".bc-agent/home.md", ".bc-agent/index.md", ".bc-agent/.obsidian"):
        assert "unique content" in rule_for(path), path
    assert "unrecognised" in rule_for(".bc-agent/archetype.md")
    assert "git show HEAD:.bc-agent/AGENTS.md" in rule_for(".bc-agent/AGENTS.md")
    assert "4 lines" in rule_for(".bc-agent/tasks/active.md")


def test_hybrid_keeps_index_and_teach_paths(tmp_path):
    out = _sections(_migrate(_vault_repo(tmp_path, "hybrid"), "hybrid").stdout)
    everything = "\n".join(out["NEEDS JUDGMENT"] + out["DELETE"] + out["MOVE"])
    assert ".bc-agent/index.md" not in everything
    assert ".bc-agent/learning" not in everything
    assert ".bc-agent/components/host.md -> docs/components/host.md" in out["MOVE"]


def test_links_section_counts_rewrites_and_unresolved(tmp_path):
    out = _sections(_migrate(_vault_repo(tmp_path)).stdout)
    links = "\n".join(out["LINKS"])
    assert "would rewrite" in links
    assert "unresolved: 1" in links
    assert "README.md:7" in links
    assert "wikilinks naming a moved file (not rewritten): 1" in links
    assert ".bc-agent/home.md:3" in links
    other = "\n".join(out["OTHER REFERENCES"])
    assert "tools/run.sh:1" in other


# --- apply ------------------------------------------------------------------------------

def _apply(tmp_path, archetype="code"):
    root = _vault_repo(tmp_path, archetype)
    head = _git(root, "rev-parse", "HEAD")
    result = _migrate(root, archetype, "--apply")
    assert result.returncode == 0, result.stdout + result.stderr
    return root, head, result.stdout


def test_apply_moves_creates_replaces_deletes_and_stages_without_committing(tmp_path):
    root, head, out = _apply(tmp_path)
    assert _git(root, "rev-parse", "HEAD") == head
    assert _git(root, "status", "--porcelain", "--untracked-files=all").splitlines()
    assert not [line for line in _git(root, "status", "--porcelain").splitlines() if line[1] != " "]
    assert (root / "docs/decisions/adr-0001-x.md").is_file()
    assert (root / "docs/decisions/0002-y.md").is_file()
    assert (root / "docs/research/2026-01-01-r/notes.md").is_file()
    assert not (root / ".bc-agent/decisions").exists()
    assert not (root / "docs/adr").exists()
    assert not (root / ".bc-agent/scratch").exists()
    assert not (root / ".bc-agent/conventions/planning-workflow.md").exists()
    assert (root / "work/0-ideas.md").is_file()
    assert (root / "AGENTS.md").read_text() == "# Project rules\n\nHand-written.\n"
    assert (root / ".bc-agent/map.md").read_text() == "# Map\n\nProject-written map.\n"
    table = _module().parse_where_things_go((root / ".bc-agent/AGENTS.md").read_text())
    assert table["decisions"] == "docs/decisions/"
    assert "commit" in out.splitlines()[-1].lower()


def test_apply_leaves_judgment_paths_untouched(tmp_path):
    root, _head, _out = _apply(tmp_path)
    for rel in (".bc-agent/tasks/active.md", ".bc-agent/tasks/issue-drafts/01-slice.md", ".bc-agent/plans/p.md",
                ".bc-agent/project/overview.md", ".bc-agent/findings/f.md", ".bc-agent/open-questions/q.md",
                ".bc-agent/home.md", ".bc-agent/.obsidian/app.json", ".bc-agent/archetype.md", "docs/plans/old.md"):
        assert _git(root, "diff", "--cached", "--name-only", "--", rel) == "", rel
        assert (root / rel).is_file(), rel


def test_apply_rewrites_links_both_directions_and_skips_fences(tmp_path):
    root, _head, _out = _apply(tmp_path)
    readme = (root / "README.md").read_text()
    assert "[ADR](docs/decisions/adr-0001-x.md)" in readme
    assert "[log](.bc-agent/log.md)" in readme
    assert "[fenced](.bc-agent/decisions/adr-0001-x.md)" in readme
    assert "[gone](nowhere/missing.md)" in readme
    adr = (root / "docs/decisions/adr-0001-x.md").read_text()
    assert "[active](../../.bc-agent/tasks/active.md)" in adr
    assert "[r](../../README.md#top)" in adr
    assert "[w](https://example.com)" in adr
    assert "[ADR](../../decisions/adr-0001-x.md)" in (root / "docs/research/2026-01-01-r/notes.md").read_text()
    assert "[one](adr-0001-x.md)" in (root / "docs/decisions/0002-y.md").read_text()
    index = (root / ".bc-agent/index.md").read_text()
    assert "[ADR](../docs/decisions/adr-0001-x.md)" in index
    assert "[decisions](../docs/decisions/)" in index
    assert (root / "tools/run.sh").read_text() == "cat .bc-agent/decisions/adr-0001-x.md\n"


def test_second_migrate_refuses_and_scaffold_names_only_judgment_paths(tmp_path):
    root, _head, _out = _apply(tmp_path)
    _commit_all(root, "migrated")
    again = _migrate(root, "code", "--apply")
    assert again.returncode == 1
    assert "Where things go" in again.stdout
    plain = subprocess.run([sys.executable, str(SCAFFOLD), "--root", str(root), "--slug", "demo",
                            "--archetype", "code", "--dry-run"], capture_output=True, text=True)
    named = plain.stdout.split("(", 1)[1].split(")", 1)[0].split(", ")
    for moved in ("decisions", "research", "scratch", "out-of-scope",
                  "conventions/planning-workflow.md", "templates/plan.md"):
        assert moved not in named, moved
    assert "tasks" in named


def test_apply_on_hybrid_keeps_index_catalog(tmp_path):
    root, _head, _out = _apply(tmp_path, "hybrid")
    assert (root / ".bc-agent/index.md").is_file()
    assert (root / ".bc-agent/learning/plan.md").read_text() == "# Mission\n"
    assert (root / "docs/components/host.md").is_file()
