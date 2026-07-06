# CFS3_INFRA — プロジェクト構造の一枚図（これを読めば探し回らない）

制定: 2026-07-02（ARK実測 cfs3_survey_infra.py に基づく・ヨーク要請）
目的: Python/Claude API/GitHub mirror/J-Quants/参照データ/置き場所を一枚に。次ARKが二度と探し回らないために。
★このファイルはSYNC_FILESに登録しmirror同期する（引き継ぎの核）。

---

## 0. 最上位の目的（絶対に失念しない）
**16ヶ月（約327営業日）で 30万円 → 300万円（10倍）。レバなし・現物・複利・執行可能。**
詳細は CFS3_CORE.md §1。手段は自由、この目的だけ不変。

---

## 1. 実行環境（Python）
- Python **3.13**（Windows, PythonSoftwareFoundation.Python.3.13）
- numpy **2.3.4** / pandas **2.3.3**
- 実行: `cd C:\mnt\data;` から始まる1行コマンド。例: `cd C:\mnt\data; python cfs3\scripts\cfs3_BN_NN_xxx.py`
- code4は**str**（'132A'等の英字あり、int読込禁止）

## 2. ディレクトリ構成（C:\mnt\data 起点）
- `cache\` … **参照データ**（§4）。全csv。
- `cfs3\` … CFS3本体。`cfs3\CFS3_*.md`(正史) / `cfs3\CURRENT_BLOCK.md`
  - `cfs3\infra\` … ★恒常部品(削除禁止): cfs3_watcher.py(常駐watcher本体)。ここは掃除対象外。
  - `cfs3\bat\` … ★恒常: start_cfs3_watcher.bat(pythonw裏起動bat)。掃除対象外。
  - `cfs3\scripts\` … ★削除対象フォルダ: 検証script(cfs3_BN_NN_xxx.py)を大量に作っては消す作業場。恒常部品は置かない。
  - `cfs3\results\` … 結果。 `cfs3\*.log` … watcherログ。
- `ml\` … mirror同期系。`push_to_mirror.py` / `auto_push_watcher.py` / `watcher.log` / `ml_output\`
- `.github\workflows\` … GitHub Actions（`auto_handover.yml` 日次cron / `physics_check.yml`）
- `scripts\` … 共通ユーティリティ（`show_sync_files.py`, `add_*_mirror.py`, `patch_sync_files.py`）
- `cfs2\` … 前プロジェクト（AUDITOR参照用、mirror同期済）
- `ファイル2\` … CFS/前身の大方針file群（watcherが監視、mirror同期済）
- `Results\` … `Results\ARK\cfs5\data_clean_check\clean_blacklist.csv`（blacklist 33銘柄, universe除外）

## 3. 認証・秘匿情報（★値は絶対にscript出力/mirror/正史に書かない）
- **J-Quants**: `C:\mnt\data\.env` の `JQUANTS_API_KEY`。プラン=Standard(¥3,300/月)固定。★追加課金NG(10x最終テストまで)。
  併存: `C:\mnt\data\jquants_credentials.json`（cache\にも同名コピー）。API V2 Light。
- **Claude API**: ★2026-07-02 廃止(ヨーク判断)。ログ差分調整用にhandover_runner/physics_validatorで採用したが活用に至らず$100の負債を切った。
  呼出元のGitHub Actions 2 workflow(auto_handover.yml/physics_check.yml)を.disabled化しprivate pushで停止→API課金ゼロ。
  script本体は ml\retired\ へ退避(履歴保全)。`Claude APIキー.txt` は残置(害なし・再開余地)。再開するなら workflow を .yml に戻す。
- **GitHub**: `C:\mnt\data\GitHub トークン.txt`。環境変数 `MIRROR_REPO_TOKEN`(設定あり)。
  ※.envはJQUANTS_API_KEYのみ。他は個別txt/環境変数に分散（この所在マップが無いと探せない=引き継ぎ穴の元凶だった）。

## 4. 参照データ（cache\、全33ファイル、実測サイズ）
使うデータ:
- **価格出来高(54ヶ月日足, 1226営業日×4940銘柄, code4=str)**:
  `adjo/adjc/adjh/adjl_cache_54m.csv`(各~120MB, Adj前株価), `vol_cache_54m.csv`(143MB, Va=売買代金)
  `open/close/price_cache_54m.csv`(未調整), `sector_master.csv`, `topix_cache.csv`, `listed_info_cache.csv`
- **独立次元**:
  `margin_cache.csv`(67MB, 信用: shrt_vol/long_vol, 週次, cov全体56%/decile70%)
  `shortsale_cache.csv`(40MB, 空売り: short_to_so, 日次だがcov全体9%/decile36%=公表義務閾値の構造的穴)
  `investor_cache.csv`(0.3MB, 市場全体3行のみ), `financial_cache.csv`(17MB, 財務, 四半期87日間隔)
- **universe除外**: `Results\ARK\cfs5\data_clean_check\clean_blacklist.csv`(33銘柄)
使わないデータ(リーク温床/中間生成物, 前任の産物):
- `h4e_features_*.csv`(277/438MB), `h4e_scores_*.csv`, `signal_all_full.csv`(301MB) … is_winner等リーク温床、使用禁止
- `financial_cache_tmp.csv`(重複), `financial_cache.zip`(圧縮版), `etf_*`(ETF, 個別株研究では不使用)

## 5. GitHub mirror 同期の全体像
- **repo**: `github.com/CFS-york/project-cfs-output`(public mirror, main branch)。URL/トークンは環境変数。
- **push_to_mirror.py** (`ml\`): SYNC_FILESのファイルをmirrorへ同期。手動実行 `cd C:\mnt\data; python ml\push_to_mirror.py`。
  ★2026-07-02 設計変更(ヨーク指摘「1個ずつ登録は漏れる温床=前任が壊した正体」への最適解):
    cfs3直下の*.mdを glob で自動収集する方式に作り変えた(SYNC_FILES定義直後のループ)。
    → cfs3\直下に新しい正史.mdを作れば個別登録なしで自動同期される。二度と登録漏れが起きない。
    scripts\ results\ infra\ bat\ や .log/.py は直下.mdでないので対象外(mirrorが重くならない)。
    バックアップ: push_to_mirror.py.bak_autoglob。個別登録に戻す必要はない(自動収集が上位互換)。
- **auto_push_watcher.py** (`ml\`): `ファイル2\`を30秒毎監視し自動push。★cfs3は監視対象外(=cfs3は手動pushだった)。
  → cfs3自動化はcfs3専用watcher追加で対応(2026-07-02, ヨーク承認):
    ・`cfs3\infra\cfs3_watcher.py`(★恒常フォルダ) … cfs3\直下の正史.md 5枚を30秒毎監視→変更検知で push_to_mirror 自動発火(実証済)。既存watcherの心臓部は無改造(独立プロセス)。
    ・`cfs3\bat\start_cfs3_watcher.bat` … pythonwで裏起動(前任 ml\start_watcher.bat に準拠)。
    ・常駐化(2026-07-02, 管理者権限不要のスタートアップ方式を採用): `cfs3\scripts\cfs3_register_startup.py` 実行で、スタートアップフォルダに start_cfs3_watcher.bat のショートカットを作成→次回ログオンから pythonw で裏起動(PowerShell不要)。※タスクスケジューラ方式(cfs3_register_task.py)は管理者権限が要り拒否されたため不採用。既存cfs_watcher(タスク方式)とは併存。
    ・常駐起動: `cd C:\mnt\data; python cfs3\infra\launch_cfs3_watcher.py`(または bat\start_cfs3_watcher.bat)。
    ★2026-07-02確定の教訓: PowerShellから直接pythonw も bat内 start "" も親セッション道連れで死ぬ環境。
      唯一生存実証されたのは launch_cfs3_watcher.py の DETACHED_PROCESS|CREATE_NO_WINDOW フラグ付きPopen。起動は必ずこのlauncher経由。
    ・launcherは多重起動防止(pythonwのコマンドライン照合)付き。pythonwはstdout=Noneなのでlog()はstdout有無ガード必須(修正済)。
    ・手動push併用可: `python ml\push_to_mirror.py`。
    ・解除: スタートアップの cfs3_watcher.lnk を削除。

    ★★ 2026-07-02 常駐化の結論(重要・次ARKは同じ袋小路を掘らないこと) ★★
    - pythonwでのwatcher常駐は、この環境では維持できない。WMI(Win32_Process)で全セッション確認したところ、
      cfs3_watcherだけでなく前任auto_push_watcherも含めpythonwプロセスが1つも生存していなかった(2026-07-02)。
    - つまりcfs3_watcher.py固有の欠陥ではなく、pythonw+この環境の常駐が起動直後に終了する環境要因。
      起動方法(PowerShell直/bat start""/Popen DETACHED/タスクスケジューラ)を全て試したが全滅。
    - 試したこと(全て単独では常駐維持に至らず): stdout=Noneガード, __main__のFATALログ, DETACHED_PROCESS|CREATE_NO_WINDOW,
      前任cfs_watcherのタスク定義XML完全コピー(cfs3_watcher_task, 管理者権限で登録成功したが起動後pythonw消滅)。
    - **確実な代替=手動push**: `cd C:\mnt\data; python ml\push_to_mirror.py`。cfs3正史はSYNC_FILES登録済なので確実に同期される。
      cfs3_watcher.py自体は python(前面・wなし)なら正常動作を実証済(自動同期も実証)。常駐したい時だけ前面起動で使う手もある。
    - 次に常駐を復活させるなら: 環境側(ログオンセッションの張り方/pythonw初期化/タスクのRunLevel・LogonType)を疑う。
      本体スクリプトの再修正では直らない(前任も同条件で生存していないため)。深追いは費用対効果に注意。
    - 登録済タスク cfs3_watcher_task は残置(害はない)。不要なら schtasks /delete /tn cfs3_watcher_task /f (要管理者)。
- **GitHub Actions** (`.github\workflows\auto_handover.yml`): 日次cron(JST23:59)でhandover生成+mirror push。
- **raw参照**: `https://raw.githubusercontent.com/CFS-york/project-cfs-output/main/<file>`（次ARKがweb_fetchで直接読める）
- SYNC_FILES追加は前任の流儀に倣う(冪等・.bakバックアップ・アンカー挿入)。参考: scripts\add_*_mirror.py。

