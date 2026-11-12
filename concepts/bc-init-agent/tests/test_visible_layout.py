"""Visible work layout emitted by the scaffold CLI."""
from pathlib import Path
import subprocess
import sys

SCAFFOLD = Path(__file__).resolve().parents[1] / "body/scaffold.py"


def test_code_and_ops_generated_text_has_no_retired_paths(tmp_path):
    retired = ('tasks/active.md', 'tasks/completed.md', 'parking-lot',
               'project/overview.md', '.bc-agent/decisions', '.bc-agent/research',
               'out-of-scope', 'scratch/', 'index.md', 'home.md')
    for archetype in ('code', 'ops'):
        root = tmp_path / archetype
        root.mkdir()
        subprocess.run([sys.executable, str(SCAFFOLD), '--root', str(root), '--slug', 'demo', '--archetype', archetype], check=True)
        for path in root.rglob('*.md'):
            text = path.read_text().replace(_module().DEFAULT_PATH_RULE, '').lower()
            assert not any(term in text for term in retired), str(path)


def test_ops_scaffold_keeps_distinct_operations_knowledge(tmp_path):
    subprocess.run([sys.executable, str(SCAFFOLD), '--root', str(tmp_path), '--slug', 'demo', '--archetype', 'ops'], check=True)
    assert (tmp_path / 'docs/components/README.md').is_file()
    assert not (tmp_path / 'docs/open-questions').exists()
    assert not (tmp_path / '.bc-agent/templates/open-question.md').exists()
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


def _base_scaffold(tmp_path):
    shown = subprocess.run(
        ['git', 'show', f'{BASE_COMMIT}:concepts/bc-init-agent/body/scaffold.py'],
        cwd=SCAFFOLD.parent, capture_output=True)
    if shown.returncode != 0:
        pytest.skip(f'base commit {BASE_COMMIT} is not available (shallow clone or export)')
    base = tmp_path / 'base_scaffold.py'
    base.write_bytes(shown.stdout)
    return base


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
    'docs/components/README.md',
}
HYBRID_FILES = OPS_FILES | {
    '.bc-agent/index.md',
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
    base = _base_scaffold(tmp_path)
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
        assert 'open-questions' not in roles
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


def test_hybrid_generated_text_has_no_retired_paths(tmp_path):
    retired = ('tasks/active.md', 'tasks/completed.md', 'parking-lot', '.bc-agent/decisions',
               '.bc-agent/research', 'out-of-scope', 'scratch/', 'home.md')
    root = _scaffold(tmp_path, 'hybrid')
    rule = _module().DEFAULT_PATH_RULE
    found = [(str(p.relative_to(root)), term) for p in root.rglob('*.md')
             for term in retired if term in p.read_text().replace(rule, '').lower()]
    assert found == []


def _raw(root, archetype, *extra, script=SCAFFOLD):
    return subprocess.run(
        [sys.executable, str(script), '--root', str(root), '--slug', 'demo',
         '--date', '2026-01-02', '--archetype', archetype, *extra],
        capture_output=True, text=True)


def _write(root, files):
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)


# --- earlier-layout projects ---------------------------------------------------

EARLIER_LAYOUT = {
    'code': {'.bc-agent/tasks/active.md': '# Active\n\n- my task\n',
             '.bc-agent/project/overview.md': '# Overview\n\nmine\n',
             '.bc-agent/index.md': '# Index\n\ncustom\n',
             '.bc-agent/AGENTS.md': '# Custom vault instructions\n\nkeep me\n'},
    'ops': {'.bc-agent/components/README.md': '# Components\n\nweb host\n',
            '.bc-agent/findings/README.md': '# Findings\n',
            '.bc-agent/open-questions/README.md': '# Open questions\n',
            '.bc-agent/plans/README.md': '# Plans\n'},
    'hybrid': {'.bc-agent/decisions/adr-0001.md': '# ADR\n'},
}


@pytest.mark.parametrize('archetype', VISIBLE)
def test_earlier_layout_is_refused_before_any_write(tmp_path, archetype):
    _write(tmp_path, EARLIER_LAYOUT[archetype])
    before = _snapshot(tmp_path)
    result = _raw(tmp_path, archetype)
    assert result.returncode != 0
    assert _snapshot(tmp_path) == before
    for rel in EARLIER_LAYOUT[archetype]:
        if rel != '.bc-agent/AGENTS.md':
            assert rel.split('/')[1] in result.stdout
    assert 'nothing was written' in result.stdout
    assert 'separate, explicit step' in result.stdout
    assert '--allow-earlier-layout' in result.stdout


