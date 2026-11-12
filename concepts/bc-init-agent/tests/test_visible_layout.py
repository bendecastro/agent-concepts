"""Visible work layout emitted by the scaffold CLI."""
from pathlib import Path
import subprocess
import sys

SCAFFOLD = Path(__file__).resolve().parents[1] / "body/scaffold.py"


def test_code_scaffold_creates_visible_work_layout(tmp_path):
    subprocess.run([sys.executable, str(SCAFFOLD), '--root', str(tmp_path), '--slug', 'demo'], check=True)
    assert (tmp_path / 'glossary.md').is_file()
    assert (tmp_path / 'work/0-ideas.md').is_file()
    for stage in ('1-planned', '2-active', '3-done', '4-dropped'):
        assert (tmp_path / 'work' / stage).is_dir()
    for path in ('docs/decisions', 'docs/research'):
        assert (tmp_path / path).is_dir()
    assert {p.name for p in (tmp_path / '.bc-agent').iterdir()} == {
        'AGENTS.md', 'map.md', 'log.md', 'conventions', 'references', 'templates'}


def test_where_things_go_table_has_stable_role_paths(tmp_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location('scaffold', SCAFFOLD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for archetype in ('code', 'ops', 'hybrid'):
        root = tmp_path / archetype
        root.mkdir()
        subprocess.run([sys.executable, str(SCAFFOLD), '--root', str(root), '--slug', 'demo', '--archetype', archetype], check=True)
        roles = module.parse_where_things_go((root / '.bc-agent/AGENTS.md').read_text())
        assert set(roles) >= {'work-planned', 'work-active', 'work-done', 'work-dropped', 'ideas', 'decisions', 'research', 'glossary', 'requirements', 'architecture', 'project-skills', 'project-agents'}
        assert roles['work-planned'] == 'work/1-planned/'


def test_code_and_ops_generated_text_has_no_retired_paths(tmp_path):
    retired = ('tasks/active.md', 'tasks/completed.md', 'parking-lot',
               'project/overview.md', '.bc-agent/decisions', '.bc-agent/research',
               'out-of-scope', 'scratch/', 'index.md', 'home.md')
    for archetype in ('code', 'ops'):
        root = tmp_path / archetype
        root.mkdir()
        subprocess.run([sys.executable, str(SCAFFOLD), '--root', str(root), '--slug', 'demo', '--archetype', archetype], check=True)
        for path in root.rglob('*.md'):
            text = path.read_text().lower()
            assert not any(term in text for term in retired), str(path)


def test_ops_scaffold_keeps_distinct_operations_knowledge(tmp_path):
    subprocess.run([sys.executable, str(SCAFFOLD), '--root', str(tmp_path), '--slug', 'demo', '--archetype', 'ops'], check=True)
    assert (tmp_path / 'docs/components/README.md').is_file()
    assert (tmp_path / 'docs/open-questions/README.md').is_file()
    assert not (tmp_path / 'docs/plans').exists()


def test_code_and_ops_layout_table_marks_optional_destinations(tmp_path):
    for archetype in ('code', 'ops'):
        root = tmp_path / archetype
        root.mkdir()
        subprocess.run([sys.executable, str(SCAFFOLD), '--root', str(root), '--slug', 'demo', '--archetype', archetype], check=True)
        rows = (root / '.bc-agent/AGENTS.md').read_text().splitlines()
        for role in ('requirements', 'architecture', 'project-skills'):
            assert 'created on first need' in next(row for row in rows if row.startswith(f'| {role} |'))
        assert 'not yet decided' in next(row for row in rows if row.startswith('| project-agents |'))


def test_code_and_ops_runway_uses_visible_work_and_research(tmp_path):
    for archetype in ('code', 'ops'):
        root = tmp_path / archetype
        root.mkdir()
        subprocess.run([sys.executable, str(SCAFFOLD), '--root', str(root), '--slug', 'demo', '--archetype', archetype], check=True)
        text = (root / '.bc-agent/conventions/architecture-runway.md').read_text()
        assert 'git log' in text
        assert '-- docs/research' in text
        assert '-- docs work' in text
        assert '.bc-agent/tasks' not in text


# --- helpers for the exact-behaviour tests below ------------------------------

import hashlib
import importlib.util
import re

import pytest

VISIBLE = ('code', 'ops', 'hybrid')
BASE_COMMIT = 'e27f2e6'


def _module():
    spec = importlib.util.spec_from_file_location('scaffold', SCAFFOLD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(root, archetype, *extra, script=SCAFFOLD):
    return subprocess.run(
        [sys.executable, str(script), '--root', str(root), '--slug', 'demo',
         '--date', '2026-01-02', '--archetype', archetype, *extra],
        check=True, capture_output=True, text=True).stdout


def _scaffold(tmp_path, archetype):
    root = tmp_path / archetype
    root.mkdir()
    _run(root, archetype)
    return root


def _files(root):
    return {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}


def _snapshot(root):
    return {rel: (hashlib.sha256((root / rel).read_bytes()).hexdigest(), (root / rel).stat().st_mtime_ns)
            for rel in _files(root)}


CODE_FILES = {
    'AGENTS.md',
    '.bc-agent/AGENTS.md',
    '.bc-agent/map.md',
    '.bc-agent/log.md',
    '.bc-agent/conventions/architecture-runway.md',
    '.bc-agent/conventions/file-layout.md',
    '.bc-agent/conventions/git-and-commit-policy.md',
    '.bc-agent/conventions/validation.md',
    '.bc-agent/references/agent-skills.md',
    '.bc-agent/references/commands.md',
    '.bc-agent/templates/adr.md',
    '.bc-agent/templates/work-item.md',
    'glossary.md',
    'work/0-ideas.md',
    'work/1-planned/.gitkeep',
    'work/2-active/.gitkeep',
    'work/3-done/.gitkeep',
    'work/4-dropped/.gitkeep',
    'docs/decisions/.gitkeep',
    'docs/research/.gitkeep',
}
OPS_FILES = CODE_FILES | {
    '.bc-agent/templates/component.md',
    '.bc-agent/templates/finding.md',
    '.bc-agent/templates/open-question.md',
    'docs/components/README.md',
    'docs/open-questions/README.md',
}
HYBRID_FILES = OPS_FILES | {
    '.bc-agent/index.md',
    '.bc-agent/project/overview.md',
    '.bc-agent/learning/plan.md',
    '.bc-agent/learning/review.md',
    '.bc-agent/learning/notes.md',
    '.bc-agent/learning/records/.gitkeep',
    '.bc-agent/sources/README.md',
    '.bc-agent/concepts/README.md',
    '.bc-agent/concepts/entities/README.md',
    '.bc-agent/concepts/syntheses/README.md',
    '.bc-agent/questions/README.md',
    '.bc-agent/sessions/README.md',
    '.bc-agent/references/teach-skill.md',
    '.bc-agent/references/teach-resources.md',
    '.bc-agent/templates/learning-session.md',
}


@pytest.mark.parametrize('archetype, expected', [
    ('code', CODE_FILES), ('ops', OPS_FILES), ('hybrid', HYBRID_FILES)])
def test_visible_scaffold_generates_exact_file_list(tmp_path, archetype, expected):
    assert _files(_scaffold(tmp_path, archetype)) == expected


@pytest.mark.parametrize('archetype', ['learning', 'knowledge'])
def test_vault_archetypes_output_is_byte_identical_to_base(tmp_path, archetype):
    base = tmp_path / 'base_scaffold.py'
    base.write_bytes(subprocess.run(
        ['git', 'show', f'{BASE_COMMIT}:concepts/bc-init-agent/body/scaffold.py'],
        cwd=SCAFFOLD.parent, check=True, capture_output=True).stdout)
    old, new = tmp_path / 'old', tmp_path / 'new'
    old.mkdir()
    new.mkdir()
    _run(old, archetype, script=base)
    _run(new, archetype)
    assert _files(new) == _files(old)
    for rel in _files(old):
        assert (new / rel).read_bytes() == (old / rel).read_bytes(), rel


CODE_ROLES = {
    'work-planned': 'work/1-planned/',
    'work-active': 'work/2-active/',
    'work-done': 'work/3-done/',
    'work-dropped': 'work/4-dropped/',
    'ideas': 'work/0-ideas.md',
    'decisions': 'docs/decisions/',
    'research': 'docs/research/',
    'glossary': 'glossary.md',
    'requirements': 'docs/PRD.md',
    'architecture': 'ARCHITECTURE.md',
    'project-skills': '.agents/skills/',
    'project-agents': '',
}


@pytest.mark.parametrize('archetype', VISIBLE)
def test_where_things_go_roles_resolve_in_scaffolded_tree(tmp_path, archetype):
    module = _module()
    root = _scaffold(tmp_path, archetype)
    text = (root / '.bc-agent/AGENTS.md').read_text()
    roles = module.parse_where_things_go(text)
    assert set(module.LAYOUT_ROLES) <= set(roles)
    if archetype == 'code':
        assert roles == CODE_ROLES
    else:
        assert {role: roles[role] for role in CODE_ROLES} == CODE_ROLES
        assert roles['components'] == 'docs/components/'
        assert roles['open-questions'] == 'docs/open-questions/'
    if archetype == 'hybrid':
        assert roles['teach-workspace'] == '.bc-agent/references/teach-skill.md'
    assert roles['project-agents'] == ''
    notes = {row.split('|')[1].strip(): row for row in text.splitlines() if row.startswith('| ')}
    for role, path in roles.items():
        if path and 'created on first need' not in notes[role]:
            assert (root / path).exists(), (role, path)


LINK = re.compile(r'\[[^\]]*\]\(([^)\s]+)\)')


@pytest.mark.parametrize('archetype', VISIBLE)
def test_generated_markdown_links_resolve(tmp_path, archetype):
    root = _scaffold(tmp_path, archetype)
    generated = {root / rel for rel in _files(root)}
    broken = []
    for path in root.rglob('*.md'):
        for target in LINK.findall(path.read_text()):
            if re.match(r'[a-z]+:', target) or target.startswith('#'):
                continue
            resolved = (path.parent / target.split('#', 1)[0]).resolve()
            if resolved not in generated:
                broken.append(f'{path.relative_to(root)} -> {target}')
    assert broken == []


@pytest.mark.parametrize('archetype', VISIBLE)
def test_work_item_template_has_lifecycle_fields_and_no_plan_template(tmp_path, archetype):
    root = _scaffold(tmp_path, archetype)
    text = (root / '.bc-agent/templates/work-item.md').read_text()
    for field in ('Why:', 'Done when:', 'Issue:', '## Steps', '## Outcome'):
        assert field in text
    assert 'Status:' not in text
    assert not (root / '.bc-agent/templates/plan.md').exists()


@pytest.mark.parametrize('archetype', VISIBLE)
def test_second_run_changes_nothing(tmp_path, archetype):
    root = _scaffold(tmp_path, archetype)
    before = _snapshot(root)
    out = _run(root, archetype)
    assert _snapshot(root) == before
    assert 'Nothing to do' in out


@pytest.mark.parametrize('archetype', VISIBLE)
def test_dry_run_creates_nothing(tmp_path, archetype):
    out = _run(tmp_path, archetype, '--dry-run')
    assert 'Would create' in out
    assert list(tmp_path.iterdir()) == []


def test_old_layout_files_survive_code_scaffold(tmp_path):
    old = {
        '.bc-agent/tasks/active.md': '# Active\n\n- my task\n',
        '.bc-agent/project/overview.md': '# Overview\n\nmine\n',
        '.bc-agent/index.md': '# Index\n\ncustom\n',
        '.bc-agent/AGENTS.md': '# Custom vault instructions\n\nkeep me\n',
    }
    for rel, text in old.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text)
    out = _run(tmp_path, 'code')
    for rel, text in old.items():
        assert (tmp_path / rel).read_text() == text
    assert 'earlier-layout paths exist under .bc-agent' in out


def test_hybrid_generated_text_has_no_retired_paths(tmp_path):
    retired = ('tasks/active.md', 'tasks/completed.md', 'parking-lot', '.bc-agent/decisions',
               '.bc-agent/research', 'out-of-scope', 'scratch/', 'home.md')
    root = _scaffold(tmp_path, 'hybrid')
    found = [(str(p.relative_to(root)), term) for p in root.rglob('*.md')
             for term in retired if term in p.read_text().lower()]
    assert found == []


def test_parse_where_things_go_rejects_text_without_table():
    with pytest.raises(ValueError):
        _module().parse_where_things_go('# Agents\n\n## Something else\n\n| a | b |\n')
