# Current agent-wiki reality

> Verbatim copy of the scout artifact, with one disclosed change: two paths in
> sections C and F that were written relative to the codebase-design vault (its
> concepts/plus-operator-coercion.md and concepts/README.md) were qualified with
> their vault root. They otherwise read as paths in this repository, which is
> ambiguous to a reader and a false positive for `scripts/lint.py`. No
> measurement, command, or number was altered.

Measured 2026-08-26. This is a read-only measurement; the only intended write is this artifact. Search used max depth 10 and pruned `node_modules`, `.git`, and `/home/ben/Sync/Work/PUBLIC/Agents/docs/research`.

## A. Inventory

Discovery command actually run:
```sh
find /home/ben/Sync -maxdepth 10 \
  \( -path '/home/ben/Sync/*/node_modules' -o -path '/home/ben/Sync/*/.git' -o -path '/home/ben/Sync/Work/PUBLIC/Agents/docs/research' \) -prune \
  -o \( -type d \( -name '.bc-agent' -o -name '.agent' \) -print -o -type d -path '*/agent/wiki' -print \) 2>/dev/null | sort
```
It found 10 name candidates. Qualification required both `index.md` and `log.md`; `/home/ben/Sync/AI/homeflix/.agent` was excluded because both were missing. Nine qualified:
```text
/home/ben/Sync/Documents/Learning/codebase-design/.bc-agent
/home/ben/Sync/Documents/Learning/sql/.bc-agent
/home/ben/Sync/Music/.bc-agent
/home/ben/Sync/Scripts/.bc-agent
/home/ben/Sync/Work/CV/.bc-agent
/home/ben/Sync/Work/Development/dng/files/pub/agent/wiki
/home/ben/Sync/Work/Development/wp-theme-builds/localhost/image-maze/.bc-agent
/home/ben/Sync/Work/PUBLIC/Homeflix/.agent
/home/ben/Sync/Work/homeflix-prod/.agent
```

Inventory command summed regular-file apparent sizes, counted files by first relative directory, and ran `git log -1 --format=%cs -- .`:
```text
codebase-design/.bc-agent: files 70; Markdown 55; total 115386 B; log 7871 B; index 4293 B; last commit 2026-08-26
  .obsidian 3, root 10, concepts 11, conventions 5, decisions 1, learning 1, learning-records 10, lessons 10, out-of-scope 1, project 1, questions 1, references 6, research 1, scratch 1, sessions 1, sources 1, tasks 3, templates 3
  largest: log.md 7871 B; GLOSSARY.md 5926 B; conventions/planning-workflow.md 5729 B
sql/.bc-agent: files 42; Markdown 37; total 37686 B; log 379 B; index 1105 B; last commit 2026-08-26
  .obsidian 3, root 10, concepts 1, conventions 5, decisions 1, learning 1, learning-records 1, lessons 1, out-of-scope 1, project 1, questions 1, references 6, research 1, scratch 1, sessions 1, sources 1, tasks 3, templates 3
  largest: conventions/planning-workflow.md 5729 B; AGENTS.md 4215 B; learning/plan.md 3703 B
Music/.bc-agent: files 76; Markdown 69; total 192403 B; log 25062 B; index 4572 B; last commit 2026-08-26
  .obsidian 3, root 6, _meta 1, components 7, conventions 6, decisions 9, findings 9, open-questions 5, plans 4, project 4, raw 2, references 8, research 1, scratch 1, tasks 3, templates 6
  largest: log.md 25062 B; plans/music-on-the-go.md 12408 B; project/music-wiki-prd.md 8713 B
Scripts/.bc-agent: files 61; Markdown 54; total 222108 B; log 8146 B; index 5037 B; last commit 2026-08-24
  .obsidian 3, root 5, autoresearch 2, conventions 9, decisions 11, out-of-scope 1, project 12, references 9, research 3, scratch 1, tasks 3, templates 2
  largest: project/wallpaper-rotation-spec.md 22167 B; project/wallpaper-architecture-deepening-prd.md 22004 B; project/animated-wallpaper-rotation-prd.md 16599 B
CV/.bc-agent: files 53; Markdown 42; total 192933 B; log 8733 B; index 1999 B; last commit 2026-08-26
  .obsidian 3, root 6, components 1, conventions 6, decisions 3, findings 9, open-questions 3, out-of-scope 1, plans 1, project 1, references 5, research 5, scratch 1, tasks 3, templates 5
  largest: project/overview.md 9151 B; log.md 8733 B; findings/job-ad-scan-saas.md 7700 B
dng/files/pub/agent/wiki: files 22; Markdown 22; total 36866 B; log 2861 B; index 874 B; last commit 2026-06-08
  root 5, conventions 3, decisions 1, project 4, references 4, tasks 3, templates 2
  largest: references/tags-and-categories.md 10957 B; project/seo-deep-improved-search-2026-plan.md 8001 B; log.md 2861 B
image-maze/.bc-agent: files 2651; Markdown 239; total 60813914 B; log 199069 B; index 18172 B; last commit 2026-08-25
  .obsidian 4, root 5, agents 4, conventions 7, decisions 30, open-questions 1, out-of-scope 1, project 81, raw 1, references 14, research 12, scratch 314, scripts 1, tasks 3, temp 2171, templates 2
  largest: log.md 199069 B; project/architecture-module-map.md 70757 B; project/plans/digital-chest-unlock/referral-unlock-plan.md 46829 B
Homeflix/.agent: files 42; Markdown 42; total 220363 B; log 41822 B; index 6426 B; last commit 2026-08-25
  root 5, conventions 3, decisions 10, project 12, references 6, tasks 3, templates 3
  largest: log.md 41822 B; references/gotchas.md 18871 B; project/agent-first-core-setup-plan.md 18821 B
homeflix-prod/.agent: files 45; Markdown 45; total 307786 B; log 70353 B; index 6985 B; last commit 2026-08-24
  root 5, conventions 3, decisions 11, open-questions 1, project 13, references 6, tasks 3, templates 3
  largest: log.md 70353 B; references/gotchas.md 25889 B; project/agent-first-core-setup-plan.md 18821 B
```