@pytest.mark.parametrize('rel', [
    '.bc-agent/tasks/active.md', '.bc-agent/decisions/x.md', '.bc-agent/research/README.md',
    '.bc-agent/scratch/.gitkeep', '.bc-agent/out-of-scope/.gitkeep', '.bc-agent/home.md',
    '.bc-agent/components/README.md', '.bc-agent/findings/README.md',
    '.bc-agent/open-questions/README.md', '.bc-agent/plans/README.md',
    '.bc-agent/conventions/planning-workflow.md', '.bc-agent/templates/plan.md'])
def test_each_earlier_layout_path_is_detected(tmp_path, rel):
    _write(tmp_path, {rel: 'old\n'})
    result = _raw(tmp_path, 'ops')
    assert result.returncode != 0
    assert rel.removeprefix('.bc-agent/').split('/')[0] in result.stdout or rel.removeprefix('.bc-agent/') in result.stdout


def test_hybrid_does_not_count_its_own_teach_catalog(tmp_path):
    _write(tmp_path, {'.bc-agent/index.md': '# Catalog\n'})
    assert _raw(tmp_path, 'hybrid').returncode == 0


def test_hybrid_counts_project_folder_as_earlier_layout(tmp_path):
    _write(tmp_path, {'.bc-agent/project/overview.md': '# Teach\n'})
    result = _raw(tmp_path, 'hybrid')
    assert result.returncode != 0
    assert 'project' in result.stdout


@pytest.mark.parametrize('archetype', VISIBLE)
def test_allow_earlier_layout_creates_missing_files_beside_old_ones(tmp_path, archetype):
    _write(tmp_path, EARLIER_LAYOUT[archetype])
    out = _run(tmp_path, archetype, '--allow-earlier-layout')
    for rel, text in EARLIER_LAYOUT[archetype].items():
        assert (tmp_path / rel).read_text() == text
    assert (tmp_path / 'work/0-ideas.md').is_file()
    assert 'earlier-layout paths exist under .bc-agent' in out


# --- --force scope -------------------------------------------------------------

def test_force_never_overwrites_project_files_outside_bc_agent(tmp_path):
    root = _scaffold(tmp_path, 'ops')
    mine = {'glossary.md': 'my terms\n', 'work/0-ideas.md': 'my ideas\n',
            'docs/components/README.md': 'my hosts\n',
            'AGENTS.md': 'my root\n', '.bc-agent/log.md': 'old log\n'}
    _write(root, mine)
    _run(root, 'ops', '--force')
    for rel, text in mine.items():
        if rel == '.bc-agent/log.md':
            assert (root / rel).read_text() != text
        else:
            assert (root / rel).read_text() == text, rel


# --- generated text --------------------------------------------------------------

@pytest.mark.parametrize('archetype', VISIBLE)
def test_stage_folders_keep_gitkeep_permanently(tmp_path, archetype):
    text = (_scaffold(tmp_path, archetype) / '.bc-agent/conventions/file-layout.md').read_text()
    assert 'keep their `.gitkeep`' in text
    assert 'remove it' not in text


@pytest.mark.parametrize('archetype', VISIBLE)
def test_codebase_docs_scope_excludes_table_records(tmp_path, archetype):
    root = _scaffold(tmp_path, archetype)
    root_agents = ' '.join((root / 'AGENTS.md').read_text().split())
    assert 'follow `codebase-docs`' in root_agents
    assert 'does not apply to the paths named in the "Where things go" table' in root_agents
    skills = ' '.join((root / '.bc-agent/references/agent-skills.md').read_text().split())
    assert 'not the paths named in the "Where things go" table' in skills
    assert 'not this vault' not in skills


@pytest.mark.parametrize('archetype', VISIBLE)
def test_agents_redirects_skill_default_paths_to_table(tmp_path, archetype):
    text = (_scaffold(tmp_path, archetype) / '.bc-agent/AGENTS.md').read_text()
    rule = _module().DEFAULT_PATH_RULE
    assert rule in text
    for example in ('`docs/adr/`', '`.bc-agent/project/overview.md`', '`.bc-agent/out-of-scope/`'):
        assert example in rule
    assert 'Why:' in rule
    assert text.index(rule) < text.index('## Work items')


