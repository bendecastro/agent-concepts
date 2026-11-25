"""docs/guardrails/README.md and its map row, emitted by the scaffold for the archetypes that get the design page."""
from pathlib import Path
import importlib.util
import subprocess
import sys

import pytest

SCAFFOLD = Path(__file__).resolve().parents[1] / "body/scaffold.py"
VISIBLE = ('code', 'ops', 'hybrid')
MAP_ROW = '`docs/guardrails/README.md`'


def _module():
    spec = importlib.util.spec_from_file_location('scaffold', SCAFFOLD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(root, archetype, *extra):
    return subprocess.run(
        [sys.executable, str(SCAFFOLD), '--root', str(root), '--slug', 'demo',
         '--date', '2026-01-02', '--archetype', archetype, *extra],
        check=True, capture_output=True, text=True).stdout


@pytest.mark.parametrize('archetype', VISIBLE)
def test_fresh_scaffold_creates_guardrails_readme(tmp_path, archetype):
    _run(tmp_path, archetype)
    text = (tmp_path / 'docs/guardrails/README.md').read_text()
    for heading in ('## Targets', '## Budgets', '## Checks', '## Where a rule lives', '## How to measure'):
        assert heading in text
    assert '`bc-performance-guardrails` skill' in text
    assert "the agent's choice" in text
    assert 'docs/design/README.md' in text
    assert 'scripts/gate' in text
    assert text.count('(none yet)') == 3


@pytest.mark.parametrize('archetype', VISIBLE)
def test_scaffold_creates_no_measuring_script(tmp_path, archetype):
    _run(tmp_path, archetype)
    assert sorted(p.name for p in (tmp_path / 'docs/guardrails').iterdir()) == ['README.md']
    assert sorted(p.name for p in (tmp_path / 'scripts').iterdir()) == ['gate']


@pytest.mark.parametrize('archetype', ['learning', 'knowledge'])
def test_vault_archetypes_get_no_guardrails_readme(tmp_path, archetype):
    _run(tmp_path, archetype)
    assert not (tmp_path / 'docs/guardrails').exists()


@pytest.mark.parametrize('force', [(), ('--force',)])
@pytest.mark.parametrize('archetype', VISIBLE)
def test_existing_guardrails_readme_is_not_overwritten(tmp_path, archetype, force):
    readme = tmp_path / 'docs/guardrails/README.md'
    readme.parent.mkdir(parents=True)
    readme.write_text('# Our limits\n')
    out = _run(tmp_path, archetype, *force)
    assert readme.read_text() == '# Our limits\n'
    assert f'= {readme}' in out


@pytest.mark.parametrize('archetype', VISIBLE)
def test_map_routes_guardrail_work_to_guardrails_readme(tmp_path, archetype):
    _run(tmp_path, archetype)
    rows = [line for line in (tmp_path / '.bc-agent/map.md').read_text().splitlines() if MAP_ROW in line]
    assert len(rows) == 1
    assert 'speed' in rows[0] and 'structure' in rows[0]


@pytest.mark.parametrize('archetype', VISIBLE)
def test_second_run_leaves_guardrails_readme_and_map_unchanged(tmp_path, archetype):
    _run(tmp_path, archetype)
    paths = (tmp_path / 'docs/guardrails/README.md', tmp_path / '.bc-agent/map.md')
    before = [p.read_bytes() for p in paths]
    out = _run(tmp_path, archetype)
    assert [p.read_bytes() for p in paths] == before
    assert 'Nothing to do' in out


def test_existing_map_without_guardrails_row_gets_upgrade_note(tmp_path):
    module = _module()
    _run(tmp_path, 'code')
    assert not any('docs/guardrails/README.md' in note for note in module.upgrade_notes(tmp_path, 'code'))
    (tmp_path / '.bc-agent/map.md').write_text('# Map\n\n- [log.md](log.md)\n')
    assert any('docs/guardrails/README.md' in note for note in module.upgrade_notes(tmp_path, 'code'))