## B. Token cost of traversal

Token estimate is apparent bytes / 4. The three largest vaults are image-maze, homeflix-prod, and Scripts. The “index + 3 pages” proxy is the standard trio `project/overview.md`, `references/commands.md`, `tasks/active.md`, all present in those vaults.

Command/output:
```sh
# stat each top-three vault and the standard trio; compute bytes/4
```
```text
image-maze/.bc-agent: pages 239; whole 60813914 B = 15203478.5 tokens; index 18172 B = 4543; trio 1397+18208+8850=28455 B; index+trio 46627 B = 11656.75; log 199069 B = 49767.25; index-linked unique pages 118 (239 exist)
homeflix-prod/.agent: pages 45; whole 307786 B = 76946.5 tokens; index 6985 B = 1746.25; trio 5164+6777+13509=25450 B; index+trio 32435 B = 8108.75; log 70353 B = 17588.25; index-linked unique pages 41 (45 exist)
Scripts/.bc-agent: pages 54; whole 222108 B = 55527 tokens; index 5037 B = 1259.25; trio 5425+817+1531=7773 B; index+trio 12810 B = 3202.5; log 8146 B = 2036.5; index-linked unique pages 44 (54 exist)
```
Image-maze’s 239 Markdown pages include generated `temp/`/`scratch/`; the graph/qmd view excludes those and sees 155 pages.

Exact byte/token command and output used for B:
```sh
for v in /home/ben/Sync/Work/Development/wp-theme-builds/localhost/image-maze/.bc-agent /home/ben/Sync/Work/homeflix-prod/.agent /home/ben/Sync/Scripts/.bc-agent; do total=$(find "$v" -type f -printf '%s\n' | awk '{s+=$1} END{print s+0}'); idx=$(stat -c%s "$v/index.md"); log=$(stat -c%s "$v/log.md"); md=$(find "$v" -type f -name '*.md' -printf '%p\n' | wc -l); printf '%s total=%s whole_tokens=%s index=%s index_tokens=%s log=%s log_tokens=%s md=%s\n' "$v" "$total" "$(awk -v n="$total" 'BEGIN{printf "%.2f",n/4}')" "$idx" "$(awk -v n="$idx" 'BEGIN{printf "%.2f",n/4}')" "$log" "$(awk -v n="$log" 'BEGIN{printf "%.2f",n/4}')" "$md"; done
```
```text
image-maze/.bc-agent total=60813914 whole_tokens=15203478.50 index=18172 index_tokens=4543.00 log=199069 log_tokens=49767.25 md=239
homeflix-prod/.agent total=307786 whole_tokens=76946.50 index=6985 index_tokens=1746.25 log=70353 log_tokens=17588.25 md=45
Scripts/.bc-agent total=222108 whole_tokens=55527.00 index=5037 index_tokens=1259.25 log=8146 log_tokens=2036.50 md=54
```