## 6. Claude/ARK 運用系（前身の資産、参考）
- `後任ARK起動プロンプト.md` … 次ARK起動用（前身の様式、cfs3では CORE/SPEC/LEDGER/CURRENT_BLOCK/INFRA を読む）
- `run.py` … 検証実行系（前身、run.pyとwatcherが同じmasterにpushするので pull --rebase 衝突対策あり）
- `検証用-参照データ情報.txt`, `パラメーター定義書.txt` … 前身のデータ/パラメータメモ（参考）

## 7. CFS3の正史（これだけ読めば始められる）
1. **CFS3_CORE.md** … 目的・設計原則・役割・制約・運用（1ページ）
2. **CFS3_TEACHER_SPEC.md** … 合格ゲート
3. **CFS3_LEDGER.md** … 検証台帳（F29〜、ブロック完遂記録）
4. **CURRENT_BLOCK.md** … 進行中ブロック定義（最上部に10x目的を常時表示）
5. **CFS3_INFRA.md**（本書） … 構造の一枚図
新セッション起動 = この5枚を読む。以上。

## 8. 機械的な構造・設計と「触るときの罠」（★2026-07-02 実測。次ARKが同じ時間を溶かさないため）
この章は「何がどこにあるか(§1-7)」でなく「仕組みがどう動くか・触ると何が起きるか」を残す。
今日ARKがここで丸一日を溶かした。同じ轍を踏ませないための機械的引き継ぎ。