@pytest.mark.parametrize('archetype', VISIBLE)
def test_next_number_counts_month_folders(tmp_path, archetype):
    text = (_scaffold(tmp_path, archetype) / '.bc-agent/AGENTS.md').read_text()
    assert 'including the month folders under `3-done/`, plus one' in ' '.join(text.split())


@pytest.mark.parametrize('archetype', ['code', 'ops'])
def test_code_and_ops_skill_map_has_no_vault_wording(tmp_path, archetype):
    text = (_scaffold(tmp_path, archetype) / '.bc-agent/references/agent-skills.md').read_text()
    assert 'vault' not in text.lower()
    assert 'index' not in text.lower()
    assert 'code/hybrid' not in text
    assert 'architecture-runway.md' in text


@pytest.mark.parametrize('archetype', ['ops', 'hybrid'])
def test_ops_templates_are_linked_and_used(tmp_path, archetype):
    root = _scaffold(tmp_path, archetype)
    map_text = (root / '.bc-agent/map.md').read_text()
    for name in ('component', 'finding'):
        assert f'[templates/{name}.md](templates/{name}.md)' in map_text
    assert 'open-question' not in map_text
    agents = (root / '.bc-agent/AGENTS.md').read_text()
    assert 'under `docs/components/` from [templates/component.md](templates/component.md)' in agents
    assert 'under `docs/research/` from [templates/finding.md](templates/finding.md)' in agents


def test_code_map_and_agents_do_not_mention_ops_templates(tmp_path):
    root = _scaffold(tmp_path, 'code')
    assert 'templates/component.md' not in (root / '.bc-agent/map.md').read_text()
    assert 'docs/components/' not in (root / '.bc-agent/AGENTS.md').read_text()


@pytest.mark.parametrize('archetype', VISIBLE)
def test_open_questions_live_in_work_items(tmp_path, archetype):
    root = _scaffold(tmp_path, archetype)
    text = (root / '.bc-agent/AGENTS.md').read_text()
    rule = ' '.join(text[text.index('## Work items'):text.index('## Keep it current')].split())
    assert 'An unanswered question that blocks a piece of work is a step in that work item' in rule
    assert 'a planned work item whose answer lands in `docs/research/`' in rule
    assert 'a line in `work/0-ideas.md`' in rule
    assert 'Why: `work/` stays the single place that shows what is pending' in rule
    generated = ' '.join(p.read_text() for p in root.rglob('*.md'))
    assert 'open-questions/' not in generated


def test_hybrid_shares_the_root_glossary_with_teach(tmp_path):
    root = _scaffold(tmp_path, 'hybrid')
    agents = (root / '.bc-agent/AGENTS.md').read_text()
    rows = {row.split('|')[1].strip(): row for row in agents.splitlines() if row.startswith('| ')}
    assert 'teach' not in rows['glossary']
    assert '`glossary.md`' in rows['teach-workspace']
    assert 'project/overview.md' not in rows['teach-workspace']
    section = ' '.join(agents[agents.index('## Hosted teach workspace'):].split())
    assert 'shared with the project' in section
    assert 'project/overview.md' not in section
    assert 'overview' not in (root / '.bc-agent/index.md').read_text()


def test_hybrid_points_orientation_at_table_and_links_teach_pages(tmp_path):
    root = _scaffold(tmp_path, 'hybrid')
    agents = (root / '.bc-agent/AGENTS.md').read_text()
    assert 'Project orientation is the "Where things go" table above, not `index.md`' in ' '.join(agents.split())
    map_text = (root / '.bc-agent/map.md').read_text()
    assert '[references/teach-skill.md](references/teach-skill.md)' in map_text
    assert '[index.md](index.md)' in map_text


@pytest.mark.parametrize('archetype', VISIBLE)
def test_visible_log_seed_names_visible_layout(tmp_path, archetype):
    text = (_scaffold(tmp_path, archetype) / '.bc-agent/log.md').read_text()
    assert 'vault' not in text
    assert '`work/`' in text


@pytest.mark.parametrize('archetype', VISIBLE)
def test_existing_root_agents_note_names_where_things_go(tmp_path, archetype):
    _write(tmp_path, {'AGENTS.md': '# mine\n'})
    out = _run(tmp_path, archetype)
    assert 'search-first' not in out
    assert '"Where things go" table' in out


# --- upgrade notes ----------------------------------------------------------------