## C. Link graph

The graph command used `wiki_lint.py`’s Markdown/wikilink regex and resolver. Graph sources exclude `log.md` and `templates/`; ignored directories are `.obsidian`, `scratch`, `temp`, `node_modules`, `vendor`. The histogram is `inbound-count:number-of-eligible-pages`; eligible excludes `index.md`, `log.md`, templates, and generated maintenance reports. `index` is labelled a hub when it resolves at least `max(3,pages/4)` unique local targets.

```text
vault                                      md/wl occurrences  local md/wl  inbound histogram (count:pages)                         index unique/eligible  broken/ambig  orphans
codebase-design                            49/28              37/28      0:21,1:12,2:10,3:2,4:3,5:1,7:1                 27/50                 0/0          21
sql                                        28/0               27/0       0:17,1:8,2:5,3:2                                  12/32                 0/0          17
Music                                      11/197             10/197     0:12,1:12,2:7,3:4,4:7,5:2,6:7,7:3,8:3,10:3,11:1 45/61                 0/0          12
Scripts                                    155/0              112/0      0:7,1:9,2:16,3:11,4:2,5:4,7:1                    44/50                 0/0          7
CV                                         164/0              47/0       0:12,1:12,2:7,3:1,4:3                           23/35                 0/0          12
dng/files/pub/agent/wiki                   24/0               24/0       0:6,1:7,2:2,3:3                               13/18                 0/0          6
image-maze                                 400/0              345/0      0:14,1:63,2:33,3:12,4:8,5:6,6:4,7:6,8:1,9:2,10:2 118/151              0/0          14
Homeflix                                   210/0              182/0      1:6,2:3,3:3,4:8,5:8,6:1,7:3,8:2,9:1,10:1,21:1 41/37                 0/0          0
homeflix-prod                              272/0              242/0      1:7,2:3,3:3,4:4,5:5,6:5,7:1,8:3,9:2,10:2,11:1,12:1,13:1,14:1,23:1 41/40       0/0          0
```
All nine pass the mechanical hub threshold, but only public Homeflix has zero `missing_index`; the detector reports nonzero missing-index counts for the other 8/9. The top inbound targets include `codebase-design/.bc-agent/concepts/plus-operator-coercion.md` line 7 (codebase-design), `findings/existing-music-stack-recon.md:11` (Music), `decisions/adr-0010-abandon-wallpaper-crossfade.md:7` (Scripts), `project/plans/digital-chest-unlock/referral-unlock-plan.md:10` (image-maze), `decisions/adr-0008-single-filesystem-data-root-hardlinks.md:21` (Homeflix), and the same ADR at `:23` (homeflix-prod).

## D. Page anatomy samples