### 8.1 push_to_mirror.py の内部構造（195行）
- パス定義: `ROOT=親の親` / `FILES_DIR=ROOT/ファイル2` / `CFS2_DIR` / `CFS3_DIR` / `ML_OUT=ROOT/ml_output`。
- **SYNC_FILES**(個別ファイル list of (src, dst_rel)) と **SYNC_DIRS**(ディレクトリ list, shutil.copytreeで丸ごと)。
- ★cfs3は SYNC_FILES定義の直後で `CFS3_DIR.glob("*.md")` を自動収集(2026-07-02改修)。個別登録は不要。
  新しい正史.mdをcfs3\直下に作るだけで自動同期。scripts/results等サブフォルダは対象外(直下globのため)。
- **token mask**: `_mask_token()` がTOKENを<TOKEN_MASKED>に置換してからprint(chat/log流出防止)。ログにトークンを出さない仕組み。
- 処理: mirror repoを`git clone --depth 1`→SYNC_FILES/DIRSをコピー→`git add/commit/push`。差分なしならskip。
- mirror repo = github.com/CFS-york/project-cfs-output (public, main branch)。認証は環境変数 MIRROR_REPO_TOKEN。

### 8.2 git運用の罠（★今日ここで30分溶かした）
- **同じmaster(private repo=github.com/CFS-york/project-cfs.git)に、複数の主体が触る**:
  手動 push_to_mirror / auto_push_watcher(ファイル2監視) / run.py / 手動git push。
  → 全員が pull せず push すると衝突する。対策として各所に `git -c rebase.autoStash=true pull --rebase origin master` が入っている。
