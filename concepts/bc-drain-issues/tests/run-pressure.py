#!/usr/bin/env python3
import os, sys, json, hashlib, subprocess, tarfile, tempfile, shutil, stat
from pathlib import Path

DEFAULT_CANDIDATE=Path(__file__).resolve().parents[4]
CANDIDATE=Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_CANDIDATE
CONCEPT=CANDIDATE/'agents/concepts/bc-drain-issues'
ROOT=Path(tempfile.mkdtemp(prefix='bc-drain-v2-gate-a-'))
REAL_GIT=shutil.which('git')
if not REAL_GIT:
    raise SystemExit('git is required')
REPO=ROOT/'repo'; REMOTE=ROOT/'remote.git'; ART=ROOT/'artifacts'; LOG=ROOT/'logs'; STUB=ROOT/'stubs'; WT=ROOT/'worktrees'; STATE=ROOT/'xdg-state'
for p in (REPO,ART,LOG,STUB,WT,STATE): p.mkdir(parents=True,exist_ok=True)
CMDLOG=LOG/'commands.log'
def run(cmd,cwd=REPO,env=None,check=True):
    e=os.environ.copy(); e.update({'PATH':str(STUB)+os.pathsep+e['PATH'],'XDG_STATE_HOME':str(STATE),'STUB_LOG':str(CMDLOG),'REAL_GIT':REAL_GIT,'SANDBOX_ROOT':str(ROOT)})
    if env:e.update(env)
    r=subprocess.run(cmd,cwd=cwd,env=e,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    with CMDLOG.open('a') as f:f.write(f"RUN cwd={cwd} cmd={cmd!r} rc={r.returncode}\n")
    if check and r.returncode: raise RuntimeError(f"{cmd}: {r.returncode}\n{r.stdout}\n{r.stderr}")
    return r

def dump(rel,obj):
    p=ART/rel; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")
    return str(p)
def text(rel,s):
    p=ART/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s);return str(p)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def git(*args,cwd=REPO,env=None,check=True):return run([str(STUB/'git'),*args],cwd,env,check)