Command actually run for bytes and first three physical lines:
```sh
for f in /home/ben/Sync/Music/.bc-agent/findings/existing-music-stack-recon.md /home/ben/Sync/Scripts/.bc-agent/project/wallpaper-rotation-spec.md /home/ben/Sync/Work/CV/.bc-agent/findings/job-ad-scan-saas.md /home/ben/Sync/Work/Development/wp-theme-builds/localhost/image-maze/.bc-agent/project/architecture-module-map.md /home/ben/Sync/Work/PUBLIC/Homeflix/.agent/references/gotchas.md /home/ben/Sync/Documents/Learning/codebase-design/.bc-agent/learning-records/0001-variables-let-const.md; do printf '%s\t' "$f"; wc -c < "$f"; done
```
```text
Music/findings/existing-music-stack-recon.md 2173 B; first3: 1 `---` / 2 `type: finding` / 3 `status: stable`
Scripts/project/wallpaper-rotation-spec.md 22167 B; first3: 1 `# Wallpaper Rotation Specification` / 2 blank / 3 `Updated: 2026-08-24`
CV/findings/job-ad-scan-saas.md 7700 B; first3: 1 `> **Superseded as a data source.** Raw scan data now lives in` / 2 `> .bc-agent/research/scans/*.json ...` / 3 `> Kept for the written analysis below.`
image-maze/project/architecture-module-map.md 70757 B; first3: 1 `# Architecture Module Map` / 2 blank / 3 `Status: Current`
Homeflix/references/gotchas.md 18871 B; first3: 1 `# References — Gotchas` / 2 blank / 3 `Updated: 2026-08-17`
codebase-design/learning-records/0001-variables-let-const.md 1489 B; first3: 1 `---` / 2 `Status: demonstrated` / 3 `---`
```

Cold-reader assessment from the sampled prose/status fields: Music has no explicit opening TL;DR (heading then `## Question`), dates 2026-05-29, and no “current through” marker: not enough to know it remains true today. Scripts has an opening synopsis, `Updated: 2026-08-24`, and explicitly describes normative/current truth and pending requirements: current as of that date. CV opens with explicit “Superseded as a data source”; a 2026-08-01 rescan is dated: the superseded state is clear, but it is not current data. Image-maze says `Status: Current`, `Updated: 2026-08-17`, and “verified against shipped code”: current as of that date, not rechecked today. Homeflix has an opening description and `Updated: 2026-08-17`; bullets individually mark historical/fixture-only states, but the mixed page has no single validity state. The learning record opens with a learner-state summary and `Status: demonstrated` but no date: learning status is clear, freshness is not.

## E. Existing machinery

### Source surface and detector

Files/line ranges read:
- `/home/ben/Sync/Work/PUBLIC/Agents/concepts/bc-wiki-maintain/body/SKILL.md:26-183` — detector-first loop, classify every unpromoted heading, additive/commit/contradiction gates, verification; `:185-208` runner contract.
- `.../bc-wiki-maintain/body/wiki_lint.py:22-57,71-121,123-138,140-204,206-299,300-363,365-434,436-510` — parser/resolver, promotion, qmd, lint, classification, output/CLI.
- `.../bc-wiki-maintain/body/runner/run-lint.sh:1-69` and `run-promotion.sh:1-254`; installed units `/home/ben/.config/systemd/user/bc-wiki-*`.
- `/home/ben/Sync/Work/PUBLIC/Agents/concepts/bc-init-agent/body/SKILL.md:18-80`; `body/scaffold.py:821-987`.
- `/home/ben/Sync/Work/PUBLIC/Agents/concepts/qmd/body/SKILL.md:17-59`.

Exactly implemented detector checks/functions:
- `without_code` masks fenced/inline code; `links` extracts Markdown and `[[wikilink]]`; `skip_link` ignores empty, fragments, external, and special targets; `resolve_link` resolves local targets and identifies broken/ambiguous stem matches.
- `log_headings` recognizes `##` headings and valid `## [YYYY-MM-DD]`; `promotion_status` compares current headings with the latest vault-specific `wiki: promote` commit, counts unpromoted entries, computes ranges, and flags undatable headings.
- `qmd_paths`, `qmd_covering_path`, `qmd_status` parse/check canonical and machine qmd coverage, including intentional exclusion and canonical-only/unindexed states.
- `ignored_path` excludes `.git`, `.obsidian`, `scratch`, `temp`, `node_modules`, `vendor`; `maintenance_report` excludes generated `_meta` lint/health/semantic pages.
- `lint` checks page enumeration, broken links, ambiguous links, inbound/orphan pages, possible index omissions, stale `tasks/active.md` references (>90 days), unknown active-reference dates, unpromoted log headings, and qmd coverage. `log.md` is not a graph source; templates are excluded from graph/index/orphan findings.
- `verify_classification` requires one exact-heading JSONL row with valid verdict/reason/page rules; `classification_summary` renders it; `print_report` emits findings plus `PROMOTION_REQUIRED`, `PROMOTION_RANGE`, and headings; `main` provides text/JSON/verification modes and normal lint exits nonzero for broken/ambiguous links. `text`, `rel`, `key`, `git`, `git_root`, `git_path`, and `git_date` are support helpers.

