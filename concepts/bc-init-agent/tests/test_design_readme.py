"""docs/design/README.md and its map row, emitted by the scaffold for visible-layout projects."""
from pathlib import Path
import importlib.util
import subprocess
import sys

import pytest

SCAFFOLD = Path(__file__).resolve().parents[1] / "body/scaffold.py"
VISIBLE = ('code', 'ops', 'hybrid')
MAP_ROW = '`docs/design/README.md`'


def _module():
    spec = importlib.util.spec_from_file_location('scaffold', SCAFFOLD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(root, archetype):
    return subprocess.run(
        [sys.executable, str(SCAFFOLD), '--root', str(root), '--slug', 'demo',
         '--date', '2026-01-02', '--archetype', archetype],
        check=True, capture_output=True, text=True).stdout


@pytest.mark.parametrize('archetype', VISIBLE)
def test_fresh_scaffold_creates_design_readme(tmp_path, archetype):
    _run(tmp_path, archetype)
    text = (tmp_path / 'docs/design/README.md').read_text()
    for heading in ('## Current truth vs decision log', '## Where a rule lives',
                    '## Before adding or restyling a control', '## Pages', '## Checks'):
        assert heading in text
    assert "the project's decision log" in text
    assert text.count('(none yet)') == 2


@pytest.mark.parametrize('archetype', ['learning', 'knowledge'])
def test_vault_archetypes_get_no_design_readme(tmp_path, archetype):
    _run(tmp_path, archetype)
    assert not (tmp_path / 'docs/design').exists()


@pytest.mark.parametrize('archetype', VISIBLE)
def test_existing_design_readme_is_not_overwritten(tmp_path, archetype):
    readme = tmp_path / 'docs/design/README.md'
    readme.parent.mkdir(parents=True)
    readme.write_text('# Our design\n')
    out = _run(tmp_path, archetype)
    assert readme.read_text() == '# Our design\n'
    assert f'= {readme}' in out


@pytest.mark.parametrize('archetype', VISIBLE)
def test_map_routes_design_work_to_design_readme(tmp_path, archetype):
    _run(tmp_path, archetype)
    rows = [line for line in (tmp_path / '.bc-agent/map.md').read_text().splitlines() if MAP_ROW in line]
    assert len(rows) == 1
    assert 'design' in rows[0].lower() and 'CLI' in rows[0]


@pytest.mark.parametrize('archetype', VISIBLE)
def test_second_run_leaves_design_readme_and_map_unchanged(tmp_path, archetype):
    _run(tmp_path, archetype)
    paths = (tmp_path / 'docs/design/README.md', tmp_path / '.bc-agent/map.md')
    before = [p.read_bytes() for p in paths]
    out = _run(tmp_path, archetype)
    assert [p.read_bytes() for p in paths] == before
    assert 'Nothing to do' in out


def test_existing_map_without_design_row_gets_upgrade_note(tmp_path):
    module = _module()
    _run(tmp_path, 'code')
    assert not any('docs/design/README.md' in note for note in module.upgrade_notes(tmp_path, 'code'))
    (tmp_path / '.bc-agent/map.md').write_text('# Map\n\n- [log.md](log.md)\n')
    assert any('docs/design/README.md' in note for note in module.upgrade_notes(tmp_path, 'code'))
