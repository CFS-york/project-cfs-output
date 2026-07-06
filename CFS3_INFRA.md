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
- **Claude API**: `C:\mnt\data\Claude APIキー.txt`。$100使用済のため節約意識。
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
  cfs3正史4枚+CFS3_INFRA.mdはSYNC_FILESに登録済(cfs3_add_mirror.py で追加)。
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