`bc-init-agent` performs recon and adaptive grilling before a proposed plan; supports `code`, `ops`, `learning`, `knowledge`, and `hybrid`; then `scaffold.py` creates missing files additively/idempotently, preserves existing files, supports dry-run and explicit force, and never migrates old docs automatically. Close-out registers qmd by default and offers publish authorization.

`qmd` is global-mode hybrid search: `query` uses expansion/embedding/reranking, `search` is BM25, `vsearch` semantic; project-local `qmd init` is deliberately unsupported; collection definitions and index mutation are centrally owned.

### qmd coverage and real query

Commands:
```sh
qmd --version
qmd collection list
python3 /home/ben/Sync/Work/PUBLIC/Agents/concepts/bc-wiki-maintain/body/wiki_lint.py <vault> --json
```
`qmd --version` returned `qmd 2.5.3`. `qmd collection list` reported 8 collections: `wiki`, `music`, `scripts`, `image-maze`, `agents`, `homeflix`, `homeflix-prod`, `codebase-design`. Both `/home/ben/.config/qmd/index.yml` and canonical `/home/ben/Sync/Scripts/config/qmd-collections.yml` contain those eight path definitions.

```text
codebase-design registered (canonical + machine)
sql intentional exclusion (documented scaffold exclusion)
Music registered (canonical + machine)
Scripts registered (canonical + machine)
CV intentional exclusion (documented personal-data exclusion)
dng/files/pub/agent/wiki unregistered (absent from both)
image-maze registered (canonical + machine)
Homeflix registered (canonical + machine)
homeflix-prod registered (canonical + machine)
```
Thus 6/9 are registered, 2/9 intentional exclusions, and 1/9 unregistered. qmd’s live collection counts are Music 69, Scripts 54, image-maze 155, Homeflix 42, homeflix-prod 45, codebase-design 52 (templates ignored).

Real query command:
```sh
qmd query 'wallpaper renderer lifecycle' -c scripts --no-rerank --format json
```
Measured with Python `time.perf_counter` around the real subprocess: return code 0, elapsed `67.077` seconds; stderr reported expansion `57.3s` and embedding `7.2s`. Output was a JSON array of result objects with fields `docid`, `score`, `file`, `line`, `title`, `context`, `snippet`. First results:
```json
[
 {"docid":"#d9a41b","score":1,"file":"qmd://scripts/project/wallpaper-architecture-deepening-prd.md","line":12,"title":"Wallpaper Architecture Deepening PRD","context":"Project agent wiki for the Scripts repo ...","snippet":"@@ -11,4 @@ ..."},
 {"docid":"#a03c17","score":0.5,"file":"qmd://scripts/project/wallpaper-rotation-spec.md","line":75,"title":"Wallpaper Rotation Specification","context":"Project agent wiki for the Scripts repo ...","snippet":"@@ -74,4 @@ ..."}
]
```
(The actual command returned full snippets; the excerpt shows the output shape.)

### Installed runner

`systemctl --user list-timers --all` and `systemctl --user cat/is-enabled/is-active` were run. Installed units are 10 regular files under `/home/ben/.config/systemd/user/`: five timers and five oneshot services. All five timers are loaded, enabled, active; all five services are installed `static` and currently inactive between runs.

