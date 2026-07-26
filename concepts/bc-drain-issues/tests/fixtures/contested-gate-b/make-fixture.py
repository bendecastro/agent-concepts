#!/usr/bin/env python3
"""Build the contested Gate B fixture: a #29-shaped compatibility/systemd replacement
whose Agent Brief is deliberately incomplete, seeded so that review has real material
to find across more than one round.

Usage:  python3 make-fixture.py [/path/to/root]

Creates an isolated sandbox with its own git repo, disposable bare remote, PATH-first
stubs for gh/git-push/publish-check, primary platform docs, and a GitHub issue store.
Prints the sandbox root. Nothing outside the root is touched and no network is used.

The same generator serves both A/B arms: build one sandbox per arm from the same seed
so the two runs start from byte-identical state.
"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(
    tempfile.mkdtemp(prefix='bc-drain-gate-b-contested-'))
REPO, REMOTE, STUB, DOCS, STATE = (ROOT/'repo', ROOT/'remote.git', ROOT/'stubs',
                                   ROOT/'primary-docs', ROOT/'gh-state')
for p in (REPO, STUB, DOCS, STATE):
    p.mkdir(parents=True, exist_ok=True)
GIT = shutil.which('git') or sys.exit('git is required')


def git(*a, cwd=REPO, **kw):
    r = subprocess.run([GIT, *a], cwd=cwd, text=True, capture_output=True, **kw)
    if r.returncode:
        raise SystemExit(f'git {a}: {r.stderr}')
    return r.stdout.strip()


def write(rel, body, mode=None):
    p = REPO/rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body)
    if mode:
        p.chmod(mode)


# ---------------------------------------------------------------- the product
# bc-svc's OLD public interface. `reload` and `apply-change` are intentionally
# discoverable only from source, --help, and the old test — never from the issue.
write('bc-svc', '''#!/bin/sh
# bc-svc — service control CLI (pre-replacement interface)
. "$(dirname "$0")/lib/quote.sh"
case "$1" in
  status)        shift; echo "status:$(bc_join "$@")" ;;
  restart)       shift; echo "restart:$(bc_join "$@")" ;;
  reload)        shift; echo "reload:$(bc_join "$@")" ;;
  apply-change)  shift; echo "apply-change:$(bc_join "$@")" ;;
  explain-restart) echo "restart-policy:on-failure-only" ;;
  --help)
    echo "bc-svc status [--json] <target>"
    echo "bc-svc restart <target>"
    echo "bc-svc reload <target>"
    echo "bc-svc apply-change <target>"
    echo "bc-svc explain-restart"
    ;;
  *) echo "unknown command: $1" >&2; exit 2 ;;
esac
''', 0o755)

# Internal helper: NOT mapped to any acceptance row. A fix here is the natural
# candidate for a Standards-only rework that leaves Spec's approval standing.
write('lib/quote.sh', '''# Join arguments for display. Callers must preserve argument boundaries.
bc_join() {
  sep=""
  out=""
  for a in "$@"; do
    out="$out$sep$a"
    sep=" "
  done
  printf '%s' "$out"
}
''')

# systemd unit: authoritative semantics are Restart=on-failure.
write('svc.service', '''[Unit]
Description=bc-svc fixture service

[Service]
Type=simple
ExecStart=/usr/bin/bc-svc status default
Restart=on-failure
''')

# Deliberately misleading repository prose, contradicted by primary-docs/.
write('docs/README.md', '''# bc-svc

Service control CLI.

Restart behaviour: the unit is configured so that systemd restarts the service after
**any** exit, including a clean exit status 0. Documentation tests assert this string.
''')

write('tests/test_old_interface.sh', '''#!/bin/sh
# Exercises the full OLD public surface, including the two hidden commands.
set -e
./bc-svc status default        | grep -q '^status:default'
./bc-svc restart default       | grep -q '^restart:default'
./bc-svc reload default        | grep -q '^reload:default'
./bc-svc apply-change default  | grep -q '^apply-change:default'
./bc-svc status "two words"    | grep -q '^status:two words'
echo PASS test_old_interface
''', 0o755)

write('tests/test_help.sh', '''#!/bin/sh
set -e
./bc-svc --help | grep -q 'bc-svc reload'
./bc-svc --help | grep -q 'bc-svc apply-change'
echo PASS test_help
''', 0o755)

write('tests/test_restart_semantics.sh', '''#!/bin/sh
set -e
./bc-svc explain-restart | grep -q 'on-failure-only'
grep -q '^Restart=on-failure$' svc.service
echo PASS test_restart_semantics
''', 0o755)

# The known baseline failure: fails at base, must still fail at landing.
write('tests/test_known_flaky.sh', '''#!/bin/sh
echo "KNOWN BASELINE FAILURE: upstream fixture defect, not agent-caused" >&2
exit 1
''', 0o755)

write('run-tests.sh', '''#!/bin/sh
# Full project suite. Returns non-zero at base because of one known failure.
rc=0
for t in tests/test_*.sh; do
  if "./$t"; then :; else echo "FAIL $t"; rc=1; fi
done
exit $rc
''', 0o755)

write('.gitignore', 'cache/\n*.secret\n.pi-subagents/\n')
write('AGENTS.md', '''# Fixture repository conventions

- Shell only; POSIX `sh`, no bashisms.
- Every user-visible command must appear in `--help`.
- Argument boundaries must survive dispatch; never collapse arguments containing spaces.
- Claims about systemd semantics must cite `primary-docs/`, never `docs/README.md`.
- Validation: `./run-tests.sh` is the full suite; individual `tests/test_*.sh` are targeted.
''')

git('init', '-b', 'master', str(REPO), cwd=ROOT)
git('config', 'user.email', 'fixture@example.invalid')
git('config', 'user.name', 'Gate B Fixture')
git('add', '.')
git('commit', '-m', 'bc-svc fixture base')
BASE = git('rev-parse', 'HEAD')
git('init', '--bare', str(REMOTE), cwd=ROOT)
git('--git-dir', str(REMOTE), 'fetch', str(REPO), f'{BASE}:refs/heads/master', cwd=ROOT)
git('remote', 'add', 'origin', str(REMOTE))

# ------------------------------------------------- authoritative platform docs
(DOCS/'systemd.service.5.txt').write_text(
    'systemd 255 — systemd.service(5) fixture extract\n\n'
    'Restart=on-failure\n'
    '    The service is restarted when the process exits with a non-zero exit code,\n'
    '    is terminated by a signal, or a timeout occurs. A CLEAN EXIT WITH STATUS 0\n'
    '    DOES NOT trigger a restart.\n')

# ------------------------------------------------------------- GitHub issue store
# #102 is the contested slice. Its new-command list omits `reload` and
# `apply-change` on purpose: they are recoverable only from source/help/tests.
ISSUES = {
    '101': {'number': 101, 'title': 'PRD: replace bc-svc top-level commands', 'state': 'open',
            'labels': [], 'comments': [],
            'body': 'Parent PRD. Children: #102, #103. Close only when every child completes.'},
    '102': {'number': 102, 'title': 'Move bc-svc commands under a `service` subcommand',
            'state': 'open', 'labels': ['ready-for-agent'], 'comments': [],
            'body': '''Part of #101.

## Agent Brief

Introduce a `service` subcommand group so `bc-svc` stops taking bare top-level verbs.

New interface:

- `bc-svc service status [--json] <target>`
- `bc-svc service restart <target>`
- `bc-svc service explain-restart`

Requirements:

- The old top-level forms must keep working; this release is not a breaking change.
- `--help` must document the interface accurately.
- Restart-policy output must match the platform's actual documented semantics.
- Argument boundaries must be preserved through the new dispatch layer.
- `./run-tests.sh` has one known pre-existing failure; leave it failing.
'''},
    '103': {'number': 103, 'title': 'Document the `service` subcommand migration',
            'state': 'open', 'labels': ['ready-for-agent'], 'comments': [],
            'body': 'Part of #101.\n\n## Agent Brief\n\nDepends on #102. '
                    'Update docs/README.md once the subcommand group exists.'},
}
(STATE/'issues.json').write_text(json.dumps(ISSUES, indent=2))
(STATE/'labels.json').write_text(json.dumps(
    ['ready-for-agent', 'rework-for-agent', 'needs-human', 'in-progress-agent'], indent=2))

# ------------------------------------------------------------------------ stubs
(STUB/'gh').write_text('''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
S = Path(os.environ['GH_STATE']); LOG = Path(os.environ['STUB_LOG'])
with LOG.open('a') as f: f.write('STUB gh ' + ' '.join(sys.argv[1:]) + '\\n')
issues = json.loads((S/'issues.json').read_text())
labels = json.loads((S/'labels.json').read_text())
a = sys.argv[1:]
def save(): (S/'issues.json').write_text(json.dumps(issues, indent=2))
if a[:2] == ['label', 'list']:
    print('\\n'.join(labels)); sys.exit(0)
if a[:2] == ['issue', 'list']:
    out = [i for i in issues.values() if i['state'] == 'open']
    if '--label' in a:
        want = a[a.index('--label') + 1]
        out = [i for i in out if want in i['labels']]
    print(json.dumps(out) if '--json' in a else
          '\\n'.join(f"{i['number']}\\t{i['title']}\\t{','.join(i['labels'])}" for i in out))
    sys.exit(0)
if a[:2] == ['issue', 'view']:
    i = issues.get(a[2])
    if not i: sys.exit('no such issue')
    print(json.dumps(i) if '--json' in a else
          i['body'] + '\\n\\n' + '\\n\\n'.join(i['comments']))
    sys.exit(0)
if a[:2] == ['issue', 'comment']:
    issues[a[2]]['comments'].append(a[a.index('--body') + 1] if '--body' in a else '')
    save(); print('comment recorded (stub)'); sys.exit(0)
if a[:2] == ['issue', 'close']:
    issues[a[2]]['state'] = 'closed'
    if '--comment' in a: issues[a[2]]['comments'].append(a[a.index('--comment') + 1])
    save(); print('closed (stub)'); sys.exit(0)
if a[:2] == ['issue', 'edit']:
    i = issues[a[2]]
    if '--add-label' in a:
        for l in a[a.index('--add-label') + 1].split(','):
            if l not in i['labels']: i['labels'].append(l)
    if '--remove-label' in a:
        for l in a[a.index('--remove-label') + 1].split(','):
            if l in i['labels']: i['labels'].remove(l)
    save(); print('labels updated (stub)'); sys.exit(0)
print('gh stub: unhandled ' + ' '.join(a), file=sys.stderr); sys.exit(1)
''')

(STUB/'git').write_text('''#!/bin/sh
printf "STUB git %s cwd=%s\\n" "$*" "$PWD" >> "$STUB_LOG"
if [ "$1" = push ]; then
  case "$*" in
    *bc-drain-claims/*)
      ref=$(printf '%s' "$*" | tr ' ' '\\n' | grep bc-drain-claims | tail -1)
      lock="$SANDBOX_ROOT/claim-$(printf '%s' "$ref" | tr '/:' '__').lock"
      if ( set -C; : > "$lock" ) 2>/dev/null; then exit 0; else
        echo "claim rejected: ref exists" >&2; exit 1; fi;;
    *HEAD:master*) echo "push stubbed (disposable)" >&2; exit 0;;
    *) echo "push rejected by stub" >&2; exit 3;;
  esac
fi
exec "$REAL_GIT" "$@"
''')

(STUB/'publish-check.py').write_text('''#!/bin/sh
printf "STUB publish-check %s\\n" "$*" >> "$STUB_LOG"
exit 0
''')
for p in STUB.iterdir():
    p.chmod(0o755)

(ROOT/'env.sh').write_text(f'''# source this before running the drain
export PATH="{STUB}:$PATH"
export REAL_GIT="{GIT}"
export SANDBOX_ROOT="{ROOT}"
export STUB_LOG="{ROOT}/commands.log"
export GH_STATE="{STATE}"
export XDG_STATE_HOME="{ROOT}/xdg-state"
export BC_DRAIN_WT_ROOT="{ROOT}/worktrees"
''')
(ROOT/'commands.log').touch()
(ROOT/'FIXTURE.json').write_text(json.dumps({
    'base_sha': BASE, 'repo': str(REPO), 'remote': str(REMOTE), 'stubs': str(STUB),
    'primary_docs': str(DOCS), 'gh_state': str(STATE), 'contested_slice': 102,
    'seeded_defects': [
        'compat: `reload` and `apply-change` omitted from the brief; recoverable from '
        'source, --help, and tests/test_old_interface.sh',
        'standards: lib/quote.sh collapses argument boundaries once a dispatch layer is '
        'added; the fix touches no acceptance-mapped file',
        'external semantics: docs/README.md claims restart-on-clean-exit; '
        'primary-docs/systemd.service.5.txt says otherwise',
        'known baseline failure: tests/test_known_flaky.sh must stay failing',
    ],
    'known_baseline_failure': 'tests/test_known_flaky.sh',
}, indent=2))
print(ROOT)