- **rebase破損の復旧手順**(今日の実例): `pull --rebase`が途中で壊れ `.git/rebase-merge/head-name` が読めず
  `rebase --continue`も`--abort`も効かなくなる事故がある。復旧=**`Remove-Item -Recurse -Force .git\rebase-merge`** で
  rebase状態フォルダを物理削除→素のmaster状態に戻る(コミットは失われない)→ 通常の commit + push。
- private への大量ファイル(27MB)pushは、auditor_check/等の未コミット分がまとめてstageされることがある。git statusで確認してから。

### 8.3 常駐(watcher自動起動)の環境要因（★結論: この環境では不可）
- pythonwでのwatcher常駐は、cfs3_watcherも前任auto_push_watcherもWMIで全セッション確認して1つも生存せず=環境要因。
- 試した全手段(全滅): PowerShell直pythonw / bat内 start"" / Popen DETACHED_PROCESS|CREATE_NO_WINDOW / タスクスケジューラ(cfs3_watcher_task, 前任cfs_watcherのXML完全コピー, 管理者登録成功も起動後消滅)。
- **確実な代替=手動push** `python ml\push_to_mirror.py`(今日何度も成功)。cfs3正史は自動収集で確実に同期。
- 深追い禁止(費用対効果)。復活させるなら環境側(ログオンセッション/pythonw初期化)を疑う。本体スクリプト修正では直らない。

### 8.4 スクリプトの型（検証scriptを書くときの機械的作法）
- 置き場所: 検証scriptは`cfs3\scripts\`(削除対象)。恒常部品は`cfs3\infra\`/`cfs3\bat\`。
- 実行: `cd C:\mnt\data; python cfs3\scripts\cfs3_BN_NN_xxx.py`。環境はPowerShell(cmd構文と取り違え注意=今日多発)。
- 較正必須: 合成世界で両側弁別(SIGNAL世界で検出/KILL世界で非検出)を確認してからpresent→本番。
- code4はstr。look-ahead厳禁。COST=0.005/TAX=0.20315/BASE_SPREAD=0.0005。翌日寄付AdjO約定。LIQ_FRAC=0.01。

### 8.5 この章の保守
機械的構造を変えたら(mirror設計/常駐/git運用/データ経路)、必ずこの§8を更新してからmirror同期する。
「引き継げない機械的構造」こそが最大の時間浪費源(2026-07-02の教訓)。