```text
bc-wiki-lint.timer                  enabled active; next 04:15 (+15m randomized)
bc-wiki-maintain.timer              enabled active; CV, 03:30 (+15m randomized)
bc-wiki-maintain-imagemaze.timer    enabled active; 04:45 (+15m randomized)
bc-wiki-maintain-homeflix.timer     enabled active; 05:30 (+15m randomized)
bc-wiki-maintain-homeflix-prod.timer enabled active; 06:15 (+15m randomized)
bc-wiki-*.service                   static inactive (Type=oneshot)
```
Installed services point to the canonical `run-lint.sh`/`run-promotion.sh` under `AGENT_CONCEPTS=/home/ben/Sync/Work/PUBLIC/Agents`; lint uses `/home/ben/.config/agent-concepts/wiki-lint-vaults.txt`, which contains 8 paths and omits dng. The lint runner is detection-only, continues after a path failure, and reports a final failure count. Promotion services require a clean tree, run detection, fail closed on invalid/malformed ranges, invoke Pi only when required, require complete classification, reject staging/outside-vault/deletion/non-Markdown/non-additive changes, then create one exact-range commit. Today’s journal shows lint checked 8 paths with 0 failures; four promotion runs finished: CV, image-maze, and public Homeflix were no-ops; homeflix-prod classified one entry `skip` and made no commit.

## F. Evidence of the problem

Exact read-only command run against every qualifying vault:
```sh
python3 /home/ben/Sync/Work/PUBLIC/Agents/concepts/bc-wiki-maintain/body/wiki_lint.py <vault>
```
Summary lines (all exited 0; nonzero would only be broken/ambiguous links):
```text
codebase-design: Pages 55; Broken 0; Ambiguous 0; Orphans 21; Missing index 14; Unpromoted 18; undatable 1; PROMOTION_RANGE=2026-06-28..2026-07-14
sql: Pages 37; Broken 0; Ambiguous 0; Orphans 17; Missing index 20; Unpromoted 1; undatable 1; PROMOTION_RANGE=invalid
Music: Pages 69; Broken 0; Ambiguous 0; Orphans 12; Missing index 13; Unpromoted 37; PROMOTION_RANGE=2026-05-29..2026-08-05
Scripts: Pages 54; Broken 0; Ambiguous 0; Orphans 7; Missing index 7; Unpromoted 12; undatable 12; PROMOTION_RANGE=invalid
CV: Pages 42; Broken 0; Ambiguous 0; Orphans 12; Missing index 13; Unpromoted 0; PROMOTION_RANGE=none
dng/files/pub/agent/wiki: Pages 22; Broken 0; Ambiguous 0; Orphans 6; Missing index 6; Unpromoted 0; PROMOTION_RANGE=none
image-maze: Pages 155; Broken 0; Ambiguous 0; Orphans 14; Missing index 16; Unpromoted 0; PROMOTION_RANGE=none
Homeflix: Pages 42; Broken 0; Ambiguous 0; Orphans 0; Missing index 0; Unpromoted 0; PROMOTION_RANGE=none
homeflix-prod: Pages 45; Broken 0; Ambiguous 0; Orphans 0; Missing index 3; Unpromoted 1; PROMOTION_RANGE=2026-08-24..2026-08-24
```

Concrete stuck/failure instances from `--json` and raw `grep -n '^## ' log.md`:
- **Invalid promotion range:** `sql/.bc-agent/log.md:6` is `## 2026-07-31`; `Scripts/.bc-agent/log.md` has 12 bare headings (`## 2026-06-26`, `## 2026-07-13`, `## 2026-07-15`, `## 2026-07-22`, `## 2026-07-23`, `## 2026-07-25`, `## 2026-07-26`, `## 2026-07-27` twice, `## 2026-07-29`, `## 2026-08-18`, `## 2026-08-24`). All 13 are undatable and both vaults emit `PROMOTION_RANGE=invalid`.
- **Unpromoted log backlog:** no dedicated promotion commit exists for codebase-design (18 headings, including bare `## 2026-06-28`), sql (1), Music (37), Scripts (12), or dng (0 headings). Music’s backlog starts `## [2026-05-29] maintenance | Initialized plan wiki` and ends `## [2026-08-05] convention | AGENTS.md trimmed to rules; reference material demoted`. homeflix-prod has one post-boundary heading: `## [2026-08-24] wiki | Resolved all six 2026-08-24 promotion conflicts`. CV’s latest promotion is `cdf6775` on 2026-08-25; image-maze `7a241f6`; public Homeflix `be448a5`; homeflix-prod `c5f9ec1`.
- **Missing index examples:** codebase-design 14 includes `codebase-design/.bc-agent/concepts/README.md`, `references/paths.md`, `tasks/parking-lot.md`; sql 20 includes `GLOSSARY.md`, `MISSION.md`, `NOTES.md`; Music 13 includes `decisions/vocabulary-gated-comment-writes.md` and `findings/sticker-db-syncthing-fork.md`; Scripts 7 includes `references/paths.md`; CV 13 includes `findings/README.md`; dng 6 includes `project/create-agent-wiki-plan.md` and `project/seo-deep-improved-search-2026-plan.md`; image-maze 16 includes `references/dcu-trusted-proxy.md`, `references/docker.md`, and four unlisted PRD/plan pages; homeflix-prod 3 are `project/agent-first-acquisition-plan.md`, `project/agent-first-core-setup-plan.md`, and `project/agent-first-storage-plan.md`.
- **Orphan examples (exact graph counts above):** codebase-design has 21 including all ten `learning-records/*.md`; sql has 17 including `learning/plan.md`; Music has 12 including `home.md` and `decisions/adr-0001-local-project-agent-wiki.md`; Scripts has 7 including `conventions/file-layout.md`; CV has 12 including `findings/README.md`; dng has 6 including both project plans; image-maze has 14 including `project/plans/digital-chest-unlock/referral-engine-study.md`, `references/age-verification-seam.md`, and `references/wordpress-local-env.md`. Homeflix and homeflix-prod have zero orphans.