def test_map_note_ignores_inline_code_for_paths_outside_bc_agent(tmp_path):
    module = _module()
    root = _scaffold(tmp_path, 'code')
    (root / '.bc-agent/map.md').write_text('# Map\n\n- `work/` — work items\n- [log.md](log.md)\n')
    assert not any('map.md' in note for note in module.upgrade_notes(root, 'code'))
    (root / '.bc-agent/map.md').write_text('# Map\n\n- `log.md`\n')
    assert any('map.md' in note for note in module.upgrade_notes(root, 'code'))


def test_table_note_uses_the_parser(tmp_path):
    module = _module()
    root = _scaffold(tmp_path, 'code')
    agents = root / '.bc-agent/AGENTS.md'
    agents.write_text('# A\n\n## Where things go\n| Role | Path | Notes |\n| --- | --- | --- |\n| glossary | `glossary.md` | x |\n')
    assert not any('Where things go' in note for note in module.upgrade_notes(root, 'code'))
    agents.write_text('# A\n\n## Where things go\n\nnothing here\n')
    assert any('Where things go' in note for note in module.upgrade_notes(root, 'code'))
    agents.write_text('# A\n')
    assert any('Where things go' in note for note in module.upgrade_notes(root, 'code'))


# --- parser contract ----------------------------------------------------------------

TABLE_HEAD = '| Role | Path | Notes |\n| :--- | --- | --- |\n'


@pytest.mark.parametrize('row, expected', [
    ('| decisions | `docs/decisions/` | x |', 'docs/decisions/'),
    ('| decisions | decisions/ | x |', 'decisions/'),
    ('| decisions |  decisions/  | x | extra |', 'decisions/'),
    ('| project-agents | — | x |', ''),
    ('| project-agents | - | x |', ''),
    ('| project-agents |  | x |', ''),
])
def test_parse_where_things_go_path_cells(row, expected):
    text = f'# A\n\n## Where things go\n\n{TABLE_HEAD}{row}\n'
    assert _module().parse_where_things_go(text) == {row.split('|')[1].strip(): expected}


@pytest.mark.parametrize('heading', ['## Where things go  ', '## Where things go\r'])
def test_parse_where_things_go_tolerates_trailing_space_and_crlf(heading):
    text = f'# A\n\n{heading}\n\n{TABLE_HEAD}| glossary | `glossary.md` | x |\n'.replace('\n', '\r\n' if heading.endswith('\r') else '\n')
    text = text.replace('\r\r', '\r')
    assert _module().parse_where_things_go(text) == {'glossary': 'glossary.md'}


@pytest.mark.parametrize('text', [
    '# Agents\n\n## Something else\n\n| a | b |\n',
    '# Agents\n\n### Where things go\n\n| Role | Path |\n| --- | --- |\n| glossary | `g.md` |\n',
    '# Agents\n\nSee ## Where things go below\n',
])
def test_parse_where_things_go_rejects_missing_heading(text):
    with pytest.raises(ValueError):
        _module().parse_where_things_go(text)


def test_parse_where_things_go_rejects_heading_without_rows():
    with pytest.raises(ValueError):
        _module().parse_where_things_go(f'# A\n\n## Where things go\n\n{TABLE_HEAD}\n## Next\n')


def test_parse_where_things_go_rejects_duplicate_role():
    text = f'# A\n\n## Where things go\n\n{TABLE_HEAD}| glossary | `a.md` | x |\n| glossary | `b.md` | y |\n'
    with pytest.raises(ValueError):
        _module().parse_where_things_go(text)


# --- learning and knowledge unchanged ------------------------------------------------

@pytest.mark.parametrize('archetype', ['learning', 'knowledge'])
def test_vault_archetypes_printed_output_matches_base(tmp_path, archetype):
    base = _base_scaffold(tmp_path)
    outputs = []
    for script in (base, SCAFFOLD):
        root = tmp_path / 'root'
        if root.exists():
            subprocess.run(['rm', '-rf', str(root)], check=True)
        root.mkdir()
        _write(root, {'AGENTS.md': '# mine\n', '.bc-agent/map.md': '# Map\n\n- `log.md`\n'})
        runs = [_raw(root, archetype, script=script), _raw(root, archetype, script=script),
                _raw(root, archetype, '--force', script=script)]
        outputs.append([(r.returncode, r.stdout, r.stderr) for r in runs])
    assert outputs[1] == outputs[0]
