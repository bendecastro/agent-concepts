"""wiki_lint.py on projects scaffolded with the visible layout (bc-init-agent code/ops/hybrid)."""
from __future__ import annotations

import importlib.util
import inspect
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
LINTER = ROOT / "concepts/bc-wiki-maintain/body/wiki_lint.py"
SCAFFOLD = ROOT / "concepts/bc-init-agent/body/scaffold.py"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scaffold(root: Path, archetype: str = "code") -> Path:
    root.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [sys.executable, str(SCAFFOLD), "--root", str(root), "--slug", "demo", "--archetype", archetype],
        check=True, capture_output=True,
    )
    return root


def lint(root: Path) -> tuple[int, dict]:
    result = subprocess.run(
        [sys.executable, str(LINTER), str(root / ".bc-agent"), "--json"],
        capture_output=True, text=True, check=False,
    )
    return result.returncode, json.loads(result.stdout)


def lint_text(root: Path) -> str:
    return subprocess.run(
        [sys.executable, str(LINTER), str(root / ".bc-agent")], capture_output=True, text=True, check=False,
    ).stdout


def write(path: Path, body: str = "# Item\n\nWhy: x\n\n## Outcome\n\nShipped.\n") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def commit_all(root: Path) -> None:
    for args in (("init", "-q"), ("add", "."), ("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "initial")):
        subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


def findings(report: dict, check: str) -> list[dict]:
    return [entry for entry in report["work_findings"] if entry["check"] == check]


def test_fresh_code_scaffold_is_visible_layout_with_no_vault_demands(tmp_path):
    root = scaffold(tmp_path / "p")
    code, report = lint(root)
    assert report["layout"] == "visible"
    assert report["missing_index"] == []
    assert report["work_findings"] == []
    assert report["broken_links"] == []
    output = lint_text(root)
    for vault_page in ("index.md", "tasks/active.md", "project/overview.md"):
        assert vault_page not in output
    # Exit 1 here only reflects the not-a-git-repo promotion range, as for a vault.
    assert report["unpromoted_log"]["note"] == "unknown: not a git repository"


def test_where_things_go_parser_copy_matches_bc_init_agent():
    """The linter carries a copy of the contract's parser; this fails when they drift."""
    linter, contract = load("wiki_lint_copy", LINTER), load("scaffold_contract", SCAFFOLD)
    assert inspect.getsource(linter.parse_where_things_go) == inspect.getsource(contract.parse_where_things_go)
    for name in ("WHERE_THINGS_GO_HEADING", "_UNDECIDED_PATH_CELLS"):
        assert getattr(linter, name) == getattr(contract, name)
    assert linter._WHERE_THINGS_GO_LINE.pattern == contract._WHERE_THINGS_GO_LINE.pattern
    assert linter._WHERE_THINGS_GO_LINE.flags == contract._WHERE_THINGS_GO_LINE.flags


def test_fresh_hybrid_scaffold_checks_teach_index_only_for_teach_pages(tmp_path):
    root = scaffold(tmp_path / "p", "hybrid")
    _code, report = lint(root)
    assert report["layout"] == "visible"
    assert report["work_findings"] == []
    assert report["missing_index"] == []
    write(root / ".bc-agent/learning/uncatalogued-note.md", "# Note\n")
    _code, report = lint(root)
    assert report["missing_index"] == ["learning/uncatalogued-note.md"]


def test_learning_vault_keeps_vault_checks(tmp_path):
    root = scaffold(tmp_path / "p", "learning")
    write(root / ".bc-agent/project/stray.md", "# Stray\n")
    _code, report = lint(root)
    assert report["layout"] == "vault"
    assert "project/stray.md" in report["missing_index"]


def test_duplicate_number_across_stages_including_done_months_is_an_error(tmp_path):
    root = scaffold(tmp_path / "p")
    write(root / "work/1-planned/007-search.md")
    write(root / "work/3-done/2026-03/007-ranking.md")
    write(root / "work/2-active/008-other.md")
    code, report = lint(root)
    duplicates = findings(report, "duplicate-number")
    assert [entry["path"] for entry in duplicates] == ["work/1-planned/007-search.md", "work/3-done/2026-03/007-ranking.md"]
    assert all(entry["severity"] == "error" and entry["fix"] for entry in duplicates)
    assert code == 1
    assert "work/3-done/2026-03/007-ranking.md" in lint_text(root)


def test_duplicate_check_uses_the_table_path_not_a_hard_coded_work_folder(tmp_path):
    root = scaffold(tmp_path / "p")
    agents = root / ".bc-agent/AGENTS.md"
    agents.write_text(agents.read_text().replace("`work/1-planned/`", "`plans/todo/`"), encoding="utf-8")
    write(root / "plans/todo/007-a.md")
    write(root / "work/2-active/007-b.md")
    _code, report = lint(root)
    assert [entry["path"] for entry in findings(report, "duplicate-number")] == ["plans/todo/007-a.md", "work/2-active/007-b.md"]


def test_item_directly_in_done_or_misnamed_month_folder_is_an_error(tmp_path):
    root = scaffold(tmp_path / "p")
    write(root / "work/3-done/001-loose.md")
    write(root / "work/3-done/March/002-misfiled.md")
    write(root / "work/3-done/2026-03/003-ok.md")
    code, report = lint(root)
    month = findings(report, "done-month-folder")
    assert [entry["path"] for entry in month] == ["work/3-done/001-loose.md", "work/3-done/March"]
    assert all(entry["severity"] == "error" for entry in month)
    assert code == 1
    # .gitkeep files and well-formed month folders are not reported.
    assert not any(entry["path"].endswith((".gitkeep", "2026-03")) for entry in report["work_findings"])


def test_status_line_in_file_item_or_folder_plan_is_an_error(tmp_path):
    root = scaffold(tmp_path / "p")
    write(root / "work/2-active/001-file.md", "# File\n\nStatus: active\n")
    write(root / "work/1-planned/002-folder/plan.md", "# Folder\n\n**Status:** planned\n")
    write(root / "work/1-planned/003-quoted.md", "# Quoted\n\n```\nStatus: example only\n```\n")
    code, report = lint(root)
    assert [entry["path"] for entry in findings(report, "status-line")] == [
        "work/1-planned/002-folder/plan.md", "work/2-active/001-file.md"]
    assert code == 1


def test_done_or_dropped_item_without_a_filled_outcome_is_an_error(tmp_path):
    root = scaffold(tmp_path / "p")
    placeholder = (root / ".bc-agent/templates/work-item.md").read_text()
    write(root / "work/3-done/2026-03/001-template.md", placeholder)
    write(root / "work/4-dropped/002-no-section.md", "# Dropped\n\nWhy: x\n")
    write(root / "work/4-dropped/003-empty/plan.md", "# Empty\n\n## Outcome\n\n## Notes\n\nlater\n")
    write(root / "work/3-done/2026-03/004-filled.md")
    write(root / "work/2-active/005-active.md", placeholder)
    code, report = lint(root)
    assert [entry["path"] for entry in findings(report, "missing-outcome")] == [
        "work/3-done/2026-03/001-template.md", "work/4-dropped/002-no-section.md", "work/4-dropped/003-empty/plan.md"]
    assert code == 1


def test_badly_named_item_and_folder_without_plan_are_warnings(tmp_path):
    root = scaffold(tmp_path / "p")
    write(root / "work/1-planned/search-ranking.md")
    write(root / "work/1-planned/12-short.md")
    write(root / "work/2-active/004-big/requirements.md", "# Req\n")
    write(root / "work/2-active/005-good/plan.md")
    commit_all(root)
    code, report = lint(root)
    assert [entry["path"] for entry in findings(report, "item-name")] == [
        "work/1-planned/12-short.md", "work/1-planned/search-ranking.md"]
    assert [entry["path"] for entry in findings(report, "missing-plan")] == ["work/2-active/004-big"]
    assert {entry["severity"] for entry in findings(report, "item-name") + findings(report, "missing-plan")} == {"warning"}
    assert not [entry for entry in report["work_findings"] if entry["severity"] == "error"]
    assert code == 0, "warnings alone must not fail the linter"


def test_missing_role_path_is_a_warning_unless_created_on_first_need_or_undecided(tmp_path):
    root = scaffold(tmp_path / "p", "ops")
    (root / "glossary.md").unlink()
    for gitkeep in (root / "docs/decisions").iterdir():
        gitkeep.unlink()
    (root / "docs/decisions").rmdir()
    _code, report = lint(root)
    roles = findings(report, "role-path")
    # requirements, architecture and project-skills are "created on first need";
    # project-agents has no decided path.
    assert [entry["path"] for entry in roles] == ["docs/decisions", "glossary.md"]
    assert {entry["severity"] for entry in roles} == {"warning"}
    assert "decisions" in roles[0]["problem"]


def test_broken_link_in_map_still_fails_a_visible_layout_project(tmp_path):
    root = scaffold(tmp_path / "p")
    with (root / ".bc-agent/map.md").open("a", encoding="utf-8") as handle:
        handle.write("\n- [gone](references/gone.md)\n")
    code, report = lint(root)
    assert report["broken_links"] == [{"page": "map.md", "link": "[gone](references/gone.md)"}]
    assert code == 1


def test_where_things_go_heading_inside_a_code_fence_does_not_switch_a_vault_to_visible(tmp_path):
    root = scaffold(tmp_path / "p", "learning")
    agents = root / ".bc-agent/AGENTS.md"
    quoted = "\n```markdown\n## Where things go\n\n| Role | Path | Notes |\n|---|---|---|\n| ideas | `work/0-ideas.md` | |\n```\n"
    # Placed before the vault's own (bulleted) "Where things go" section, so a raw-text
    # search would find the fenced table first.
    original = agents.read_text()
    agents.write_text(original.replace("## Where things go", quoted.strip() + "\n\n## Where things go", 1), encoding="utf-8")
    write(root / ".bc-agent/project/stray.md", "# Stray\n")
    _code, report = lint(root)
    assert report["layout"] == "vault"
    assert "project/stray.md" in report["missing_index"]


def test_status_line_in_any_markdown_file_of_a_folder_item_is_an_error(tmp_path):
    root = scaffold(tmp_path / "p")
    write(root / "work/1-planned/002-folder/plan.md", "# Folder\n\nWhy: x\n")
    write(root / "work/1-planned/002-folder/requirements.md", "# Req\n\nStatus: draft\n")
    write(root / "work/1-planned/002-folder/evidence/run.md", "# Run\n\n- Status: green\n")
    _code, report = lint(root)
    assert [entry["path"] for entry in findings(report, "status-line")] == [
        "work/1-planned/002-folder/evidence/run.md", "work/1-planned/002-folder/requirements.md"]


def test_readme_is_folder_documentation_and_other_non_markdown_is_a_warning(tmp_path):
    root = scaffold(tmp_path / "p")
    for folder in ("work/3-done", "work/3-done/2026-03", "work/4-dropped", "work/1-planned"):
        write(root / folder / "README.md", "# About this folder\n\nStatus: explains the stage\n")
    image = root / "work/4-dropped/diagram.png"
    image.write_bytes(b"\x89PNG\r\nStatus: binary\n")
    write(root / "work/3-done/2026-03/003-ok.md")
    commit_all(root)
    code, report = lint(root)
    assert [(entry["check"], entry["path"], entry["severity"]) for entry in report["work_findings"]] == [
        ("non-markdown", "work/4-dropped/diagram.png", "warning")]
    assert code == 0


def test_item_numbers_compare_as_integers_and_zero_is_not_a_number(tmp_path):
    root = scaffold(tmp_path / "p")
    write(root / "work/1-planned/1000-big.md")
    write(root / "work/3-done/2026-03/1000-also.md")
    write(root / "work/2-active/007-a.md")
    write(root / "work/2-active/0007-b.md")
    write(root / "work/1-planned/000-zero.md")
    _code, report = lint(root)
    assert [entry["path"] for entry in findings(report, "duplicate-number")] == [
        "work/2-active/0007-b.md", "work/2-active/007-a.md",
        "work/1-planned/1000-big.md", "work/3-done/2026-03/1000-also.md"]
    assert [entry["path"] for entry in findings(report, "item-name")] == ["work/1-planned/000-zero.md"]


def test_two_roles_with_the_same_path_do_not_count_items_twice(tmp_path):
    root = scaffold(tmp_path / "p")
    agents = root / ".bc-agent/AGENTS.md"
    agents.write_text(agents.read_text().replace("`work/2-active/`", "`work/1-planned/`"), encoding="utf-8")
    write(root / "work/1-planned/007-a.md")
    _code, report = lint(root)
    assert findings(report, "duplicate-number") == []


# --- .bc-agent/ holds agent mechanics only (owner decision 2026-11-12) ---------

def test_every_visible_archetype_scaffold_has_no_agent_mechanics_findings(tmp_path):
    for archetype in ("code", "ops", "hybrid"):
        root = scaffold(tmp_path / archetype, archetype)
        _code, report = lint(root)
        assert findings(report, "agent-mechanics") == [], archetype


def test_lint_allows_exactly_the_bc_agent_entries_the_hybrid_scaffold_generates(tmp_path):
    linter, contract = load("wiki_lint_mechanics", LINTER), load("scaffold_mechanics", SCAFFOLD)
    root = tmp_path / "p"
    vault = root / ".bc-agent"
    generated = {
        path.relative_to(vault).parts[0]
        for path, _text, _root in contract.targets(root, "demo", "2026-11-12", "hybrid")
        if path.is_relative_to(vault)
    }
    assert generated == linter.AGENT_MECHANICS_ENTRIES | linter.HYBRID_TEACH_ENTRIES


def test_unexpected_entries_under_bc_agent_are_errors_naming_where_knowledge_lives(tmp_path):
    root = scaffold(tmp_path / "p")
    vault = root / ".bc-agent"
    for folder in ("scratch", "research", "tasks", "decisions", "project", ".obsidian", "learning"):
        write(vault / folder / "note.md", "# Note\n")
    (vault / "stray.txt").write_text("x\n", encoding="utf-8")
    (vault / ".DS_Store").write_text("x\n", encoding="utf-8")
    commit_all(root)
    code, report = lint(root)
    found = findings(report, "agent-mechanics")
    assert [entry["path"] for entry in found] == [
        ".bc-agent/.obsidian", ".bc-agent/decisions", ".bc-agent/learning", ".bc-agent/project",
        ".bc-agent/research", ".bc-agent/scratch", ".bc-agent/stray.txt", ".bc-agent/tasks"]
    assert {entry["severity"] for entry in found} == {"error"}
    assert "project knowledge lives at the table's role paths; `.bc-agent/` holds agent mechanics only" in found[0]["problem"]
    assert code == 1
    assert "- .bc-agent/scratch — " in lint_text(root)


def test_agent_extras_row_allows_declared_bc_agent_entries(tmp_path):
    root = scaffold(tmp_path / "p")
    agents = root / ".bc-agent/AGENTS.md"
    row = "| agent-extras | `.bc-agent/autoresearch/`, `.bc-agent/runs.jsonl` | records a tool reads by path |\n"
    text = agents.read_text()
    anchor = next(line for line in text.splitlines(keepends=True) if line.startswith("| project-agents |"))
    agents.write_text(text.replace(anchor, anchor + row), encoding="utf-8")
    write(root / ".bc-agent/autoresearch/run.md", "# Run\n")
    (root / ".bc-agent/runs.jsonl").write_text("{}\n", encoding="utf-8")
    write(root / ".bc-agent/scratch/x.md", "# X\n")
    _code, report = lint(root)
    assert [entry["path"] for entry in findings(report, "agent-mechanics")] == [".bc-agent/scratch"]
    assert findings(report, "role-path") == []


def test_vault_layout_keeps_its_folders_without_agent_mechanics_findings(tmp_path):
    root = scaffold(tmp_path / "p", "learning")
    write(root / ".bc-agent/scratch/x.md", "# X\n")
    _code, report = lint(root)
    assert report["layout"] == "vault"
    assert report["work_findings"] == []