No repository file was edited or committed. `/home/ben/Sync/Work/PUBLIC/Agents` status at the end showed only the task-provided untracked `docs/research/wiki-autonomy-council/` directory; its contents were not inspected.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Artifact contains measured paths, byte/page/link/promotion counts, source ranges, timer/qmd observations, and concrete orphan/index/backlog instances."
    }
  ],
  "changedFiles": [
    "/tmp/bc-swarm/2026-08-26-wiki-autonomy/vault-reality.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "find /home/ben/Sync -maxdepth 10 ... (pruned node_modules, .git, forbidden docs/research)",
      "result": "passed",
      "summary": "10 candidates; 9 qualified vaults."
    },
    {
      "command": "python3 /home/ben/Sync/Work/PUBLIC/Agents/concepts/bc-wiki-maintain/body/wiki_lint.py <each qualifying vault>",
      "result": "passed",
      "summary": "All 9 read-only runs exited 0; summaries are included."
    },
    {
      "command": "systemctl --user list-timers --all; systemctl --user cat/is-enabled/is-active bc-wiki units",
      "result": "passed",
      "summary": "Five timers loaded/enabled/active; five oneshot services installed/static/inactive."
    },
    {
      "command": "qmd query 'wallpaper renderer lifecycle' -c scripts --no-rerank --format json",
      "result": "passed",
      "summary": "Registered collection query returned JSON results in 67.077 seconds."
    },
    {
      "command": "/usr/bin/time -f ... qmd query ...",
      "result": "failed",
      "summary": "Tool path absent; timing was rerun successfully with Python perf_counter."
    }
  ],
  "validationOutput": [
    "No detector-reported broken or ambiguous links across 9 vaults.",
    "Invalid promotion ranges: sql and Scripts; unpromoted counts: 18, 1, 37, 12, and 1 in the affected vaults.",
    "Agents repository status showed only the task-provided untracked docs/research/wiki-autonomy-council/ directory; no repository file was edited by this run."
  ],
  "residualRisks": [
    "image-maze whole-vault traversal is 60,813,914 bytes because generated temp/scratch files dominate; index links 118 of 239 Markdown pages.",
    "Eight of nine vaults have nonzero detector missing_index counts; 89 eligible pages are orphaned across the corrected graph counts.",
    "The qmd measurement used --no-rerank; full reranked latency was not measured in this run."
  ],
  "noStagedFiles": true,
  "diffSummary": "No repository files changed; only the requested external artifact was written.",
  "reviewFindings": [
    "high: sql and Scripts have PROMOTION_RANGE=invalid with undatable bare log headings.",
    "high: scheduled lint covers 8 paths and omits the discovered dng agent/wiki vault.",
    "medium: image-maze contains 2,171 temp files totaling 49,058,054 bytes and 14 orphan pages in the detector graph."
  ],
  "manualNotes": "All measurements are read-only."
}
```