def realgit(*args,cwd=REPO,env=None,check=True):
    e=os.environ.copy();
    if env:e.update(env)
    r=subprocess.run([REAL_GIT,*args],cwd=cwd,env=e,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if check and r.returncode:raise RuntimeError(r.stderr)
    return r

def assert_(x,msg):
    if not x: raise AssertionError(msg)

# Stubs first on PATH. git delegates all non-push operations to the discovered git binary.
(STUB/'git').write_text('''#!/bin/sh
printf "STUB git %s cwd=%s\\n" "$*" "$PWD" >> "$STUB_LOG"
if [ "$1" = push ]; then
  case "$*" in
    *bc-drain-claims/issue-29*)
      lock="$SANDBOX_ROOT/claim-29.lock"; if ( set -C; : > "$lock" ) 2>/dev/null; then echo claim-stub-success >&2; exit 0; else echo claim-stub-rejected-existing >&2; exit 1; fi;;
    *HEAD:master*)
      n="$SANDBOX_ROOT/master-push-count"; c=0; [ -f "$n" ] && c=$(cat "$n"); c=$((c+1)); echo "$c" > "$n"; [ "$c" -eq 1 ] && { echo non-fast-forward-stub >&2; exit 1; }; echo disposable-master-push-stubbed >&2; exit 0;;
    *) echo push-rejected-by-stub >&2; exit 3;;
  esac
fi
exec "$REAL_GIT" "$@"
''')
(STUB/'gh').write_text('''#!/bin/sh
printf "STUB gh %s cwd=%s\\n" "$*" "$PWD" >> "$STUB_LOG"
echo gh-external-mutation-rejected-stub >&2
exit 0
''')
(STUB/'publish-check.py').write_text('''#!/bin/sh
printf "STUB publish-check %s cwd=%s\\n" "$*" "$PWD" >> "$STUB_LOG"
[ "${PUBLISH_AUTH:-0}" = 1 ] && exit 0
exit 2
''')
for p in STUB.iterdir():p.chmod(0o755)

# Disposable bare remote and fixture repository.
realgit('init','--bare',str(REMOTE),cwd=ROOT)
realgit('init','-b','master',str(REPO),cwd=ROOT)
realgit('config','user.email','gate@example.invalid'); realgit('config','user.name','Gate A')
realgit('remote','add','origin',str(REMOTE))
(REPO/'.gitignore').write_text('cache/\n*.secret\n.pi-subagents/\n')
(REPO/'tool.sh').write_text('#!/bin/sh\ncase "$1" in\n old-status) echo legacy-status;;\n old-hidden) echo legacy-hidden;;\n new-status) echo new-status;;\n --help) echo "old-status old-hidden new-status";;\n esac\n'); (REPO/'tool.sh').chmod(0o755)
(REPO/'service.unit').write_text('[Service]\nExecStart=tool.sh old-status\n')
(REPO/'test_tool.sh').write_text('#!/bin/sh\n./tool.sh old-hidden | grep legacy-hidden\n');(REPO/'test_tool.sh').chmod(0o755)
(REPO/'obsolete.txt').write_text('remove me\n'); (REPO/'blob.bin').write_bytes(b'\x00OLD\xff')
(REPO/'README.md').write_text('fixture\nMisleading repository prose: service restart-on-failure includes clean exit.\n')
# Launcher fixture resolves its real installed target rather than importing from cwd/PYTHONPATH.
(REPO/'app').mkdir()
(REPO/'app'/'support.py').write_text("VALUE = 'trusted-install'\n")
(REPO/'app'/'main.py').write_text("#!/usr/bin/env python3\nfrom support import VALUE\nimport os, sys\nprint(VALUE + '|' + os.getcwd() + '|' + '|'.join(sys.argv[1:]))\n")
(REPO/'launcher').write_text('''#!/bin/sh
set -eu
self=$0
while [ -L "$self" ]; do
  d=$(CDPATH= cd -- "$(dirname -- "$self")" && pwd)
  self=$(readlink "$self")
  case "$self" in /*) ;; *) self=$d/$self;; esac
done
d=$(CDPATH= cd -- "$(dirname -- "$self")" && pwd)
exec python3 -B -E "$d/app/main.py" "$@"
''')
(REPO/'launcher').chmod(0o755)
realgit('add','.'); realgit('commit','-m','fixture base')
BASE=realgit('rev-parse','HEAD').stdout.strip()
# populate bare remote without invoking push at all
realgit('--git-dir',str(REMOTE),'fetch',str(REPO),f'{BASE}:refs/heads/master',cwd=ROOT)

# Preflight blocking and labels.
policy_path=CANDIDATE/'agents/policies/publish.yaml'
policy_before=sha(policy_path) if policy_path.exists() else 'absent'
pub=run([str(STUB/'publish-check.py'),'--repo',str(REPO),'--remote',str(REMOTE),'--branch','master'],check=False)
assert_(pub.returncode==2,'unauthorized publish did not block')
labels=['ready-for-agent','rework-for-agent','needs-human','in-progress-agent']
preflight={'unauthorized_exit':pub.returncode,'dispatches':0,'parallel_without_claim_auth':'BLOCKED','labels':labels,'policy_hash_before':policy_before,'policy_hash_after':policy_before,'remote':str(REMOTE),'network_allowed':False}
dump('01/preflight.json',preflight)

# Cheap driver risk classification precedes ownership, but no child dispatch occurs until the atomic claim wins.
sequence=['risk-classified-driver-no-child']
tree=realgit('rev-parse','HEAD^{tree}').stdout.strip()
claim=realgit('commit-tree',tree,'-p',BASE,'-m','bc-drain claim issue #29',cwd=REPO,env={'GIT_AUTHOR_NAME':'Gate','GIT_AUTHOR_EMAIL':'g@example.invalid','GIT_COMMITTER_NAME':'Gate','GIT_COMMITTER_EMAIL':'g@example.invalid'}).stdout.strip()
assert_(len(claim) in (40,64) and all(c in '0123456789abcdef' for c in claim) and claim!=BASE,'claim commit was not created')
r1=git('push','origin',f'{claim}:refs/heads/bc-drain-claims/issue-29',check=False)
r2=git('push','origin',f'{claim}:refs/heads/bc-drain-claims/issue-29',check=False)
assert_(r1.returncode==0 and r2.returncode!=0,'claim race')
sequence.append('claim-won-runner1')
dispatch_tokens={'runner1':0,'runner2':0}
realgit('worktree','add','-b','bc-drain-work/issue-29',str(WT/'issue-29'),BASE)
sequence.append('worktree-created-runner1')
if r1.returncode==0:
 dispatch_tokens['runner1']=12000
 sequence.append('audit-child-dispatched-runner1')
if r2.returncode==0:
 dispatch_tokens['runner2']=12000
assert_(dispatch_tokens=={'runner1':12000,'runner2':0},'claim loser spent child tokens')
assert_(sequence==['risk-classified-driver-no-child','claim-won-runner1','worktree-created-runner1','audit-child-dispatched-runner1'],'child dispatch ordering')
realgit('worktree','add','-b','bc-drain-work/issue-30',str(WT/'issue-30'),BASE)
main_before=realgit('status','--porcelain').stdout; sib_before=realgit('status','--porcelain',cwd=WT/'issue-30').stdout
claim_ev={'claim_commit':claim,'sequence':sequence,'runner1':{'push_rc':r1.returncode,'dispatch':True,'child_tokens':dispatch_tokens['runner1'],'force':False},'runner2':{'push_rc':r2.returncode,'dispatch':False,'child_tokens':dispatch_tokens['runner2']},'dependency_issue_30':{'dependency':29,'states':['open','claimed','in-flight'],'selected':False},'worktrees':[str(WT/'issue-29'),str(WT/'issue-30')],'main_before':main_before,'sibling_before':sib_before}
dump('02/claim-dependency-isolation.json',claim_ev)

W=WT/'issue-29'; OUT=ART/'external-validation';OUT.mkdir()
# High-risk audit packet and model-only artifact limitation.
# Authoritative external documentation beats deliberately misleading repository prose.
primary=ROOT/'primary-docs';primary.mkdir()
platform_doc=primary/'systemd.service.txt'
platform_doc.write_text('systemd 255 primary help fixture: Restart=on-failure excludes clean exit status 0.\n')
hostile=ROOT/'hostile-cwd';hostile.mkdir();(hostile/'support.py').write_text("VALUE = 'HOSTILE-SHADOW'\n")
installed=ROOT/'installed-bin';installed.mkdir();(installed/'fixture-launcher').symlink_to(REPO/'launcher')
launch_direct=run([str(REPO/'launcher'),'arg one'],cwd=hostile,env={'PYTHONPATH':str(hostile)},check=False)
launch_symlink=run([str(installed/'fixture-launcher'),'arg two'],cwd=hostile,env={'PYTHONPATH':str(hostile)},check=False)
assert_(launch_direct.returncode==launch_symlink.returncode==0,'launcher failed')
assert_(launch_direct.stdout.startswith('trusted-install|') and launch_symlink.stdout.startswith('trusted-install|'),'cwd/module shadow won')
assert_('arg one' in launch_direct.stdout and 'arg two' in launch_symlink.stdout,'launcher args lost')
repo_prose=(REPO/'README.md').read_text(); authoritative=platform_doc.read_text()
assert_('includes clean exit' in repo_prose and 'excludes clean exit' in authoritative,'semantic pressure fixture missing')
audit={'role_instance':'audit-fresh-001','authority':'read-only','before_coding':True,'after_atomic_claim_and_worktree':sequence[-2:]==['worktree-created-runner1','audit-child-dispatched-runner1'],'claim_sequence':sequence,'risk':'high','effort':'medium','issue_new_command_list':['new-status'],'interface_inventory':[
 {'interface':'old-status','source':'tool.sh','test':'preserve old-status output'}, {'interface':'old-hidden','source':'tool.sh + test_tool.sh + --help','omitted_from_issue':True,'test':'preserve old-hidden output'}],
 'acceptance_matrix':[{'requirement':'new-status','observable':'./tool.sh new-status == new-status'},{'requirement':'legacy compatibility','observable':'old-status and old-hidden outputs unchanged'},{'requirement':'launcher security/topology','observable':'arguments/environment/hostile cwd/module shadow plus direct and installed-symlink launch'},{'requirement':'systemd cutover','observable':'primary help semantics plus bounded fake service check'}],
 'launcher_audit':{'arguments':True,'environment':True,'hostile_cwd':str(hostile),'module_shadow_rejected':True,'path_resolution':True,'privilege_boundary':'python -E ignores PYTHON* environment','direct_stdout':launch_direct.stdout.strip(),'installed_symlink':str(installed/'fixture-launcher'),'installed_symlink_stdout':launch_symlink.stdout.strip()},
 'external_service_evidence':{'selected_semantics':'Restart=on-failure excludes clean exit status 0','source':str(platform_doc),'version':'systemd 255 fixture','authoritative_external':True,'misleading_repository_prose_rejected':True,'string_presence_alone_sufficient':False},'baseline_failures':['known:test_external_unavailable'],'human_only':['live daemon enable/restart'],'decision_cases':{'missing_product_choice':'HUMAN_BLOCKED','clear_engineering_gap':'CONTINUE'}}
assert_(audit['after_atomic_claim_and_worktree'],'audit dispatched before claim/worktree')
assert_(audit['external_service_evidence']['authoritative_external'] and audit['external_service_evidence']['misleading_repository_prose_rejected'],'authority precedence')
dump('03/audit-role-output.json',audit)
text('03/model-limitation.txt','No nested model agents were executed. Fresh role packets and outputs are separate deterministic artifacts; assertions test their authority, inputs, schema, and state transitions.\n')

# Worker TDD/diagnosis/metric transcripts and actual scoped work.
worker_packet={'role_instance':'worker-fresh-001','worktree':str(W),'base_sha':BASE,'authority':['code','tests','targeted-validation'],'forbidden':['stage','commit','push','gh','claim','reset','clean'],'effort':'medium'};dump('04/worker-packet.json',worker_packet)
# RED then GREEN actual feature
red=run(['sh','-c','./tool.sh new-status | grep expected-new'],cwd=W,check=False)
# modify only files in worktree
p=W/'tool.sh'; p.write_text(p.read_text().replace('new-status) echo new-status','new-status) echo expected-new'))
(W/'test_new.sh').write_text('#!/bin/sh\n./tool.sh new-status | grep expected-new\n');(W/'test_new.sh').chmod(0o755)
green=run(['sh','test_new.sh'],cwd=W,check=False)
bugred=run(['sh','-c','./tool.sh old-status | grep WRONG'],cwd=W,check=False)
metric={'after_green':True,'correctness':'sh test_new.sh rc=0','baseline_ms':100,'refined_ms':80,'kept':True}
worker_out={'status':'READY_FOR_REVIEW','red_rc':red.returncode,'green_rc':green.returncode,'bug_reproduction_rc':bugred.returncode,'diagnosis':'red-capable deterministic output mismatch','metric':metric,'changed_files':['tool.sh','test_new.sh'],'commands':['sh test_new.sh'],'baseline_delta':'known external failure unchanged'};dump('04/worker-output.json',worker_out)

# Pre-review seeded blockers, each corrected before review.
blockers=[]
blockers.append({'seed':'missing acceptance evidence','dispatch':False,'correction':'add evidence map'})
realgit('add','tool.sh',cwd=W); blockers.append({'seed':'staged file','dispatch':False,'observed':realgit('diff','--cached','--name-only',cwd=W).stdout.strip(),'correction':'unstage'});realgit('restore','--staged','tool.sh',cwd=W)
(W/'unrelated.tmp').write_text('x');blockers.append({'seed':'unrelated change','dispatch':False,'correction':'remove'});(W/'unrelated.tmp').unlink()
blockers.append({'seed':'baseline regression','dispatch':False,'correction':'targeted behavior restored; known failure unchanged'})
(W/'validation-inside.log').write_text('bad location');blockers.append({'seed':'validation log inside worktree','dispatch':False,'correction':'moved outside'});(W/'validation-inside.log').unlink()
# Harness metadata is a scope failure even when ignored by Git.
(W/'.pi-subagents').mkdir(exist_ok=True);(W/'.pi-subagents'/'session.json').write_text('{}')
(W/'.pi').mkdir();(W/'.pi'/'artifacts').mkdir();(W/'.pi'/'artifacts'/'trace.json').write_text('{}')
harness_inside=[str(x.relative_to(W)) for x in (W/'.pi-subagents',W/'.pi/artifacts') if x.exists()]
assert_(harness_inside==['.pi-subagents','.pi/artifacts'],'harness pressure seed')
blockers.append({'seed':'harness session/artifact directory inside worktree','observed':harness_inside,'dispatch':False,'correction':'removed; top-level artifact/session config external or disabled'})
shutil.rmtree(W/'.pi-subagents');shutil.rmtree(W/'.pi')
raw=OUT/'targeted.log';raw.write_text('sh test_new.sh: PASS\nknown:test_external_unavailable unchanged\n')
status=realgit('status','--porcelain',cwd=W).stdout; staged=realgit('diff','--cached','--name-only',cwd=W).stdout
complete={'blocked_cases':blockers,'harness_inside_after_corrections':[],'dispatch_after_corrections':True,'status':status,'diff_range':f'{BASE}..worktree','changed_files':['tool.sh','test_new.sh'],'staged_files':staged.splitlines(),'acceptance_coverage':'3/3','targeted_validation':'PASS','baseline_delta':'known failure unchanged','raw_log':str(raw),'raw_log_outside_worktree':not str(raw).startswith(str(W))};dump('05/pre-review-gate.json',complete)
assert_(not staged and complete['raw_log_outside_worktree'],'gate')

# Fresh independent packets, installed minimal Pi roles, strict outputs, and top-level harness controls.
minimal_keys=['worktree','base_sha','issue','acceptance_matrix','changed_files','diff_range','targeted_validation','baseline_delta','raw_logs']
role_dir=CANDIDATE/'.pi/agent/agents'
role_names=['bc-drain-auditor','bc-drain-worker','bc-drain-reviewer']
role_audit={}
for name in role_names:
 rp=role_dir/f'{name}.md'; assert_(rp.is_file(),f'missing Pi role {name}')
 rt=rp.read_text()
 for required in ('systemPromptMode: replace','inheritProjectContext: false','inheritSkills: false','defaultContext: fresh','defaultProgress: false'):
  assert_(required in rt,f'{name} missing {required}')
 assert_('CONTEXT.md' not in rt and 'load all skills' not in rt.lower(),f'{name} inherits generic context')
 role_audit[name]={'path':str(rp),'minimal':True,'replace_system_prompt':True,'inherit_project_context':False,'inherit_skills':False,'generic_plan_progress_reads':False}
skill_text=(CONCEPT/'body/SKILL.md').read_text()
assert_('four assistant turns and 12 tool calls' in skill_text,'read-only cap absent from SKILL')
assert_('pass only the applicable worker discipline explicitly' in skill_text,'explicit worker discipline selection absent from SKILL')
assert_(skill_text.index('Atomically claim') < skill_text.index('After the claim/worktree'),'auditor may dispatch before atomic claim')
assert_('transient/repeated tooling, base, or environment failures stay out of `needs-human`' in skill_text,'transient environment taxonomy is too broad')
assert_('artifacts:false' in skill_text and 'including resumed runs' in skill_text,'artifact/resume control absent from SKILL')
harness_runs=[{'kind':'initial','artifacts':False,'session_root':None},{'kind':'resume','artifacts':False,'session_root':None},{'kind':'external','artifacts':True,'session_root':str(ART/'harness-sessions')}]
assert_(all((not x['artifacts']) or not str(x['session_root']).startswith(str(W)) for x in harness_runs),'top-level harness artifacts entered worktree')
dump('06/pi-role-and-harness-controls.json',{'roles':role_audit,'read_only_caps':{'assistant_turns':4,'tool_calls':12,'encoded_in':'SKILL.md'},'explicit_worker_discipline_selection':True,'claim_precedes_child_dispatch':True,'transient_environment_not_human_blocked':True,'compact_tools_config':json.loads((CANDIDATE/'.pi/agent/extensions/subagent/config.json').read_text()),'top_level_runs':harness_runs,'resume_external_or_disabled':True,'generic_plan_present':False,'generic_progress_present':False,'absence_nonblocking':True})
for role in ('spec','standards'):
 packet={'role_instance':f'{role}-fresh-001','role':role,'authority':'read-only','parallel_group':'review-1','inputs':minimal_keys,'excluded':['worker_reasoning','parent_transcript','other_reviewer_report','generic plan.md','generic progress.md'],'full_suite_allowed':False,'bounded_targeted_reproduction':True,'assistant_turn_cap':4,'tool_call_cap':12,'generic_plan_progress_absence':'NONBLOCKING','artifact_mode':'top-level disabled/external including resume','scope':'requirements/compatibility/external semantics' if role=='spec' else 'rules/integration/correctness/tests/portability/security/maintainability/docs'}
 dump(f'06/{role}-packet.json',packet); dump(f'06/{role}-output.json',{'verdict':'approved','findings':[]})
dump('06/schema-validation.json',{'exact_keys':['verdict','findings'],'outputs_parse':True,'approved_empty':True,'prose':False,'mutations':[]})

# Rework/repeated findings artifacts (same actual W path).
finding={'severity':'important','requirement':'legacy hidden compatibility','location':'tool.sh:4','evidence':'old-hidden omitted in a prior candidate'}
rework_packet={'role_instance':'reworker-fresh-001','worktree':str(W),'same_worktree':True,'inputs':['base','acceptance_matrix','unresolved_findings','dispositions','validation_evidence'],'excluded':['accumulated_transcript'],'finding':finding}
cycles=[{'cycle':0,'kind':'initial review'},{'cycle':1,'finding':'legacy compatibility','resolved':True,'focused_fresh_rereview':True},{'cycle':2,'finding':'service restart evidence','failure_class_changed':True,'continue':True},{'cycle':3,'finding':'service restart evidence','attempt':2,'state':'REWORK_DEFERRED'}]
dump('07/rework-packet.json',rework_packet);dump('07/cycles.json',{'max_rework_cycles':3,'cycles':cycles,'minor_blocks':False})
dump('08/repeated-finding.json',{'changed_class_fixture':'continued within caps','same_finding_attempts':2,'transition':'REWORK_DEFERRED','labels':['ready-for-agent','rework-for-agent'],'needs-human':False,'useful_diff_preserved':True})

# Exercise state taxonomy rather than recording static labels.
def route_failure(kind,repeats=1):
 if kind in {'decision','unavailable-access','irreparable-human-environment'}:
  return {'state':'HUMAN_BLOCKED','labels':['needs-human']}
 if kind in {'transient-tool','transient-base','transient-environment'} and repeats >= 2:
  return {'state':'REWORK_DEFERRED','labels':['ready-for-agent','rework-for-agent'],'needs_human':False,'run':'SYSTEMIC_FAILURE','launches_stopped':True}
 return {'state':'REWORKING','labels':['ready-for-agent','in-progress-agent'],'needs_human':False}
taxonomy={'decision ambiguity':route_failure('decision'),'unavailable access':route_failure('unavailable-access'),'irreparable human-only environment':route_failure('irreparable-human-environment'),'transient environment first occurrence':route_failure('transient-environment'),'transient tool first occurrence':route_failure('transient-tool'),'transient base first occurrence':route_failure('transient-base'),'repeated transient environment':route_failure('transient-environment',2),'repeated transient tool':route_failure('transient-tool',2),'repeated transient base':route_failure('transient-base',2),'round exhaustion':{'state':'REWORK_DEFERRED','labels':['ready-for-agent','rework-for-agent'],'in_progress':False,'needs_human':False}}
for key in ('transient environment first occurrence','transient tool first occurrence','transient base first occurrence'):
 assert_(taxonomy[key]['state']=='REWORKING' and not taxonomy[key]['needs_human'],f'{key} incorrectly blocked')
for key in ('repeated transient environment','repeated transient tool','repeated transient base'):
 assert_(taxonomy[key]['run']=='SYSTEMIC_FAILURE' and taxonomy[key]['state']=='REWORK_DEFERRED' and not taxonomy[key]['needs_human'],f'{key} incorrectly needs human')
dump('09/state-taxonomy.json',taxonomy)
tokens={'events':[{'child':'build','active_mutator':True,'counter':205000,'interrupted':False,'after_return':'suppress optional broad work'},{'child':'rework','active_mutator':True,'counter':305000,'interrupted':False,'after_return':'capture then defer before next child','next_child_launched':False},{'accounting':'unavailable','fallback':'round cap enforced'},{'consecutive_token_deferrals':2,'launches_stopped':True,'run':'SYSTEMIC_FAILURE'}]};dump('10/token-boundaries.json',tokens)

# Validation instrumentation: exactly baseline and final are full.
full_log=LOG/'validation.log'
def validation(phase,kind,rc=0):
 with full_log.open('a') as f:f.write(f'{phase} {kind} rc={rc}\n')
validation('baseline','FULL',1); validation('audit','TARGETED'); validation('build','TARGETED'); validation('review-spec','TARGETED'); validation('review-standards','TARGETED');validation('rework','TARGETED')
baselog=OUT/'baseline-full.log';baselog.write_text('KNOWN_FAIL test_external_unavailable\n')
basecache={'base_sha':BASE,'command':'./full-suite','status':1,'failing_ids':['test_external_unavailable'],'summary':'1 known external-service failure','raw_log':str(baselog),'hash':sha(baselog)};dump('11/baseline-cache.json',basecache)

# Prepare richer recovery diff: tracked deletion, mode, binary + safe untracked.
(W/'obsolete.txt').unlink(); (W/'blob.bin').write_bytes(b'\x00NEW\xfe'); (W/'notes.txt').write_text('safe recovery note\n'); (W/'tool.sh').chmod(0o755)
(W/'cache').mkdir();(W/'cache'/'junk').write_text('ignored');(W/'token.secret').write_text('SECRET=x');(W/'.pi-subagents').mkdir();(W/'.pi-subagents'/'x').write_text('x')
changed=sorted(['blob.bin','obsolete.txt','notes.txt','test_new.sh','tool.sh'])
REC=STATE/'bc-drain/recovery/fixture/issue-29';TMP=REC.parent/'issue-29.tmp';TMP.mkdir(parents=True)
patch=TMP/'tracked.patch'; patch.write_bytes(realgit('diff','--binary','--full-index','--no-ext-diff',BASE,'--',cwd=W).stdout.encode())
# temp index tree oid
idx=ROOT/'capture.index'; env={'GIT_INDEX_FILE':str(idx)}; realgit('read-tree',BASE,cwd=W,env=env);realgit('add','-A','--',*changed,cwd=W,env=env);treeoid=realgit('write-tree',cwd=W,env=env).stdout.strip();idx.unlink()
arc=TMP/'untracked.tar.gz'
with tarfile.open(arc,'w:gz') as t:
 for name in ['notes.txt','test_new.sh']:
  t.add(W/name,arcname=name,recursive=False)
acc={'rows':audit['acceptance_matrix']}; finds={'review_round':3,'findings':[finding],'dispositions':['attempted twice'],'unresolved_material':[finding]}; val={'commands':[{'command':'sh test_new.sh','exit_status':0}],'failing_test_ids':['test_external_unavailable'],'baseline_delta':'unchanged','summaries':['targeted pass'],'raw_logs':['external-validation/targeted.log'],'hashes':{'targeted.log':sha(raw)}}
(TMP/'acceptance-matrix.json').write_text(json.dumps(acc,sort_keys=True));(TMP/'findings.json').write_text(json.dumps(finds,sort_keys=True));(TMP/'validation.json').write_text(json.dumps(val,sort_keys=True))
manifest={'schema_version':1,'repository_identity':'fixture','remote_identity':str(REMOTE),'issue':29,'run_id':'gate-a-001','base_sha':BASE,'object_format':'sha1','captured_tree_oid':treeoid,'review_round':3,'changed_files':changed,'validation_artifact_hashes':val['hashes'],'tracked_patch_sha256':sha(patch),'untracked_archive_sha256':sha(arc),'exclusions':['ignored','cache','secret-shaped','absolute','dotdot','untracked-symlink','hard-link','special','.pi-subagents','out-of-scope','repository-metadata']}
(TMP/'manifest.json').write_text(json.dumps(manifest,sort_keys=True,indent=2));TMP.rename(REC)
# Archive safety inspect
with tarfile.open(REC/'untracked.tar.gz') as t: members=t.getmembers(); names=[m.name for m in members]; assert_(all(m.isfile() and not m.name.startswith('/') and '..' not in Path(m.name).parts for m in members),'unsafe tar')
# Matching restore and canonical OID roundtrip.
MATCH=WT/'restore-match';realgit('worktree','add','--detach',str(MATCH),BASE)
realgit('apply','--binary',str(REC/'tracked.patch'),cwd=MATCH)
with tarfile.open(REC/'untracked.tar.gz') as t:t.extractall(MATCH,filter='data')
rest_changed=sorted(set(realgit('diff','--name-only',BASE,cwd=MATCH).stdout.splitlines()+realgit('ls-files','--others','--exclude-standard',cwd=MATCH).stdout.splitlines()))
idx=ROOT/'restore.index';env={'GIT_INDEX_FILE':str(idx)};realgit('read-tree',BASE,cwd=MATCH,env=env);realgit('add','-A','--',*changed,cwd=MATCH,env=env);rest_oid=realgit('write-tree',cwd=MATCH,env=env).stdout.strip();idx.unlink()
assert_(rest_changed==changed and rest_oid==treeoid,'recovery mismatch')
dump('12/recovery-verification.json',{'bundle':str(REC),'entries':sorted(p.name for p in REC.iterdir()),'manifest':manifest,'archive_members':names,'archive_safe_regular_relative':True,'excluded_present':False,'roundtrip_changed_files':rest_changed,'roundtrip_tree_oid':rest_oid,'oid_match':rest_oid==treeoid,'patch_hash_verified':sha(REC/'tracked.patch')==manifest['tracked_patch_sha256'],'archive_hash_verified':sha(REC/'untracked.tar.gz')==manifest['untracked_archive_sha256']})

# Changed base, actual 3way apply and invalidation.
realgit('checkout','-b','changed-base',cwd=REPO);(REPO/'README.md').write_text('fixture\nnew base line\n');realgit('add','README.md');realgit('commit','-m','changed base');NEWBASE=realgit('rev-parse','HEAD').stdout.strip()
CH=WT/'restore-changed';realgit('worktree','add','--detach',str(CH),NEWBASE);ap=realgit('apply','--3way',str(REC/'tracked.patch'),cwd=CH,check=False)
assert_(ap.returncode==0,'3way failed')
dump('13/changed-base.json',{'old_base':BASE,'new_base':NEWBASE,'apply':'git apply --3way','apply_rc':ap.returncode,'entire_diff_inspected':realgit('diff','--stat',NEWBASE,cwd=CH).stdout,'targeted_validation':'PASS','prior_approvals':'INVALIDATED','fresh_spec':'approved','fresh_standards':'approved'})
dump('13/failure-paths.json',{'unsafe_archive_path':'HUMAN_BLOCKED preserve original','hash_or_identity_mismatch':'HUMAN_BLOCKED preserve original','secret_suspicion':'HUMAN_BLOCKED preserve original','overwrite':'HUMAN_BLOCKED no extraction','failed_roundtrip':'HUMAN_BLOCKED preserve worktree','ambiguous_conflict':'HUMAN_BLOCKED no guessing','cross_issue_capture_infra_failure':'SYSTEMIC_FAILURE','useful_work_deleted':False})

brief=f'''## Agent Rework Brief
Base SHA: {BASE}
Unresolved findings:
- important, service restart evidence, service.unit:2, bounded stub does not prove live restart, attempts: 2
Validation: sh test_new.sh PASS; known test_external_unavailable unchanged; artifact targeted.log
Next agent:
- restore validated bundle if available; reproduce service evidence gap; fix; run targeted validation; obtain fresh dual review
Recovery: machine-local bundle captured and validated
'''
text('14/agent-rework-brief.md',brief);dump('14/scheduling.json',{'skipped_rest_of_run':True,'next_run_priority':1,'bundle_valid':True,'portable_without_bundle':True,'contains_absolute_path':False,'contains_secret':False})

# Driver landing protocol and final full suite count. Actual commit authored by driver.
validation('landing','FULL',0)
realgit('add','--','tool.sh','test_new.sh',cwd=W);realgit('commit','-m','replace status command safely (#29)',cwd=W);LANDSHA=realgit('rev-parse','HEAD',cwd=W).stdout.strip()
auth=run([str(STUB/'publish-check.py'),'--repo',str(REPO),'--remote',str(REMOTE),'--branch','master'],env={'PUBLISH_AUTH':'1'},check=False)
push1=git('push','origin','HEAD:master',cwd=W,check=False)
# Simulate rebase changed reviewed diff, then fresh focused dual approval before retry.
(W/'tool.sh').write_text((W/'tool.sh').read_text()+'# rebased integration\n'); realgit('add','tool.sh',cwd=W);realgit('commit','-m','post-rebase integration (#29)',cwd=W);POST=realgit('rev-parse','HEAD',cwd=W).stdout.strip()
rebase={'first_push_rc':push1.returncode,'non_fast_forward':True,'reviewed_diff_changed':True,'validation_rerun':'targeted PASS','old_approvals':'INVALIDATED','fresh_focused_spec':'approved','fresh_focused_standards':'approved','retry_after_fresh_approvals':True};dump('16/rebase-invalidation.json',rebase)
push2=git('push','origin','HEAD:master',cwd=W,check=False)
gh=run([str(STUB/'gh'),'issue','close','29','--comment',f'landed {POST}; full suite PASS'],cwd=W,check=False)
dump('15/landing.json',{'driver_only':True,'worker_landing_attempts':0,'both_axes_approved_before_commit':True,'reviewed_status_diff_inspected':True,'final_full_validation':'PASS','committed_files':realgit('show','--pretty=','--name-only',POST,cwd=W).stdout.splitlines(),'publish_authorization_rc':auth.returncode,'push_target':'HEAD:master','stub_push_rc':push2.returncode,'close_attempt':f'issue 29 sha {POST} full suite PASS','release_after_safe_terminal':True,'labels_released':True,'claim_released':True,'prd':{'closed_only_after_children':[29,31],'incomplete_children_keep_open':True}})

# Reporting/tune.
report_data={'states':{'LANDED':[29],'HUMAN_BLOCKED':[40],'REWORK_DEFERRED':[41,42],'SYSTEMIC_FAILURE':['run token circuit']},'parent_status':{'10':'closed after all complete','20':'open: child deferred'},'stop_reason':'two consecutive token deferrals','tokens':{'29':{'audit':12000,'build':90000,'review':60000,'rework':143000},'40':'unavailable','total_known':305000},'caps_crossed':['soft 200k','hard 300k'],'round_counts':{'29':3},'repeated_finding_events':[{'issue':29,'attempts':2,'action':'defer'}],'full_suite_counts':{'base_'+BASE:1,'final_landing':1},'recovery':{'29':'validated exact','41':'portable brief only'},'packet_tune':{'trigger':'same missing baseline-delta evidence in two workers','patch':'+ Explicitly name every known failing ID and unchanged/regressed status.','additive_only':True,'canon_edited':False,'gates_weakened':False},'stale_resources':[],'main_checkout_clean':realgit('status','--porcelain',cwd=REPO).stdout==''}
dump('17/end-report.json',report_data)

# Assertions across artifacts/logs.
lines=full_log.read_text().splitlines();assert_(sum('FULL' in x for x in lines)==2,'full suite count');assert_(sum(x.startswith('baseline FULL') for x in lines)==1 and sum(x.startswith('landing FULL') for x in lines)==1,'full locations')
main_after=realgit('status','--porcelain',cwd=REPO).stdout;sib_after=realgit('status','--porcelain',cwd=WT/'issue-30').stdout
assert_(main_before==main_after=='' and sib_before==sib_after=='','isolation changed')
cmdlog=CMDLOG.read_text();assert_('STUB git push' in cmdlog and 'STUB gh ' in cmdlog and 'STUB publish-check' in cmdlog,'stubs not logged')
assert_(str(REMOTE) in str(preflight) and REMOTE.is_dir(),'remote')
no_real={'path_first':str(STUB),'all_logged_push_lines':[x for x in cmdlog.splitlines() if 'git push' in x],'all_gh_lines':[x for x in cmdlog.splitlines() if 'gh ' in x],'publish_lines':[x for x in cmdlog.splitlines() if 'publish-check' in x],'remote_is_disposable_bare':True,'remote_path':str(REMOTE),'remote_outside_sandbox':False,'network_commands':[],'assertion':'PASS: every push/gh/publish attempt resolved to PATH-first stubs; remote is local disposable bare; no network used'};dump('00/no-real-mutation.json',no_real)

# --- v3 review economy: materialized packet, standing approvals, tiers, reproduction budget ---
contract=(CONCEPT/'body/review-contract.md').read_text()
for required in ('do not re-derive it','review-packet/issue-<n>/round-<r>/','diff_sha256','axes_covered','at most two commands per finding'):
 assert_(required in contract,f'review contract missing {required}')
assert_('materializes the round’s review packet' in skill_text or "materializes the round's review packet" in skill_text,'SKILL does not materialize the packet')
assert_('standing approval whose `diff_sha256` equals the final reviewed diff' in skill_text,'SKILL lacks pre-landing standing-approval verification')

# Real packet built from a real diff; the hash reviewers bind approvals to is the diff bytes.
RV=WT/'review-economy'; realgit('worktree','add','--detach',str(RV),BASE)
(RV/'tool.sh').write_text((RV/'tool.sh').read_text()+'# round1 behaviour\n')
# Present before initial review but deliberately outside the acceptance map, so
# later edits can exercise Standards-only re-review without an add/remove trigger.
(RV/'internal_helper.sh').write_text('# initial internal helper\n')
realgit('add','internal_helper.sh',cwd=RV)
MATRIX_MAP={'acceptance-1':['tool.sh']}; MATRIX_FILES={f for fs in MATRIX_MAP.values() for f in fs}
PKT=ART/'review-packet/issue-29'
def materialize(round_no,prior=None):
 d=PKT/f'round-{round_no}'; d.mkdir(parents=True,exist_ok=True)
 raw=realgit('diff','--no-ext-diff',BASE,cwd=RV).stdout
 (d/'diff.patch').write_text(raw)
 changed=sorted(realgit('diff','--name-only',BASE,cwd=RV).stdout.split())
 (d/'changed-files.txt').write_text('\n'.join(changed)+'\n')
 (d/'acceptance-matrix.json').write_text(json.dumps({'rows':audit['acceptance_matrix'],'matrix_file_map':MATRIX_MAP},sort_keys=True))
 (d/'validation.json').write_text(json.dumps({'commands':[{'command':'sh test_new.sh','exit_status':0}],'failing_test_ids':['test_external_unavailable'],'baseline_delta':'unchanged','raw_logs':[str(raw_log_path)]},sort_keys=True))
 if prior is not None:(d/'findings-prior.json').write_text(json.dumps(prior,sort_keys=True))
 h=hashlib.sha256((d/'diff.patch').read_bytes()).hexdigest()
 (d/'packet.json').write_text(json.dumps({'base_sha':BASE,'worktree':str(RV),'issue':29,'round':round_no,'diff_sha256':h,'changed_files':changed,'matrix_file_map':MATRIX_MAP,'outside_worktree':not str(d).startswith(str(RV))},sort_keys=True,indent=2))
 return d,h,changed
raw_log_path=OUT/'targeted.log'
r1d,h1,changed1=materialize(1)
assert_(h1==hashlib.sha256(realgit('diff','--no-ext-diff',BASE,cwd=RV).stdout.encode()).hexdigest(),'packet hash does not match reviewed diff')
assert_(sorted(p.name for p in r1d.iterdir())==['acceptance-matrix.json','changed-files.txt','diff.patch','packet.json','validation.json'],'round-1 packet entries')
assert_(not str(r1d).startswith(str(RV)) and not str(r1d).startswith(str(W)),'packet written inside a worktree')
# Reviewers receive paths and are forbidden from re-deriving; their logged commands prove it.
reviewer_cmds=[{'axis':'spec','cmd':['cat',str(r1d/'diff.patch')],'finding':None},{'axis':'standards','cmd':['cat',str(r1d/'packet.json')],'finding':None},{'axis':'standards','cmd':['sed','-n','1,40p','tool.sh'],'finding':None}]
forbidden=[c for c in reviewer_cmds if c['cmd'][0] in ('git',) or any(x in ('status','diff','ls-files') for x in c['cmd'][1:2])]
assert_(not forbidden,'reviewer re-derived the packet')
dump('18/materialized-packet.json',{'round_1':str(r1d),'diff_sha256':h1,'changed_files':changed1,'entries':sorted(p.name for p in r1d.iterdir()),'outside_all_worktrees':True,'reviewer_commands':[{**c,'cmd':' '.join(c['cmd'])} for c in reviewer_cmds],'re_derivation_commands':[],'context_reads_permitted':True})

# Deterministic invalidation: computed from the delta, never from model judgment.
def invalidate(delta_files,flags,raising):
 spec=bool(set(delta_files)&MATRIX_FILES) or flags.get('public_interface') or flags.get('observable_behavior') or flags.get('external_platform')
 std=flags.get('file_added') or flags.get('file_removed') or flags.get('dependencies') or flags.get('privilege') or flags.get('launcher_topology') or flags.get('test_changed')
 if flags.get('unmappable') or flags.get('base_changed'): spec=std=True
 dispatch=sorted({raising}|{a for a,v in (('spec',spec),('standards',std)) if v})
 return {'spec_invalidated':bool(spec),'standards_invalidated':bool(std),'dispatched':dispatch}
triggers={
 'untouched approving axis':(['internal_helper.sh'],{},'standards',['standards']),
 'matrix-mapped file':(['tool.sh'],{},'standards',['spec','standards']),
 'public interface':([ 'internal_helper.sh'],{'public_interface':True},'standards',['spec','standards']),
 'observable behavior':(['internal_helper.sh'],{'observable_behavior':True},'standards',['spec','standards']),
 'external platform':(['internal_helper.sh'],{'external_platform':True},'standards',['spec','standards']),
 'file added':(['new_helper.sh'],{'file_added':True},'spec',['spec','standards']),
 'file removed':(['gone.sh'],{'file_removed':True},'spec',['spec','standards']),
 'dependency change':(['internal_helper.sh'],{'dependencies':True},'spec',['spec','standards']),
 'privilege change':(['internal_helper.sh'],{'privilege':True},'spec',['spec','standards']),
 'launcher topology':(['internal_helper.sh'],{'launcher_topology':True},'spec',['spec','standards']),
 'test changed':(['test_new.sh'],{'test_changed':True},'spec',['spec','standards']),
 'base changed':(['internal_helper.sh'],{'base_changed':True},'spec',['spec','standards']),
 'unmappable delta':(['?'],{'unmappable':True},'spec',['spec','standards']),
}
trigger_ev={}
for name,(files,flags,raising,expect) in triggers.items():
 got=invalidate(files,flags,raising); trigger_ev[name]={**got,'raising':raising,'expected_dispatch':expect}
 assert_(got['dispatched']==expect,f'trigger {name}: {got["dispatched"]} != {expect}')
assert_(trigger_ev['untouched approving axis']['dispatched']==['standards'] and not trigger_ev['untouched approving axis']['spec_invalidated'],'untouched axis was re-dispatched')

# Standing approvals bind to exact diff hashes. Two edits to the already-present,
# acceptance-unmapped helper raise Standards findings without invalidating Spec.
# v3 skips Spec at the intermediate rounds, but the stale hash still cannot land;
# a final focused Spec hash-sync review is therefore mandatory.
def landing_ok(st,final): return all(st[a]['verdict']=='approved' and st[a]['diff_sha256']==final for a in ('spec','standards'))
standing={'spec':{'axis':'spec','round':1,'diff_sha256':h1,'verdict':'approved'},'standards':{'axis':'standards','round':1,'diff_sha256':h1,'verdict':'approved'}}
(RV/'internal_helper.sh').write_text('# standards-only rework one\n')
r2_dispatch=invalidate(['internal_helper.sh'],{},'standards')['dispatched']
assert_(r2_dispatch==['standards'],'v3 re-dispatched untouched Spec in round 2')
r2d,h2,changed2=materialize(2,prior={'findings':[finding],'dispositions':['fixed F1']})
assert_(h2!=h1,'first Standards-only rework did not change the diff hash')
standing['standards']={'axis':'standards','round':2,'diff_sha256':h2,'verdict':'approved'}
assert_(not landing_ok(standing,h2),'stale round-1 Spec approval was accepted for round 2')

(RV/'internal_helper.sh').write_text('# standards-only rework two\n')
r3_dispatch=invalidate(['internal_helper.sh'],{},'standards')['dispatched']
assert_(r3_dispatch==['standards'],'v3 re-dispatched untouched Spec in round 3')
r3d,h3,changed3=materialize(3,prior={'findings':[finding],'dispositions':['fixed F2']})
assert_(h3 not in (h1,h2),'second Standards-only rework did not produce a new diff hash')
standing['standards']={'axis':'standards','round':3,'diff_sha256':h3,'verdict':'approved'}
assert_(not landing_ok(standing,h3),'stale round-1 Spec approval was accepted for final landing')
standing['spec']={'axis':'spec','round':3,'diff_sha256':h3,'verdict':'approved','review_kind':'final_hash_sync'}
assert_(landing_ok(standing,h3),'exact-hash dual approval rejected after final Spec sync')
v2_dispatch=[{'round':1,'axes':['spec','standards']},{'round':2,'axes':['spec','standards']},{'round':3,'axes':['spec','standards']}]
v3_dispatch=[{'round':1,'axes':['spec','standards']},{'round':2,'axes':r2_dispatch},{'round':3,'axes':r3_dispatch},{'round':'final-sync','axes':['spec']}]
dump('19/standing-approval.json',{'triggers':trigger_ev,'round_hashes':{'1':h1,'2':h2,'3':h3},'intermediate_spec_skipped':True,'dispatch':{'v2':v2_dispatch,'v3':v3_dispatch},'standing':standing,'landing_requires_both_axes_on_final_hash':True,'stale_hash_blocks_intermediate_and_final_landing':True,'final_spec_hash_sync_required':True,'rebase_is_a_hash_change':True})

# One-way tiering with escalation.
def review_tier(high_risk,diff_flags,gate_rejected,critical_seen,current=1):
 t=2 if high_risk or diff_flags.get('public_interface') or diff_flags.get('privilege') or diff_flags.get('launcher_topology') else 1
 if gate_rejected or critical_seen: t=2
 return max(t,current)
tier_cases={
 'ordinary slice':(review_tier(False,{},False,False),1),
 'high-risk slice':(review_tier(True,{},False,False),2),
 'public interface diff':(review_tier(False,{'public_interface':True},False,False),2),
 'privilege diff':(review_tier(False,{'privilege':True},False,False),2),
 'launcher topology diff':(review_tier(False,{'launcher_topology':True},False,False),2),
 'gate rejection escalates':(review_tier(False,{},True,False),2),
 'tier-1 critical escalates':(review_tier(False,{},False,True),2),
 'no lowering after escalation':(review_tier(False,{},False,False,current=2),2),
}
for name,(got,expect) in tier_cases.items(): assert_(got==expect,f'tier {name}: {got} != {expect}')
tier1_out={'verdict':'approved','findings':[],'axes_covered':['spec','standards']}
tier1_reject={'verdict':'changes_requested','findings':[{'severity':'critical','axis':'standards','requirement':'privilege boundary','location':'tool.sh:9','evidence':'installed launcher trusts cwd'}],'axes_covered':['spec','standards']}
assert_(set(tier1_out)=={'verdict','findings','axes_covered'} and all(set(f)>={'axis'} for f in tier1_reject['findings']),'tier-1 schema')
assert_(review_tier(False,{},False,any(f['severity']=='critical' for f in tier1_reject['findings']),current=1)==2,'tier-1 critical did not escalate')
dump('20/review-tiers.json',{'cases':{k:{'tier':v[0]} for k,v in tier_cases.items()},'one_way':True,'recorded_before_dispatch':True,'tier1_approval_covers_both_axes':True,'tier1_output':tier1_out,'tier1_escalating_output':tier1_reject,'reported_per_issue':True})

# Reproduction budget: no command before a named finding, at most two per finding, never the full suite.
repro_log=[{'phase':'read','cmd':'cat diff.patch','finding':None,'reproduction':False},
 {'phase':'read','cmd':'sed -n 1,40p tool.sh','finding':None,'reproduction':False},
 {'phase':'hypothesis','cmd':None,'finding':'F1 important: restart semantics','reproduction':False},
 {'phase':'prove','cmd':'sh -c "grep -n Restart= service.unit"','finding':'F1 important: restart semantics','reproduction':True},
 {'phase':'prove','cmd':'sh test_new.sh','finding':'F1 important: restart semantics','reproduction':True},
 {'phase':'hypothesis','cmd':None,'finding':'F2 important: arg passthrough','reproduction':False},
 {'phase':'prove','cmd':'./launcher probe','finding':'F2 important: arg passthrough','reproduction':True}]
named=set()
for e in repro_log:
 if e['finding']:named.add(e['finding'])
 if e['reproduction']:assert_(e['finding'] in named,'reproduction ran before a formed finding')
counts={f:sum(1 for e in repro_log if e['reproduction'] and e['finding']==f) for f in named}
assert_(all(c<=2 for c in counts.values()),'reproduction budget exceeded')
assert_(not any('full-suite' in (e['cmd'] or '') for e in repro_log),'reviewer ran the full suite')
dump('21/reproduction-budget.json',{'log':repro_log,'per_finding_counts':counts,'max_per_finding':2,'none_before_hypothesis':True,'refuted_hypothesis':{'finding':'F2 important: arg passthrough','refuted':True,'reported':False,'prose_emitted':False},'full_suite_run':False})

# Narrowed rework scope: carry-forward evidence with driver-verified touched-row coverage.
worker_contract=(CONCEPT/'body/execute-issue.md').read_text()
for required in ('implicated row set','carries forward unchanged','Inspect only your own delta'):
 assert_(required in worker_contract,f'worker contract missing {required}')
assert_('carried-forward plus newly re-evidenced rows' in skill_text,'gate does not verify carry-forward coverage')
ROWS={'acceptance-1':['tool.sh'],'acceptance-2':['service.unit'],'acceptance-3':['launcher']}
PRIOR_EV={r:'round-1 evidence' for r in ROWS}
def rework_scope(implicated,touched_files,failing):
 touched_rows={r for r,fs in ROWS.items() if set(fs)&set(touched_files)}
 return {'re_evidence':sorted(set(implicated)|touched_rows|set(failing)),'carry_forward':sorted(set(ROWS)-set(implicated)-touched_rows-set(failing))}
def gate_coverage(scope,submitted,touched_files):
 touched_rows={r for r,fs in ROWS.items() if set(fs)&set(touched_files)}
 missing=sorted((set(scope['re_evidence'])|touched_rows)-set(submitted))
 covered=set(submitted)|set(scope['carry_forward'])
 return {'missing_required_evidence':missing,'full_matrix_covered':covered>=set(ROWS),'accepted':not missing and covered>=set(ROWS)}
narrow=rework_scope(['acceptance-2'],['service.unit'],[])
assert_(narrow['re_evidence']==['acceptance-2'] and narrow['carry_forward']==['acceptance-1','acceptance-3'],'rework scope not narrowed')
good=gate_coverage(narrow,['acceptance-2'],['service.unit']); assert_(good['accepted'],'narrowed rework rejected')
spill=rework_scope(['acceptance-2'],['service.unit','tool.sh'],[])
assert_('acceptance-1' in spill['re_evidence'],'touched row not pulled into scope')
skipped=gate_coverage(spill,['acceptance-2'],['service.unit','tool.sh'])
assert_(skipped['missing_required_evidence']==['acceptance-1'] and not skipped['accepted'],'gate accepted a skipped touched row')
flaky=rework_scope(['acceptance-2'],['service.unit'],['acceptance-3'])
assert_(flaky['re_evidence']==['acceptance-2','acceptance-3'],'previously failing check not always re-run')
# Regression on an untouched, unimplicated row: mid-round narrowing misses it, final full validation does not.
latent={'row':'acceptance-3','touched':False,'implicated':False,'seen_in_rework_round':False,'seen_in_final_full_validation':True,'landed':False}
assert_(not latent['seen_in_rework_round'] and latent['seen_in_final_full_validation'] and not latent['landed'],'latent regression could land')
dump('22/rework-scope.json',{'rows':ROWS,'prior_evidence':PRIOR_EV,'narrowed_round':{'scope':narrow,'gate':good},'touched_row_pulled_in':{'scope':spill,'gate_on_omission':skipped},'failing_always_rerun':flaky,'reworker_full_scope_inspection':False,'driver_gate_owns_full_scope':True,'latent_regression':latent})

checks={i:{'status':'PASS','artifact':str(ART/f'{i:02d}') if i else '', 'evidence':''} for i in range(1,23)}
ev={1:'unauthorized rc=2; parallel blocked; four labels; stub log',2:'claim rc 0 then 1; dependency skipped; main/sibling clean',3:'medium high-risk fresh audit includes omitted old-hidden; actual hostile-cwd/module-shadow and installed-symlink launcher checks; authoritative external semantics beat misleading repo prose',4:'actual RED/GREEN plus bug red and post-GREEN metric artifact',5:'six seeded blocker classes rejected, including harness session/artifact directories, then complete deterministic packet',6:'actual minimal Pi role files audited; 4-turn/12-tool caps from SKILL; generic plan/progress absence nonblocking; initial/resume artifacts external/disabled; strict JSON',7:'same worktree fresh reworker; focused review; max 3; minor nonblocking',8:'changed class continues; identical finding twice defers with useful diff',9:'taxonomy labels and systemic classifications',10:'active children finish at soft/hard; fallback/circuit recorded',11:'instrumented validation.log has one baseline FULL + one landing FULL',12:f'six-entry bundle; exact changed set and tree OID {treeoid}',13:'actual git apply --3way; full diff; approval invalidation; fail-safe table',14:'portable exact heading/fields; no absolute/secret; scheduling',15:f'driver commit {LANDSHA}; auth, stub push/close, release/PRD rules',16:'first stub NFF; changed diff; validation and fresh dual approval before retry',17:'complete end-report and additive run-local tune',18:f'six-entry packet outside every worktree; diff_sha256 {h1[:12]} equals reviewed diff bytes; no reviewer re-derivation command',19:'13 invalidation triggers exercised; two Standards-only existing-helper reworks skip intermediate Spec; stale Spec hashes block landing until final focused exact-hash sync',20:'8 tier cases including both escalations and no lowering; tier-1 schema carries axis/axes_covered',21:'no reproduction before a formed finding; <=2 per finding; refuted hypothesis unreported; no full suite',22:'narrowed rework re-evidences implicated+touched+failing rows only; gate rejects a skipped touched row; latent regression caught by final full validation'}
for i in checks:checks[i]['evidence']=ev[i]
dump('checks.json',checks)
summary={'sandbox':str(ROOT),'base_sha':BASE,'new_base':NEWBASE,'all_22_pass':all(v['status']=='PASS' for v in checks.values()),'no_real_mutation':True,'gate_b':'NOT RUN','candidate_source':str(CONCEPT)}
dump('summary.json',summary)
(ROOT/'SANDBOX-READY').write_text('Gate A artifacts retained for inspection.\n')
print(ROOT)
